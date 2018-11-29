#!/bin/bash

# set terminal back to normal colors
# sometimes happened that force quit from tapestry script leave terminal in black mode
# in this case, ./t.sh must be launched

setterm -foreground black
clear
sleep 1
setterm -foreground white
clear
