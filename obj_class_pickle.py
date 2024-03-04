import pickle

class DataGraphs():
    def __init__(self, seed, ran_dom, n, e, rep, shortest_path, fail_random, failure_num, hops_dict, hops_dict_sc):
        self.seed = seed
        self.ran_dom = ran_dom
        self.n = n
        self.e = e
        self.rep = rep
        self.shortest_path = shortest_path
        self.fail_random = fail_random
        self.failure_num = failure_num
        self.hops_dict = hops_dict
        self.hops_dict_sc = hops_dict_sc

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
    
    @staticmethod
    def load(filename) -> 'DataGraphs':
        with open(filename, 'rb') as file:
            return pickle.load(file)
     
# filename = "bla.pickle"

# toPickle = {}
# toPickle["n"] = 2
# toPickle["e"] = True
# toPickle["hops"] = [(1,2), (2,3)]
# with open(filename, 'wb') as file:
#     pickle.dump(toPickle, file)

# with open(filename, 'rb') as file:
#     pickled = pickle.load(file)
#     print(pickled["n"])

#from obj_class_pickle import DataGraphs
#import pickle
#result = DataGraphs.load("results/SQ1_ShortCut_1_graph_True_40_160_0_False.pickle") 
#result
#<obj_class_pickle.DataGraphs object at 0x000001AF9A901750>
#result.e