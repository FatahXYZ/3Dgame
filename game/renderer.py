"""
Renderer Module
Handles all OpenGL rendering including 3D objects, textures, and scene setup.
"""

from OpenGL.GL import *
from OpenGL.GLU import *
import math


class Renderer:
    """
    Manages OpenGL rendering for the 3D game world.
    Handles drawing platforms, player, goal, and camera setup.
    """
    
    def __init__(self, width, height):
        """
        Initialize the renderer and set up OpenGL state.
        
        Args:
            width (int): Window width
            height (int): Window height
        """
        self.width = width
        self.height = height
        self.setup_opengl()
    
    def setup_opengl(self):
        """
        Configure OpenGL settings for 3D rendering.
        Sets up depth testing, lighting, and projection matrix.
        """
        # Enable depth testing for proper 3D rendering
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        # Enable smooth shading
        glShadeModel(GL_SMOOTH)
        
        # Set up basic lighting for better 3D visualization
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Light position (above and to the side)
        light_position = [10.0, 20.0, 10.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        
        # Ambient light
        ambient_light = [0.3, 0.3, 0.3, 1.0]
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
        
        # Diffuse light
        diffuse_light = [0.8, 0.8, 0.8, 1.0]
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
        
        # Set background color (sky blue)
        glClearColor(0.5, 0.7, 1.0, 1.0)
        
        # Set up projection matrix
        self.setup_projection()
    
    def setup_projection(self):
        """
        Set up the perspective projection matrix.
        Defines the viewing frustum and field of view.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Perspective projection
        # FOV, aspect ratio, near plane, far plane
        gluPerspective(60.0, self.width / self.height, 0.1, 1000.0)
        
        glMatrixMode(GL_MODELVIEW)
    
    def begin_frame(self):
        """
        Clear the screen and prepare for rendering a new frame.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
    
    def apply_camera(self, camera_pos):
        """
        Apply camera transformation using gluLookAt.
        
        Args:
            camera_pos (tuple): Camera position and target (px, py, pz, tx, ty, tz)
        """
        px, py, pz, tx, ty, tz = camera_pos
        gluLookAt(px, py, pz,  # Camera position
                  tx, ty, tz,  # Look-at target
                  0, 1, 0)     # Up vector
    
    def draw_cube(self, x, y, z, size, color):
        """
        Draw a textured/colored cube at the specified position.
        
        Args:
            x (float): X position (center)
            y (float): Y position (center)
            z (float): Z position (center)
            size (float): Cube size
            color (tuple): RGB color (r, g, b) normalized 0-1
        """
        glPushMatrix()
        glTranslatef(x, y, z)
        
        s = size / 2  # Half size for vertices
        
        glColor3f(*color)
        
        # Draw cube faces
        glBegin(GL_QUADS)
        
        # Front face
        glNormal3f(0, 0, 1)
        glVertex3f(-s, -s, s)
        glVertex3f(s, -s, s)
        glVertex3f(s, s, s)
        glVertex3f(-s, s, s)
        
        # Back face
        glNormal3f(0, 0, -1)
        glVertex3f(-s, -s, -s)
        glVertex3f(-s, s, -s)
        glVertex3f(s, s, -s)
        glVertex3f(s, -s, -s)
        
        # Top face
        glNormal3f(0, 1, 0)
        glVertex3f(-s, s, -s)
        glVertex3f(-s, s, s)
        glVertex3f(s, s, s)
        glVertex3f(s, s, -s)
        
        # Bottom face
        glNormal3f(0, -1, 0)
        glVertex3f(-s, -s, -s)
        glVertex3f(s, -s, -s)
        glVertex3f(s, -s, s)
        glVertex3f(-s, -s, s)
        
        # Right face
        glNormal3f(1, 0, 0)
        glVertex3f(s, -s, -s)
        glVertex3f(s, s, -s)
        glVertex3f(s, s, s)
        glVertex3f(s, -s, s)
        
        # Left face
        glNormal3f(-1, 0, 0)
        glVertex3f(-s, -s, -s)
        glVertex3f(-s, -s, s)
        glVertex3f(-s, s, s)
        glVertex3f(-s, s, -s)
        
        glEnd()
        
        # Draw wireframe edges for better visibility
        glDisable(GL_LIGHTING)
        glColor3f(0, 0, 0)
        glLineWidth(2.0)
        
        # Draw edges
        glBegin(GL_LINE_LOOP)
        glVertex3f(-s, -s, s)
        glVertex3f(s, -s, s)
        glVertex3f(s, s, s)
        glVertex3f(-s, s, s)
        glEnd()
        
        glBegin(GL_LINE_LOOP)
        glVertex3f(-s, -s, -s)
        glVertex3f(-s, s, -s)
        glVertex3f(s, s, -s)
        glVertex3f(s, -s, -s)
        glEnd()
        
        glBegin(GL_LINES)
        glVertex3f(-s, -s, s)
        glVertex3f(-s, -s, -s)
        glVertex3f(s, -s, s)
        glVertex3f(s, -s, -s)
        glVertex3f(s, s, s)
        glVertex3f(s, s, -s)
        glVertex3f(-s, s, s)
        glVertex3f(-s, s, -s)
        glEnd()
        
        glEnable(GL_LIGHTING)
        glPopMatrix()
    
    def draw_box(self, x, y, z, width, height, depth, color):
        """
        Draw a rectangular box (platform) at the specified position.
        
        Args:
            x (float): X position (center)
            y (float): Y position (center)
            z (float): Z position (center)
            width (float): Width (X dimension)
            height (float): Height (Y dimension)
            depth (float): Depth (Z dimension)
            color (tuple): RGB color (r, g, b) normalized 0-1
        """
        glPushMatrix()
        glTranslatef(x, y, z)
        
        w = width / 2
        h = height / 2
        d = depth / 2
        
        glColor3f(*color)
        
        # Draw box faces
        glBegin(GL_QUADS)
        
        # Front face
        glNormal3f(0, 0, 1)
        glVertex3f(-w, -h, d)
        glVertex3f(w, -h, d)
        glVertex3f(w, h, d)
        glVertex3f(-w, h, d)
        
        # Back face
        glNormal3f(0, 0, -1)
        glVertex3f(-w, -h, -d)
        glVertex3f(-w, h, -d)
        glVertex3f(w, h, -d)
        glVertex3f(w, -h, -d)
        
        # Top face
        glNormal3f(0, 1, 0)
        glVertex3f(-w, h, -d)
        glVertex3f(-w, h, d)
        glVertex3f(w, h, d)
        glVertex3f(w, h, -d)
        
        # Bottom face
        glNormal3f(0, -1, 0)
        glVertex3f(-w, -h, -d)
        glVertex3f(w, -h, -d)
        glVertex3f(w, -h, d)
        glVertex3f(-w, -h, d)
        
        # Right face
        glNormal3f(1, 0, 0)
        glVertex3f(w, -h, -d)
        glVertex3f(w, h, -d)
        glVertex3f(w, h, d)
        glVertex3f(w, -h, d)
        
        # Left face
        glNormal3f(-1, 0, 0)
        glVertex3f(-w, -h, -d)
        glVertex3f(-w, -h, d)
        glVertex3f(-w, h, d)
        glVertex3f(-w, h, -d)
        
        glEnd()
        
        # Draw edges for better visibility
        glDisable(GL_LIGHTING)
        glColor3f(0, 0, 0)
        glLineWidth(1.5)
        
        glBegin(GL_LINE_LOOP)
        glVertex3f(-w, -h, d)
        glVertex3f(w, -h, d)
        glVertex3f(w, h, d)
        glVertex3f(-w, h, d)
        glEnd()
        
        glBegin(GL_LINE_LOOP)
        glVertex3f(-w, -h, -d)
        glVertex3f(-w, h, -d)
        glVertex3f(w, h, -d)
        glVertex3f(w, -h, -d)
        glEnd()
        
        glBegin(GL_LINES)
        glVertex3f(-w, -h, d)
        glVertex3f(-w, -h, -d)
        glVertex3f(w, -h, d)
        glVertex3f(w, -h, -d)
        glVertex3f(w, h, d)
        glVertex3f(w, h, -d)
        glVertex3f(-w, h, d)
        glVertex3f(-w, h, -d)
        glEnd()
        
        glEnable(GL_LIGHTING)
        glPopMatrix()
    
    def draw_grid(self, size=50, spacing=5):
        """
        Draw a ground grid for spatial reference.
        
        Args:
            size (int): Grid size (number of lines)
            spacing (float): Spacing between grid lines
        """
        glDisable(GL_LIGHTING)
        glColor3f(0.3, 0.3, 0.3)
        glLineWidth(1.0)
        
        glBegin(GL_LINES)
        for i in range(-size, size + 1):
            # Lines parallel to X axis
            glVertex3f(-size * spacing, 0, i * spacing)
            glVertex3f(size * spacing, 0, i * spacing)
            # Lines parallel to Z axis
            glVertex3f(i * spacing, 0, -size * spacing)
            glVertex3f(i * spacing, 0, size * spacing)
        glEnd()
        
        glEnable(GL_LIGHTING)
