#!/bin/bash

cd $HOME/linux_source/linux
#make clean

KERNEL=kernel7l
make -j12 ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs

cd $HOME/scripts
