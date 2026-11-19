#!/bin/bash
cd "$(dirname "$0")"
python3 -u chain.py odysseus - walk talk shrug > logs/r1_ody.log 2>&1 &
sleep 2; python3 -u chain.py polyphemus - wave leandown scorn > logs/r1_poly.log 2>&1 &
sleep 2; python3 -u chain.py crew - point plead torch > logs/r1_crew.log 2>&1 &
sleep 2; python3 -u chain.py cyc2 - shrug back smith_hammer > logs/r1_cyc2.log 2>&1 &
sleep 2; python3 -u chain.py thucydides - palmsup > logs/r1_thuc.log 2>&1 &
wait
