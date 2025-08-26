#!/usr/bin/env python3
import sys
from .config import Config
from .input_map import GamepadApp
from .util import log

def main():
    cfg = Config()
    app = GamepadApp(cfg)
    log("Install deps: pip install pygame pynput")
    if sys.platform.startswith("win"):
        log("For Windows volume control: pip install pycaw comtypes")
    app.run()

if __name__ == "__main__":
    main()