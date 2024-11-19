#!bin/bash
  fluidsynth -is --audio-driver=alsa --gain 3 /usr/share/sounds/sf2/FluidR3_GM.sf2 &
  
  sleep 10

  aconnect 28:0 128:0

  # set the priority of pi user to 18 (max sss 19)
  sudo renice -n 18 -u piano