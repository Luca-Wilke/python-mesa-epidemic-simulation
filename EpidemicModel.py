from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from human import Human


class EpidemicModel(Model):
    def __init__(self,
                 width=30,
                 height=30,
                 initial_population=300,
                 initial_infection_rate_of_population=0.05,
                 infection_rate=0.43,
                 incubation_time=9,
                 duration=5,
                 mortality_rate=0.012,
                 immunity=True,
                 immunity_duration=120):
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
        self.immunity = immunity
        self.immunity_duration = immunity_duration
        # create random schedule
        self.schedule = RandomActivation(self)
        # create grid
        self.grid = MultiGrid(width, height, torus=False)
        # statistics
        self.num_infected = round(initial_population * initial_infection_rate_of_population)  # currently infected
        self.total_infected = self.num_infected  # total infections
        self.new_infections = 0  # infections per day
        self.total_deaths = 0
        self.total_cured = 0
        self.current_cured = 0
        # batch runner
        self.running = True
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
                "new infections": lambda a: a.new_infections,
                "total deaths": lambda a: a.total_deaths,
                "total cured": lambda a: a.total_cured,
                "current cured": lambda a: a.current_cured}
        )

    def create_agent(self, unique_index, infected):
        human = Human(unique_index, self, infected=infected)
        x = self.random.randrange(self.width)
        y = self.random.randrange(self.height)
        self.grid.place_agent(human, (x, y))
        self.schedule.add(human)

    def step(self):
        self.day += 1
        # print("BEGIN: DAY " + str(self.day))
        self.data_collector.collect(self)
        self.current_cured = 0
        self.new_infections = 0
        self.schedule.step()
        # print("END: DAY " + str(self.day))
