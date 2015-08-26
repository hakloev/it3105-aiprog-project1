import heapq

from datastructures import *

class AStar(object):

    def __init__(self, board=None, start_node=None, goal_node=None):
        self.board = board
        self.start_node = start_node
        self.goal_node = goal_node
        self.openset = []
        heapq.heapify(self.openset)
        self.closedset = set()


    def agenda_loop(self):
        heapq.heappush(self.openset, (self.start_node.f, self.start_node))

        while len(self.openset):
            node = heapq.heappop(self.openset)[1]
            self.closedset.add(node)
            
            if node == self.goal_node:
                print('Done, reached goal node')
                print('--- PATH ---')
                while (node.parent != None):
                    print(node)
                    node = node.parent
                break
            
            successors = self.board.get_all_successor_nodes(node) 
            
            for successor in successors:
                node.children.add(successor)
                if (successor not in self.closedset) and (successor not in self.openset):
                    self.board.attach_and_eval(successor, node)
                    heapq.heappush(self.openset, (successor.f, successor))
                elif (node.g + node.arc_cost < successor.g):
                    self.board.attach_and_eval(successor, node)
                    if (successor in self.closedset):
                        print('in closed, prop path')
                        self.board.propagate_path(node)

    
if __name__ == '__main__':
    board = Board()
    a = AStar(board, board.get_start_node(), board.get_goal_node())
    a.agenda_loop()
