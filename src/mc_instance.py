import docker
import os
class MinecraftDockerBuilder:

    def __init__(self, base_docker_image, image_name, image_tag, docker_templates_path, docker_build_path, java_executable_url, instance_type) -> None:
        self.docker_client = docker.from_env()
        self.base_docker_image = base_docker_image
        self.image_name = image_name
        self.image_tag = image_tag
        self.docker_templates_path = docker_templates_path
        self.docker_build_path = docker_build_path
        self.java_executable_url = java_executable_url
        self.instance_type = instance_type

    def configure_docker_image(self):
        #  Load and configure image
        dockerfile = open(self.docker_templates_path+f"/{self.instance_type}_dockerfile", "r", encoding="utf-8").read()
        mappings = {
            "docker_image_origin" : self.base_docker_image,
            "java_executable_url" : self.java_executable_url,
            # "entrypoint_content" : entrypoint_file
        }
        
        self.dockerfile = dockerfile.format_map(mappings)
        return self.dockerfile

    def build_docker_image(self, overwrite):
        self.configure_docker_image()
        print(f"Building minecraft server image {self.image_name}:{self.image_tag} ")
        self.export_dockerfile(self.docker_build_path+'/Dockerfile')
        #  Build image and tag
        build_params = {
        "path":'./build/',
        "tag": f"{self.image_name}:{self.image_tag}"
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
        
        print('Exported dockerfile to', path,'.')


class MinecraftVanillaDockerBuilder(MinecraftDockerBuilder):

    def __init__(self, base_docker_image, image_name, image_tag, docker_templates_path, docker_build_path, java_executable_url) -> None:
        super().__init__(base_docker_image, image_name, image_tag, docker_templates_path, docker_build_path, java_executable_url, instance_type='vanilla')

class MinecraftForgeDockerBuilder(MinecraftDockerBuilder):

    def __init__(self, base_docker_image, image_name, image_tag, docker_templates_path, docker_build_path, java_executable_url) -> None:
        super().__init__(base_docker_image, image_name, image_tag, docker_templates_path, docker_build_path, java_executable_url, instance_type='forge')
