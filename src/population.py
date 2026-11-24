from src.candidate import Candidate
from typing import List
from src.map import Map
from src.city import City
class Population:
    def __init__(self, n: int, map: Map):
        if n <= 0:
         raise ValueError("Liczebność populacji musi być większa od zera")
        
        self.n: int = n
        self.map: Map = map

        self.population: List[Candidate] = self._make_population(self.n, self.map)

    @staticmethod
    def _make_population(n: int, map: Map) -> List[Candidate]:
        population = []
        for _ in range(n):
            population.append(Candidate(map))
        return population

    def __repr__(self) -> str:
        return str(self.population)

    def __iter__(self):
        return self.population.__iter__()
    
if __name__ == "__main__":
    m = Map(10, 10)
    m.add_city([City(1,5), City(3,2), City(5,3), City(4,5), City(2,3), City(4,3)])
    p = Population(100, m)
    print(p)