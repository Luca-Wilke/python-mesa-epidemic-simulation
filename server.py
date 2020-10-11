from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from EpidemicModel import EpidemicModel
from human import InfectionState


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Color": "green",
        "Layer": "0",
        "r": 0.5}
    if agent.infected and agent.infection_state is InfectionState.SYMPTOMS:
        portrayal["Color"] = "red"
    else:
        if agent.infected and agent.infection_state is InfectionState.INCUBATION:
            portrayal["Color"] = "yellow"

    return portrayal


def start_server():
    grid = CanvasGrid(
        agent_portrayal,
        25,  # amount of horizontal cells
        25,  # amount of vertical cells
        500,  # canvas width
        500)  # canvas height

    chart = ChartModule(
        [
            {
                "Label": "current infections",
                "Color": "Red"
            },
            {
                "Label": "total deaths",
                "Color": "Black"
            }
        ],
        data_collector_name="data_collector"
    )

    server = ModularServer(
        EpidemicModel,
        [grid, chart],
        "Epidemic simulation")
    server.launch(8521, True)
