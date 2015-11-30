from argparse import ArgumentParser
from greengraphertools import Greengraph, Map
from matplotlib import pyplot as plt

def process():
    parser = ArgumentParser(description = 'A program which displays a graph of the amount of green along a straight line between two cities on Google Maps')
    parser.add_argument('--begin','-b',default = 'Cambridge', help = 'City to start measuring from',type = str)
    parser.add_argument('--end','-e',default = 'Oxford', help = 'City to finish measuring at',type = str)
    parser.add_argument('--steps','-s',help = 'Number of equal steps between cities to show greenness. Default is 20.',default = 20,type = int)
    parser.add_argument('--out','-o',default = 'graph.png',help = 'Name of output file to save graph to',type = str)
    arguments = parser.parse_args()

    if arguments.steps < 1:
        raise ValueError('Steps number must be a positive integer greater than 0')

    mygraph = Greengraph(arguments.begin,arguments.end)
    data = mygraph.green_between(arguments.steps)
    plt.plot(data)
    plt.savefig(arguments.out)
    plt.show()

if __name__ == '__main__':
    process()
