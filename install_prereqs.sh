#!/usr/bin/env bash

unamestr=`uname`
if [[ "$unamestr" = *'CYGWIN'* ]]; then
   echo "Cygwin not supported, install using native Windows method"
   exit
elif [[ "$unamestr" = *'Linux'* ]]; then
   PACKAGE_MANAGER_INSTALL='apt install'
fi

$PACKAGE_MANAGER_INSTALL python3 python3-pip
pip3 install python3-xlib
$PACKAGE_MANAGER_INSTALL python3-tk python3-dev scrot

pip3 install pyautogui
