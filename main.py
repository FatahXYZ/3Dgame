#!/usr/bin/env python3
"""
3D Platformer Game
A simple 3D platformer built with Python, Pyglet, and OpenGL for Linux.

This is the main entry point for the game.
Run this file to start the game.
"""

import sys
import os

# Add the parent directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.game import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError running game: {e}")
        print("\nMake sure you have all dependencies installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
