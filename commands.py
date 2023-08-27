from src.mc_instance import MinecraftVanillaDockerBuilder
from src.mc_instance import MinecraftForgeDockerBuilder
from src.mc_manifest import GameManifest
import json
import os

current_directory = os.path.abspath(os.path.dirname(__file__))


DOCKER_IMAGE_ORIGIN = 'ghcr.io/graalvm/jdk-community:20.0.1-ol9'
DOCKER_TEMPLATE_PATH = os.path.join(current_directory, 'docker-templates')
DOCKER_BUILD_PATH = os.path.join(current_directory, 'build')

def cache_game_manifest():
    global mc 
    mc = GameManifest()

def build_vanilla_image(game_instance : dict, overwrite=False):

    builder = MinecraftVanillaDockerBuilder(
        base_docker_image = DOCKER_IMAGE_ORIGIN,
        image_name = "minecraft-vanilla-server",
        image_tag = game_instance['id'],
        docker_templates_path = DOCKER_TEMPLATE_PATH,
        docker_build_path = DOCKER_BUILD_PATH,
        java_executable_url = game_instance['server_download_url']
    )
    builder.build_docker_image(overwrite)

def build_handler(version, game_type, overwrite):
    mc.filter_manifest('release')
    mc.build_manifest()
    
    if version == '':
        print('No target version provided \n Example : python build.py vanilla --target 1.12.2')
    elif version == 'all':
        for game_instance in mc.manifest:
            if game_type == 'vanilla':
                build_vanilla_image(game_instance, overwrite)
        
    elif ',' in version:
        versions = version.split(",")
        #  first loop to check that input is correct
        for ver in versions:
            mc.get_game_instance_by_version(ver)
        for ver in versions:
            game_instance = mc.get_game_instance_by_version(ver)
            if game_type == 'vanilla':
                build_vanilla_image(game_instance, overwrite)

    else:
        game_instance = mc.get_game_instance_by_version(version)
        if game_type == 'vanilla':
            build_vanilla_image(game_instance, overwrite)

def pretty_list_version(type):
    if type :
        mc.filter_manifest(type)

    if type == 'snapshot' or not type:
        print('Snapshots versions will be shown even if they cant be builded from this tool.')
    mc.build_manifest()
    manifest = mc.manifest
    
    print('Available Minecraft Version for build (in order of release): ')
    
    for version in manifest :
        try:
            print(f"-> Version : {version['id']:20}  Release Type : {version['type']:<10}  Release Date : {str(version['releaseTime'])[:10]}")
        except KeyError:
            print('Error while parsing')
            print(json.dumps(version, indent=4))

cache_game_manifest()