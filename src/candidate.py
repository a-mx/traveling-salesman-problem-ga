import random
from typing import List, Callable
import math
from src.city import City
from src.map import Map
class Candidate:
    def __init__(
        self,
        map: Map,
        representation: List[City] =None,
    ):
        self.map = map
        self.representation = representation if representation is not None else self._random_representation()


    def _random_representation(self) -> List[City]:
        cities = self.map.cities.copy()
        r = []
        while cities:
            n = len(cities)
            idx = random.randint(0, n-1)
            city = cities[idx]
            r.append(city)
            cities.pop(idx)
        return r

    def get_fitness(self) -> float:
        if len(self.representation) < 2:
            return 0
        total_distance = 0
        for idx in range(len(self.representation)):
            city_a = self.representation[idx]
            city_b = self.representation[(idx + 1) % len(self.representation)]
            total_distance += self._dist(city_a, city_b)

        if total_distance == 0:
            return 0.0

        route_length = self.get_route_length()
        if route_length == 0:
            return 0.0
        return 1 / route_length

    def get_route_length(self) -> float:
        if len(self.representation) < 2:
            return 0.0

        return sum(
            self._dist(self.representation[idx], self.representation[(idx + 1) % len(self.representation)])
            for idx in range(len(self.representation))
        )
    def _dist(self, c1: City, c2: City) -> float:
        i = self.map.get_idx(c1.x, c1.y)
        j = self.map.get_idx(c2.x, c2.y)
        return self.map.get_dist(i, j)
    
    def __repr__(self) -> str:
        return str(self.representation) \
        + f" Fitness: {self.get_fitness():.8f}\n"
    
if __name__ == "__main__":
    m = Map(10, 10)
    m.add_city([City(1,5), City(3,2), City(5,3), City(4,5), City(2,3), City(4,3)])
    c = Candidate(m)
    print(c)