#!/bin/bash
cd "$(dirname "$0")"
python3 -u chain.py odysseus gen/odysseus__shrug__a1_white.png think flat smug > logs/r2_ody.log 2>&1 &
sleep 2; python3 -u chain.py polyphemus gen/polyphemus__scorn__a1_white.png beam tender armswide > logs/r2_poly.log 2>&1 &
sleep 2; python3 -u chain.py crew - point:2 plead:2 torch:2 > logs/r2_crew.log 2>&1 &
sleep 2; python3 -u chain.py cyc2 gen/cyc2__smith_hammer__a1_white.png smith_tongs smith_flat > logs/r2_cyc2.log 2>&1 &
sleep 2; python3 -u chain.py thucydides - palmsup:2 > logs/r2_thuc.log 2>&1 &
wait
