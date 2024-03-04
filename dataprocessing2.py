from obj_class_pickle import DataGraphs
import matplotlib.pyplot as plt 
import os
from itertools import permutations

import json
import os

def loadAndCalculateRatio(directory):
    resultRatiosByFile = {}
    nodes = 0

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):  # Ensure we're processing JSON files
            resultRatiosByFile[filename] = {}
            # Construct the full file path
            file_path = os.path.join(directory, filename)
            # Load the JSON data from the file
            with open(file_path, 'r') as file:
                result = json.load(file)
                # Assuming the JSON structure mirrors the previously used DataGraphs structure
                hops_dict = result['resultHops']
                hops_dict_sc = result['resultHopsShortCut']
                nodes = max(nodes, len(result['nodes']))
                for src in hops_dict:
                    resultRatiosByFile[filename][src] = {}
                    for destination in hops_dict[src]:
                        lst_hops = hops_dict[src][destination]
                        lst_hops_sc = hops_dict_sc[src][destination]
                        # Ensure we're not dividing by zero
                        lst_ratio = [a / b if b != 0 else 0 for a, b in zip(lst_hops, lst_hops_sc)]
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



#folders = ["30nodes","40nodes","50nodes","60nodes","70nodes","80nodes","90nodes","100nodes", "zoo", "zoo2", "zoo3", "workingzoo"]  # noqa: E501
folders = ["zoo", "zoo2", "zoo3", "workingzoo"]
for folder in folders:
    subfolder = folder
    directory = f"/home/mikheil/Desktop/SQ1_ShortCut-main/results/{subfolder}"
    Figdirectory = f"/home/mikheil/Desktop/SQ1_ShortCut-main/figs/{subfolder}"
    resultRatiosByFile, nodes = loadAndCalculateRatio(directory)
 
    endResult = fillDict_collected(resultRatiosByFile)

    #lst_nodes = list(range(0, nodes))
    #perm_nodes = permutations(lst_nodes, 2)
    #data2d = list(endResult.values())[1:]
    data2d = [endResult[i] for i in sorted(endResult.keys())]  # Ensure all failure numbers are included
    draw_collected(Figdirectory, data2d)
    print("done")
    pass

    #for perm in perm_nodes:
        #source = perm[0]
        #destination = perm[1]
        #data2d = list(endResult[source][destination].values())[1:]
        #draw(Figdirectory, data2d, source, destination)
        #pass
