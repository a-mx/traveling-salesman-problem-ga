class City:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __repr__(self) -> str:
        return f"City({self.x},{self.y})"