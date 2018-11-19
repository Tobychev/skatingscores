import matplotlib.pyplot as pl
import numpy as np

def kosttnerplot(names,element,pc,title="",showzero=False):
    a,b = np.polyfit(element,pc,1)
    scores = np.array(pc)/np.array(element)
    dists  = (np.array(pc) - b - a*np.array(element)) / np.sqrt(1+a*a)
    cor = np.array( [min(element), max(pc)])
    x = np.array( [min(element)*.9, max(element)*1.1]  )
    pl.scatter(element,pc)
    pl.plot(x, a*x+b)
    for i,namn in enumerate(names):
        pl.annotate(namn,(element[i]+.1,pc[i]+.1))
    
    pl.text(cor[0],(1-.03)*cor[1],"Slope: {:4.3}".format(a),fontsize=12)
    pl.text(cor[0],(1-.01)*cor[1],"Most Kostner: {}".format(names[np.argmax(dists)]),fontsize=12)
    pl.title(title)
    pl.xlabel("Element score")
    pl.ylabel("PC score")
    if showzero:
        pl.xlim(0,max(element)*1.2)
        pl.ylim(0,max(pc)*1.2)
    pl.show()

def show_pc_scores(skaters,title=""):
    Intr = []
    Comp = []
    Perf = []
    Skat = []
    Tran = []
    names = [el["name"] for el in skaters]
    pc_names = ["Skating Skills","Transitions","Performance","Composition","Interpretation",""]
    for skater in skaters:
        Skat.append(np.mean( np.array( skater["components"]["Skating Skills"]["scores"] )))
        Tran.append(np.mean( np.array( skater["components"]["Transitions"]["scores"] )))
        Perf.append(np.mean( np.array( skater["components"]["Performance"]["scores"] )))
        Comp.append(np.mean( np.array( skater["components"]["Composition"]["scores"] )))
        Intr.append(np.mean( np.array( skater["components"]["Interpretation"]["scores"] )))

    Skat = np.array(Skat)
    Tran = np.array(Tran)
    Perf = np.array(Perf)
    Comp = np.array(Comp)
    Intr = np.array(Intr)

    pcs = np.vstack( (Skat, Tran, Perf, Comp, Intr) )
    pl.plot(pcs,'o-')

    for i,namn in enumerate(names):
        pl.annotate(namn,(4.2,pcs[-1,i]))

    pl.xlim((-0.3,5.2))
    pl.xticks(range(len(pc_names)),pc_names)
    pl.ylabel("Score")
    pl.title(title)

    pl.show()
