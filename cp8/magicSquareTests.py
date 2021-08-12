import datetime
import random
import unittest

from genetic_algorithms.utils import genetic


class MagicSquareTests(unittest.TestCase):
    def test_size_3(self):
        self.generate(3, 50)

    def test_size_5(self):
        self.generate(5, 500)

    def test_size_10(self):
        self.generate(10, 5000)

    def test_size_4(self):
        self.generate(4, 50)

    def test_benchmark(self):
        genetic.Benchmark.run(self.test_size_4)

    def generate(self, diagonalSize, max_age):
        nSquared = diagonalSize * diagonalSize

        gene_set = [i for i in range(1, nSquared + 1)]
        expectedSum = diagonalSize * (nSquared + 1) / 2

        def fn_get_fitness(genes):
            return get_fitness(genes, diagonalSize, expectedSum)

        def fn_display(candidate):
            display(candidate, diagonalSize, start_time)

        geneIndexes = [i for i in range(0, len(gene_set))]

        def fnMutate(genes):
            mutate(genes, geneIndexes)

        def fnCustomCreate():
            return random.sample(gene_set, len(gene_set))

        optimal_value = Fitness(0)
        start_time = datetime.datetime.now()
        best = genetic.get_best(fn_get_fitness, nSquared, optimal_value,
                                gene_set, fn_display, fnMutate,
                                fnCustomCreate, max_age)

        self.assertTrue(not optimal_value > best.Fitness)


class Fitness:
    SumOfDifferences = None

    def __init__(self, sumOfDifferences):
        self.SumOfDifferences = sumOfDifferences

    def __gt__(self, other):
        return self.SumOfDifferences < other.SumOfDifferences

    def __str__(self):
        return "{0}".format(self.SumOfDifferences)


def mutate(genes, indexes):
    indexA, indexB = random.sample(indexes, 2)
    genes[indexA], genes[indexB] = genes[indexB], genes[indexA]


def get_fitness(genes, diagonalSize, expectedSum):
    rows, columns, northeastDiagonalSum, southeastDiagonalSum = \
        get_sums(genes, diagonalSize)

    sumOfDifferences = sum(int(abs(s - expectedSum))
                           for s in rows + columns +
                           [southeastDiagonalSum, northeastDiagonalSum]
                           if s != expectedSum)

    return Fitness(sumOfDifferences)


def get_sums(genes, diagonalSize):
    rows = [0 for _ in range(diagonalSize)]
    columns = [0 for _ in range(diagonalSize)]
    southeastDiagonalSum = 0
    northeastDiagonalSum = 0
    for row in range(diagonalSize):
        for column in range(diagonalSize):
            value = genes[row * diagonalSize + column]
            rows[row] += value
            columns[column] += value
        southeastDiagonalSum += genes[row * diagonalSize + row]
        northeastDiagonalSum += genes[row * diagonalSize +
                                      (diagonalSize - 1 - row)]
    return rows, columns, northeastDiagonalSum, southeastDiagonalSum


def display(candidate, diagonalSize, start_time):
    time_diff = datetime.datetime.now() - start_time
    rows, columns, northeastDiagonalSum, southeastDiagonalSum = \
    get_sums(candidate.Genes, diagonalSize)
    for rowNumber in range(diagonalSize):
        row = candidate.Genes[
              rowNumber * diagonalSize:(rowNumber + 1) * diagonalSize]
        print("\t ", row, "=", rows[rowNumber])
    print(northeastDiagonalSum, "\t", columns, "\t", southeastDiagonalSum)
    print(" - - - - - - - - - - -", candidate.Fitness, str(time_diff))