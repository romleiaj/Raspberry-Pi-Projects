#!/bin/bash
SESSION=power_control

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd ${SCRIPT_DIR}

echo "$(date) Creating tmux session ${SESSION}"
tmux new-session -d -s $SESSION

sleep 1
echo "$(date) Starting power control server..."
tmux select-window -t $SESSION:0
tmux rename-window -t $SESSION:0 'GPIO control server'
tmux send-keys -t $SESSION:0 "cd ${SCRIPT_DIR}" C-m
tmux send-keys -t $SESSION:0 "${SCRIPT_DIR}/launch_gpio_ctrl.sh" C-m

