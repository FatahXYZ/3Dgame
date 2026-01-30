"""
Player Module
Handles player character state, movement, and input processing.
"""

from game import config


class Player:
    """
    Represents the player character with position, velocity, and state.
    Handles movement input and jumping mechanics.
    """
    
    def __init__(self, start_pos, size, speed, jump_force):
        """
        Initialize the player.
        
        Args:
            start_pos (list): Starting position [x, y, z]
            size (float): Size of the player cube
            speed (float): Movement speed
            jump_force (float): Initial velocity when jumping
        """
        self.x, self.y, self.z = start_pos
        self.size = size
        self.speed = speed
        self.jump_force = jump_force
        
        # Velocity
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.velocity_z = 0.0
        
        # State
        self.is_grounded = False
        self.is_jumping = False
    
    def update(self, dt):
        """
        Update player position based on velocity.
        
        Args:
            dt (float): Delta time since last update
        """
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.z += self.velocity_z * dt
    
    def move(self, direction_x, direction_z):
        """
        Set player horizontal velocity based on input direction.
        
        Args:
            direction_x (float): X-axis movement (-1 to 1)
            direction_z (float): Z-axis movement (-1 to 1)
        """
        self.velocity_x = direction_x * self.speed
        self.velocity_z = direction_z * self.speed
    
    def jump(self):
        """
        Make the player jump if they are on the ground.
        """
        if self.is_grounded and not self.is_jumping:
            self.velocity_y = self.jump_force
            self.is_grounded = False
            self.is_jumping = True
    
    def land_on_platform(self, platform_y):
        """
        Handle landing on a platform.
        
        Args:
            platform_y (float): The Y position to set the player to
        """
        self.y = platform_y
        self.velocity_y = 0.0
        self.is_grounded = True
        self.is_jumping = False
    
    def apply_gravity(self, gravity_velocity):
        """
        Apply gravity to the player's vertical velocity.
        
        Args:
            gravity_velocity (float): Velocity change from gravity
        """
        self.velocity_y = gravity_velocity
    
    def get_position(self):
        """
        Get player position.
        
        Returns:
            list: Position [x, y, z]
        """
        return [self.x, self.y, self.z]
    
    def set_position(self, x, y, z):
        """
        Set player position (useful for collision resolution).
        
        Args:
            x (float): X position
            y (float): Y position
            z (float): Z position
        """
        self.x = x
        self.y = y
        self.z = z
