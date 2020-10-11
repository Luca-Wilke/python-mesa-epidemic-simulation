from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt
from EpidemicModel import EpidemicModel
import server


def run_on_server():
    server.start_server()


def run_and_plot():
    model = EpidemicModel()
    for i in range(90):
        model.step()
        print(str(i))

    model.data_collector.get_model_vars_dataframe().plot()
    plt.show()


if __name__ == '__main__':
    run_on_server()
