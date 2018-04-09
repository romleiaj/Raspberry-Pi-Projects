# Raspberry-Pi-Projects
Nifty script for remotely turning on/off computers via a raspberry pi and sainsmart 5V relay module.
If you wish to run a headless setup, simple edit etc/rc.local file with "su pi -c 'source /path/to/tmux_launch.sh'" and it run will run on power up with no ssh required. When sshed into machine, simply run 'tmux attach' to view running session as pi user.
