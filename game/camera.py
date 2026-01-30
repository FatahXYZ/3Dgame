"""
Camera Module
Implements a third-person chase camera that smoothly follows the player.
"""


class Camera:
    """
    Third-person chase camera that follows the player with smooth interpolation.
    
    The camera maintains a fixed distance and height offset from the player,
    smoothly interpolating to new positions for a cinematic feel.
    """
    
    def __init__(self, distance, height, smoothing=0.1):
        """
        Initialize the camera.
        
        Args:
            distance (float): Distance behind the player
            height (float): Height above the player
            smoothing (float): Smoothing factor (0-1), lower = smoother
        """
        self.distance = distance
        self.height = height
        self.smoothing = smoothing
        
        # Camera position and target
        self.x = 0.0
        self.y = height
        self.z = distance
        
        # Look-at target position
        self.target_x = 0.0
        self.target_y = 0.0
        self.target_z = 0.0
    
    def update(self, player_x, player_y, player_z, dt):
        """
        Update camera position to follow the player smoothly.
        
        Args:
            player_x (float): Player's X position
            player_y (float): Player's Y position
            player_z (float): Player's Z position
            dt (float): Delta time since last update
        """
        # Calculate desired camera position (behind and above player)
        desired_x = player_x
        desired_y = player_y + self.height
        desired_z = player_z + self.distance
        
        # Smooth interpolation towards desired position
        # Using exponential smoothing for natural camera movement
        self.x += (desired_x - self.x) * self.smoothing
        self.y += (desired_y - self.y) * self.smoothing
        self.z += (desired_z - self.z) * self.smoothing
        
        # Update look-at target (focus on player)
        self.target_x = player_x
        self.target_y = player_y + 1.0  # Look slightly above player's center
        self.target_z = player_z
    
    def apply(self):
        """
        Apply camera transformation to OpenGL.
        Sets up the view matrix to look at the player from the camera position.
        
        Returns:
            tuple: Camera position and target (pos_x, pos_y, pos_z, target_x, target_y, target_z)
        """
        return (self.x, self.y, self.z, 
                self.target_x, self.target_y, self.target_z)
