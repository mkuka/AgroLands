# Land Use Analysis
We compute the land use for five counties in Iowa state, Black Hawk, Butler, Franklin, Carroll, Webst. In oreder to do the analysis, first we create Shapely Point type object for each pixel and use the affine projection matrix to convert it to a position in UTM Zone 15. 

### Setup for spyder on Windows
Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) as admin and relevant python modules, such as [geopandas](https://geopandas.org/en/stable/) to access geospatial data and apply spatial operations on geometric types, [rasterio](https://rasterio.readthedocs.io/en/latest/) to access geospatial raster data, etc.
```
conda create -n spyder-env -y
conda activate spyder-env
conda install spyder-kernels rasterio -y 

conda install matplotlib
conda install shapely

conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install python=3 geopandas

set spyder preference
```
