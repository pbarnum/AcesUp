#!/bin/bash

# vars
NAME=acesup
SPEC=$NAME.spec
DIST_BIN=./dist/$NAME
PATH_BIN=/usr/bin/$NAME

# build the game
echo -e "Building $NAME...\n"
pyinstaller $SPEC --onefile

# we need root to add it to the path
if [[ `id -u` -ne 0 ]]; then
    echo -e "\nRun this script as root to add it into your PATH"
else
    # move the binary to the path
    echo -e "\nAdding $NAME to path..."
    cp $DIST_BIN $PATH_BIN

    # change group/owner for game
    echo -e "\nChanging ownership for $NAME..."
    chown root:$USER $PATH_BIN
fi
