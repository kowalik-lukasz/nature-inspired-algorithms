class Solve:
    def __init__(self, filename: str, index_row: bool = True, index_col: bool = False):
        """
        Displays the problem instance visually. The instance must exist within problem-instances directory
        :param filename: the name of the problem instance
        :param index_row: a flag indicating whether the first row contains headers (default: True)
        :param index_col: a flag indicating whether the first column contains headers (default: False)
        """
        self.filename = filename
        self.index_row = index_row
        self.index_col = index_col

    def reference(self):
        print("Solving with the reference algorithm...")

    def nature(self):
        print("Solving with the nature inspired algorithm...")