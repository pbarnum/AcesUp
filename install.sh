#!/bin/bash

# vars
NAME=acesup
SPEC=$NAME.spec
DIST_BIN=./dist/$NAME

# build the game
echo -e "Building $NAME...\n"
pyinstaller $SPEC --clean --onefile
