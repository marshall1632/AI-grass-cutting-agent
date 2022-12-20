import random


class Environment:

    def __init__(self, filename):
        self.grid2D = []
        self.filename = filename
        self.initializeGrid()

    def initializeGrid(self):
        try:
            with open(self.filename) as file:
                rows = int(file.readline())
                cols = int(file.readline())
                for i in range(rows):
                    row = file.readline().strip()
                    col = []
                    for j in range(len(row)):
                        col.append(row[j])
                    self.grid2D.append(col)
        except FileNotFoundError:
            print("File doesn't exist")

    def showEnvironment(self):
        for rows in range(len(self.grid2D)):
            for cols in range(len(self.grid2D[0])):
                print(self.grid2D[rows][cols], end=' ')
            print()
