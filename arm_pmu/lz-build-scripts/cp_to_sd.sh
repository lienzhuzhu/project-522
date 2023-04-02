#!/usr/bin/bash

cd $HOME/linux_source/linux

sudo env PATH=$PATH make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=/media/lienzhu/rootfs/ modules_install

sudo cp arch/arm/boot/zImage /media/lienzhu/bootfs/kernel7.img
sudo cp arch/arm/boot/dts/*.dtb /media/lienzhu/bootfs/
sudo cp arch/arm/boot/dts/overlays/*.dtb* /media/lienzhu/bootfs/overlays/
sudo cp arch/arm/boot/dts/overlays/README /media/lienzhu/bootfs/overlays/

cd /media/lienzhu
