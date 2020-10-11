from mesa import Agent


class RandomWalker(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        possible_positions = self.model.grid.get_neighborhood(
            self.pos, # search for cells around current position
            moore=True, # moore neighborhood definition
            include_center=True) # the random walker does not have to change it's position
        next_position = self.random.choice(possible_positions)
        self.model.grid.move_agent(self, next_position)
