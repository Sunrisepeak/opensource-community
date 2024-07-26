#!/bin/bash

if pip list | grep qq-botpy
then
    echo qq-botpy installed
else
    pip install qq-botpy
fi

# Check for curl
if command -v curl &> /dev/null
then
    echo "Public IP (via curl): xx" #$(curl -s ifconfig.me)"
else
    # Check for wget
    if command -v wget &> /dev/null
    then
        echo "Public IP (via wget): xx" #$(wget -qO- ifconfig.me)"
    else
        echo "Neither curl nor wget is installed."
    fi
fi

python3 yy_qbot.py