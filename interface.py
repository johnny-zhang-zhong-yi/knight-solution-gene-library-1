import random

#create a board with two dimension grid
def create_grid(dimension):
    return [[False for i in range(dimension)] #set all grids are false to represent the grids are empty
                for i in range(dimension)
            ]
#list all the possible choices
def check_area(x,y,grid):
    deltas = [
        (2, 1),
        (1, 2),
        (1, -2),
        (-2, 1),
        (-1, 2),
        (2, -1),
        (-1, -2),
        (-2, -1),
    ]
    valid = []
    for d in deltas:
        destination = (x + d[0], y + d[1])
        dx = destination[0] -1
        dy = destination[1] -1
        if 0 <= dx and dx < len(grid) and 0 <= dy and dy < len(grid): #check whether the choices are within the board size
            if grid[dx][dy] is False: #check whether the choices are empty
                valid.append(destination)
    if len(valid) == 0:
        return None
    else:
        return random.sample(valid, 1)[0]

#find a common point from two parents
def common_point(parent1, parent2):
    for i in range(1,len(parent1)):
        for j in range(1,len(parent2)):
            if parent1[i] == parent2[j]:
                child_gene = parent1[0:i] + parent2[j:len(parent2)]
                return child_gene
    return None

class IndividualGene:
    #for the initial position cho0se a random start position
    def __init__(self, configuration):
        self.configuration = configuration
        self.gene = [(configuration.start_row,configuration.start_col)] #the starting position of the knight
        self.fill_path() #create the path

    def fill_path(self):
        grid = create_grid(self.configuration.board_size) #create a board with two dimension grid
        for i in self.gene:
            grid[i[0] -1][i[1] -1] = True
        last_gene = self.gene[len(self.gene)-1]
        while True:
            last_gene = check_area(last_gene[0], last_gene[1],grid) #check and select a grid to move
            if last_gene is None:
                break
            self.gene.append(last_gene)
            grid[last_gene[0] -1][last_gene[1] -1] = True

#mutation is that the line will be maintained until a random postition and randomized on from this point onwards
    def mutate(self):
        splitter = random.randint(1,len(self.gene))
        self.gene = self.gene[0:splitter]
        self.fill_path()

#crossover is the product of the replication of one line until the first shared position and replication the second line
    #  from that moment on until the second shared number
    def crossover(self, other):
        parent1 = self.gene
        parent2 = other.gene
        child_gene = common_point(parent1, parent2)
        if child_gene is None:
            return self.mutate()
        grid = create_grid(self.configuration.board_size)
        last_gene = None
        for index, step in enumerate(child_gene):
            if grid[step[0] -1][step[1] -1] is False:
                grid[step[0] -1][step[1] -1] = True
            else:
                child_gene = child_gene[0:index]
                break
        self.fill_path()


#number of steps that follow the rule
    def fitness(self):
        return len(self.gene)

#sequence of steps
    def path(self):
        return self.gene


class Configuration:
    def __init__(self, board_size, start_row, start_col, generation_max):
        self.board_size = board_size
        self.start_row = start_row
        self.start_col = start_col
        self.generation_max = generation_max

