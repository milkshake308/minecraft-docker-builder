import requests
import sys

VERSION_MANIFEST = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
FORGE_VERSION_MANIFEST = 'https://meta.multimc.org/v1/net.minecraftforge/index.json'

class GameManifest:

    def __init__(self) -> None:
        self.raw_manifest = requests.get(VERSION_MANIFEST).json()['versions']
        
    def filter_manifest(self, type_filter) -> None:


        filtered_manifest = [entry for entry in self.raw_manifest if entry['type'] == type_filter]
        print(f"Filtered {len(self.raw_manifest)-len(filtered_manifest)} entry from manifest")
        self.raw_manifest = filtered_manifest

    def build_manifest(self) -> None:

        raw_manifest = self.raw_manifest
        
        self.manifest = []
        
        progress_max = len(raw_manifest)
        count = 0
        for game_instance in raw_manifest:
            count += 1
            server_download_url = self.get_java_executable_link(game_instance, count, progress_max)
            
            if not server_download_url == '' :
                game_instance['server_download_url'] = server_download_url
                self.manifest.append(game_instance)

    def get_game_instance_by_version(self, version_string) -> dict:
        try:
            game_instance = [game_instance for game_instance in self.manifest if game_instance['id'] == version_string]
            return game_instance[0]
        except Exception :
            print(f'Critical error : Version {version_string} does not exists in manifest !')
            sys.exit(1)
    
    def get_java_executable_link(self, game_instance, progess_current=1, progress_max=1) -> str:
        instance_manifest = game_instance['url']

        print(f"\rFetching subcontent : {progess_current} / {progress_max}", end='', flush=True)

        # return to line after completion
        if progess_current == progress_max:
            print()
        
        instance_manifest = requests.get(instance_manifest).json()

        try:
            return instance_manifest['downloads']['server']['url']
        #  Some old mc version do not have download link
        except KeyError :
            return ''