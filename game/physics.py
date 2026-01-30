"""
Physics Module
Implements basic physics including gravity, collision detection, and player movement.
"""


class PhysicsEngine:
    """
    Handles physics calculations for the game including gravity and collisions.
    """
    
    def __init__(self, gravity):
        """
        Initialize the physics engine.
        
        Args:
            gravity (float): Gravity acceleration (negative value pulls down)
        """
        self.gravity = gravity
    
    def apply_gravity(self, velocity_y, dt):
        """
        Apply gravity to vertical velocity.
        
        Args:
            velocity_y (float): Current vertical velocity
            dt (float): Delta time since last update
            
        Returns:
            float: Updated vertical velocity
        """
        return velocity_y + self.gravity * dt
    
    def check_collision_with_platform(self, player_pos, player_size, platform_pos, platform_size):
        """
        Check if player is colliding with (standing on) a platform.
        Uses AABB (Axis-Aligned Bounding Box) collision detection.
        
        Args:
            player_pos (list): Player position [x, y, z]
            player_size (float): Player cube size
            platform_pos (list): Platform position [x, y, z]
            platform_size (list): Platform dimensions [width, height, depth]
            
        Returns:
            bool: True if player is on top of the platform
        """
        px, py, pz = player_pos
        ps = player_size / 2  # Half size for collision bounds
        
        plat_x, plat_y, plat_z = platform_pos
        plat_w, plat_h, plat_d = platform_size
        
        # Check if player is horizontally aligned with platform
        x_overlap = (px + ps > plat_x - plat_w/2 and 
                     px - ps < plat_x + plat_w/2)
        z_overlap = (pz + ps > plat_z - plat_d/2 and 
                     pz - ps < plat_z + plat_d/2)
        
        # Check if player is just above the platform surface
        # Allow small tolerance for landing
        from game import config
        y_on_platform = (py - ps <= plat_y + plat_h/2 + config.COLLISION_Y_TOLERANCE_ABOVE and
                        py - ps >= plat_y + plat_h/2 - config.COLLISION_Y_TOLERANCE_BELOW)
        
        return x_overlap and z_overlap and y_on_platform
    
    def resolve_platform_collision(self, player_pos, player_size, platform_pos, platform_size):
        """
        Resolve collision by placing player on top of platform.
        
        Args:
            player_pos (list): Player position [x, y, z]
            player_size (float): Player cube size
            platform_pos (list): Platform position [x, y, z]
            platform_size (list): Platform dimensions [width, height, depth]
            
        Returns:
            float: Corrected Y position for player
        """
        plat_y = platform_pos[1]
        plat_h = platform_size[1]
        
        # Place player on top of platform
        return plat_y + plat_h/2 + player_size/2
    
    def check_point_in_box(self, point, box_center, box_size):
        """
        Check if a point is inside a box (for goal detection).
        
        Args:
            point (list): Point position [x, y, z]
            box_center (list): Box center position [x, y, z]
            box_size (float): Box size (assuming cube)
            
        Returns:
            bool: True if point is inside the box
        """
        half_size = box_size / 2
        
        return (abs(point[0] - box_center[0]) < half_size and
                abs(point[1] - box_center[1]) < half_size and
                abs(point[2] - box_center[2]) < half_size)
