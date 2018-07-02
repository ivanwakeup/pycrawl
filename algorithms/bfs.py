graph = {'A': ['B', 'C'],
         'B': ['A', 'D', 'E'],
         'C': ['A', 'F'],
         'D': ['B'],
         'E': ['B', 'F'],
         'F': ['C', 'E']}


def bfs(graph, start_node):
    visited = [start_node]
    hit_order = []
    queue = [start_node]
    while queue:
        node = queue.pop(0)
        hit_order.append(node)
        neighbors = graph[node]
        for i in neighbors:
            if i not in visited:
                queue.append(i)
                visited.append(i)
    return hit_order


print(bfs(graph, 'B'))