
from numpy import *
import time
import matplotlib.pyplot as plt

path = [35, 73, 58, 2, 72, 18, 92, 17, 23, 31, 60, 77, 36, 43, 51, 9, 3, 59, 98, 45, 48, 28, 0, 52, 39, 11, 14, 12, 46, 54, 41, 63, 19, 66, 7, 37, 55, 87, 97, 85, 61, 49, 67, 90, 75, 94, 69, 93, 20,
        22, 29, 53, 5, 79, 1, 34, 82, 4, 70, 71, 27, 42, 24, 38, 33, 16, 57, 89, 21, 74, 30, 64, 78, 84, 26, 76, 88, 40, 68, 32, 13, 99, 96, 86, 95, 83, 47, 10, 65, 62, 81, 6, 25, 8, 15, 50, 91, 80, 56, 44]

x = []
y = []
for line in open('Yinjun.txt'):
    iterms = line.strip('\n').split(' ')
    x.append(float(iterms[1]))
    y.append(float(iterms[2]))
for i in range(99):
    plt.plot(x[i], y[i], 'ok')
# for j in range(-1, 129):
#     plt.plot([x[path[j] - 1], x[path[j + 1] - 1]],
#              [y[path[j] - 1], y[path[j + 1] - 1]], 'k')
for k in range(-1, 99):
    print path[k]
    # plt.plot([x[path[k]], x[path[k + 1]]], [y[path[k]], y[path[k + 1]]], 'r')
    plt.plot([x[path[k]], x[path[k + 1]]], [y[path[k]], y[path[k + 1]]], 'g')
plt.show()


# def showCluster(dataSet, k, centroids, clusterAssment):
#     numSamples, dim = dataSet.shape
#     if dim != 2:
#         print "Sorry! I can not draw because the dimension of your data is not 2!"
#         return 1

#     mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
#     if k > len(mark):
#         print "Sorry! Your k is too large! please contact Zouxy"
#         return 1

#         # draw all samples
#     for i in xrange(numSamples):
#         markIndex = int(clusterAssment[i, 0])
#         plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

#     mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
#     # draw the centroids
#     for i in range(k):
#         plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)

#     plt.show()
