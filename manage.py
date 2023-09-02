#!/usr/bin/python3
from commands import context_handler, pretty_list_version
import argparse
import config 

parser = argparse.ArgumentParser(description="Minecraft Server Docker Image Builder")

subparsers = parser.add_subparsers(title="commands", dest="command")

#  Command 'build'
build_parser = subparsers.add_parser('build', help="Build minecraft server docker images")

build_parser.add_argument('-t', '--target', required=True, choices=['vanilla', 'forge'], help="Target instance to build")
build_parser.add_argument('-f', '--force', action='store_true', help="Overwrite image if exist in Docker")
build_parser.add_argument('-v', '--version', required=True, help="Target version to build")
build_parser.add_argument('--repository', '--repo', action='store_true', help="Docker repository")
build_parser.add_argument('--maintainer', action='store_true', help="Image maintainer identity")
build_parser.add_argument('--dump', action='store_true', help="Dump Manifest Json, Instance Json")

#  Command 'list'
list_parser = subparsers.add_parser("list", help="Get a list of buildable minecraft versions")
list_parser.add_argument('-t', '--target', required=True, choices=['vanilla', 'forge'], help="Target instance to build")


args = parser.parse_args()


if args.command == 'build':
    overwrite, dump_json = False, False
    if args.force:
        overwrite = True
    if args.repository:
        config.REGISTRY_REPO_MAINTAINER = args.repository
    if args.maintainer:
        config.DOCKER_IMAGE_MAINTAINER = args.args.maintainer
    if args.dump:
        dump_json = True
    context_handler(args.version, args.target, overwrite, dump_json)
elif args.command == 'list':
    pretty_list_version(args.target)
else:
    parser.print_usage()
