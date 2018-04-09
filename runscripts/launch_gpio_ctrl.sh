#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python $SCRIPT_DIR/../ping_rpi_gpio_serv_control.py
