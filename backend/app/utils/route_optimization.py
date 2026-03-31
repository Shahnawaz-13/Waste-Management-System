import heapq
from collections import defaultdict


class CityGraph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_road(self, source: str, destination: str, distance: float):
        self.graph[source].append((destination, distance))
        self.graph[destination].append((source, distance))

    def shortest_path(self, start: str, end: str):
        queue = [(0, start, [])]
        visited = set()

        while queue:
            total_distance, node, path = heapq.heappop(queue)
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]
            if node == end:
                return {"distance": total_distance, "path": path}

            for neighbor, weight in self.graph[node]:
                if neighbor not in visited:
                    heapq.heappush(queue, (total_distance + weight, neighbor, path))

        return {"distance": None, "path": []}
