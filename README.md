### Deep learning project seed
Use this seed to start new deep learning / ML projects.

- Built in setup.py
- Built in requirements
- Examples with MNIST
- Badges
- Bibtex

#### Goals  
The goal of this seed is to structure ML paper-code the same so that work can easily be extended and replicated.   

### DELETE EVERYTHING ABOVE FOR YOUR PROJECT  
 
---

<div align="center">    
 
# Your HPC Project Name     

[![Paper](http://img.shields.io/badge/paper-arxiv.1001.2234-B31B1B.svg)](https://www.nature.com/articles/nature14539)
[![Conference](http://img.shields.io/badge/NeurIPS-2019-4b44ce.svg)](https://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018)
[![Conference](http://img.shields.io/badge/ICLR-2019-4b44ce.svg)](https://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018)
[![Conference](http://img.shields.io/badge/AnyConference-year-4b44ce.svg)](https://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018)  
<!--
ARXIV   
[![Paper](http://img.shields.io/badge/arxiv-math.co:1480.1111-B31B1B.svg)](https://www.nature.com/articles/nature14539)
-->
![CI testing](https://github.com/amorehead/deep-learning-hpc-project-template/workflows/CI%20testing/badge.svg?branch=master&event=push)


<!--  
Conference   
-->   
</div>
 
## Description   
What it does   

## How to run   
First, create a Conda environment for the project:
```bash
# Clone project   
git clone https://github.com/YourGithubName/deep-learning-hpc-project-template

# Install project   
cd deep-learning-hpc-project-template

# (Optional) Load Conda module on HPC cluster
module load python/3.7.0-anaconda3-5.3.0

# Create Conda environment in this directory using provided 'environment.yml' file:
conda env create --prefix ./venv -f environment.yml

# (Optional) Create Conda environment in a particular directory using provided 'environment.yml' file:
conda env create --prefix MY-VENV-DIR -f environment.yml

# Activate the Conda environment described in 'environment.yml':
conda activate ./venv

# (Optional) Activate the Conda environment located in a particular directory:
conda activate MY-VENV-DIR

# (Optional) Deactivate the current Conda environment:
conda deactivate

# (Optional) To remove this long prefix in your shell prompt, modify the env_prompt setting in your .condarc file:
conda config --set env_prompt '({name})'

# (Optional - 1) Perform a full update on the Conda environment created using 'environment.yml':
conda env update --prefix ./venv --file environment.yml --prune

# (Optional - 2) Perform a full update on the Conda environment located in a particular directory:
conda env update --prefix MY-VENV-DIR --file environment.yml --prune
```

Optionally, (re)install all project dependencies :
```bash
# (Optional - 1) Reinstall project pip dependencies in the Conda environment currently activated:
pip3 install -e .

# (Optional - 2) Reinstall all run time pip dependencies in the Conda environment currently activated:
pip3 install -r requirements.txt

# (Optional - 3) Reinstall all test time pip dependencies in the Conda environment currently activated:
pip3 install -r tests/requirements.txt
 ```   

Further optionally, authenticate with Weights and Biases (Wandb) for advanced logging:
```bash
# (Optional) Sign into a Wandb account for logging:
wandb login
 ```   

 Then, navigate to any file and run it:
 ```bash
# Module folder
cd project

# Run module (example: mnist as your main contribution)   
python lit_classifier_main.py    
```

## Imports
This project is set up as a package which means you can now easily import any file into any other file like so:
```python
from project.datasets.mnist import mnist
from project.lit_classifier_main import LitClassifier
from pytorch_lightning import Trainer

# Model
model = LitClassifier()

# Data
train, val, test = mnist()

# Train
trainer = Trainer()
trainer.fit(model, train, val)

# Test using the best model!
trainer.test(test_dataloaders=test)
```

### Citation   
```
@article{YourName,
  title={Your Title},
  author={Your team},
  journal={Location},
  year={Year}
}
```   