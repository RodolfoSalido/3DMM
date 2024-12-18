# Three-Dimensional Microbial Mapping (3DMM)
The following repository contains scripted microbiome data analysis workflows to reproduce the key findings of the paper **_The International Space Station Has a Unique and Extreme Microbial and Chemical Environment Driven by Use Patterns_**, and generate most of the published figures. 

## Summary of findings. 
>Space habitation provides unique challenges in built environments isolated from Earth. We produced a 3D map of the microbes and metabolites throughout the United States Orbital Segment (USOS) of the International Space Station (ISS), with 803 samples collected during space flight, including controls. We find that the use of each of the nine sampled modules within the ISS strongly drives the microbiology and chemistry of the habitat. Relating the microbiology to other Earth habitats, we find that, as with human microbiota, built environment microbiota also align naturally along an axis of industrialization, with the ISS providing an extreme example of an industrialized environment. We demonstrate the utility of culture-independent sequencing for microbial risk monitoring, especially as the location of sequencing moves to space. The resulting resource of chemistry and microbiology in the space-built environment will guide long-term efforts to maintain human health in space for longer durations.

## Installation
The repository relies on the qiime2 environment, [installed in a conda virtual environment.](https://docs.qiime2.org/2024.10/install/). Due to dependencies on some of the analysis packages performed on the manuscript and the timescale of the project, more than one release of qiime2 was employed. Conda environment exports of these environments are made available for convenient installation. 

Install both qiime2 environments using the provided `qiime2-{release}.yml` environment exports. 

```
conda env create -f qiime2-2021.8_3DMM.yml
```

```
conda env create -f qiime2-2023.5_3DMM.yml
```
## Running Jupyter Notebooks
Most analyses were performed in Jupyter Electronic Lab Notebooks (ELN). Some components of the analyses where performed in [Qiita](https://qiita.ucsd.edu/study/description/14542), or in a high performance cloud computer cluster. Nonetheless, the appropriate output files from analysis components performed outside of Jupyter ELNs are included in this repository in order to generate the resulting published figures. 

### Running Jupyter Notebooks
After installing the appropriate qiime2 environments, you will need to activate them and launch jupyter notebook. 
#### qiime2-2021.8
This qiime2 release was used to perform the data preprocessing with KatharoSeq, the microbiome composition analysis, source tracking, metagenomic analyses, and the Antimicrobial Resistance (AMR) Analyses.

Activate the conda virtual environment and launch a jupyter instance using the following commands:
```
conda activate qiime2-2021.8
jupyter notebook
```
Then navigate to the following jupyter notebooks and run the modules in each notebook sequentially. 
- 1_3DMM_pre-processing_KatharoSeq.ipynb
- 2_3DMM_alpha_beta_diversity.ipynb
- 3_3DMM_source_tracker.ipynb
- 5_3DMM_metagenomics.ipynb
- 6_3DMM_AMR.ipynb

#### qiime2-2023.5
This qiime2 release was used to perform the multi study analysis. 
Activate the conda virtual environment and launch a jupyter instance using the following commands:
```
conda activate qiime2-2023.5
jupyter notebook
```
Then navigate to the following jupyter notebooks and run the modules in each notebook sequentially. 
- 4_3DMM_multi-study_analysis.ipynb

## Citation
```
CELL citation pending pubication. 
```
