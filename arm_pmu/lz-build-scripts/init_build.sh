#!/bin/bash

sudo apt update
sudo apt install -y git bc bison flex libssl-dev make libc6-dev libncurses5-dev
sudo apt install -y crossbuild-essential-armhf

cd $HOME
mkdir linux_source
cd linux_source

git clone --depth=1 https://github.com/raspberrypi/linux

cd linux
KERNEL=kernel7l
make -j12 ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2709_defconfig
make -j12 ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs

cd $HOME/scripts
