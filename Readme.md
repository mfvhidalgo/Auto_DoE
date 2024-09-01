# Auto_DoE

This is a collection of scripts which are useful in creating various common Design of Experiments (DoE) designs.

# Installation

## Python
1. Download Python, ideally from [Anaconda](https://www.anaconda.com/download/success).
2. Open your preferred IDE, such as Spyder.
3. If not yet installed, go to the Python terminal in your IDE and type (and enter) ```pip install pandas```, ```pip install doepy```, and ```pip install openpyxl```.

## R

1. Download and install [R](https://cran.r-project.org/) and [RStudio](https://posit.co/downloads/).
2. Open RStudio and type ```install.packages("AlgDesign")``` in the console.

# Downloading a copy

The script can be either manually downlaoded from Github or installed via Git.

## Downloading from Github

* Go to [the Github repo](https://github.com/mfvhidalgo/Auto_DoE)
* Hit the green <u>**<> Code**</u> button on the upper right corner then hit <u>**Download ZIP**</u>.
* The files of interest are in the src folder

## Downloading using Git

* open Git bash
* enter
```
git clone https://github.com/mfvhidalgo/ML
```

# Running the script

0. Refer to docs > Guide.docx for details on how to use these scripts.
1. Fill out **Features.xlsx**. This is an Excel file containing the feature names and levels.
2. Run **Common_DoEs.py**. This is a Python file which takes the info from Features.xlsx and creates an Excel file containing the most common DoEs for those features.
3. Open **Optimal_Design.R** and change all fields containing the ```DEFINE_ME!``` line. Run the script to create an Excel file containing an optimal design.

# Last tested with

### Python 3.11.9
* pandas 2.2.2
* doepy 0.0.1
* openpyxl 3.1.5

### R 3.6.1
* AlgDesign 1.2.1
* rstudioapi 0.16.0


