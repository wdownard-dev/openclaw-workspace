#!/usr/bin/env bash
cd "$(dirname "$0")"; F=/home/williamdownard/openclaw-sites/bin/ffmpeg
IN="-i ../../audio-n/narration_voice_only.wav -i roomtone.wav -i st1_drone.wav -i st2_hit.wav -i st3_outro.wav -i sfx_swallow.wav -i sfx_snap.wav -i sfx_ship.wav -i sfx_horn.wav -i sfx_splinter.wav"
$F -y -loglevel error $IN -filter_complex_script chain.txt -ar 48000 -ac 1 premix.wav
$F -hide_banner -i premix.wav -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2> pass1.txt
