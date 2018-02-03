#!/usr/bin/env bash

unamestr=`uname`
if [[ "$unamestr" = *'CYGWIN'* ]]; then
   apt='apt-cyg'
elif [[ "$unamestr" = *'Linux'* ]]; then
   apt='apt'
fi

$apt install python3 python3-pip
pip3 install python3-xlib
$apt install scrot python3-tk python3-dev

pip3 install pyautogui