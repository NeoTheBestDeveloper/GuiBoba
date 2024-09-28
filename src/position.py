__all__ = [
    "Position",
]


class Position:
    _col: int
    _row: int

    def __init__(self, pos: str) -> None:
        self._row, self._col = map(int, pos.split('.'))

    def add_cols(self, cols: int = 1) -> None:
        self._col += cols

    def add_rows(self, rows: int = 1) -> None:
        self._row += rows
        self._col = 0

    def __str__(self) -> str:
        return f"{self._row}.{self._col}"
