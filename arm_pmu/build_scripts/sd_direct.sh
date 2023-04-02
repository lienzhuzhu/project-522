#!/usr/bin/bash

cd $HOME/linux_source/linux

sudo env PATH=$PATH make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=/media/lienzhu/rootfs/ modules_install

sudo cp arch/arm/boot/zImage /media/lienzhu/boot/kernel7.img
sudo cp arch/arm/boot/dts/*.dtb /media/lienzhu/boot/
sudo cp arch/arm/boot/dts/overlays/*.dtb* /media/lienzhu/boot/overlays/
sudo cp arch/arm/boot/dts/overlays/README /media/lienzhu/boot/overlays/

cd /media/lienzhu
