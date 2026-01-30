"""
Main Game Module
The core game engine that manages game loop, input, and coordinates all systems.
"""

import pyglet
from pyglet.window import key
from pyglet.gl import *

from game import config
from game.camera import Camera
from game.physics import PhysicsEngine
from game.player import Player
from game.renderer import Renderer


class Game(pyglet.window.Window):
    """
    Main game class that extends Pyglet window.
    Manages the game loop, input handling, and coordinates all game systems.
    """
    
    def __init__(self):
        """
        Initialize the game window and all game systems.
        """
        # Create window with OpenGL context
        super().__init__(
            width=config.WINDOW_WIDTH,
            height=config.WINDOW_HEIGHT,
            caption=config.WINDOW_TITLE,
            resizable=False,
            vsync=True  # Enable VSync for smooth rendering on Linux
        )
        
        # Initialize game systems
        self.renderer = Renderer(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.physics = PhysicsEngine(config.GRAVITY)
        self.camera = Camera(
            config.CAMERA_DISTANCE,
            config.CAMERA_HEIGHT,
            config.CAMERA_SMOOTHING
        )
        
        # Initialize player
        self.player = Player(
            config.PLAYER_START_POS,
            config.PLAYER_SIZE,
            config.PLAYER_SPEED,
            config.PLAYER_JUMP_FORCE
        )
        
        # Initialize platforms from config
        self.platforms = config.PLATFORMS
        
        # Input state
        self.keys_pressed = set()
        
        # Game state
        self.game_won = False
        self.win_message_shown = False
        
        # Set up game loop timer
        pyglet.clock.schedule_interval(self.update, 1.0 / config.TARGET_FPS)
        
        print("=" * 60)
        print("3D PLATFORMER GAME - Linux Edition")
        print("=" * 60)
        print("\nControls:")
        print("  W/A/S/D - Move player")
        print("  SPACE   - Jump")
        print("  ESC     - Quit game")
        print("\nObjective:")
        print("  Jump across platforms to reach the golden goal marker!")
        print("\nStarting game...")
        print("=" * 60)
    
    def on_key_press(self, symbol, modifiers):
        """
        Handle key press events.
        
        Args:
            symbol: Key symbol pressed
            modifiers: Key modifiers (shift, ctrl, etc.)
        """
        self.keys_pressed.add(symbol)
        
        # Jump on spacebar
        if symbol == key.SPACE:
            self.player.jump()
        
        # Quit on ESC
        if symbol == key.ESCAPE:
            self.close()
    
    def on_key_release(self, symbol, modifiers):
        """
        Handle key release events.
        
        Args:
            symbol: Key symbol released
            modifiers: Key modifiers
        """
        self.keys_pressed.discard(symbol)
    
    def process_input(self):
        """
        Process continuous input for player movement.
        Handles WASD movement keys.
        """
        direction_x = 0.0
        direction_z = 0.0
        
        # Horizontal movement (X axis)
        if key.D in self.keys_pressed:
            direction_x += 1.0
        if key.A in self.keys_pressed:
            direction_x -= 1.0
        
        # Forward/backward movement (Z axis)
        if key.W in self.keys_pressed:
            direction_z -= 1.0
        if key.S in self.keys_pressed:
            direction_z += 1.0
        
        # Apply movement
        self.player.move(direction_x, direction_z)
    
    def update(self, dt):
        """
        Update game state (game loop).
        
        Args:
            dt (float): Delta time since last update
        """
        if self.game_won:
            return
        
        # Process input
        self.process_input()
        
        # Apply gravity to player
        new_velocity_y = self.physics.apply_gravity(self.player.velocity_y, dt)
        self.player.apply_gravity(new_velocity_y)
        
        # Update player position
        self.player.update(dt)
        
        # Check for collisions with platforms
        player_pos = self.player.get_position()
        self.player.is_grounded = False
        
        for platform in self.platforms:
            if self.physics.check_collision_with_platform(
                player_pos,
                self.player.size,
                platform["pos"],
                platform["size"]
            ):
                # Resolve collision - place player on platform
                corrected_y = self.physics.resolve_platform_collision(
                    player_pos,
                    self.player.size,
                    platform["pos"],
                    platform["size"]
                )
                self.player.land_on_platform(corrected_y)
                break
        
        # Check if player reached the goal
        if self.physics.check_point_in_box(
            player_pos,
            config.GOAL_POSITION,
            config.GOAL_SIZE
        ):
            if not self.win_message_shown:
                self.game_won = True
                self.win_message_shown = True
                print("\n" + "=" * 60)
                print("CONGRATULATIONS! YOU WON!")
                print("=" * 60)
                print("\nYou successfully reached the goal!")
                print("Close the window or press ESC to exit.")
        
        # Update camera to follow player
        px, py, pz = player_pos
        self.camera.update(px, py, pz, dt)
    
    def on_draw(self):
        """
        Render the game scene.
        Called automatically by Pyglet for each frame.
        """
        # Begin rendering
        self.renderer.begin_frame()
        
        # Apply camera transformation
        camera_pos = self.camera.apply()
        self.renderer.apply_camera(camera_pos)
        
        # Draw ground grid for reference
        self.renderer.draw_grid(size=20, spacing=5)
        
        # Draw all platforms
        for platform in self.platforms:
            pos = platform["pos"]
            size = platform["size"]
            self.renderer.draw_box(
                pos[0], pos[1], pos[2],
                size[0], size[1], size[2],
                config.PLATFORM_COLOR
            )
        
        # Draw goal marker
        self.renderer.draw_cube(
            config.GOAL_POSITION[0],
            config.GOAL_POSITION[1],
            config.GOAL_POSITION[2],
            config.GOAL_SIZE,
            config.GOAL_COLOR
        )
        
        # Draw player
        px, py, pz = self.player.get_position()
        self.renderer.draw_cube(
            px, py, pz,
            self.player.size,
            config.PLAYER_COLOR
        )
        
        # Draw win message if game is won
        if self.game_won:
            self.draw_win_text()
    
    def draw_win_text(self):
        """
        Draw victory text overlay when player wins.
        Uses Pyglet's 2D text rendering over the 3D scene.
        """
        # Switch to 2D rendering for text
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Disable depth test and lighting for 2D overlay
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        
        # Create and draw text label
        label = pyglet.text.Label(
            'YOU WIN!',
            font_name='Arial',
            font_size=48,
            bold=True,
            x=self.width // 2,
            y=self.height // 2,
            anchor_x='center',
            anchor_y='center',
            color=(255, 215, 0, 255)  # Gold color
        )
        label.draw()
        
        # Draw subtitle
        subtitle = pyglet.text.Label(
            'Press ESC to exit',
            font_name='Arial',
            font_size=24,
            x=self.width // 2,
            y=self.height // 2 - 60,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255)
        )
        subtitle.draw()
        
        # Restore OpenGL state
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def run(self):
        """
        Start the game loop.
        This method starts the Pyglet event loop.
        """
        pyglet.app.run()


def main():
    """
    Main entry point for the game.
    Creates and runs the game instance.
    """
    # Create and run game
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
