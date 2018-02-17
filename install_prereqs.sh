#!/usr/bin/env bash

unamestr=`uname`
if [[ "$unamestr" = *'CYGWIN'* ]]; then
   echo "Cygwin not supported, install using native Windows method"
   exit
elif [[ "$unamestr" = *'Linux'* ]]; then
   PACKAGE_MANAGER_INSTALL='apt install'
fi

echo "Package manager identified."
echo "If you get Permission-related errors, re-run this file using elevated privileges (sudo)"

$PACKAGE_MANAGER_INSTALL python3 python3-pip libjpeg8-dev zlib1g-dev
pip3 install python3-xlib
pip3 install Image
pip3 install pillow
$PACKAGE_MANAGER_INSTALL python3-tk python3-dev scrot

pip3 install pyautogui
