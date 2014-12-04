import subprocess, os, time, random,resource
import matplotlib.pyplot as plt
import numpy


from deap import base
from deap import creator
from deap import tools
from deap import algorithms


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.attr_bool, 7)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluateRuntime(individual):
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
    print threads
    print vector_s
    print 'Number of threads: ', threads
    print 'Vector of particles: ', vector_s
    print "Game starts.. "
    start_time = time.time()
    os.system("./run.sh %s %s" % (threads,vector_s))
    print "end"
    return (time.time() - start_time),

# Operator registering
toolbox.register("evaluate", evaluateRuntime)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selDoubleTournament, fitness_size=3, parsimony_size=1.5, fitness_first=True)
#toolbox.register("map", futures.map)

def main():
    pop = toolbox.population(n=40)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    stats.register("std", numpy.std)
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=4, stats=stats, halloffame=hof, verbose=True)
    return pop, logbook, hof

if __name__ == "__main__":
    pop, log, hof = main()
    print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))
    gen, avg, min_, max_, std= log.select("gen", "avg", "min", "max","std")
    plt.plot(avg, gen, label="average")
    plt.plot(min_, gen, label="minimum")
    plt.plot(max_, gen, label="maximum")
    plt.plot(std, gen, label="deviation")	
    plt.xlabel("Fitness")
    plt.ylabel("Generation")
    plt.legend(loc="lower left")
    plt.savefig("plot_sel_tourndb_onecx.png", dpi=200)
