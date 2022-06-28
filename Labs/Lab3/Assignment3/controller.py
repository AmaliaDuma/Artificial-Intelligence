from repository import *


class Controller:
    def __init__(self, repository):
        # args - list of parameters needed in order to create the controller
        self._nr_seeds = None
        self._repository = repository
        self._steps_nr = None
        self._population_size = None
        self._nr_iterations = None
        self._mutation_prob = None
        self._crossover_prob = None
        self._statistics = []  # [[average_fitness_1, random_seed_1],...[average_fitness_numberOfIterations_, random_seed__numberOfIterations]]
        self._iteration = 0
        self._last_stats = []

    def set_nr_seeds(self, nr):
        self._nr_seeds = nr

    def set_drone(self, x, y):
        self._repository.set_drone(x, y)

    def set_steps(self, steps):
        self._steps_nr = steps

    def set_nr_iterations(self, iterations):
        self._nr_iterations = iterations

    def set_mutation_prob(self, probability):
        self._mutation_prob = probability

    def set_crossover_prob(self, probability):
        self._crossover_prob = probability

    def set_population_size(self, size):
        self._population_size = size

    def iteration(self, args=0):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parrents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors

        population = self._repository.current_population()
        self._repository.evaluate_population(population)
        select = population.selection(population.size()-2)
        parents = select[:len(select) // 2]
        pairs = len(parents) // 2
        used_pairs = []
        nr_of_pairs = 0

        for i in range(pairs):
            first = parents[randint(0, len(parents) - 1)]
            second = parents[randint(0, len(parents) - 1)]
            if [first, second] not in used_pairs:
                nr_of_pairs += 2
                used_pairs.append([first, second])
                firstCrossed, secondCrossed = first.crossover(second, self._crossover_prob)
                first.mutate(self._mutation_prob)
                secondCrossed.mutate(self._mutation_prob)
                self._repository.add_individual(population, firstCrossed)
                self._repository.add_individual(population, secondCrossed)
        select = population.selection(population.size() - nr_of_pairs)
        population.set_individuals(select)
        
    def run(self, args):
        # args - list of parameters needed in order to run the algorithm
        
        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics
        
        # return the results and the info for statistics

        self._last_stats = []
        for i in range(0, self._nr_iterations):
            self.iteration()
            if args == self._nr_seeds - 1:
                self._last_stats.append(self._repository.avg_fitness_and_deviation())

        self._statistics.append(self._repository.get_best_fitness())
        # self._statistics.append([np.average(f), np.std(f)])
    
    
    def solver(self, args=0):
        # args - list of parameters needed in order to run the solver
        
        # create the population,
        # run the algorithm
        # return the results and the statistics

        for i in range(self._nr_seeds):
            seed(30 - i)
            population = self._repository.createPopulation([self._population_size, self._steps_nr])
            self._repository.add_population(population)
            self.run(i)
            # print(self._statistics[i])

        return self._repository.get_first_path(), self._statistics, self._last_stats

    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (0, 0))

        return mapImage
       