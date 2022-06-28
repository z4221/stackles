#!/bin/sh

PROGRAM=compilerout.c

gcc -Os -Wall -Wpedantic -fsanitize=address -fsanitize=undefined $PROGRAM
