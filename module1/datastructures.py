
class Board(object):

    def __init__(self):
        self.grid_data = self.init_grid_from_file()
        self.make_grid_from_data(self.grid_data)

    def init_grid_from_file(self):
        grid_data = list()
        with open('./boards/%s' % 'board1.txt', 'r') as f:
            for i, line in enumerate(f.readlines()):
                if i != 1:
                    grid_data.append(tuple(map(int, line.strip('()\n').split(','))))
                else:
                    grid_data.append([tuple(map(int, el.strip('()').split(','))) for el in line.rstrip().split(' ')])
        
        return grid_data

    def make_grid_from_data(self, data):
        grid_size = data[0]
        grid = [[Node(x=x, y=y, cost=0) for x in range(grid_size[0])] for y in range(grid_size[1])]
        
        trigger_points = data[1]
        grid[trigger_points[0][1]][trigger_points[0][0]].start = True
        grid[trigger_points[1][1]][trigger_points[1][0]].goal = True
        
        for obstacle in data[2:]:
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
        return ("Node((%s, %s), s=%s, g=%s, c=%s)" % (self.x, self.y, self.start, self.goal, self.cost)).ljust(31)

if __name__ == '__main__':
    board = Board()

