from enum import Enum
from numpy.random import choice
from RandomWalker import RandomWalker


class InfectionState(Enum):
    HEALTHY = 0  # the agent does not have the virus
    INCUBATION = 1  # the agent does not show symptoms but can infect other agents
    SYMPTOMS = 2  # the agent does show symptoms and can infect other agents


class Human(RandomWalker):
    # human agent derived from RandomWalker class handling the movement
    def __init__(self, unique_id, model, infected):
        super().__init__(unique_id, model)
        self.infected = infected
        self.infected_duration = 0
        self.infection_state = InfectionState.INCUBATION if self.infected else InfectionState.HEALTHY
        # if the model virus does have immunity: immunity = infected. Else: immunity = false
        self.immunity = self.infected if self.model.immunity is True else False
        self.immunity_left = self.model.immunity_duration

    def get_other_humans_on_cell(self):
        # get list of human agents which are placed on the same cell
        this_cell_content = self.model.grid.get_cell_list_contents([self.pos])
        return [obj for obj in this_cell_content if isinstance(obj, Human) and obj is not self]

    def update_infection(self):
        # update self.infection_state
        self.infected_duration += 1
        self.infection_state = InfectionState.SYMPTOMS if self.infected_duration >= self.model.incubation_time else \
            InfectionState.INCUBATION
        if self.infected_duration >= self.model.incubation_time + self.model.duration:
            # cured
            # print("Agent " + str(self.unique_id) + " has been cured")
            self.infected = False
            self.infected_duration = 0
            self.model.num_infected -= 1
            self.model.total_cured += 1
            self.model.current_cured += 1
            return
        if self.infection_state is InfectionState.SYMPTOMS:
            # die with a probability of self.model.mortality_rate / self.model.duration
            chance_of_dying = self.model.mortality_rate / self.model.duration
            if choice([True, False], p=[chance_of_dying, 1 - chance_of_dying]):
                # dying
                # print("Agent " + str(self.unique_id) + " died")
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                self.model.total_deaths += 1
                self.model.num_infected -= 1

    def step(self):
        self.move()
        # update immunity left in case there is one
        if self.immunity:
            self.immunity_left -= 1
            if self.immunity_left <= 0:
                # print("Agent " + str(self.unique_id) + " has lost it's immunity")
                self.immunity = False
                self.immunity_left = self.model.immunity_duration
        if not self.infected:
            return
        # infect others
        other_humans = self.get_other_humans_on_cell()
        for i in range(len(other_humans)):
            if other_humans[i].infected:
                # other human is already infected
                continue
            # infect others with a chance of model.infection_rate percent in case the other agent does not have immunity
            if choice([True, False], p=[self.model.infection_rate, 1 - self.model.infection_rate]) and not other_humans[i].immunity:
                # print("Agent " + str(self.unique_id) + " has infected Agent " + str(other_humans[i].unique_id))
                other_humans[i].infected = True
                self.model.num_infected += 1
                self.model.total_infected += 1
                self.model.new_infections += 1
                # set the other agents immunity
                if self.model.immunity:
                    other_humans[i].immunity = True
                    other_humans[i].immunity_left = self.model.immunity_duration

        # update infection
        self.update_infection()
