# -*- coding: utf-8 -*-
"""
Google Translate in Flow Launcher.

Entry point: sets up plugin path and runs the translator.
"""

import os
import sys

# Add plugin root and subfolders to path for Flow Launcher
plugin_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, plugin_root)
sys.path.insert(0, os.path.join(plugin_root, "lib"))
sys.path.insert(0, os.path.join(plugin_root, "plugin"))

from plugin.Translator import GoogTranslate

if __name__ == "__main__":
    GoogTranslate()
