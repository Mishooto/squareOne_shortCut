from obj_class_pickle import DataGraphs
import matplotlib.pyplot as plt 
import os
from itertools import permutations

def loadAndCalculateRatio(directory):
    resultRatiosByFile = {}
    nodes = 0
    for filename in os.listdir(directory):
        resultRatiosByFile[filename] = {}
        result = DataGraphs.load(f"{directory}/{filename}") 
        nodes = max(nodes, len(result.n))
        for src in result.hops_dict:
            resultRatiosByFile[filename][src] = {}
            for destination in result.hops_dict[src]:
                lst_hops = result.hops_dict[src][destination]
                lst_hops_sc = result.hops_dict_sc[src][destination]
                lst_ratio = [a / b for a, b in zip(lst_hops, lst_hops_sc)]
                resultRatiosByFile[filename][src][destination] = lst_ratio
    return resultRatiosByFile, nodes

def prepareResultDict(resultRatiosByFile):
    result_dict_by_failureNum = {}
    for firstkey in resultRatiosByFile:
        for src2 in resultRatiosByFile[firstkey]:
            result_dict_by_failureNum[src2] = {}
            for destination2 in resultRatiosByFile[firstkey][src2]:
                result_dict_by_failureNum[src2][destination2] = {}
                for i in range(0, len(resultRatiosByFile[firstkey][src2][destination2])):  # noqa: E501
                    result_dict_by_failureNum[src2][destination2][i] = []
    return result_dict_by_failureNum

def fillDict(resultRatiosByFile):
    preparedDict = prepareResultDict(resultRatiosByFile)
    for filename in resultRatiosByFile:
        for source in resultRatiosByFile[filename]:
            for destination in resultRatiosByFile[filename][source]:
                lst_specified = resultRatiosByFile[filename][source][destination] 
                for j in range(0, len(lst_specified)):
                    preparedDict[source][destination][j].append(lst_specified[j])
    return preparedDict

def draw(figdirectory, data2d, source, destination):
    if not os.path.exists(figdirectory):
        os.makedirs(figdirectory)
    fig = plt.figure()
    plt.ioff()
    plt.boxplot(data2d)
    #plt.title("Boxplot Using Matplotlib")
    plt.xlabel('number of failures')
    plt.ylabel('hops ratio without/with ShortCut')
    fig.savefig(f"{figdirectory}/{source}_{destination}.png", dpi=fig.dpi)
    plt.close(fig)

def draw_collected(figdirectory, data2d):
    if not os.path.exists(figdirectory):
        os.makedirs(figdirectory)
    fig = plt.figure()
    plt.ioff()
    plt.boxplot(data2d)
    #plt.title("Boxplot Using Matplotlib")
    plt.xlabel('number of failures')
    plt.ylabel('hops ratio without/with ShortCut')
    fig.savefig(f"{figdirectory}/collected.png", dpi=fig.dpi)
    #plt.close(fig)

def fillDict_collected(resultRatiosByFile):
    preparedDict = prepareResultDict_collected(resultRatiosByFile)
    for filename in resultRatiosByFile:
        for source in resultRatiosByFile[filename]:
            for destination in resultRatiosByFile[filename][source]:
                lst_specified = resultRatiosByFile[filename][source][destination] 
                for j in range(0, len(lst_specified)):
                    preparedDict[j].append(lst_specified[j])
    return preparedDict

def prepareResultDict_collected(resultRatiosByFile):
    result_dict_by_failureNum = {}
    for firstkey in resultRatiosByFile:
        for src2 in resultRatiosByFile[firstkey]:
            #result_dict_by_failureNum[src2] = {}
            for destination2 in resultRatiosByFile[firstkey][src2]:
                #result_dict_by_failureNum[src2][destination2] = {}
                for i in range(0, len(resultRatiosByFile[firstkey][src2][destination2])):  # noqa: E501
                    result_dict_by_failureNum[i] = []
    return result_dict_by_failureNum

folders = ["30nodes","40nodes","50nodes","60nodes","70nodes","80nodes","90nodes","100nodes", "zoo", "zoo2"]  # noqa: E501
for folder in folders:
    subfolder = folder
    directory = f"/home/mikheil/Desktop/SQ1_ShortCut-main/results/{subfolder}"
    Figdirectory = f"/home/mikheil/Desktop/SQ1_ShortCut-main/figs/{subfolder}"
    resultRatiosByFile, nodes = loadAndCalculateRatio(directory)
    #endResult = fillDict(resultRatiosByFile)
    endResult = fillDict_collected(resultRatiosByFile)

    #lst_nodes = list(range(0, nodes))
    #perm_nodes = permutations(lst_nodes, 2)
    data2d = list(endResult.values())[1:]
    draw_collected(Figdirectory, data2d)
    print("done")
    pass
    #for perm in perm_nodes:
        #source = perm[0]
        #destination = perm[1]
        #data2d = list(endResult[source][destination].values())[1:]
        #draw(Figdirectory, data2d, source, destination)
        #pass
