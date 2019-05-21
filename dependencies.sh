#!/bin/bash
echo "Compiling dependencies, please wait..."
g++ -o easyPET_edugate_analyser easyPET_edugate_analyser.C `root-config --cflags --libs` -O3 -std=c++0x
echo "Done!"