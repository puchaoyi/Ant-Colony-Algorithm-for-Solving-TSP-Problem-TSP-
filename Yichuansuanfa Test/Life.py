# -*- coding: utf-8 -*-

"""Life.py

生命类
"""

import random


class Life(object):

    def __init__(self, env, gene=None):
        self.env = env

        # if gene == None:
        #     self.__rndGene()
        if type(gene) == type([]):
            self.gene = []
            for k in gene:
                self.gene.append(k)
        else:
            self.gene = gene

    def __rndGene(self):
        self.gene = ""
        for i in range(self.env.geneLength):
            self.gene += str(random.randint(0, 1))

    def setScore(self, v):
        self.score = v

    def addScore(self, v):
        self.score += v
