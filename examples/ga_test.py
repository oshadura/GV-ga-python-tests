#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import subprocess, os, time, random,resource
import matplotlib.pyplot as plt


from deap import base
from deap import creator
from deap import tools
from deap import algorithms

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.attr_bool, 7)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):

    a = individual[0:4]
    b = individual[4:7]
    threads = int(''.join(str(i) for i in a),2)
    vector = ''.join(map(str, b))
    if vector == '000':
        vector_s = 8
    elif vector == '001':
        vector_s = 16
    elif vector == '010':
        vector_s = 32
    elif vector == '100':
        vector_s = 64
    elif vector == '011':
        vector_s = 128
    elif vector == '101':
        vector_s = 256
    elif vector == '110':
        vector_s = 512
    elif vector == '111':
        vector_s = 1024
    if threads == 0:
	threads = 16 
    print "Game starts.. "
    print "Threads: ",threads
    print "Vector: ",vector_s
    start_time = time.time()
    start_time = time.time()
    os.system("./run.sh %s %s" % (threads,vector_s))
    print "end"
#    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#    print "memory usage: ", mem
    return (time.time() - start_time),

# Operator registering
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
#toolbox.register("map", futures.map)

def main():
    import numpy

    pop = toolbox.population(n=30)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=4, stats=stats, halloffame=hof, verbose=True)

    return pop, logbook, hof

if __name__ == "__main__":
    pop, log, hof = main()
    print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))
    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")
    plt.savefig("plot.png", dpi=200)
