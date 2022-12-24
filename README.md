# Land Use Analysis
This computes the land use for five counties in Iowa state, Black Hawk, Butler, Franklin, Carroll, Webst. In oreder to do the analysis, first we create Shapely Point type object for each pixel and use the affine projection matrix to convert it to a position in UTM Zone 15. 

### Setup for spyder on Windows
Install miniconda as admin and relevant python modules, such as geopandas, rasterio
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
