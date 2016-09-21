# -*- coding: utf-8 -*-

"""GA.py

遗传算法类
"""
import sys
import random
import math
import time
import Tkinter
import threading


import random
from Life import Life


class GA(object):

    def __init__(self, xRate=0.7, mutationRate=0.005, lifeCount=50, geneLength=100, judge=lambda lf, av: 1, save=lambda: 1, mkLife=lambda: None, xFunc=None, mFunc=None):
        self.xRate = xRate
        self.mutationRate = mutationRate
        self.mutationCount = 0
        self.generation = 0
        self.lives = []
        self.bounds = 0.0  # 得分总数
        self.best = None
        self.lifeCount = lifeCount
        self.geneLength = geneLength
        self.__judge = judge
        self.save = save
        self.mkLife = mkLife  # 默认的产生生命的函数
        self.xFunc = (xFunc, self.__xFunc)[xFunc == None]   # 自定义交叉函数
        self.mFunc = (mFunc, self.__mFunc)[mFunc == None]   # 自定义变异函数

        for i in range(lifeCount):
            self.lives.append(Life(self, self.mkLife()))

    def __xFunc(self, p1, p2):
        # 默认交叉函数
        r = random.randint(0, self.geneLength)
        gene = p1.gene[0:r] + p2.gene[r:]
        return gene

    def __mFunc(self, gene):
        # 默认突变函数
        r = random.randint(0, self.geneLength - 1)
        gene = gene[:r] + ("0", "1")[gene[r:r] == "1"] + gene[r + 1:]
        return gene

    def __bear(self, p1, p2):
        # 根据父母 p1, p2 生成一个后代
        r = random.random()
        if r < self.xRate:
            # 交叉
            gene = self.xFunc(p1, p2)
        else:
            gene = p1.gene

        r = random.random()
        if r < self.mutationRate:
            # 突变
            gene = self.mFunc(gene)
            self.mutationCount += 1

        return Life(self, gene)

    def __getOne(self):
        # 根据得分情况，随机取得一个个体，机率正比于个体的score属性
        r = random.uniform(0, self.bounds)
        for lf in self.lives:
            r -= lf.score
            if r <= 0:
                return lf

    def __newChild(self):
        # 产生新的后代
        return self.__bear(self.__getOne(), self.__getOne())

    def judge(self, f=lambda lf, av: 1):
        # 根据传入的方法 f ，计算每个个体的得分
        lastAvg = self.bounds / float(self.lifeCount)
        self.bounds = 0.0
        self.best = Life(self)
        self.best.setScore(-1.0)
        for lf in self.lives:
            lf.score = f(lf, lastAvg)
            if lf.score > self.best.score:
                self.best = lf
            self.bounds += lf.score

    def next(self, n=1):
        # 演化至下n代
        while n > 0:
            # self.__getBounds()
            self.judge(self.__judge)
            newLives = []
            newLives.append(Life(self, self.best.gene))  # 将最好的父代加入竞争
            # self.bestHistory.append(self.best)
            while (len(newLives) < self.lifeCount):
                newLives.append(self.__newChild())
            self.lives = newLives
            self.generation += 1
            #print("gen: %d, mutation: %d, best: %f" % (self.generation, self.mutationCount, self.best.score))
            self.save(self.best, self.generation)

            n -= 1

"""TSP.py

TSP问题
"""


class MyTSP(object):
    "TSP"

    def __init__(self, root, width=800, height=700, n=130):
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
            # x += 30
            # y += 30
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

        # print self.order
        # print self.distance(self.ga.best.gene)
        self.__t = None


    def line(self, order):
        "将节点按 order 顺序连线"
        self.canvas.delete("line")

        def line2(i1, i2):
            p1, p2 = self.nodes[i1], self.nodes[i2]
            self.canvas.create_line(p1, p2, fill="#000000", tags="line")
            return i2

        reduce(line2, order, order[-1])
        print order

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
                distance += math.sqrt((p1[0] - p2[0])
                                      ** 2 + (p1[1] - p2[1]) ** 2)
            return distance

        # print self.order
        # distance=distance(self,self.oder)
        # print distance

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    MyTSP(Tkinter.Tk()).mainloop()
