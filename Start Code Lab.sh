#!/usr/bin/env bash
# Double-click to open the Code Lab on Linux.
# (If double-click opens it in a text editor instead, either mark it executable
#  in your file manager's properties, or run:  bash "Start Code Lab.sh")
cd "$(dirname "$0")" || exit 1
echo "Starting the Code Lab... (press Ctrl+C when you're done)"
python3 code_lab/code_lab.py
