import subprocess, os, time, random,resource
import matplotlib.pyplot as plt
import numpy

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
    toolbox.attr_bool, 12)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluateMemory(individual):
    a = individual[0:4]
    b = individual[4:12]
    threads = int(''.join(str(i) for i in a),2)
    nbuff = int(''.join(str(i) for i in b),2)
    if threads == 0:
      threads = 16
    if nbuff == 0 then
      nbuff = 
    print 'Number of threads: ', threads
    print 'Number of buffered particles: ', nbuff
    print "Game starts.. "
  #insert what to measure & how
    os.system("./run_mod.sh %s %s" % (nbuff,threads))
    print "end"
  #insert return
    return ,

# Operator registering
toolbox.register("evaluate", evaluateMemory)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
#toolbox.register("map", futures.map)

def main():
    pop = toolbox.population(n=40)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=5, stats=stats, halloffame=hof, verbose=True)

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
