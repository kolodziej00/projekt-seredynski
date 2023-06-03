class Canvas:
    def __init__(self, rows, cols, p_init_C, isSharing):
        self.rows = rows + 2
        self.cols = cols + 2
        self.p_init_C = p_init_C
        self.isSharing = isSharing
