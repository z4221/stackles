#!/bin/sh

PROGRAM=compilerout.c

#gcc -Os -Wall -Wpedantic -fsanitize=address -fsanitize=undefined $PROGRAM
musl-gcc -O3 -static $PROGRAM
strip a.out
