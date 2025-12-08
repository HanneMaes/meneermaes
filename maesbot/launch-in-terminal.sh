#!/bin/bash
cd /home/hanne/Documents/meneermaes/maesbot
kitty --start-as=normal \
  -o initial_window_width=700 \
  -o initial_window_height=500 \
  -e ./init.sh
