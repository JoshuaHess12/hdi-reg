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
python app/command_elastix.py --path_to_yaml /data/yourfile.yaml --out_dir /data
```

### Usage without Docker:
If you are unable to use Docker on your machine, then you can still use hdi-reg:
1. [download Elastix](https://github.com/SuperElastix/elastix/releases/tag/5.0.1) 
2. Make Elastix accessible to your `$PATH` environment (Ex. on a Mac, access your `.bash_profile` and add `export PATH=~/elastix-latest/bin:$PATH` and `export DYLD_LIBRARY_PATH=~/elastix-latest/lib:$DYLD_LIBRARY_PATH`)
3. Run registration as above in step 5.

## Contributing to hdi-reg
If you are interested in contributing to hdi-reg, access the contents to see the software organization. Code structure is documented for each module.
