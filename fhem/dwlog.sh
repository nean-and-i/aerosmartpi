#!/bin/bash
# create cronjob to gather log from aerosmartpi
#*/5 * * * * /opt/fhem/dwlog.sh
TODAY=`date +"%Y-%m"`
scp pi@<aerosmartpi>:/var/lib/munin-node/plugin-state/dw.state /opt/fhem/log/
chown fhem /opt/fhem/log/dw.state
awk -v now="$(date +"%F_%T")" '{ print now " " $0}' /opt/fhem/log/dw.state | grep -v beschattungaussentemp >> /opt/fhem/log/dw-$TODAY.log
chown fhem /opt/fhem/log/dw-$TODAY.log
