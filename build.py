from commands import build_handler, pretty_list_version
import argparse
import json

parser = argparse.ArgumentParser(description="Minecraft Server Docker Image Builder")

subparsers = parser.add_subparsers(title="commands", dest="command")

# Command 'vanilla'
parser_vanilla = subparsers.add_parser("vanilla", help="Build vanilla minecraft server docker image")
parser_vanilla.add_argument("--target", "-t", help="Target version to build (release only!)")
parser_vanilla.add_argument("--overwrite", help="Overwrite image if exist in Docker")

# Command 'forge'
parser_forge = subparsers.add_parser("forge", help="Build forge minecraft server docker image")
parser_forge.add_argument("--target", "-t", help="Target version to build (release only!)")
parser_forge.add_argument("--overwrite", help="Overwrite image if exist in Docker")

# Command 'List'
parser_list = subparsers.add_parser("list", help="Get a list of buildable minecraft versions")
parser_list.add_argument("--type", help="Filter versions by type release, snapshot")

args = parser.parse_args()


if args.command == "vanilla":
    overwrite = True if args.overwrite else False
    build_handler(args.target, 'vanilla', overwrite)

if args.command == "forge":

    overwrite = True if args.overwrite else False
    print("Forge image builder not yet implemented")
    # TODO: implement it :)
    # build_handler(args.target)

if args.command == "list":
    pretty_list_version(args.type)  # Pass the 'type' argument to pretty_list_version