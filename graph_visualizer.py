import pygame
import heapq

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Graph and marker positions
graph = {
    0: {1: 1},
    1: {0: 1, 2: 5, 3: 1},
    2: {1: 5, 3: 2, 4: 7},
    3: {1: 1, 2: 2, 4: 2},
    4: {2: 7, 3: 2},
}

marker_positions = {
    0: (100, 500),
    1: (200, 400),
    2: (300, 300),
    3: (500, 400),
    4: (600, 300),
}

class GraphVisualizer:
    def __init__(self, screen_size=(800, 600)):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Aruco Marker Shortest Path Finder")
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.shortest_path = []
        self.source = None
        self.destination = None

    def dijkstra(self, graph, start, end):
        queue = [(0, start, [])]  # (cost, node, path)
        visited = set()
        while queue:
            (cost, node, path) = heapq.heappop(queue)
            if node in visited:
                continue
            path = path + [node]
            visited.add(node)
            if node == end:
                return cost, path

            for neighbor, weight in graph[node].items():
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path))
        return float("inf"), []

    def draw_graph(self):
        self.screen.fill(WHITE)

        # Draw edges
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                pygame.draw.line(self.screen, BLACK, marker_positions[node], marker_positions[neighbor], 2)
                mid_x = (marker_positions[node][0] + marker_positions[neighbor][0]) // 2
                mid_y = (marker_positions[node][1] + marker_positions[neighbor][1]) // 2
                label = self.font.render(str(weight), True, BLACK)
                self.screen.blit(label, (mid_x, mid_y))

        # Draw nodes
        for marker_id, pos in marker_positions.items():
            pygame.draw.circle(self.screen, BLUE, pos, 20)
            label = self.font.render(f"id{marker_id}", True, WHITE)
            self.screen.blit(label, (pos[0] - 20, pos[1] - 20))

    def draw_path(self, path):
        """Draws the path between nodes in green"""
        if path:
            for i in range(len(path) - 1):
                start_pos = marker_positions[path[i]]
                end_pos = marker_positions[path[i + 1]]
                pygame.draw.line(self.screen, GREEN, start_pos, end_pos, 4)

    def visualize(self):
        self.draw_graph()  # Display the graph initially with all connections in black
        pygame.display.flip()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Get source and destination input from user
            if self.source is None:
                try:
                    self.source = int(input("Enter source node (0-4): "))
                except ValueError:
                    pass
            elif self.destination is None:
                try:
                    self.destination = int(input("Enter destination node (0-4): "))
                except ValueError:
                    pass
            else:
                # Compute and draw the shortest path
                cost, self.shortest_path = self.dijkstra(graph, self.source, self.destination)
                print(f"Shortest path: {self.shortest_path} with total cost: {cost}")
                self.draw_graph()  # Redraw the base graph
                self.draw_path(self.shortest_path)  # Highlight the shortest path
                pygame.display.update()  # Update the display with the new path

                # Reset source and destination for next input
                self.source = None
                self.destination = None

        pygame.quit()

