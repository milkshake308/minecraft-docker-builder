import docker
import os


class MinecraftDockerBuilder:

    def __init__(self, base_docker_image, repo_maintainer, maintainer_label, rcon_password, image_name, image_tag, docker_templates_path, docker_build_path, java_executable_url, instance_type, entrypoint_file) -> None:
        self.docker_client          = docker.from_env()
        self.base_docker_image      = base_docker_image
        self.repo_maintainer        = repo_maintainer 
        self.maintainer_label       = maintainer_label
        self.__rcon_password        = rcon_password
        self.image_name             = image_name
        self.image_tag              = image_tag
        self.docker_templates_path  = docker_templates_path + '/'
        self.docker_build_path      = docker_build_path + '/'
        self.java_executable_url    = java_executable_url
        self.instance_type          = instance_type
        self.entrypoint_file        = entrypoint_file

    def configure_docker_image(self):
        #  Load and configure image
        dockerfile = open(self.docker_templates_path+self.instance_type+'-dockerfile', "r", encoding="utf-8").read()
        mappings = {
            "docker_image_origin" : self.base_docker_image,
            "java_executable_url" : self.java_executable_url,
            "entrypoint_file" : self.entrypoint_file,
            "rcon_password" : self.__rcon_password,
            "maintainer_label" : self.maintainer_label,
        }
        
        self.dockerfile = dockerfile.format_map(mappings)
        return self.dockerfile
    
    def remove_existing_image(self):
        try:
            existing_image = f"{self.repo_maintainer}/{self.image_name}:{self.image_tag}"
            self.docker_client.images.remove(existing_image, force=True)
            print(f"Overwriting previous image: {existing_image}")
        except docker.errors.ImageNotFound:
            pass

    def build_docker_image(self, overwrite):
        self.configure_docker_image()
        self.export_dockerfile(self.docker_build_path+'Dockerfile')
        if overwrite:
            self.remove_existing_image()
        print(f"Building minecraft server image {self.image_name}:{self.image_tag} ")
        #  Build image and tag
        build_params = {
        "path":'./build/',
        'nocache': True,
        'rm': True,  ## Clear intermediate containers  
        "tag": f"{self.repo_maintainer}/{self.image_name}:{self.image_tag}"
        }
        try:
            image, build_logs = self.docker_client.images.build(**build_params)
            print(f"Image ID: {image.id}")
            print(f"Tags: {', '.join(image.tags)}")
            print("Image built successfully!")
        except docker.errors.APIError as e:
            self.export_dockerfile(f"./dockerfile_{self.image_name}_{self.image_tag}")
            print(e)
            print('A Docker API error occured')
    
    def export_dockerfile(self, path):
        self.configure_docker_image()
        with open(path, "w", encoding="utf-8") as file:
            file.write(self.dockerfile)
        
        print('Exported dockerfile to', path)