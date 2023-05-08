# import sktda

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.spatial.distance as d
import persim
import ripser
import tadasets
from persim import plot_diagrams

# def discreteDistance(X, Y):
#     n = np.empty((len(X), len(X)), dtype=float)
#     return n

def mink0p5(u, v):
    return d.minkowski(u, v, p=0.5)

def mink0p75(u, v):
    return d.minkowski(u, v, p = 0.75)
    
def mink1p5(u, v):
    return d.minkowski(u, v, p = 1.5)

def mink2p5(u, v):
    return d.minkowski(u, v, p = 2.5)

def mink3(u, v):
    return d.minkowski(u, v, p = 3)

def mink5(u, v):
    return d.minkowski(u, v, p = 5)

def discrete(u, v):
    if u is v:
        return 0
    else:
        return 1


# metrics = ["euclidean", "cityblock", "chebyshev", "cosine", "minkowski", "hamming"] # cosine-cosine and hamming-hamming break sometimes
# metrics = ["euclidean", "cityblock", "chebyshev", "cosine", "hamming", mink3, mink1]
# metrics = [mink0p5, mink0p75, "cityblock", mink1p5, "euclidean", mink2p5, mink3, mink5, "chebyshev", "cosine", "braycurtis", "hamming"]
metrics = [mink0p5, mink0p75, "cityblock", mink1p5, "euclidean", mink2p5, mink3, mink5, "chebyshev", "braycurtis", "hamming"]
# metrics = ["cityblock", mink1p5, "euclidean", mink2p5, mink3, mink5, "chebyshev", "braycurtis", "hamming", discrete]

def generatePersDistsCSV(filePath, file, outPath, delim = None):
    arr = np.loadtxt(filePath + file, dtype=float, delimiter=delim)
    
    print("Input Array Shape: ", arr.shape, " (rows, columns)")
    
    # print(arr)
    ml = len(metrics)
    mat = np.empty((ml, ml), dtype=float)
    
    print("Compiling Diagram List...")
    diagramList = []
    for i in range(ml):
        print("\tprogress: ", i)
        diagramList.append(ripser.ripser(arr, maxdim=1, distance_matrix=False, metric=metrics[i])['dgms'][1])
    print("Diagram List Complete")
    
    for i in range(ml):
        diagram1 = diagramList[i]
        for j in range(ml):
            diagram2 = diagramList[j]
            
            if j < i:
                continue
            
            elif (
                j == i or
                ((len(diagram1) == 0 and len(diagram2) == 0))
            ):
                distance = 0
                
            else:
                distance = persim.bottleneck(diagram1, diagram2)
            
            print(i, j, ": ", distance)
            mat[i][j] = distance
            mat[j][i] = distance
                
            
    mat = pd.DataFrame(mat)
    mat.columns = metrics
    mat.index = metrics
    print(mat)
    mat.to_csv(outPath + "out-" + file[:-4] + ".csv", index=True, sep = ",")

if __name__ == "__main__":
    print("RUNNING YO")
    
    # data = np.random.random((100,2))
    # diagram = ripser.ripser(data)["dgms"]
    
    data = np.loadtxt("finalProject/scav/data/points400_2.csv", delimiter=",", dtype = float)
    diagram = ripser.ripser(data, maxdim = 2, distance_matrix = False, metric = "hamming")['dgms']
    
    # # print(diagram)
    plot_diagrams(diagram, show=False)
    plt.title("points400_2 Hamming")
    plt.show()
    # arr = np.loadtxt("LaTeX\\2023-04-14 ETS HW9\\data\\points22.csv", delimiter=",", dtype=float)
    
    # arr1 = np.loadtxt("finalProject/data/points400_2-Reg.csv", delimiter=",", dtype=float)
    # arr2 = np.loadtxt("finalProject/data/points400_2-Discrete.csv", delimiter=",", dtype=float)
    # diagram1 = ripser.ripser(arr1, maxdim = 1, distance_matrix=True)['dgms'][1]
    # diagram2 = ripser.ripser(arr2, maxdim = 1, distance_matrix=True)['dgms'][1]
    
    # generatePersDistsCSV("finalProject/PH-roadmap/data_sets/roadmap_datasets_point_cloud/", "dragon_vrip.ply.txt_2000_.txt", "finalProject/out/")
    # generatePersDistsCSV("finalProject/PH-roadmap/data_sets/roadmap_datasets_point_cloud/", "celegans_weighted_undirected_reindexed_for_matlab.txt_maxdist_2.6429_SP_distmat.txt_point_cloud.txt", "finalProject/out/")
    # generatePersDistsCSV("finalProject/PH-roadmap\data_sets/roadmap_datasets_point_cloud/", "HIV1_2011.all.nt.concat.fa_hdm.txt_point_cloud.txt", "finalProject/out/")
    # generatePersDistsCSV("finalProject/PH-roadmap\data_sets/roadmap_datasets_point_cloud/", "house104_edge_list.txt_0.72344_point_cloud.txt", "finalProject/out/")
    # generatePersDistsCSV("finalProject/scav/data/", "points1.csv", "finalProject/out/", delim=",")
    # generatePersDistsCSV("finalProject/scav/data/", "points6.csv", "finalProject/out/", delim=",")
    # generatePersDistsCSV("finalProject/scav/data/", "points12.csv", "finalProject/out/", delim=",")
    # generatePersDistsCSV("finalProject/scav/data/", "points400_1.csv", "finalProject/out/", delim=",")
    # generatePersDistsCSV("finalProject/scav/data/", "points400_2.csv", "finalProject/out/", delim=",")

    
    
    # diagram1 = ripser.ripser(arr1, maxdim = 1, distance_matrix=False, metric="euclidean")['dgms'][1]
    # print(len(diagram1))
    # diagram2 = ripser.ripser(arr1, maxdim = 1, distance_matrix=False, metric="l1")['dgms'][1]
    # print(len(diagram2))
    # print(diagram2)
    
    # # plot_diagrams([diagram1, diagram2], labels=["1", "2"], show=True)
    
    # distance_bottleneck, matching = persim.bottleneck(diagram1, diagram2, matching=True)
    # persim.bottleneck_matching(diagram1, diagram2, matching, labels=['Reg $H_1$', 'Block $H_1$'])
    # plt.title("Distance {:.3f}".format(distance_bottleneck))
    # plt.show()
    
    # print(bottleneck(diagram1, diagram2, matching=True))
        

