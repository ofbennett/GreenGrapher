from argparse import ArgumentParser
from greengraphertools import Greengraph, Map
from matplotlib import pyplot as plt

def process():
    parser = ArgumentParser(description = 'A program which displays a graph of the amount of green along a straight line between two cities on Google Maps')
    parser.add_argument('city1')
    parser.add_argument('city2')
    parser.add_argument('--steps','-s',help = 'Number of equal steps between cities to show greenness. Default is 20.',default = 20)
    arguments = parser.parse_args()
    # print arguments.city1, arguments.city2, arguments.steps
    mygraph = Greengraph(arguments.city1,arguments.city2)
    data = mygraph.green_between(arguments.steps)
    plt.plot(data)
    plt.show()

if __name__ == '__main__':
    process()
