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

    if not agent.infected and agent.immunity:
        portrayal["Color"] = "blue"

    return portrayal


def start_server():
    grid = CanvasGrid(
        agent_portrayal,
        30,  # amount of horizontal cells
        30,  # amount of vertical cells
        500,  # canvas width
        500)  # canvas height

    chart_infections = ChartModule(
        [
            {
                "Label": "current infections",
                "Color": "Red"
            },
            {
                "Label": "current cured",
                "Color": "Green"
            }
        ],
        data_collector_name="data_collector"
    )

    chart_total = ChartModule(
        [
            {
                "Label": "total infections",
                "Color": "Red"
            },
            {
                "Label": "total deaths",
                "Color": "Black"
            },
            {
                "Label": "total cured",
                "Color": "Green"
            }
        ],
        data_collector_name="data_collector"
    )

    chart_current = ChartModule(
        [
            {
                "Label": "new infections",
                "Color": "Red"
            },
            {
                "Label": "current cured",
                "Color": "Green"
            }
        ],
        data_collector_name="data_collector"
    )

    chart_deaths = ChartModule(
        [
            {
                "Label": "total deaths",
                "Color": "Black"
            }
        ],
        data_collector_name="data_collector"
    )

    server = ModularServer(
        EpidemicModel,
        [grid, chart_current, chart_infections, chart_total, chart_deaths],
        "Epidemic simulation")
    server.launch(8521, True)
