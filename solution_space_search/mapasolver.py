class Node:
    def __init__(self, power, affected_pieces):
        self.power = power
        self.affected_pieces = affected_pieces

    power : int
    affected_pieces = []


class Graph:
    def __init__(self, nodes):
        self.nodes = nodes

    nodes = []
    solutions = []
    max_clicks, min_clicks = 0, 0
    real_max_clicks = 0
    map_states = 0

    def failed(self):
        for node in self.nodes:
            if node.power >= 6:
                return True
        return False

    def win_condition(self):
        for node in self.nodes:
            if node.power <= 3 or node.power >= 6:
                return False
        return True

    def update(self, node, damage):
        node.power += 2 * damage #damage is 1 or -1 to make it positive or negative
        for affected in node.affected_pieces:
            self.nodes[affected - 1].power += 1 * damage

    def DFS(self, depth, parent_index, solution):
        self.map_states += 1
        if depth > self.min_clicks and self.win_condition():
            self.solutions.append(solution.copy())
        # if depth > self.real_max_clicks:
        #     return
        for i in range(len(self.nodes)):
            if i < parent_index: continue #cut repetition
            if solution[i] == 2: continue
            self.update(self.nodes[i], 1)
            if not self.failed(): #cut failed branch
                solution[i] += 1
                self.DFS(depth + 1, i, solution)
                solution[i] -= 1
            self.update(self.nodes[i], -1)

    def find_min_max(self):
        minv = len(self.nodes[0].affected_pieces)
        maxv = minv
        for node in self.nodes:
            v = len(node.affected_pieces)
            if v < minv:
                minv = v
            elif v > maxv:
                maxv = v
        return minv, maxv

    def find_real_upper(self, max_heat):
        segregated_nodes = self.nodes.copy()
        segregated_nodes.sort(key=lambda x: len(x.affected_pieces))
        cur_heat = 0
        for node in segregated_nodes:
            for i in range(2): #2 clicks for each piece starting from the lowest
                # print(node.affected_pieces)
                cur_heat += 1 + len(node.affected_pieces) * 0.5
                if cur_heat > max_heat:
                    return
                self.real_max_clicks += 1

    def find_solutions(self):
        solution = [0] * len(self.nodes)
        minv, maxv = self.find_min_max()

        sum_of_power = 0
        for node in self.nodes:
            sum_of_power += node.power

        min_heat = len(self.nodes) * 2.0 - sum_of_power * 0.5
        max_heat = len(self.nodes) * 2.5 - sum_of_power * 0.5

        self.min_clicks = min_heat / (1 + maxv * 0.5)
        self.max_clicks = max_heat / (1 + minv * 0.5)
        print(self.min_clicks)
        print(self.max_clicks)

        self.find_real_upper(max_heat)
        print(self.real_max_clicks)

        self.DFS(1, 0, solution)

        return self.solutions



def main():
    '''
    nodes = [Node(0, [10]),
          Node(0, [3,10,11]),
          Node(0, [2,4,11]),
          Node(0, [3,5,6,11,12]),
          Node(0, [4,6,12,13,14]),
          Node(0, [4,5,7,14]),
          Node(0, [6,8,14]),
          Node(0, [7,9,14]),
          Node(0, [8,10,14,15,16]),
          Node(0, [1,2,9,11,16]),
          Node(0, [2,3,4,10,12,16]),
          Node(0, [4,5,11,13,15,16]),
          Node(0,[5,12,15]),
          Node(0, [6,7,8,9,15]),
          Node(0, [9,12,13,14,16]),
          Node(0, [9,10,11,12,15])]
    nodes = [Node(2, []), #2,3,5,6,7
          Node(2, [1,3,8,12]),
          Node(3, [2,5,4,12,11,1]),
          Node(2, [3,5,6,11]),
          Node(2, [3,4,6,1]),
          Node(2, [4,5,7,9,1,15]),
          Node(2, [6,8,1,15]),
          Node(2, [2,7,16]),
          Node(2, [6,15]),
          Node(2, []),
          Node(2, [3,4,13]),
          Node(2, [2,3,14]),
          Node(2, [11,14]),
          Node(2,[13,12]),
          Node(2, [6,7,9,16]),
          Node(2, [8,15])]
    '''
    nodes = [Node(0, []),
             Node(0, [7, 8, 3]),
             Node(0, [5, 1, 1]),
             Node(0, [1, 2, 5, 6, 7, 8]),
             Node(0, [2, 3, 4, 7]),
             Node(0, [2, 4, 8]),
             Node(0, [4, 5]),
             Node(0, [1, 4, 6])]

    graph = Graph(nodes)
    solutions = graph.find_solutions()
    print(*solutions, sep='\n')
    print(len(solutions))
    print(graph.map_states)

if __name__ == "__main__":
    main()