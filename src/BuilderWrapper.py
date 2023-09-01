from src.MinecraftDockerBuilder import MinecraftDockerBuilder
from src.VersionParser import MinecraftVersion
import config


def build_vanilla_image(game_instance: dict, overwrite=False):

    if overwrite:
        print("Existing images will be overwritten.")

    builder = MinecraftDockerBuilder(
        base_docker_image       = config.DOCKER_IMAGE_DEFAULT,
        repo_maintainer         = config.REGISTRY_REPO_MAINTAINER,
        maintainer_label        = config.DOCKER_IMAGE_MAINTAINER,
        image_name              = "minecraft-vanilla-server",
        image_tag               = game_instance['id'],
        docker_templates_path   = config.DOCKER_TEMPLATE_PATH,
        docker_build_path       = config.DOCKER_BUILD_PATH,
        java_executable_url     = game_instance['server_download_url'],
        instance_type           = 'vanilla',
        entrypoint_file         = config.DOCKER_ENTRYPOINT_VANILLA,
        rcon_password           = config.RCON_PASSWORD,
    )
    builder.build_docker_image(overwrite)

def build_forge_image(game_instance: dict, overwrite=False):

    if overwrite:
        print("Existing images will be overwritten.")

    #  "Legacy" servers (pre 1.17.1) requires Java 8
    if MinecraftVersion(game_instance['id']) < MinecraftVersion("1.17.1"):
        base_image      = config.DOCKER_IMAGE_FORGE_LEGACY
        entrypoint_file = config.DOCKER_ENTRYPOINT_FORGE_LEGACY
    else:
        base_image      = config.DOCKER_IMAGE_DEFAULT
        entrypoint_file = config.DOCKER_ENTRYPOINT_FORGE

    builder = MinecraftDockerBuilder(
        base_docker_image       = base_image,
        repo_maintainer         = config.REGISTRY_REPO_MAINTAINER,
        maintainer_label        = config.DOCKER_IMAGE_MAINTAINER,
        image_name              = "minecraft-forge-server",
        image_tag               = game_instance['id'],
        docker_templates_path   = config.DOCKER_TEMPLATE_PATH,
        docker_build_path       = config.DOCKER_BUILD_PATH,
        java_executable_url     = game_instance['server_download_url'],
        instance_type           = 'forge',
        entrypoint_file         = entrypoint_file,
        rcon_password           = config.RCON_PASSWORD,
    )
    builder.build_docker_image(overwrite)


