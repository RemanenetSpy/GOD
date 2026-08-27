"""
PyGame Renderer for Universal Game Runner.

Handles 2D visualization of grid-based environments.
"""

import sys
import math
import time

try:
    import pygame
except ImportError:
    print("Error: PyGame not installed. Please run: pip install pygame")
    sys.exit(1)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GREY = (50, 50, 50)
GREEN = (0, 255, 0)

class PyGameRenderer:
    def __init__(self, grid_size: int, window_width: int = 600, window_height: int = 700):
        """Initialize PyGame renderer."""
        pygame.init()
        self.grid_size = grid_size
        self.width = window_width
        self.height = window_height
        self.cell_size = window_width // grid_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Universal AGI Game Runner")
        self.font = pygame.font.SysFont('Arial', 18)
        self.clock = pygame.time.Clock()
        
    def handle_events(self):
        """Process PyGame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def draw(self, env_instance, stats: dict = None):
        """Draw the current state of the environment."""
        self.screen.fill(BLACK)
        
        # Get grid from environment (assuming standardized interface)
        if hasattr(env_instance, 'grid'):
            grid = env_instance.grid
            
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    rect = (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                    center = (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2)
                    
                    cell_value = grid[i, j]
                    
                    # Draw base grid elements
                    if cell_value == 2: # Wall/Obstacle
                        pygame.draw.rect(self.screen, BLUE, rect)
                        pygame.draw.rect(self.screen, BLACK, rect, 1) # Outline
                    elif cell_value == 1: # Resource
                        pygame.draw.circle(self.screen, GREEN, center, self.cell_size // 3)
                    elif cell_value == 4: # Pellet
                        pygame.draw.circle(self.screen, WHITE, center, self.cell_size // 6)
                    elif cell_value == 5: # Power Pellet
                        pygame.draw.circle(self.screen, WHITE, center, self.cell_size // 3)
        
        # Draw Entities (Pac-Man, Ghosts) - If environment exposes them
        # Generic approach: Check for attributes or parsing the grid if entities are in grid
        
        # Pac-Man (from env attribute)
        if hasattr(env_instance, 'pacman_pos'):
            px, py = env_instance.pacman_pos
            center = (py * self.cell_size + self.cell_size // 2, px * self.cell_size + self.cell_size // 2)
            pygame.draw.circle(self.screen, YELLOW, center, self.cell_size // 2 - 2)
            
            # Simple mouth animation
            # pygame.draw.polygon(...) 
            
        # Ghosts (from env attribute)
        if hasattr(env_instance, 'ghosts'):
            ghost_colors = [RED, PINK, CYAN, ORANGE]
            for idx, ghost in enumerate(env_instance.ghosts):
                if ghost['alive']:
                    gx, gy = ghost['pos']
                    center = (gy * self.cell_size + self.cell_size // 2, gx * self.cell_size + self.cell_size // 2)
                    color = ghost_colors[idx % 4]
                    
                    if ghost.get('scared', False):
                        color = BLUE # Scared color
                        
                    pygame.draw.circle(self.screen, color, center, self.cell_size // 2 - 2)
                    
                    # Eyes
                    eye_color = WHITE
                    pygame.draw.circle(self.screen, eye_color, (center[0]-4, center[1]-4), 3)
                    pygame.draw.circle(self.screen, eye_color, (center[0]+4, center[1]-4), 3)

        # Draw Stats Panel
        panel_y = self.width # Start below grid
        stats_text = []
        if stats:
            stats_text.append(f"Score: {stats.get('score', 0)}")
            stats_text.append(f"Steps: {stats.get('steps', 0)}")
            stats_text.append(f"Energy: {stats.get('energy', 'N/A')}")
            stats_text.append(f"Plan Depth: {stats.get('planning_depth', 'N/A')}")
        
        if hasattr(env_instance, 'lives'):
             stats_text.append(f"Lives: {env_instance.lives}")
        
        for idx, text in enumerate(stats_text):
            surface = self.font.render(text, True, WHITE)
            self.screen.blit(surface, (20, panel_y + 20 + idx * 25))

        pygame.display.flip()
        self.clock.tick(30) # Cap at 30 FPS
