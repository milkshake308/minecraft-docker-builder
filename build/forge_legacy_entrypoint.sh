#!/bin/bash

if [ "${EULA^^}" = "TRUE" ]; then
    echo "eula=true" > eula.txt 
else
    echo "EULA has not been accepted, please read eula https://www.minecraft.net/en-us/eula then set environnement variable EULA=TRUE before launching the minecraft server"
    exit 1
fi

if [ -z "${JAVA_ARGS}" ]; then
    jvm_args="-Xmx2G -Xms512M"
    echo "No custom java arguments passed, assuming default $jvm_args"
    export JAVA_ARGS=$jvm_args
fi
cd /minecraft
java $JAVA_ARGS -jar server.jar nogui