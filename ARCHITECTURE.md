# Game Architecture

## Overview

This 3D platformer game follows a modular architecture with clear separation of concerns. Each module handles a specific aspect of the game.

## Module Structure

```
game/
├── __init__.py      # Package initialization
├── config.py        # Configuration and constants
├── game.py          # Main game loop and coordination
├── player.py        # Player character logic
├── camera.py        # Camera system
├── physics.py       # Physics engine
└── renderer.py      # OpenGL rendering
```

## Core Systems

### 1. Configuration System (`config.py`)

**Purpose**: Centralized configuration for all game parameters

**Key Constants**:
- Window settings (width, height, title, FPS)
- Player properties (size, speed, jump force, starting position)
- Physics parameters (gravity)
- Camera settings (distance, height, smoothing)
- Game objects (platforms, goal)
- Colors for rendering

**Design Rationale**: Having all configuration in one place makes the game easy to customize and tune without modifying core logic.

### 2. Game Engine (`game.py`)

**Purpose**: Main game loop and system coordination

**Key Responsibilities**:
- Window management (extends `pyglet.window.Window`)
- Game loop management via Pyglet's clock
- Input handling (keyboard events)
- System coordination (physics, rendering, camera)
- Game state management (win condition)

**Game Loop Flow**:
1. Process input (WASD movement, Space for jump)
2. Apply physics (gravity)
3. Update player position
4. Check collisions with platforms
5. Check goal condition
6. Update camera position
7. Render scene

### 3. Player System (`player.py`)

**Purpose**: Player character state and behavior

**Key Features**:
- Position tracking (x, y, z)
- Velocity tracking (for physics)
- Movement control
- Jump mechanics (prevents double-jumping)
- Ground state tracking

**State Machine**:
- `is_grounded`: Whether player is on a platform
- `is_jumping`: Whether player is in a jump

### 4. Camera System (`camera.py`)

**Purpose**: Third-person chase camera

**Key Features**:
- Smooth camera following using exponential smoothing
- Fixed distance and height offset from player
- Look-at target (focuses on player)

**Algorithm**:
```
desired_position = player_position + offset
current_position += (desired_position - current_position) * smoothing
```

This creates a smooth, cinematic camera that follows the player without being too rigid.

### 5. Physics Engine (`physics.py`)

**Purpose**: Physics simulation and collision detection

**Key Components**:

1. **Gravity System**:
   - Applies constant downward acceleration
   - `velocity_y = velocity_y + gravity * dt`

2. **AABB Collision Detection**:
   - Uses Axis-Aligned Bounding Box collision
   - Checks if player overlaps with platform on X and Z axes
   - Checks if player is at correct Y height to be "on" the platform

3. **Collision Resolution**:
   - Places player on top of platform when collision detected
   - Stops vertical velocity

4. **Goal Detection**:
   - Point-in-box check for win condition

### 6. Renderer (`renderer.py`)

**Purpose**: OpenGL rendering system

**Key Features**:

1. **OpenGL Setup**:
   - Depth testing for proper 3D rendering
   - Basic lighting (one directional light)
   - Smooth shading
   - Perspective projection

2. **Drawing Functions**:
   - `draw_cube()`: Draws cubes for player and goal
   - `draw_box()`: Draws rectangular boxes for platforms
   - `draw_grid()`: Draws ground reference grid

3. **Rendering Pipeline**:
   - Clear screen
   - Apply camera transformation (`gluLookAt`)
   - Draw scene objects (grid, platforms, goal, player)
   - Draw UI overlay (win text)

**Note**: Currently uses colored geometry. Can be extended to support textures.

## Data Flow

```
Input (Keyboard)
    ↓
Game.process_input()
    ↓
Player.move() / Player.jump()
    ↓
Physics.apply_gravity()
    ↓
Player.update()
    ↓
Physics.check_collision()
    ↓
Player.land_on_platform()
    ↓
Camera.update()
    ↓
Renderer.draw()
```

## Extension Points

The game is designed to be easily extensible:

1. **New Platform Types**: Add entries to `config.PLATFORMS`
2. **Custom Physics**: Extend `PhysicsEngine` class
3. **Advanced Camera**: Extend `Camera` class (e.g., collision-aware camera)
4. **Texture Support**: Extend `Renderer` to load and apply textures
5. **Power-ups**: Add new game objects and collision checks
6. **Enemies**: Add AI entities with physics

## Performance Considerations

- **VSync**: Enabled to prevent screen tearing
- **Fixed Time Step**: Game loop runs at `TARGET_FPS`
- **Efficient Collision**: Only checks collisions with nearby platforms
- **Minimal State Changes**: OpenGL state changes are minimized in renderer

## Linux Compatibility

The game is built with Linux as the primary target:

- Uses Pyglet (cross-platform but well-supported on Linux)
- OpenGL 2.1 (widely available on Linux systems)
- No platform-specific code
- Tested with X11 window system
- Works with various Linux distributions

## Dependencies

- **Pyglet**: Window management and OpenGL context
- **PyOpenGL**: OpenGL bindings for Python
- **NumPy**: Mathematical operations (future use)

## Testing

Tests are located in `tests/test_game.py` and cover:
- Configuration loading
- Player creation and movement
- Jump mechanics
- Physics (gravity, collision)
- Camera updates
- Goal detection

Tests run without requiring a display/GUI.
