import os

current_directory = os.path.abspath(os.path.dirname(__file__))

DOCKER_IMAGE_DEFAULT            = 'ghcr.io/graalvm/jdk-community:17'  ## Default image
DOCKER_IMAGE_FORGE_LEGACY       = 'openjdk:8'  ## For Minecraft version > 1.17.1
DOCKER_ENTRYPOINT_VANILLA       = 'vanilla_entrypoint.sh'
DOCKER_ENTRYPOINT_FORGE         = 'forge_entrypoint.sh'
DOCKER_ENTRYPOINT_FORGE_LEGACY  = 'forge_legacy_entrypoint.sh'  ## For Minecraft version > 1.17.1
RCON_PASSWORD                   = 'rcon'
REGISTRY_REPO_MAINTAINER        = 'milkshake303'  ## Will be overwritten when using --repo
DOCKER_IMAGE_MAINTAINER         = 'Aaron S <rnsaa@proton.me>'  ## Will be overwritten when using --maintainer

DOCKER_TEMPLATE_PATH            = os.path.join(current_directory, 'docker-templates')
DOCKER_BUILD_PATH               = os.path.join(current_directory, 'build')