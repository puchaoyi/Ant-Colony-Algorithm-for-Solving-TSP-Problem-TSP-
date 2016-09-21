import random
import copy
import time
import sys
# (ALPHA, BETA, RHO, Q) = (1.0, 2.0, 0.5, 100.0)
# (city_num, ant_num, iter_max) = (130, 34, 1000)
(ALPHA, BETA, RHO, Q) = (1.0, 2.5, 0.5, 100.0)
(city_num, ant_num, iter_max) = (130, 4, 1000)
distance_x = []
distance_y = []
for line in open('testSet.txt'):
    items = line.strip('\n').split(' ')
    distance_x.append(float(items[1]))
    distance_y.append(float(items[2]))
distance_graph = [[0.0 for col in xrange(city_num)]
                  for raw in xrange(city_num)]
pheromone_graph = [[1.0 for col in xrange(
    city_num)] for raw in xrange(city_num)]

class Ant(object):

    def __init__(self, ID):

        self.ID = ID

        self.__clean_data()

    def __lt__(self, other):

        return self.total_distance < other.total_distance

    def __clean_data(self):

        self.path = []
        self.total_distance = 0.0
        self.move_count = 0
        self.current_city = -1
        self.open_table_city = [True for i in xrange(city_num)]

        city_index = random.randint(1, city_num - 1)
        self.current_city = city_index
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1

    def __choice_next_city(self):

        next_city = -1
        select_citys_prob = [0.0 for i in xrange(city_num)]
        total_prob = 0.0

        for i in xrange(city_num):
            if self.open_table_city[i]:
                try:
                    select_citys_prob[i] = pow( pheromone_graph[self.current_city][i], ALPHA ) *\
                        pow((1.0 / distance_graph[self.current_city][i]), BETA)
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError, e:
                    print 'Ant ID: {ID}, current city: {current}, target city: {target}'.format(
                        ID=self.ID, current=self.current_city, target=i)
                    sys.exit(1)

        # select city by way of roulette
        if total_prob > 0.0:
            temp_prob = random.uniform(0.0, total_prob)
            for i in xrange(city_num):
                if self.open_table_city[i]:
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        if next_city == -1:
            for i in xrange(city_num):
                if self.open_table_city[i]:
                    next_city = i
                    break

        return next_city

    def __cal_total_distance(self):

        temp_distance = 0.0

        for i in xrange(1, city_num):
            start, end = self.path[i], self.path[i - 1]
            temp_distance += distance_graph[start][end]

        end = self.path[0]
        temp_distance += distance_graph[start][end]
        self.total_distance = temp_distance
        print "best_path:", self.path
        Path = self.path
        return Path

    def __move(self, next_city):

        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.total_distance += distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1

    def search_path(self):

        self.__clean_data()

        while self.move_count < city_num:

            next_city = self.__choice_next_city()
            self.__move(next_city)

        self.__cal_total_distance()


class TSP(object):

    def __init__(self):
        self.ants = [Ant(ID) for ID in xrange(ant_num)]
        self.best_ant = Ant(-1)
        self.best_ant.total_distance = 1 << 31

        for i in xrange(city_num):
            for j in xrange(city_num):
                temp_distance = pow(
                    (distance_x[i] - distance_x[j]), 2) + pow((distance_y[i] - distance_y[j]), 2)
                temp_distance = pow(temp_distance, 0.5)
                distance_graph[i][j] = float(int(temp_distance + 0.5))
                pheromone_graph[i][j] = 1.0

    def search_path(self):

        for i in xrange(iter_max):
            for ant in self.ants:
                ant.search_path()
                if ant < self.best_ant:
                    self.best_ant = copy.deepcopy(ant)

            self.__update_pheromone_graph()
        # print "best_ant.total_distance:", self.best_ant.total_distance


    def __update_pheromone_graph(self):

        temp_pheromone = [[0.0 for col in xrange(
            city_num)] for raw in xrange(city_num)]
        for ant in self.ants:
            for i in xrange(1, city_num):
                start, end = ant.path[i - 1], ant.path[i]
                temp_pheromone[start][end] += Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]

            end = ant.path[0]
            temp_pheromone[start][end] += Q / ant.total_distance
            temp_pheromone[end][start] = temp_pheromone[start][end]

        for i in xrange(city_num):
            for j in xrange(city_num):
                pheromone_graph[i][j] = pheromone_graph[
                    i][j] * RHO + temp_pheromone[i][j]

if __name__ == '__main__':

    test = TSP()
    test.search_path()
    print "Best Distance: ", test.best_ant.total_distance
