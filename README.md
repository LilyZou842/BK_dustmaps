
# BK_dustmaps #

This repository contains code to analyze and plot dust properties in the BICEP/Keck survey fields. In particular, I use 3D dust extinction maps from Zhang and Green 2025 and Planck thermal dust maps.

Various plots produced by the code in this repository can be found [here](https://drive.google.com/drive/folders/1Gly9R1YS5JDIdEbF0cd9WmA6joZ9E418?usp=drive_link).

For more context, see [this poster](https://drive.google.com/file/d/1oUt7DaNErQvgHQX4B8mGKdtcRC9MtQsI/view?usp=drive_link).

## Sources ##

Zhang, X., & Green, G. M. 2025, Science, 387, 1209

- Paper: https://www.science.org/doi/10.1126/science.ado9787

- Data: https://zenodo.org/records/11394477

Planck Collaboration 2016, A&A, 594, A1

- Data: 

    - Intensity: https://irsa.ipac.caltech.edu/data/Planck/release_2/all-sky-maps/previews/COM_CompMap_ThermalDust-commander_2048_R2.00/index.html

    - Polarization: https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/previews/COM_CompMap_QU-thermaldust-commander_2048_R3.00_full/index.html


## In this repository ##

Under `src/my_package`:

- `loader.py`: defines objects that load and cache large datasets.

- `constants.py`: defines constants. Also defines `data_dir` and `plt_dir`, absolute filepaths where large binary data and generated plots are stored.

Under `notebooks`:

- `Zhang_Green_maps.ipynb`: load and plot extinction and R(V) maps.

- `beta_maps.ipynb`: plots maps of beta and correlation between beta and R(V).

- `maps_from_catalog.ipynb`: create custom HEALPix maps from Zhang and Green's stellar catalog.

- `differential_maps.ipynb`: convert integrated maps to differential maps with coarser distance bins.

- `extinction_scatter.ipynb`: create a scatter plot of extinction to directly visualize stellar data.

- `make_video.ipynb`: stitch distance slices together into a movie.

## HI correlation ##

I also explored correlating the Zhang and Green dust extinction maps with neutral hydrogen emission maps. I used the [astroHOG repository](https://github.com/solerjuan/astroHOG) created by Juan D. Soler, with guidance from Minjie Lei.

HI data:

Clark, Susan E.; Hensley, Brandon, 2020, "I_v_HI4PI_Kkms.h5", Clark & Hensley 3D HI-based Stokes Parameter Maps, https://doi.org/10.7910/DVN/P41KDE/KT7PV4, Harvard Dataverse, V1

The resulting plots can be found [here](https://drive.google.com/drive/folders/1Mo1AOgQhbnsY1bXzv40WNzM9HfXKgeUi?usp=sharing). 


## How to use ##

`environment.yml` lists the required packages. Either create a new conda environment using the .yaml file, or add packages as needed.

Clone this repository by running `git clone BK_dustmaps`. Change `data_dir` and `plt_dir` in `src/my_package/constants.py` to where you wish to store large binary data and generated plots.

To run the notebooks, download and save to `data_dir` the required datasets: `Rv_map_new.h5` and all 10 `xpparams_v2_zenodo_*.h5` files from the authors' data repository (https://zenodo.org/records/11394477) and FITS files from Planck (https://irsa.ipac.caltech.edu/data/Planck/release_2/all-sky-maps/previews/COM_CompMap_ThermalDust-commander_2048_R2.00/index.html and https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/previews/COM_CompMap_QU-thermaldust-commander_2048_R3.00_full/index.html).

