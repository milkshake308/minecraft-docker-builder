from src.VersionParser import MinecraftVersion
from src.GameManifest import GameManifest, ForgeGameManifest
from src.BuilderWrapper import build_vanilla_image, build_forge_image
import json
    

#  Handle version processing then passe the rest to build_handler()
def context_handler(version, game_type, overwrite, dump_json=False):

    mc = get_builded_manifest(game_type)

    if version == '':
        print('No target version provided \n Example : python build.py vanilla --target 1.12.2')

    #  Build all possible versions
    elif version == 'all':
        for game_instance in mc.manifest:
            build_handler(
                game_type = game_type,
                game_instance = game_instance, 
                overwrite = overwrite,
                dump_manifest = mc.manifest if dump_json else None ## Build 
                )

    #  Build versions list
    elif ',' in version:
        versions = version.split(",")

        #  first loop to check that input is correct
        for ver in versions:
            mc.get_game_instance_by_version(ver)

        for ver in versions:
            game_instance = mc.get_game_instance_by_version(ver)
            
            build_handler(
                game_type = game_type,
                game_instance = game_instance, 
                overwrite = overwrite,
                dump_manifest = mc.manifest if dump_json else None
                )

    # Build version specific      
    else:
        game_instance = mc.get_game_instance_by_version(version)
        build_handler(
                game_type = game_type,
                game_instance = game_instance, 
                overwrite = overwrite,
                dump_manifest = mc.manifest if dump_json else None
                )


#  Handle image building and jsons dumpings
def build_handler(game_type, game_instance, overwrite, dump_manifest=None):
    if dump_manifest:
            print(json.dumps(dump_manifest, indent=4), json.dumps(game_instance, indent=4), sep='\n\n')
            return None
    
    if game_type == 'vanilla':
        build_vanilla_image(game_instance, overwrite)
    elif game_type == 'forge':
        build_forge_image(game_instance, overwrite)


def get_builded_manifest(game_type):
    if game_type == 'vanilla':
        mc = GameManifest()
       
    elif game_type == 'forge':
        mc = ForgeGameManifest()
    mc.save_raw_manifest(mc.filter_manifest(
       raw_manifest = mc.raw_manifest, 
       type_filter = {'type': 'release'}
       ))
    mc.build_manifest()
    return mc


def pretty_list_version(game_type):

    mc = get_builded_manifest(game_type)

    manifest = mc.manifest
    
    print('Available Minecraft Version for build (in order of release): ')
    
    for version in manifest :
        try:
            print(f"-> Version : {version['id']:20}  Release Type : {version['type']:<10}  Release Date : {str(version['releaseTime'])[:10]}")
        except KeyError:
            print('Error while parsing')
            print(json.dumps(version, indent=4))