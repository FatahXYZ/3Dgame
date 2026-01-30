#!/usr/bin/env python3
"""
Unit tests for the 3D Platformer game.
Tests game logic without requiring a display/GUI.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game import config
from game.camera import Camera
from game.physics import PhysicsEngine
from game.player import Player


def test_player_creation():
    """Test player initialization."""
    print("Testing player creation...")
    player = Player(
        config.PLAYER_START_POS,
        config.PLAYER_SIZE,
        config.PLAYER_SPEED,
        config.PLAYER_JUMP_FORCE
    )
    assert player.x == 0.0
    assert player.y == 2.0
    assert player.z == 0.0
    assert player.size == 1.0
    print("✓ Player creation test passed")


def test_player_movement():
    """Test player movement."""
    print("Testing player movement...")
    player = Player([0, 0, 0], 1.0, 5.0, 10.0)
    
    # Test horizontal movement
    player.move(1.0, 0.0)
    player.update(0.1)
    assert player.x > 0.0
    assert player.z == 0.0
    
    # Test forward movement
    player.x = 0.0
    player.move(0.0, 1.0)
    player.update(0.1)
    assert player.x == 0.0
    assert player.z > 0.0
    print("✓ Player movement test passed")


def test_player_jump():
    """Test player jumping."""
    print("Testing player jump...")
    player = Player([0, 0, 0], 1.0, 5.0, 10.0)
    player.is_grounded = True
    
    # Test jump
    player.jump()
    assert player.velocity_y == 10.0
    assert player.is_jumping
    
    # Test can't double jump
    player.jump()
    assert player.velocity_y == 10.0  # Should remain same
    print("✓ Player jump test passed")


def test_physics_gravity():
    """Test gravity application."""
    print("Testing physics gravity...")
    physics = PhysicsEngine(config.GRAVITY)
    
    velocity = 0.0
    velocity = physics.apply_gravity(velocity, 0.1)
    assert velocity < 0.0  # Gravity pulls down
    print("✓ Physics gravity test passed")


def test_collision_detection():
    """Test collision detection."""
    print("Testing collision detection...")
    physics = PhysicsEngine(config.GRAVITY)
    
    # Player on platform
    player_pos = [0, 0.75, 0]
    platform_pos = [0, 0, 0]
    platform_size = [6, 0.5, 6]
    
    collision = physics.check_collision_with_platform(
        player_pos, 1.0, platform_pos, platform_size
    )
    assert collision
    
    # Player not on platform
    player_pos = [10, 0.75, 0]
    collision = physics.check_collision_with_platform(
        player_pos, 1.0, platform_pos, platform_size
    )
    assert not collision
    print("✓ Collision detection test passed")


def test_camera_update():
    """Test camera following."""
    print("Testing camera update...")
    camera = Camera(10.0, 5.0, 0.1)
    
    # Update camera to follow player
    camera.update(5.0, 2.0, 3.0, 0.1)
    
    # Camera should move towards player
    assert camera.target_x == 5.0
    assert camera.target_y == 3.0  # 2.0 + 1.0 offset
    assert camera.target_z == 3.0
    print("✓ Camera update test passed")


def test_goal_detection():
    """Test goal detection."""
    print("Testing goal detection...")
    physics = PhysicsEngine(config.GRAVITY)
    
    # Player at goal
    player_pos = config.GOAL_POSITION.copy()
    at_goal = physics.check_point_in_box(
        player_pos, config.GOAL_POSITION, config.GOAL_SIZE
    )
    assert at_goal
    
    # Player not at goal
    player_pos = [0, 0, 0]
    at_goal = physics.check_point_in_box(
        player_pos, config.GOAL_POSITION, config.GOAL_SIZE
    )
    assert not at_goal
    print("✓ Goal detection test passed")


def test_config_loading():
    """Test configuration loading."""
    print("Testing config loading...")
    assert config.WINDOW_WIDTH > 0
    assert config.WINDOW_HEIGHT > 0
    assert len(config.PLATFORMS) > 0
    assert len(config.GOAL_POSITION) == 3
    print("✓ Config loading test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running 3D Platformer Game Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_config_loading,
        test_player_creation,
        test_player_movement,
        test_player_jump,
        test_physics_gravity,
        test_collision_detection,
        test_camera_update,
        test_goal_detection,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    if failed == 0:
        print("All tests passed! ✓")
    else:
        print(f"{failed} test(s) failed!")
    print("=" * 60)
    
    return failed


if __name__ == "__main__":
    sys.exit(run_all_tests())
