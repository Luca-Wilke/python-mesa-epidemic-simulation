from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import  DataCollector
from human import Human


class EpidemicModel(Model):
    def __init__(self,
                 width=25,
                 height=25,
                 initial_population=200,
                 initial_infection_rate_of_population=0.05,
                 infection_rate=0.35,
                 incubation_time=8,
                 duration=5,
                 mortality_rate=0.01):
        super().__init__()
        # set parameters
        self.day = 1
        self.width = width
        self.height = height
        self.initial_population = initial_population
        self.initial_infection_rate_of_population = initial_infection_rate_of_population
        self.infection_rate = infection_rate
        self.incubation_time = incubation_time
        self.duration = duration
        self.mortality_rate = mortality_rate
        # create random schedule
        self.schedule = RandomActivation(self)
        # create grid
        self.grid = MultiGrid(width, height, torus=False)
        self.num_infected = round(initial_population * initial_infection_rate_of_population) # currently infected
        self.total_infected = self.num_infected # total infections
        self.total_deaths = 0
        # create population and place every human randomly
        # create initially infected agents
        for i in range(self.num_infected):
            self.create_agent(i, infected=True)
        # create not infected agents
        for i in range(initial_population - self.num_infected):
            self.create_agent(i+self.num_infected, infected=False)
        # create data collector
        self.data_collector = DataCollector(
            model_reporters={
                "total infections": lambda a: a.total_infected,
                "current infections": lambda a: a.num_infected,
                "total deaths": lambda a: a.total_deaths}
        )

    def create_agent(self, unique_index, infected):
        human = Human(unique_index, self, infected=infected)
        x = self.random.randrange(self.width)
        y = self.random.randrange(self.height)
        self.grid.place_agent(human, (x, y))
        self.schedule.add(human)

    def step(self):
        self.day += 1
        print("BEGIN: DAY " + str(self.day))
        self.data_collector.collect(self)
        self.schedule.step()
        print("END: DAY " + str(self.day))
