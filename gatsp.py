import random
import math

class Chromosome:
    def __init__(self, sequence) -> None:
        self.sequence = sequence
        self.length = len(self.sequence)
        self.fitness = self.calculate_fitness()
        self.display()
    
    def calculate_fitness(self):
        f = 0
        for i in range(self.length-1):
            f += math.sqrt(sum([(a - b) ** 2 for a, b in zip(self.sequence[i], self.sequence[i+1])]))
        f += math.sqrt(sum([(a - b) ** 2 for a, b in zip(self.sequence[i+1], self.sequence[0])]))
        #print(f)
        return f

    def display(self):
        print(self.sequence)
        print(self.length)
        print(self.fitness)


class Population:
    def __init__(self, cities) -> None:
        self.initial_population = []
        self.population_size = 10
        self.MakeInitialPopulation(self.population_size, cities)

    def MakeInitialPopulation(self, size, cities):
        for i in range(size):
            random.shuffle(cities)
            chromosome =  Chromosome(cities)
            self.initial_population.append(chromosome)
        #return self.initial_population
    


def main():
    f = open('input.txt', 'r')
    count = int(f.readline())
    cities = []
    for i in range(count):
        t = tuple(int(x) for x in f.readline().split())
        cities.append(t)
    print(cities)
    pop = Population(cities)


if __name__ == "__main__":
    main()