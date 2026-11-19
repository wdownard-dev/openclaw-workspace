#!/bin/bash
cd "$(dirname "$0")"
python3 -u chain.py odysseus gen/odysseus__smug__a1_white.png armscrossed sworddraw swordlower > logs/r3_ody.log 2>&1 &
sleep 2; python3 -u chain.py polyphemus gen/polyphemus__armswide__a1_white.png wounded > logs/r3_poly.log 2>&1 &
sleep 2; python3 -u chain.py crew - point:3 plead:3 torch:3 > logs/r3_crew.log 2>&1 &
sleep 2; python3 -u chain.py thucydides - palmsup:3 > logs/r3_thuc.log 2>&1 &
wait
