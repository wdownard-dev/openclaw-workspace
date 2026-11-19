#!/bin/bash
cd "$(dirname "$0")"
python3 -u chain.py odysseus gen/odysseus__sworddraw__a1_white.png offerbowl tiptoe lookup > logs/r4_ody.log 2>&1 &
sleep 2; VARIANT=2 python3 -u chain.py crew - point:4 > logs/r4_crew.log 2>&1 &
sleep 2; VARIANT=2 python3 -u chain.py thucydides - palmsup:4 > logs/r4_thuc.log 2>&1 &
wait
python3 -u gen.py batch jobs_plates.json > logs/plates.log 2>&1
