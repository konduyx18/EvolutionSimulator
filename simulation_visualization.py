import pygame
import json

# Initialize Pygame
pygame.init()

# Set up the drawing window (screen width and height)
screen = pygame.display.set_mode([1000, 1000])

# Load your simulation data
with open('data_collection.json') as f:
    data_collection = json.load(f)

# Set up the scale factor based on your simulation grid size and the Pygame window size
grid_size = 20  # Assuming this is the size of your simulation grid
scale_factor = screen.get_width() / grid_size

# Initialize font module
pygame.font.init()
font = pygame.font.SysFont(None, 24)

def draw_text(surface, text, position):
    text_surface = font.render(text, True, (0, 0, 0))  # Black text
    surface.blit(text_surface, position)

def health_to_color(health):
    if health > 75:
        return (50, 205, 50)  # Lighter green
    elif health > 50:
        return (34, 139, 34)  # Green
    elif health > 25:
        return (205, 92, 92)  # Lighter red
    else:
        return (178, 34, 34)  # Dark red

def get_creature_size(creature, scale_factor):
    # Now scale_factor is being used to calculate the creature size
    return int(creature['genes']['speed'] * scale_factor / 4)

def draw_creature(surface, creature, x, y, scale_factor):
    creature_color = health_to_color(creature['health'])
    creature_size = get_creature_size(creature, scale_factor)

    if creature['genes'].get('special_gene'):  # Checking if special_gene is True
        points = [
            (x, y - creature_size), 
            (x - creature_size, y + creature_size), 
            (x + creature_size, y + creature_size)
        ]
        pygame.draw.polygon(surface, creature_color, points)
    else:
        pygame.draw.circle(surface, creature_color, (x, y), creature_size)

def draw_food(surface, x, y, scale_factor):
    food_color = (0, 0, 0)  
    food_size = int(scale_factor / 1.5, 5)  # Define a consistent size for food
    pygame.draw.rect(surface, food_color, (x - food_size // 2, y - food_size // 2, food_size, food_size))

def draw_legend(surface):
    # Set up position for the legend
    legend_x = 10
    legend_y = screen.get_height() - 150  # Give more space from the bottom

    # Health Legend - update colors to match health_to_color function
    draw_text(surface, 'Health:', (legend_x, legend_y))
    legend_y += 20
    pygame.draw.rect(surface, (50, 205, 50), (legend_x, legend_y, 15, 15))  # Lighter green
    draw_text(surface, '> 75', (legend_x + 20, legend_y))

    legend_y += 20
    pygame.draw.rect(surface, (34, 139, 34), (legend_x, legend_y, 15, 15))  # Green
    draw_text(surface, '51-75', (legend_x + 20, legend_y))

    legend_y += 20
    pygame.draw.rect(surface, (205, 92, 92), (legend_x, legend_y, 15, 15))  # Lighter red
    draw_text(surface, '26-50', (legend_x + 20, legend_y))

    legend_y += 20
    pygame.draw.rect(surface, (178, 34, 34), (legend_x, legend_y, 15, 15))  # Dark red
    draw_text(surface, '<= 25', (legend_x + 20, legend_y))

    # Speed Legend
    legend_y += 30  # Provide a gap before the speed legend
    draw_text(surface, 'Speed:', (legend_x, legend_y))
    for i in range(1, 6):  # Assuming 5 different speed levels
        radius = i * 3  # Scale the radius
        pygame.draw.circle(surface, (0, 0, 0), (legend_x + 70 + i * 20, legend_y + 10), radius)
        draw_text(surface, f'{i}', (legend_x + 70 + i * 20 - 5, legend_y + 20))

paused = False

# Simulation loop
running = True
time_step = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = not paused

    # Fill the background with a light color
    screen.fill((255, 255, 204))

    if not paused:
        # Draw creatures
        for creature in data_collection[time_step]['Creature']:
            x, y = creature['pos']
            scaled_x = int(x * scale_factor)
            scaled_y = int(y * scale_factor)
            draw_creature(screen, creature, scaled_x, scaled_y, scale_factor)

        # Draw food
        for food in data_collection[time_step]['Food']:
            x, y = food['pos']
            scaled_x = int(x * scale_factor)
            scaled_y = int(y * scale_factor)
            draw_food(screen, scaled_x, scaled_y, scale_factor)

        # Draw the text and legend
        draw_text(screen, f'Time Step: {time_step}', (10, 10))
        draw_text(screen, f'Number of Creatures: {len(data_collection[time_step]["Creature"])}', (10, 30))
        draw_legend(screen)

        # Increment the time_step to progress the simulation
        time_step += 1
        if time_step >= len(data_collection):
            time_step = 0

    # Update the display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(10)

# Done! Time to quit.
pygame.quit()
