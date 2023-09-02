# Minecraft Docker Builder Tool

The Minecraft Docker Builder Tool is designed to simplify the mass creation of Docker images for Minecraft servers, both vanilla and Forge, using all available game release versions (where download links are still available).

## Overview

- **Ease of Use**: Create Docker images for Minecraft servers in just a few simple steps.
- **Vanilla and Forge Support**: Build images for both vanilla Minecraft servers and modded Forge servers.
- **Version Management**: Enjoy flexibility in building images for different game versions.
- **Docker Compatibility**: Images are built using Docker, ensuring maximum compatibility and portability.
- **Barebone installation**: These images are meant to be as simple as possible, to provide a base for your own tools or changes on top of it.

### How It Works

1. **Select Server Type**: Choose between vanilla or Forge depending on your needs.
2. **Specify Version**: Provide the version of the game you want to use.
3. **Customize Options**: Utilize options such as overwriting existing images or Docker repository by setting them either throught cli command or overriding the default value in `config.py` .
4. **Start Building**: Let the tool automatically build your Docker image.

## Usage

```bash
# Example command to build a vanilla Docker image for minecraft 1.16.5 and 1.12.2
python manage.py build -t vanilla -v 1.16.5,1.12.2

# Example command to get a list of buildable versions for minecraft forge
python manage.py list -t forge

# Example command to build all possible vanilla Docker image
python manage.py build -t vanilla -v all

# Example command to upload push all images from a local repository
./mass_repo_upload  milkshake303
```

## Note

Please note that these Docker images are intended to serve as a basic building block for other projects. If your goal is to use these images as-is, it is recommended to use those created by [itzg on Docker Hub](https://hub.docker.com/u/itzg)
for a more ready-to-use solution.