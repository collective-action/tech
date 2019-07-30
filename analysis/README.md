# Analysis

This notebook is used to analyze the data collected.

### Setup

1. Install Anaconda with Python >= 3.6. [Miniconda](https://conda.io/miniconda.html). 
1. Clone the repository
    ```
    git clone https://github.com/organizejs/collective-actions-in-tech/
    ```
1. Install the conda environment. You'll find the `environment.yml` file in the root directory. To build the conda environment:
    ```
    conda env create -f environment.yml
    ```
1. Activate the conda environment and register it with Jupyter:
    ```
    conda activate cv
    python -m ipykernel install --user --name cait --display-name "Python (cait)"
    ```
1. Start the Jupyter notebook server on your desired
    ```
    jupyter notebook --port <PORT>
    ```


