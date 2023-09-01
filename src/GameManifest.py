import requests
import sys

VERSION_MANIFEST = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
FORGE_VERSION_MANIFEST = 'https://meta.multimc.org/v1/net.minecraftforge/index.json'


class GameManifest:

    def __init__(self) -> None:
        self.raw_manifest = requests.get(VERSION_MANIFEST).json()['versions']
        
    def filter_manifest(self, raw_manifest: list, type_filter: dict, invert_filter=False) -> []:

        filter_key = list(type_filter.keys())[0]
        filter_value = type_filter[filter_key]
        if invert_filter:
            filtered_manifest = [entry for entry in raw_manifest if entry[ filter_key ] != filter_value]
        else:
            filtered_manifest = [entry for entry in raw_manifest if entry[ filter_key ] == filter_value]
        print(f"Filtered {len(raw_manifest)-len(filtered_manifest)} entry from manifest")
        
        return filtered_manifest
    
    def save_raw_manifest(self, raw_manifest: list) -> None:
        self.raw_manifest = raw_manifest

    #  Construct manifest with download link, remove entries that do not have download links
    def build_manifest(self) -> None:

        raw_manifest = self.raw_manifest
        
        self.manifest = []
        
        #  Progress Tracking
        progress_max = len(raw_manifest)
        count = 0
        
        for game_instance in raw_manifest:
            count += 1
            server_download_url = self.get_java_executable_link(game_instance, count, progress_max)
            
            if server_download_url :
                game_instance['server_download_url'] = server_download_url
                self.manifest.append(game_instance)
        
        return self.manifest

    def get_game_instance_by_version(self, version_string) -> dict:
        try:
            game_instance = [game_instance for game_instance in self.manifest if game_instance['id'] == version_string]
            return game_instance[0]
        except Exception :
            print(f'Critical error : Version {version_string} does not exists in manifest !')
            sys.exit(1)

    def get_java_executable_link(self, game_instance, progess_current=1, progress_max=1, forge=None) -> str:
        #  Mojang no longer provides downloadable librairies this version
        if game_instance['id'] == "1.5.2":
            return None
        
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
            return None
    #  Check if link is downloadable
    def check_if_downloadable(self, url):
        try:
            response = requests.head(url)
            content_type = response.headers.get('content-type')
            if 'text' not in content_type.lower():
                return True
        except Exception:
            pass
        return False
    

class ForgeGameManifest(GameManifest):

    def __init__(self) -> None:
        super().__init__()
        self.forge_manifest = []
        self.get_forge_manifest()
    
    #  Overwriting parent method to fit Forge manifest schema
    def get_java_executable_link(self, game_instance, progess_current=1, progress_max=1, forge=None) -> str:
        #  Mojang no longer provides downloadable librairies this version
        if game_instance['id'] == "1.5.2":
            return None

        print(f"\rFetching subcontent : {progess_current} / {progress_max}", end='', flush=True)
        # return to line after completion
        if progess_current == progress_max:
            print()
        
        instance_manifest = self.get_best_forge_version(game_instance['id'])

        if instance_manifest :
            forge_version = instance_manifest['forge_version']
            minecraft_version = instance_manifest['version'] ## == game_instance['id']
            potential_urls = [
                f"https://maven.minecraftforge.net/net/minecraftforge/forge/{minecraft_version}-{forge_version}/forge-{minecraft_version}-{forge_version}-installer.jar",
                f"https://maven.minecraftforge.net/net/minecraftforge/forge/{minecraft_version}-{forge_version}-{minecraft_version}/forge-{minecraft_version}-{forge_version}-{minecraft_version}-installer.jar",
                f"https://maven.minecraftforge.net/net/minecraftforge/forge/{minecraft_version}-{forge_version}-{minecraft_version}/forge-{minecraft_version}-{forge_version}-{minecraft_version}-installer.jar"
            ] 
            for url in potential_urls:
                if self.check_if_downloadable(url):
                    return url
        return None

    def get_forge_manifest(self):

        fml = requests.get(FORGE_VERSION_MANIFEST).json()['versions']
        for game_instance in fml:
            self.forge_manifest.append({
                "forge_version": game_instance["version"],
                "version": game_instance["requires"][0]["equals"],
                "recommended": game_instance.get("recommended", False)
            })

    def get_best_forge_version(self, minecraft_version_str):

        matched_version = [ versions for versions in self.forge_manifest if versions['version'] == minecraft_version_str]
        recommended_version = [ versions for versions in matched_version if versions['recommended'] == True ]
        
        #  Either recommended or latest if recommended do not exists
        if len(recommended_version) > 0:
            return recommended_version[0]
        elif len(matched_version) > 0:
            return matched_version[0]
        else:
            return None
        