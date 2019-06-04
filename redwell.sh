#!/bin/bash

# get Tempertures
TEMP=$(grep innentemp /var/lib/munin-node/plugin-state/dw.state | cut -d" " -f 2)
echo "Temp:         $TEMP C"

STATE=$(grep irheizungstatus /var/lib/munin-node/plugin-state/ir.state | cut -d" " -f 2)
echo "IR Status:    $STATE"


##############################################################################
# MODEs
##############################################################################

# Manual hi/lo Temperature MODE
# 19.3 - 22.3
# 19.7 - 21.3 nacht/leer
# 19.3 - 20.8 herbst 2016 
MIN=19.4
MAX=20.1

# Auto MODE via Aerosmart control on-> 1 , off -> 0
DWMODE=1

# If DWMODE =1 Aerosmart Heating operation switch Hard/Soft

#SOFT WP-mode
#DW=$(grep heizstufe1anforderungstatus /var/lib/munin-node/plugin-state/dw.state | cut -d" " -f 2)

#HARD PTC-mode 
DW=$(grep heizstufe2anforderungstatus /var/lib/munin-node/plugin-state/dw.state | cut -d" " -f 2)

SMARTPLUGIP=192.168.1.31
#SMARTPLUGON=/root/tplink-smartplug.py -t $SMARTPLUGIP -c on
#SMARTPLUGOFF=/root/tplink-smartplug.py -t $SMARTPLUGIP -c off
#STATUS=/root/tplink-smartplug.py -t $SMARTPLUGIP -c status

##############################################################################
# FUNCTIONS
##############################################################################


function smartplugon {
    /root/tplink-smartplug.py -t $SMARTPLUGIP -c on
}

function smartplugoff {
    /root/tplink-smartplug.py -t $SMARTPLUGIP -c off
}

# STATUS
function status {
    STATUS=$(/root/tplink-smartplug.py -t $SMARTPLUGIP -c status)
    echo "STATUS:"
    echo "  smartplug:  $STATUS"

    if [[ $STATUS == "1" ]] ; then
        echo "irheizungstatus.value 1" > /var/lib/munin-node/plugin-state/ir.state
        STATE=1
        elif [[ $STATUS == "0" ]] ; then
            echo "irheizungstatus.value 0" > /var/lib/munin-node/plugin-state/ir.state
            STATE=0
        else
            echo "irheizungstatus.value 0" > /var/lib/munin-node/plugin-state/ir.state
            STATE=0
    fi
    echo "  IR state:   $STATE"
}




# DWMODE
function dwmode {
    echo "AEROSMART MODE ACTIVE"
    if [[ $DW -eq 1 ]] ; then
        echo "Switch heater ON"
        if [[ $STATE -eq 0 ]] ; then
            smartplugon
            status
        else
            echo "NOP"
        fi
    elif [[ $DW -eq 0 ]] ; then
        echo "Switch heater OFF"
        if [[ $STATE -eq 1 ]] ; then
            smartplugoff
            status
        else
            echo "NOP"
        fi
    elif [[ $(echo "$TEMP>$MAX" | bc) -eq 1 ]] ; then
        echo "Switch heater OFF"
        if [[ $STATE -eq 1 ]] ; then
            smartplugoff
            status
        else
            echo "NOP"
        fi
    else
        echo "NOP"
    fi
    exit 0
}


# MANUAL MODE
function manualmode {
    echo "MANUAL MODE ACTIVE"
    if [[ $(echo "$TEMP<$MIN" | bc) -eq 1 ]] ; then
        echo "Switch heater ON"
        if [[ $STATE -eq 0 ]] ; then
            smartplugon
            status
        else
            echo "NOP"
        fi
    elif [[ $(echo "$TEMP>$MAX" | bc) -eq 1 ]] ; then
        echo "Switch heater OFF"
        if [[ $STATE -eq 1 ]] ; then
            smartplugoff
            status
        else
            echo "NOP"
        fi
    else
        echo "NOP"
    fi
    exit 0
}


##############################################################################

#call functions

status

# doesn't work because not arp-scan'able
#presence

if [[ $DWMODE -eq 1 ]] ; then
    dwmode
else
    manualmode
fi

