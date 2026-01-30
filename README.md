# 3D Platformer Game

A simple yet engaging 3D platformer game built with Python, Pyglet, and OpenGL, specifically optimized for Linux systems. Jump across platforms to reach the golden goal!

## Features

- **3D Game World**: Fully realized 3D environment with textured platforms
- **Player Character**: Blue cube character with smooth movement controls
- **Physics System**: Realistic gravity and collision detection
- **Third-Person Camera**: Smooth chase camera that follows the player
- **Goal-Based Gameplay**: Navigate platforms to reach the golden goal marker
- **Linux Optimized**: Built and tested specifically for Linux environments

## Screenshots

The game features:
- Multiple platforms at varying heights
- A blue player cube that you control
- A golden goal marker to reach
- Smooth camera following system
- Grid-based ground for spatial reference

## Prerequisites

- **Operating System**: Linux (tested on Ubuntu 20.04+, should work on most distributions)
- **Python**: Python 3.7 or higher
- **Display**: OpenGL 2.1 compatible graphics card/driver

## Installation

### 1. Install System Dependencies (Ubuntu/Debian)

```bash
# Update package list
sudo apt-get update

# Install Python 3 and pip if not already installed
sudo apt-get install python3 python3-pip

# Install OpenGL and graphics libraries
sudo apt-get install python3-opengl freeglut3-dev libglu1-mesa-dev

# Install X11 dependencies for window management (usually pre-installed)
sudo apt-get install libx11-dev libxcursor-dev libxrandr-dev libxinerama-dev libxi-dev
```

### 2. Install Python Dependencies

```bash
# Navigate to the game directory
cd /path/to/3Dgame

# Install required Python packages
pip3 install -r requirements.txt

# Or install globally (may require sudo)
sudo pip3 install -r requirements.txt
```

## Running the Game

### Method 1: Direct Execution

```bash
python3 main.py
```

### Method 2: Make Executable and Run

```bash
chmod +x main.py
./main.py
```

## Controls

| Key | Action |
|-----|--------|
| **W** | Move forward |
| **A** | Move left |
| **S** | Move backward |
| **D** | Move right |
| **SPACE** | Jump |
| **ESC** | Quit game |

## Gameplay

1. You start on the first platform (gray rectangular platform)
2. Use WASD keys to move your blue character
3. Press SPACE to jump to reach higher platforms
4. Navigate across all platforms to reach the golden goal cube
5. Once you reach the goal, you win!

## Game Architecture

The game is modularly designed with the following components:

```
3Dgame/
├── game/
│   ├── __init__.py        # Package initialization
│   ├── config.py          # Game configuration and constants
│   ├── game.py            # Main game loop and window management
│   ├── player.py          # Player character logic
│   ├── camera.py          # Third-person camera system
│   ├── physics.py         # Physics engine (gravity, collisions)
│   └── renderer.py        # OpenGL rendering system
├── textures/              # Texture assets (currently using colors)
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Module Descriptions

- **config.py**: Contains all game constants (speeds, colors, platform positions)
- **game.py**: Main game class managing the game loop, input, and coordination
- **player.py**: Player state, movement, and jumping mechanics
- **camera.py**: Smooth third-person chase camera implementation
- **physics.py**: Gravity simulation and AABB collision detection
- **renderer.py**: OpenGL wrapper for drawing 3D objects

## Customization

### Adding New Platforms

Edit `game/config.py` and add to the `PLATFORMS` list:

```python
PLATFORMS = [
    # Format: {"pos": [x, y, z], "size": [width, height, depth]}
    {"pos": [0, 0, 0], "size": [6, 0.5, 6]},
    {"pos": [8, 2, 0], "size": [4, 0.5, 4]},
    # Add your platform here
    {"pos": [15, 5, 5], "size": [5, 0.5, 5]},
]
```

### Changing Player Properties

Modify these values in `game/config.py`:

```python
PLAYER_SPEED = 5.0        # Movement speed
PLAYER_JUMP_FORCE = 10.0  # Jump height
GRAVITY = -20.0           # Gravity strength
```

### Adjusting Camera

Modify camera settings in `game/config.py`:

```python
CAMERA_DISTANCE = 10.0    # Distance behind player
CAMERA_HEIGHT = 5.0       # Height above player
CAMERA_SMOOTHING = 0.1    # Smoothness (lower = smoother)
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pyglet'"
**Solution**: Install dependencies with `pip3 install -r requirements.txt`

### Issue: "OpenGL.error.NullFunctionError"
**Solution**: Install OpenGL libraries:
```bash
sudo apt-get install python3-opengl freeglut3-dev libglu1-mesa-dev
```

### Issue: Game window doesn't appear or crashes
**Solution**: 
1. Ensure you have proper graphics drivers installed
2. Check OpenGL support: `glxinfo | grep "OpenGL version"`
3. Try updating graphics drivers

### Issue: "ImportError: cannot import name 'GL_CONTEXT_FORWARD_COMPATIBLE_BIT'"
**Solution**: Update PyOpenGL:
```bash
pip3 install --upgrade PyOpenGL PyOpenGL-accelerate
```

### Issue: Low frame rate or stuttering
**Solution**:
- The game uses VSync which should provide smooth 60 FPS on most systems
- Check if other applications are using GPU resources
- Try lowering window resolution in `game/config.py`

## Known Limitations

1. **No Texture Loading**: Currently uses solid colors instead of texture images for simplicity
2. **Simple Graphics**: Uses basic cube/box shapes rather than complex 3D models
3. **Fixed Level**: Only one predefined level (easily extendable via config)
4. **No Audio**: No sound effects or music
5. **Single Player Only**: No multiplayer support
6. **No Save System**: No progress saving or level checkpoints
7. **Basic Collision**: Uses simple AABB collision (no complex geometry)
8. **Linux Only**: Optimized for Linux (should work on Windows/Mac but not tested)

## Future Enhancements

Potential improvements that could be added:

- Loading 3D models (OBJ format)
- Texture mapping from image files
- Multiple levels with level selection
- Collectible items and scoring system
- Sound effects and background music
- More complex player model/animations
- Moving platforms
- Enemies or obstacles
- Better lighting and shadows
- Configuration menu

## Technical Details

- **Language**: Python 3.7+
- **Graphics Library**: Pyglet 2.0+ (window management)
- **Rendering**: PyOpenGL 3.1+ (3D graphics)
- **Math**: NumPy for vector calculations
- **Target Platform**: Linux (Ubuntu, Debian, Fedora, etc.)

## Dependencies

See `requirements.txt` for full list:
- pyglet >= 2.0.0
- PyOpenGL >= 3.1.0
- PyOpenGL-accelerate >= 3.1.0
- numpy >= 1.21.0

## License

This is a simple educational project demonstrating 3D game development with Python.

## Contributing

Feel free to fork and extend this project! Some ideas:
- Add new level designs
- Implement texture loading
- Create 3D model support
- Add particle effects
- Improve collision detection

## Credits

Built with Python, Pyglet, and OpenGL for Linux game development education.

---

**Enjoy the game! Happy platforming! 🎮**