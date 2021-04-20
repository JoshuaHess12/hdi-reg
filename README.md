# hdi-reg
High-dimensional image registration workflow as part of the MIAAIM framework. Hdi-reg is written in Python, and utilizes the [Elastix](https://elastix.lumc.nl) library for computations.

## Implementation Details
All steps can be run from the command line using command_elastix.py or command_transformix.py. Transformix is reserved for applying existing transformation parameters to images after running Elastix. 

### Command Line Usage with Docker (recommended):
All image registration can be run with dependecies installed via Docker as follows:
1. Install [Docker](https://www.docker.com) on your machine.
2. Check that Docker is installed with `docker images`
3. Pull the hdi-reg docker container `docker pull joshuahess/hdi-reg:latest` where latest is the version number.
4. Mount your data in the Docker container and enter shell with `docker run -it -v /path/to/data:/data joshuahess/hdi-reg:latest bash`
5. Run the registration with your new data using the following command:
```bash
python app/command_elastix.py --f /data/fixedImage.nii --m /data/movingImage.nii -p /data/registrationPars.txt --out_dir /data
```
6. Tranforming images, such as multichannel images, with transformix on new data can be run as follows:
```bash
python app/command_transformix.py --in_im /data/newIm.nii  --tp /data/registrationPars.txt --out_dir /data
```

### Usage without Docker:
If you are unable to use Docker on your machine, then you can still use hdi-reg:
1. [download](https://github.com/SuperElastix/elastix/releases/tag/5.0.1) the latest version of Elastix. 
2. Make Elastix accessible to your `$PATH` environment (Ex. on a Mac, access your `.bash_profile` and add `export PATH=~/elastix-latest/bin:$PATH` and `export DYLD_LIBRARY_PATH=~/elastix-latest/lib:$DYLD_LIBRARY_PATH`)
3. Run registration and transformix as above in step 5.

#### Input Parameters:
Options for importing data and processing are listed below. Detailed descriptions of each function can be found within source code.
| hdi-reg Step | Options |
| --- | --- |
| 1.`command_elastix.py` | image registration between fixed image and moving image |
| `--fixed` | path to fixed image (Ex. `--fixed ./fixedImage.nii`) |
| `--moving` | path to moving image (Ex. `--moving ./movingImage.nii`) |
| `--out_dir` | path to output directory (Ex. `--out_dir ./outdirectory`) |
| `--p` | path(s) to parameter files for elastix registration (see examples [here](http://elastix.bigr.nl/wiki/index.php/Parameter_file_database)) (Ex. `--p ./affineParameters.txt --p ./nonlinearParameters.txt`) |
| `--mp` | path to manual landmark points (Ex. `--mp ./movingPoints.txt`) |
| `--fp` | path to manual landmark points (Ex. `--fp ./fixedPoints.txt`) |
| `--fMask` | fixed image mask to draw samples from during optimization (Ex. `--fMask ./fixedMask.nii`) |
| 1.`command_transformix.py` | transform images using saved transformation from elastix |
| `--in_im` |path to image to transform (can be multichannel) (Ex. `--in_im ./movingMultichannel.nii`) |
| `--out_dir` |  path to output directory (Ex. `--out_dir ./outdirectory`) |
| `--tps` | path(s) to parameter files exported from elastix (Ex. `--tps ./affineTransformParameters.txt --tps ./nonlinearTransformParameters.txt`) |
| `--in_target_size` | tuple indicating target size to rescale image to prior to tranformix (Ex. `--in_target_size (1000,1000`) |
| `--crops` | nested dictionary coordinates to crop ROIs from in full image for further refinement <br> <br> Options: <br> `coords_csv` path to csv file indicating coordinates of full image to crop <br> `target_size` rescaled size of ROI to produce prior to transforming <br> `correction` padding to add to edges of crop to account for misalignment on full tissue <br> `tps` transform parameters (as above) focused on ROIs <br> `fixed_pad` padding to remove from the resulting image after transforming (if this matches padding added to fixed image, then result will be fully aligned) |


