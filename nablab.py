#!/usr/bin/env python3
# NABlab Entry Point
# Launches the application shell.

import sys
from core.app_manager import AppManager

def main():
    app = AppManager()
    app.run()

if __name__ == "__main__":
    main()
