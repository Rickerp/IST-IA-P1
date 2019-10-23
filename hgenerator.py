def hGenerator(graph):
    f = open("h.txt", "w")
    f.write("[")
    for i in range(1, 114):
        distances = dijkstra(graph, i)
        f.write("[")
        for minimum_cost in distances:
            f.write(str(minimum_cost) + ", ")
        f.write("], ")
    f.write("]")
    f.close()


def dijkstra(graph, source):
    dist = list()
    # previous = list()
    queue = list()
    for i in range(1, 114):
        dist.append(200)
        queue.append(i)

    dist[source] = 0
    while queue:
        i = 0
        j = 0
        node_with_minimum_d = queue[0]
        for node in queue:
            if dist[node] < dist[node_with_minimum_d]:
                node_with_minimum_d = node
                j = i
            i += 1
        queue.pop(j)

        for neighbor in graph[node_with_minimum_d]:
            new_distance = dist[node_with_minimum_d] + 1
            if new_distance < dist[neighbor[1]]:
                dist[neighbor[1]] = new_distance

    return dist
