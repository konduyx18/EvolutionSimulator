from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import random
import json

class Food(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.eaten = False

class Creature(Agent):
    def __init__(self, unique_id, model, health=100, hunger=0, speed=1, gender=None, genes=None):
        super().__init__(unique_id, model)
        self.health = health
        self.hunger = hunger
        self.speed = speed
        self.gender = random.choice(["Male", "Female"]) if gender is None else gender
        self.genes = genes if genes is not None else {
            'speed': random.randint(1, 3),
            'sight': random.randint(1, 5),
            'special_gene': random.choice([True, False])  # Example gene, with a random chance to be True or False
        }
        self.is_pregnant = False
        self.gestation_period = 0
        self.reproduction_rate = 0.1  # Example rate, should ideally be part of genes
        
    def step(self):
        self.move_towards_food()
        self.eat()
        self.seek_mate()
        self.reproduce()
        self.hunger += 1
        if self.hunger > 20:
            self.health -= 1
        if self.health <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def move_towards_food(self):
        food_positions = [agent.pos for agent in self.model.schedule.agents if isinstance(agent, Food)]
        if food_positions:
            closest_food = min(food_positions, key=lambda pos: self.model.grid.get_distance(self.pos, pos))
            self.move_to_target(closest_food)
        else:
            self.random_move()

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def move_to_target(self, target_pos):
        path = self.model.grid.get_path(self.pos, target_pos)
        if path:
            next_step = path[0]
            self.model.grid.move_agent(self, next_step)

    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for mate in cellmates:
            if isinstance(mate, Food):
                self.hunger -= 20
                mate.eaten = True
                break

    def seek_mate(self):
        if self.gender == 'Female' and not self.is_pregnant:
            potential_mates = [agent for agent in self.model.grid.get_cell_list_contents([self.pos])
                               if isinstance(agent, Creature) and agent.gender != self.gender]
            for mate in potential_mates:
                if random.random() < self.reproduction_rate and not mate.is_pregnant:
                    mate.is_pregnant = True
                    mate.gestation_period = 3
                    break

    def reproduce(self):
        if self.is_pregnant:
            self.gestation_period -= 1
            if self.gestation_period <= 0:
                genes = self.mutate_genes()
                child = Creature(self.model.next_id(), self.model, genes=genes)
                self.model.schedule.add(child)
                self.model.grid.place_agent(child, self.pos)
                self.is_pregnant = False

    def mutate_genes(self):
        mutated_genes = self.genes.copy()
        for trait in mutated_genes:
            if random.random() < 0.1:
                mutated_genes[trait] += random.choice([-1, 1])
        return mutated_genes

class EcosystemModel(Model):
    def __init__(self, N, width, height):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.data_collection = []  # Initialize the data_collection attribute
        self.distribute_food(20)  # Initially distribute some food

        # Create agents and add them to the schedule and grid
        for i in range(self.num_agents):
            a = Creature(i, self)
            self.schedule.add(a)
            # Place the agent on a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def distribute_food(self, food_count):
        for i in range(food_count):
            food = Food(self.next_id(), self)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(food, (x, y))
            food.pos = (x, y)

    def step(self):
        # Run one step of the model
        self.schedule.step()
        # Remove eaten food from the model
        for agent in list(self.schedule.agents):
            if isinstance(agent, Food) and agent.eaten:
                self.grid.remove_agent(agent)
                self.schedule.remove(agent)
        self.data_collection.append(self.collect_data())

    def collect_data(self):
        # Collect data for creatures and food
        data = {
            'Creature': [],
            'Food': []
        }
        for agent in self.schedule.agents:
            if isinstance(agent, Creature):
                creature_data = {
                    'unique_id': agent.unique_id,
                    'pos': list(agent.pos),
                    'health': agent.health,
                    'hunger': agent.hunger,
                    'speed': agent.speed,
                    'gender': agent.gender,
                    'genes': agent.genes
                }
                data['Creature'].append(creature_data)
            elif isinstance(agent, Food):
                food_data = {
                    'unique_id': agent.unique_id,
                    'pos': list(agent.pos),
                    'eaten': agent.eaten
                }
                data['Food'].append(food_data)
        return data

# Running the model
if __name__ == "__main__":
    model = EcosystemModel(50, 20, 20)
    for i in range(100):
        model.step()

    # After running the model, save the data collection to a JSON file
    with open('data_collection.json', 'w') as f:
        json.dump(model.data_collection, f, indent=4)