import subprocess, os, time, random,resource
import matplotlib.pyplot as plt
import numpy
import ROOT
from ROOT import *

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

def getMem():
    info = ROOT.ProcInfo_t()
    ROOT.gSystem.GetProcInfo(info);
    mem = float(info.fMemResident)
    return mem*1e-3

def evaluateMemory(individual):
    a = individual[0:4]
    b = individual[4:12]
    threads = int(''.join(str(i) for i in a),2)
    nbuff = int(''.join(str(i) for i in b),2)
    if threads == 0:
      threads = 16
    if nbuff == 0:
      nbuff = 200
    print 'Number of threads: ', threads
    print 'Number of buffered particles: ', nbuff
    print "Game starts.. "
    check_mem = ROOT.gROOT.Macro('run.C(%s,%s,false,"/data/geant/workspace/Testing_GeantV/label/olwork21/vecprot_v2/ExN03.root","/data/geant/workspace/Testing_GeantV/label/olwork21/vecprot_v2/xsec_FTFP_BERT_G496p02.root","/data/geant/workspace/Testing_GeantV/label/olwork21/vecprot_v2/fstate_FTFP_BERT_G496p02.root")' % (threads,nbuff)) 
    #os.system("sh run_mem.sh %s %s" % (threads, nbuff)) 
    print ("Memory usage: %s" % (check_mem))
    print "End"
    return check_mem,

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
    stats.register("std", numpy.std)
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=5, stats=stats, halloffame=hof, verbose=True)
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
    plt.savefig("plot_mem.png", dpi=200)
