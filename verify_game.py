#!/usr/bin/env python3
"""
Verification script to check game can be initialized.
"""

import sys
import os

# Set environment variable to prevent display requirement for verification
os.environ['PYGLET_HEADLESS'] = '1'

try:
    print("Verifying 3D Platformer Game Setup...")
    print("-" * 60)
    
    # Check imports
    print("✓ Checking module imports...")
    from game import config
    from game.camera import Camera
    from game.physics import PhysicsEngine
    from game.player import Player
    from game.renderer import Renderer
    print("  All modules imported successfully")
    
    # Check configuration
    print("✓ Checking configuration...")
    print(f"  Game Title: {config.WINDOW_TITLE}")
    print(f"  Resolution: {config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
    print(f"  Platforms: {len(config.PLATFORMS)} platforms configured")
    print(f"  Goal Position: {config.GOAL_POSITION}")
    
    # Check game systems
    print("✓ Checking game systems...")
    camera = Camera(config.CAMERA_DISTANCE, config.CAMERA_HEIGHT)
    print("  Camera system initialized")
    
    physics = PhysicsEngine(config.GRAVITY)
    print("  Physics engine initialized")
    
    player = Player(
        config.PLAYER_START_POS,
        config.PLAYER_SIZE,
        config.PLAYER_SPEED,
        config.PLAYER_JUMP_FORCE
    )
    print("  Player system initialized")
    
    print("-" * 60)
    print("✓ All systems verified successfully!")
    print()
    print("To play the game, run:")
    print("  python3 main.py")
    print()
    
except Exception as e:
    print(f"✗ Verification failed: {e}")
    sys.exit(1)
