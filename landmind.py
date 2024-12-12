import pygame
import random
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

# Constants
GRID_SIZE = 25  # Increased number of cells
CELL_SIZE = 30  # Increased size of each cell
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
DETAILS_WIDTH = 250
TOTAL_WIDTH = SCREEN_SIZE + DETAILS_WIDTH
SCREEN_HEIGHT = SCREEN_SIZE
LANDMINE = 1
SAFE = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define your agents here
class LandmineAgent(Agent):
    """An agent representing a landmine."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class FinderAgent(Agent):
    """An agent responsible for finding landmines."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        self.random_move()
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if isinstance(agent, LandmineAgent) and agent not in self.model.landmine_locations:
                self.model.landmine_locations.append(agent)

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

class DestroyerAgent(Agent):
    """An agent responsible for destroying landmines."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "Idle"  # Initialize state as "Idle"

    def step(self):
        if self.model.landmine_locations:
            target = self.model.landmine_locations[0]
            if self.pos == target.pos:
                print(f"Destroyer at {self.pos} destroyed a landmine!")
                self.state = "Destroying"
                self.model.grid.remove_agent(target)
                self.model.landmine_locations.remove(target)
                self.model.destroyed_landmines += 1
            else:
                self.state = "Moving"
                self.move_towards(target.pos)
                print(f"Destroyer moving towards {target.pos} from {self.pos}")
        else:
            self.state = "Idle"  # No landmines to destroy

    def move_towards(self, target_pos):
        dx = target_pos[0] - self.pos[0]
        dy = target_pos[1] - self.pos[1]
        new_position = (self.pos[0] + (1 if dx > 0 else -1 if dx < 0 else 0),
                        self.pos[1] + (1 if dy > 0 else -1 if dy < 0 else 0))
        self.model.grid.move_agent(self, new_position)

class ScoutAgent(Agent):
    """An agent responsible for scouting and identifying potential landmines."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        for _ in range(2):
            self.random_move()
            cell_contents = self.model.grid.get_cell_list_contents([self.pos])
            for agent in cell_contents:
                if isinstance(agent, LandmineAgent) and agent not in self.model.landmine_locations:
                    self.model.landmine_locations.append(agent)

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

class LandmineModel(Model):
    """The main model for the simulation."""
    def __init__(self):
        self.schedule = SimultaneousActivation(self)
        self.grid = MultiGrid(GRID_SIZE, GRID_SIZE, torus=False)
        self.landmine_locations = []
        self.destroyed_landmines = 0

        # Load images
        self.landmine_image = pygame.image.load('landmine.jpg')
        self.finder_image = pygame.image.load('finder.jpg')
        self.destroyer_image = pygame.image.load('destroyer.jpg')
        self.scout_image = pygame.image.load('scout.jpg')

        # Resize images to fit in the grid cells
        self.landmine_image = pygame.transform.scale(self.landmine_image, (CELL_SIZE, CELL_SIZE))
        self.finder_image = pygame.transform.scale(self.finder_image, (CELL_SIZE, CELL_SIZE))
        self.destroyer_image = pygame.transform.scale(self.destroyer_image, (CELL_SIZE, CELL_SIZE))
        self.scout_image = pygame.transform.scale(self.scout_image, (CELL_SIZE, CELL_SIZE))

        # Add 20 landmines
        for i in range(20):
            x, y = self.random.randrange(GRID_SIZE), self.random.randrange(GRID_SIZE)
            landmine = LandmineAgent(f"Landmine-{i}", self)
            self.grid.place_agent(landmine, (x, y))

        # Add agents
        self.finder = FinderAgent("Finder", self)
        self.destroyer = DestroyerAgent("Destroyer", self)
        self.scout = ScoutAgent("Scout", self)
        self.grid.place_agent(self.finder, (0, 0))
        self.grid.place_agent(self.destroyer, (GRID_SIZE - 1, GRID_SIZE - 1))
        self.grid.place_agent(self.scout, (GRID_SIZE // 2, GRID_SIZE // 2))
        self.schedule.add(self.finder)
        self.schedule.add(self.destroyer)
        self.schedule.add(self.scout)

    def step(self):
        self.schedule.step()

def draw_grid(screen, grid, model):
    """Draw the grid and agents."""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            cell_contents = grid.get_cell_list_contents([(x, y)])
            for agent in cell_contents:
                if isinstance(agent, LandmineAgent):
                    screen.blit(model.landmine_image, (x * CELL_SIZE, y * CELL_SIZE))
                elif isinstance(agent, FinderAgent):
                    screen.blit(model.finder_image, (x * CELL_SIZE, y * CELL_SIZE))
                elif isinstance(agent, DestroyerAgent):
                    screen.blit(model.destroyer_image, (x * CELL_SIZE, y * CELL_SIZE))
                elif isinstance(agent, ScoutAgent):
                    screen.blit(model.scout_image, (x * CELL_SIZE, y * CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_details(screen, model):
    """Draw agent details on the side panel."""
    font = pygame.font.Font(None, 24)
    y_offset = 10
    details = [
        f"Finder Position: {model.finder.pos}",
        f"Scout Position: {model.scout.pos}",
        f"Destroyer Position: {model.destroyer.pos}",
        f"Destroyer State: {model.destroyer.state}",  # Display the destroyer's state
        f"Landmines Found: {len(model.landmine_locations)}",
        f"Landmines Destroyed: {model.destroyed_landmines}"
    ]
    pygame.draw.rect(screen, WHITE, (SCREEN_SIZE, 0, DETAILS_WIDTH, SCREEN_HEIGHT))
    for detail in details:
        text = font.render(detail, True, BLACK)
        screen.blit(text, (SCREEN_SIZE + 10, y_offset))
        y_offset += 30

def start():
    pygame.init()
    pygame.display.set_caption("Landmine Simulation with Background")
    screen = pygame.display.set_mode((TOTAL_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Load background image
    background_image = pygame.image.load('background.jpg')
    background_image = pygame.transform.scale(background_image, (SCREEN_SIZE, SCREEN_HEIGHT))

    model = LandmineModel()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        model.step()
        screen.blit(background_image, (0, 0))  # Draw the background image
        draw_grid(screen, model.grid, model)
        draw_details(screen, model)
        pygame.display.flip()
        clock.tick(3)

if __name__ == "__main__":
    start()