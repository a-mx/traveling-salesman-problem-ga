import random
from typing import Iterable, Optional

from src.candidate import Candidate


class Generations:
    def __init__(
        self,
        population: Iterable[Candidate],
        p_crossover: float = 0.75,
        p_mutation: float = 0.001,
        generation_count: int = 1000,
    ):
        if not 0 <= p_crossover <= 1:
            raise ValueError("p_crossover musi być w zakresie 0..1")

        if not 0 <= p_mutation <= 1:
            raise ValueError("p_mutation musi być w zakresie 0..1")

        if generation_count < 0:
            raise ValueError("generation_count nie może być ujemne")

        population = list(population)

        if not population:
            raise ValueError("Populacja nie może być pusta")

        self.population = population
        self.map = population[0].map
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation
        self.generation_count = generation_count
        self.history = {"min": [], "avg": [], "max": []}
        self.best: Optional[Candidate] = None

    def _copy_candidate(self, candidate: Candidate) -> Candidate:
        return Candidate(
            map=self.map,
            representation=list(candidate.representation),
        )

    def _fitness(self, candidate: Candidate) -> float:
        return candidate.get_fitness()

    def _update_best(self) -> None:
        candidate = max(self.population, key=self._fitness)

        if (
            self.best is None
            or self._fitness(candidate) > self._fitness(self.best)
        ):
            self.best = self._copy_candidate(candidate)

    def selection(self) -> None:
        sorted_population = sorted(
            self.population,
            key=self._fitness,
            reverse=True,
        )

        population_size = len(sorted_population)
        weights = list(range(population_size, 0, -1))

        self.population = random.choices(
            sorted_population,
            weights=weights,
            k=population_size,
        )

    @staticmethod
    def pmx(
        parent1: list,
        parent2: list,
    ) -> tuple[list, list]:
        size = len(parent1)

        if size < 2:
            return list(parent1), list(parent2)

        point1 = random.randrange(size)
        point2 = random.randrange(point1, size)

        child1 = [None] * size
        child2 = [None] * size

        child1[point1:point2] = parent1[point1:point2]
        child2[point1:point2] = parent2[point1:point2]

        for child, segment_source, segment_target in (
            (child1, parent2, parent1),
            (child2, parent1, parent2),
        ):
            for i in range(point1, point2):
                value = segment_source[i]

                if value not in segment_target[point1:point2]:
                    position = i

                    while position in range(point1, point2):
                        replacement = segment_target[position]
                        position = segment_source.index(replacement)

                    child[position] = value

        for i in range(size):
            if i not in range(point1, point2):
                if child1[i] is None:
                    child1[i] = parent2[i]
                if child2[i] is None:
                    child2[i] = parent1[i]

        return child1, child2

    def crossover(self) -> None:
        new_population = []
        population = self.population
        size = len(population)

        for i in range(0, size - 1, 2):
            parent1 = population[i]
            parent2 = population[i + 1]

            representation1 = list(parent1.representation)
            representation2 = list(parent2.representation)

            if random.random() < self.p_crossover:
                representation1, representation2 = self.pmx(
                    representation1,
                    representation2,
                )

            new_population.append(
                Candidate(self.map, representation1)
            )
            new_population.append(
                Candidate(self.map, representation2)
            )

        if size % 2 == 1:
            new_population.append(
                self._copy_candidate(population[-1])
            )

        self.population = new_population

    def mutation(self) -> None:
        for candidate in self.population:
            if len(candidate.representation) < 2:
                continue

            for i in range(len(candidate.representation)):
                if random.random() < self.p_mutation:
                    j = random.randrange(len(candidate.representation))

                    if i != j:
                        candidate.representation[i], candidate.representation[j] = (
                            candidate.representation[j],
                            candidate.representation[i],
                        )

    def collect_stats(self) -> None:
        route_lengths = [candidate.get_route_length() for candidate in self.population]

        self.history["min"].append(min(route_lengths))
        self.history["avg"].append(
            sum(route_lengths) / len(route_lengths)
        )
        self.history["max"].append(max(route_lengths))

    def run_generation(self) -> None:
        self.selection()
        self.crossover()
        self.mutation()
        self._update_best()

    def run(self) -> dict:
        self.collect_stats()
        self._update_best()

        for _ in range(self.generation_count):
            self.run_generation()
            self.collect_stats()

        return self.history