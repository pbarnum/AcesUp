#!/bin/bash

# we need root to run
if [[ `id -u` -ne 0 ]]; then
    echo "Please run as root"
    exit
fi

# vars
NAME=acesup
SPEC=$NAME.spec
DIST_BIN=./dist/$NAME
PATH_BIN=/usr/bin/$NAME

# build the game
echo -e "Building $NAME...\n"
pyinstaller $SPEC --onefile

# move the binary to the path
echo -e "\nAdding $NAME to path..."
mv $DIST_BIN $PATH_BIN

# change group/owner for game
echo -e "\nChanging ownership for $NAME..."
chown root:$USER $PATH_BIN
