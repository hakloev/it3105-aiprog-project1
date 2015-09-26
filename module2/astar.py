import heapq

from common import *
from astar_problem import AStarProblem


class AStar(object):    
    """
    A general A* algorithm class. Takes the mode and a problem instance as parameters
    :param mode: The mode to run the A* algorithm in
    :param problem: The problem to run A* on
    """

    def __init__(self, mode='best', problem=None):
        """
        Initializing the A* object with the given parameters
        """
        if not isinstance(problem, AStarProblem):
            raise Exception("Problem must be an instance of AStarProblem")

        self.mode = mode
        self.problem = problem

        self.open_set = []
        self.closed_set = set()

        self.g_values = {}

        self.path = []
        self.parent_of = {}

        if self.mode == 'best':
            heapq.heapify(self.open_set)

        print('A* initiated with valid problem instance')

    def agenda_loop(self):
        """
        The implementation of the A* algorithm. This is the main loop for the algorithm
        """
        self.add_node((self.problem.heuristic(self.problem.get_start_node()), self.problem.get_start_node()))
        self.g_values[self.problem.get_start_node()] = 0

        while len(self.open_set):
            node = self.take_node()
            self.closed_set.add(node)

            if self.problem.heuristic(node) == 0:
                if DEBUG:
                    print('Reached goal node!')
                log('Reached the goal node for this problem instance')
                yield {
                    'open_set': self.open_set,
                    'closed_set': self.closed_set,
                    'path': self.get_path_from_node([node])
                }
                break

            successors = self.problem.get_all_successor_nodes(node)

            for successor in successors:
                #  node.children.add(successor)
                if (successor not in self.closed_set) and (successor not in self.open_set):
                    f_value = self.attach_and_eval(successor, node)
                    self.add_node((f_value, successor))
                elif self.g_values[node] + self.problem.arc_cost(node) < self.g_values[successor]:
                    f_value = self.attach_and_eval(successor, node)
                    if successor in self.closed_set:
                        debug('Reached closed node, propagating path')
                        self.propagate_path(node)

            # Yields the current open- and closed set to the function that called the agenda_loop
            yield {
                'open_set': self.open_set,
                'closed_set': self.closed_set,
                'path': self.get_path_from_node([node])
            }

    def attach_and_eval(self, successor, node):
        self.parent_of[successor] = node
        self.g_values[successor] = self.g_values[node] + self.problem.arc_cost(node)
        #  successor.h = self.problem.heuristic(successor)
        #  successor.f = self.g_values[successor] + self.problem.heuristic(successor)
        return self.g_values[successor] + self.problem.heuristic(successor)

    def propagate_path(self, node):
        for child in node.children:
            if node.g + node.arc_cost < child.g:
                self.parent_of[child] = node
                self.g_values[child] = self.g_values[node] + self.problem.arc_cost[node]

                child.h = self.problem.heuristic(child)
                #child.f = child.g + child.h

                self.propagate_path(child)

    def add_node(self, node):
        """
        Method to add the node to the open set depending on the mode
        :param node: The node to append to the list
        """
        return {
            'best': lambda: heapq.heappush(self.open_set, node),  # Insert to ascending heap queue
            'bfs': lambda: self.open_set.append(node),  # Insert to back of queue (FIFO)
            'dfs': lambda: self.open_set.insert(0, node)  # Insert to front of queue (LIFO)
        }.get(self.mode)()

    def take_node(self):
        """
        Method to take the right node from the open set depending on the mode
        """
        return {
            'best': lambda: heapq.heappop(self.open_set)[1],  # Get first element in queue
            'bfs': lambda: self.open_set.pop(0),
            'dfs': lambda: self.open_set.pop(0)
        }.get(self.mode)()

    def backtrack_and_print_path_from_node(self, node):
        """
        This method backtracks the path from a given node, and prints the path
        It also prints the path length and total number of generated nodes
        :param node: The node to backtrack from
        """
        print('--- PATH IN REVERSE ---')
        path_length = 1  # Initiating as 1, because we do not count the goal node it self
        while node.parent:
            print(node)
            path_length += 1
            node = node.parent
        print('--- REACHED GOAL NODE (%d, %d) ---' % (path_length, (len(self.open_set) + len(self.closed_set))))

    def get_path_from_node(self, path):
        """
        This method returns a list containing a deepcopy of all node objects in the current path
        To be used with for instance the GUI visualisation
        :param node:
        :return:
        """
        while path[-1] != self.problem.get_start_node():
            path.append(self.parent_of[path[-1]])
        return path[::1]


    def get_path_length_from_goal_node(self):
        """
        Returns the total path length from the goal node
        :return: The length
        """
        path_length = 1  # Initiating as 1, because we do not count the goal node it self
        node = self.goal_node
        while node.parent:
            path_length += 1
            node = node.parent
        return path_length
