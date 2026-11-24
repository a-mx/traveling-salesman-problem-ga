from typing import List, Dict, Tuple
from src.city import City
import numpy as np
class Map:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cities : List[City] = []
        self.idx_table : Dict[Tuple[int, int], int] = {}
        self.dist_matrix : np.ndarray = self.calculate_distance_matrix()
    
    def add_city(self, c: City | List[City]):
        if isinstance(c, City):
            cities_to_add = [c]
        elif isinstance(c, list):
            cities_to_add = [city for city in c if isinstance(city, City)]
        else:
            cities_to_add = []

        for city in cities_to_add:
            index = len(self.cities)
            self.cities.append(city)
            self.idx_table[(city.x, city.y)] = index

        self.dist_matrix = self.calculate_distance_matrix()
    
    def get_idx(self, x: int, y: int) -> int:
        return self.idx_table[(x,y)]
    
    def get_dist(self, i: int, j: int) -> float:
        return self.dist_matrix[i, j]

    def calculate_distance_matrix(self) -> np.ndarray:
        city_count = len(self.cities)
        dist_matrix = np.zeros((city_count, city_count), dtype=float)
        for i, city_a in enumerate(self.cities):
            for j, city_b in enumerate(self.cities):
                dist_matrix[i][j] = np.sqrt((city_a.x - city_b.x) ** 2 + (city_a.y - city_b.y) ** 2)
        return dist_matrix
        
