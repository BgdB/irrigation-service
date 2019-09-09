#!/bin/bash

ZONE_ID=$1
DURATION=$2

gpio -g mode $ZONE_ID out
gpio -g write $ZONE_ID 1
sleep $DURATION

gpio -g write $ZONE_ID 0
