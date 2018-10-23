#!/bin/bash

setterm -foreground black
clear
python3 ./tapestry.py $1 &> /var/log/tapestry.log
setterm -foreground white
clear
