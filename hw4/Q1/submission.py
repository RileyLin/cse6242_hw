'''
*** Imports ***
    DO NOT EDIT or add anything to this section
'''
import numpy as np
import time
import argparse
import sys

def author():
        return "wlin99"      # replace gburdell3 with your Georgia Tech username.

def gtid():
    return 903349740            # replace with your GT ID number (https://registrar.gatech.edu/info/gtid-lookup)

class PageRank:
    def __init__(self, edge_file):

        self.node_degree = {}
        self.max_node_id = 0
        self.edge_file = edge_file

    def read_edge_file(self, edge_file):
        with open(edge_file) as f:
            for line in f:
                val = line.split('\t')
                yield int(val[0]), int(val[1])

    """
    Step1: Calculate the out-degree of each node and maximum node_id of the graph.
    Store the out-degree in class variable "node_degree" and maximum node id to "max_node_id".
    """
    def calculate_node_degree(self):
        for source,target in self.read_edge_file(self.edge_file):

        ### STEP 1
        ### Implement your code here
        #############################################
            # Update max_node_id
            if source > self.max_node_id:
                self.max_node_id = source
            if target > self.max_node_id:
                self.max_node_id = target
            
            # Count out-degree for source node
            if source not in self.node_degree:
                self.node_degree[source] = 0
            self.node_degree[source] += 1

        #############################################

        print("Max node id: {}".format(self.max_node_id))
        print("Total source number: {}".format(len(self.node_degree)))

    def get_max_node_id(self):
        return self.max_node_id

    def run_pagerank(self, node_weights,  damping_factor=0.85, iterations=10):

        pr_values = [1.0 / (self.max_node_id + 1)] * (self.max_node_id + 1)
        start_time = time.time()
        """ 
        Step2: Implement pagerank algorithm as described in lecture slides and the question.

        Incoming Parameters:
            node_weights: Probability of each node to flyout during random walk
            damping_factor: Probability of continuing on the random walk
            iterations: Number of iterations to run the algorithm 
            check the __main__ function to understand node_weights and max_node_id
        
        Use the calculated out-degree to calculate the pagerank value of each node
        """
        for it in range(iterations):
            
            new_pr_values = [0.0] * (self.max_node_id + 1)
            
            # Initialize with random jump probability
            for j in range(self.max_node_id + 1):
                new_pr_values[j] = (1 - damping_factor) * node_weights[j]
            
            # Add contributions from incoming edges
            for source, target in self.read_edge_file(self.edge_file):

        ### STEP 2
        ### Implement your code here
        #############################################
                # Add contribution from source to target
                # PR(target) += d * PR(source) / out_degree(source)
                if source in self.node_degree and self.node_degree[source] > 0:
                    new_pr_values[target] += damping_factor * pr_values[source] / self.node_degree[source]

        #############################################
            
            # Update pr_values for next iteration
            pr_values = new_pr_values

        print ("Completed {0}/{1} iterations. {2} seconds elapsed.".format(it + 1, iterations, time.time() - start_time))

        return pr_values