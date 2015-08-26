
class Board(object):

    def __init__(self):
        self.grid_data = self.init_grid_from_file()
        self.make_grid_from_data(self.grid_data)

    def init_grid_from_file(self):
        grid_data = None
        with open('./boards/%s' % ('board1.txt'), 'r') as f:
            grid_data = list()
            for line in f.readlines():
                grid_data.append([tuple(int(i) for i in el.strip('()').split(',')) for el in line.rstrip().split(')(')])
        return grid_data

    def make_grid_from_data(self, data):
        grid_size = data[0][0]
        grid = [[Node(x=x, y=y, cost=0) for x in range(grid_size[1])] for y in range(grid_size[1])]
        
        grid[data[1][0][1]][data[1][0][0]].start = True
        grid[data[1][1][1]][data[1][1][0]].goal = True
        
        for obstacle in data[2:]:
            obstacle = obstacle[0]
            for y in range(obstacle[3]):
                for x in range(obstacle[2]):
                    grid[obstacle[1] + y][obstacle[0] + x].cost = float('Inf')

        #for row in reversed(grid):
        #    print(row) 

class Node(object):

    def __init__(self, x=None, y=None, cost=None, parent=None):
        self.x = x
        self.y = y
        self.cost = cost
        self.start = 0
        self.goal = 0
        self.parent = parent
    
    def __repr__(self):
        return 'Node((%s, %s), s=%s, g=%s, c=%s)' % (self.x, self.y, self.start, self.goal, self.cost)

if __name__ == '__main__':
    board = Board()

