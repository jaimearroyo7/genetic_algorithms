import datetime
import genetic
import unittest
import random


class GuessPasswordTests(unittest.TestCase):
    gene_set = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.,"

    def test_hello_world(self):
        target = "Hello World!"
        self.guess_password(target)

    def test_For_I_am_fearfully_and_wonderfully_made(self):
        target = "For I am fearfully and wonderfully made."
        self.guess_password(target)

    def test_Random(self):
        length = 150
        target = ''.join(random.choice(self.gene_set) for _ in range(length))
        self.guess_password(target)

    def test_benchmark(self):
        genetic.Benchmark.run(self.test_Random)

    def guess_password(self, target):
        start_time = datetime.datetime.now()

        def fnGetFitness(genes):
            return get_fitness(genes, target)

        def fnDisplay(candidate):
            display(candidate, start_time)

        optimalfitness = len(target)
        best = genetic.get_best(
            fnGetFitness, len(target), optimalfitness, self.gene_set, fnDisplay)
        self.assertEqual(best.Genes, target)


def display(candidate, start_time):
    time_diff = datetime.datetime.now() - start_time
    print("{0}\t{1}\t{2}".format(
        candidate.Genes, candidate.Fitness, str(time_diff)))


def get_fitness(genes, target):
    return sum(1 for expected, actual in zip(target, genes)
               if expected == actual)


if __name__ == '__main__':
    unittest.main()