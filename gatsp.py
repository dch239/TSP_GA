import random
from random import uniform
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
        # print(self.length)
        print(self.fitness)


class Population:
    def __init__(self, cities) -> None:
        self.population = []
        self.sum_of_fitnesses = 0
        self.population_size = 10
        self.best_chromosome = None
        self.MakeInitialPopulation(self.population_size, cities)
        self.CalculateSumOfFitnesses()

    def MakeInitialPopulation(self, size, cities):
        for i in range(size):
            random.shuffle(cities)
            chromosome =  Chromosome(cities)
            if (self.best_chromosome == None or chromosome.fitness < self.best_chromosome.fitness):
                self.best_chromosome = chromosome
            self.population.append(chromosome)
        #return self.population

    def CalculateSumOfFitnesses(self):
        for chromosome in self.population:
            self.sum_of_fitnesses += chromosome.fitness

    def RouletteSelection(self):
        random_val = uniform(0,self.sum_of_fitnesses)
        partial_sum = 0
        for i in range(len(self.population)):
            partial_sum += self.population[i].fitness
            if (partial_sum >= random_val):
                print( str(self.sum_of_fitnesses) + " " + str(random_val) + " " + str(partial_sum) )
                return i
        print("roulette selection failed")

    def CrossOver(self):
        p1_index=p2_index=0
        while(p1_index == p2_index):
            p1_index = self.RouletteSelection()
            p2_index = self.RouletteSelection()

        print(p1_index, p2_index)
        point_a = random.randint(0, self.population[p1_index].length - 1)
        point_b = random.randint(0, self.population[p2_index].length - 1)
        if (point_a > point_b):
            point_a, point_b = point_b, point_a
        
        print(point_a, point_b)
        
        lookup = {}
        child = [None] * self.population[p1_index].length
        for i in range(point_a, point_b+1):
            child[i] = self.population[p1_index].sequence[i]
            lookup[child[i]] = True

        start = 0
        for i in range(point_a):
            for j in range(start, self.population[p2_index].length):
                if ( lookup.get(self.population[p2_index].sequence[j]) == None):
                    child[i] = self.population[p2_index].sequence[j]
                    lookup[child[i]] = True
                    start = j+1
        print(start)
        for i in range(point_b+1, self.population[p1_index].length):
            for j in range(start, self.population[p2_index].length):
                if ( lookup.get(self.population[p2_index].sequence[j]) == None):
                    child[i] = self.population[p2_index].sequence[j]
                    lookup[child[i]] = True
                    start = j+1
        print(p1_index, p2_index)
        print(f"parent1 = {self.population[p1_index].sequence}")
        print(f"parent2 = {self.population[p2_index].sequence}")
        print(f"child = {child}")
        return child
        

        

def main():
    f = open('input.txt', 'r')
    count = int(f.readline())
    cities = []
    for i in range(count):
        t = tuple(int(x) for x in f.readline().split())
        cities.append(t)
    print(cities)
    pop = Population(cities)
    pop.CrossOver()


if __name__ == "__main__":
    main()