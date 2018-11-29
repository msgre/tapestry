#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
setterm -foreground black
clear
python3 $DIR/tapestry.py $1 &> /var/log/tapestry.log
setterm -foreground white
clear
