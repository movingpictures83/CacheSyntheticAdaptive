import numpy as np
import csv
NUM_REQUEST = 40000
UNIQUE_PAGES = 500
PHASE_SHIFTS = 1000
RANDOMIZATION_RATE = 0.25
CACHE_SIZE = 50
PROB_USED = 0.8
DECAY_RATE = 0.99

HARD_PHASE_SHIFT = NUM_REQUEST/2
# LRU_PROB = 0.9

Q = list()
F = {}

## Choose page using a uniform distribution
def Random():
    return np.random.randint(0, UNIQUE_PAGES)

## Choose page using LRU distribution
def LRU():
    n = min(CACHE_SIZE, len(F))
    L = []
    for i,pg in enumerate(Q[::-1]) :
        if i >= n :
            break
        L.append(pg)
    return L[np.random.randint(0, n)]

## Choose page using LFU distribution
def LFU():
    n = min(CACHE_SIZE, len(F))
    L = []
    for key in F :
        L.append((-F[key], key))
    L.sort()
    Q = []
    for i,pg in enumerate(L):
        if i >= n :
            break
        Q.append(pg[1])
    return Q[np.random.randint(0, n)]

def update(page):
    Q.append(page)
    if page not in F :
        F[page] = 0
    for pg in F :
        F[pg] *= DECAY_RATE
    F[page] += 1
    
class CacheSyntheticAdaptivePlugin:
 def input(self, inputfile):
    pass
 def run(self):
    pass
 def output(self, outputfile):
    time = 0
    phase = 1
    epsilon = 0.25
    out_file= outputfile+"/"+str(NUM_REQUEST) + "_"+ str(CACHE_SIZE) +"_"+ ".trc"
    with open(out_file, mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i in range(0, NUM_REQUEST) :
            if i == HARD_PHASE_SHIFT :
                phase = 1 - phase
    #         if i % PHASE_SHIFTS == 0 :
    #             phase = 0 if np.random.rand() < LRU_PROB else 1

            ## With probability RANDOMIZATION_RATE choose a page from a uniform distribution
            randomize = True if time == 0 or  np.random.rand() < epsilon else False

            if randomize :
                q = Random()
            else :
                if phase == 0 :
                    q = LRU()
                if phase == 1 :
                    q = LFU()        
            update(q)        
            # print(q)
            output_writer.writerow([q])
            
            time += 1
    print("Finishd")
        
        
