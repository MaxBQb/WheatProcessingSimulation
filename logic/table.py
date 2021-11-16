class Table:
    _NO_DATA = list(tuple())

    def __init__(self, data=None):
        self.data = data or self._NO_DATA

    def column(self, number: int):
        return (row[number] for row in self.data)

    def row(self, number: int):
        return (cell for cell in self.data[number])

    def cell(self, column: int, row: int, default=Exception):
        try:
            return self.data[row][column]
        except (IndexError, TypeError):
            if default is Exception:
                raise
            return default
