from argparse import ArgumentParser

import pytorch_lightning as pl
import torch
import torch.multiprocessing as mp
from torch.nn import functional as F
from torch.utils.data import DataLoader, random_split
from torchvision import transforms
from torchvision.datasets.mnist import MNIST


class LitClassifier(pl.LightningModule):
    def __init__(self, hidden_dim=128, learning_rate=1e-3):
        super().__init__()
        self.save_hyperparameters()

        self.l1 = torch.nn.Linear(28 * 28, self.hparams.hidden_dim)
        self.l2 = torch.nn.Linear(self.hparams.hidden_dim, 10)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = torch.relu(self.l1(x))
        x = torch.relu(self.l2(x))
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log('valid_loss', loss)

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log('test_loss', loss)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.learning_rate)

    @staticmethod
    def add_model_specific_args(parent_parser):
        parser = ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument('--hidden_dim', type=int, default=128)
        parser.add_argument('--learning_rate', type=float, default=0.0001)
        return parser


def cli_main():
    pl.seed_everything(1234)

    # ------------
    # args
    # ------------
    parser = ArgumentParser()
    parser.add_argument('--batch_size', default=64, type=int)
    parser.add_argument('--early_stop_callback', type=bool, default=True)
    parser.add_argument('--num_dataloader_workers', type=int, default=4)
    parser = pl.Trainer.add_argparse_args(parser)
    parser = LitClassifier.add_model_specific_args(parser)
    args = parser.parse_args()

    # ------------
    # data
    # ------------
    dataset = MNIST('', train=True, download=True, transform=transforms.ToTensor())
    mnist_test = MNIST('', train=False, download=True, transform=transforms.ToTensor())
    mnist_train, mnist_val = random_split(dataset, [55000, 5000])

    train_loader = DataLoader(mnist_train, batch_size=args.batch_size, num_workers=args.num_dataloader_workers)
    val_loader = DataLoader(mnist_val, batch_size=args.batch_size, num_workers=args.num_dataloader_workers)
    test_loader = DataLoader(mnist_test, batch_size=args.batch_size, num_workers=args.num_dataloader_workers)

    # ------------
    # model
    # ------------
    model = LitClassifier(args.hidden_dim, args.learning_rate)

    # ------------
    # checkpoint
    # ------------
    try:
        model = LitClassifier.load_from_checkpoint(f'EarlyStopping-Adam-{args.batch_size}-{args.learning_rate}.pth')
        print('Resuming from checkpoint...')
    except:
        print('Could not restore checkpoint. Skipping...')

    # ------------
    # training
    # ------------
    trainer = pl.Trainer.from_argparse_args(args)

    trainer.accelerator = 'horovod'
    trainer.max_epochs = 5
    trainer.num_dataloader_workers = args.num_dataloader_workers
    trainer.learning_rate = args.learning_rate
    trainer.early_stop_callback = args.early_stop_callback

    trainer.fit(model, train_loader, val_loader)

    # ------------
    # testing
    # ------------
    trainer.test(test_dataloaders=test_loader)

    # ------------
    # finalizing
    # ------------
    trainer.save_checkpoint(f'EarlyStopping-Adam-{args.batch_size}-{args.learning_rate}.pth')


if __name__ == '__main__':
    mp.set_start_method('forkserver')  # Address SEGFAULT crashes caused by using distributed DataLoaders with 'fork'
    cli_main()
