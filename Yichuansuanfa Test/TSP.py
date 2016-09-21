
# -*- coding: utf-8 -*-

"""TSP.py

TSP问题
"""

import sys
import random
import math
import time
import Tkinter
import threading

from GA import GA


class MyTSP(object):
    "TSP"

    def __init__(self, root, width=800, height=800, n=130):
        self.root = root
        self.width = width
        self.height = height
        self.n = n
        self.canvas = Tkinter.Canvas(
            root,
            width=self.width,
            height=self.height,
            bg="#ffffff",
            xscrollincrement=1,
            yscrollincrement=1
        )
        self.canvas.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)
        self.title("TSP")
        self.__r = 5
        self.__t = None
        self.__lock = threading.RLock()

        self.__bindEvents()
        self.new()

    def __bindEvents(self):
        self.root.bind("q", self.quite)
        self.root.bind("n", self.new)
        self.root.bind("e", self.evolve)
        self.root.bind("s", self.stop)

    def title(self, s):
        self.root.title(s)

    def new(self, evt=None):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

        self.clear()
        self.nodes = []  # 节点坐标
        self.nodes2 = []  # 节点图片对象
        fileIn = open('testSet.txt')
        for i in range(self.n):
            x, y = map(float, fileIn.readline().strip().split(' ')[1:])
            x+=30
            y+=30
        # for i in range(self.n):
        #     x = random.random() * (self.width - 60) + 30
        #     y = random.random() * (self.height - 60) + 30
            self.nodes.append((x, y))
            node = self.canvas.create_oval(x - self.__r,
                                           y - self.__r, x + self.__r, y + self.__r,
                                           fill="#ff0000",
                                           outline="#000000",
                                           tags="node",
                                           )
            self.nodes2.append(node)

        self.ga = GA(
            lifeCount=50,
            mutationRate=0.05,
            judge=self.judge(),
            mkLife=self.mkLife(),
            xFunc=self.xFunc(),
            mFunc=self.mFunc(),
            save=self.save()
        )
        self.order = range(self.n)
        self.line(self.order)

    def distance(self, order):
        "得到当前顺序下连线总长度"
        distance = 0
        for i in range(-1, self.n - 1):
            i1, i2 = order[i], order[i + 1]
            p1, p2 = self.nodes[i1], self.nodes[i2]
            distance += math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        return distance

    def mkLife(self):
        def f():
            lst = range(self.n)
            random.shuffle(lst)
            return lst
        return f

    def judge(self):
        "评估函数"
        return lambda lf, av = 100: 1.0 / self.distance(lf.gene)

    def xFunc(self):
        "交叉函数"
        def f(lf1, lf2):
            p1 = random.randint(0, self.n - 1)
            p2 = random.randint(self.n - 1, self.n)
            # print lf1.gene
            # print type(lf2.gene[p1:p2]),type(lf1.gene)
            g1 = lf2.gene[p1:p2] + lf1.gene
            # g2 = lf1.gene[p1:p2] + lf2.gene
            g11 = []
            for i in g1:
                if i not in g11:
                    g11.append(i)
            return g11
        return f

    def mFunc(self):
        "变异函数"
        def f(gene):
            p1 = random.randint(0, self.n - 2)
            p2 = random.randint(self.n - 2, self.n - 1)
            gene[p1], gene[p2] = gene[p2], gene[p1]
            return gene
        return f

    def save(self):
        def f(lf, gen):
            pass
        return f

    def evolve(self, evt=None):
        self.__lock.acquire()
        self.__running = True
        self.__lock.release()

        while self.__running:
            self.ga.next()
            self.line(self.ga.best.gene)
            self.title("TSP - gen: %d" % self.ga.generation)
            self.canvas.update()

        self.__t = None

    def line(self, order):
        "将节点按 order 顺序连线"
        self.canvas.delete("line")

        def line2(i1, i2):
            p1, p2 = self.nodes[i1], self.nodes[i2]
            self.canvas.create_line(p1, p2, fill="#000000", tags="line")
            return i2

        reduce(line2, order, order[-1])

    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    def quite(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        sys.exit()

    def stop(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

        def distance(self, order):
            "得到当前顺序下连线总长度"
            distance = 0
            for i in range(-1, self.n - 1):
                i1, i2 = order[i], order[i + 1]
                p1, p2 = self.nodes[i1], self.nodes[i2]
                distance += math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
            return distance
            

        print self.order 
        # distance=distance(self,self.oder)
        # print distance
        

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    MyTSP(Tkinter.Tk()).mainloop()
