import pygame
import math
import heapq

# Initialize Pygame
pygame.init()

# Window setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Aruco Marker Shortest Path Finder")

# Graph structure (nodes, edges with weights)
graph = {
    0: {1: 1},
    1: {0: 1, 2: 5, 3: 1},
    2: {1: 5, 3: 2, 4: 7},
    3: {1: 1, 2: 2, 4: 2},
    4: {2: 7, 3: 2},
}

# Marker positions (for visual reference)
marker_positions = {
    0: (100, 500),
    1: (200, 400),
    2: (300, 300),
    3: (500, 400),
    4: (600, 300),
}

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Font setup
font = pygame.font.Font(None, 36)

def dijkstra(graph, start, end):
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

def draw_graph():
    screen.fill(WHITE)

    # Draw edges
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            pygame.draw.line(screen, BLACK, marker_positions[node], marker_positions[neighbor], 2)
            mid_x = (marker_positions[node][0] + marker_positions[neighbor][0]) // 2
            mid_y = (marker_positions[node][1] + marker_positions[neighbor][1]) // 2
            label = font.render(str(weight), True, BLACK)
            screen.blit(label, (mid_x, mid_y))

    # Draw nodes
    for marker_id, pos in marker_positions.items():
        pygame.draw.circle(screen, BLUE, pos, 20)
        label = font.render(f"id{marker_id}", True, WHITE)
        screen.blit(label, (pos[0] - 20, pos[1] - 20))

def draw_path(path):
    if path:
        for i in range(len(path) - 1):
            start_pos = marker_positions[path[i]]
            end_pos = marker_positions[path[i + 1]]
            pygame.draw.line(screen, GREEN, start_pos, end_pos, 4)

def main():
    running = True
    source = None
    destination = None
    shortest_path = []

    draw_graph()  # Display the graph with connections initially in black
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset the inputs
                    source = None
                    destination = None
                    shortest_path = []
                    draw_graph()  # Redraw graph in black when reset
                    pygame.display.flip()

            # Asking for input from the user
            if source is None:
                source_input = input("Enter source node (0-4): ")
                if source_input.isdigit():
                    source = int(source_input)
            elif destination is None:
                dest_input = input("Enter destination node (0-4): ")
                if dest_input.isdigit():
                    destination = int(dest_input)
                    cost, shortest_path = dijkstra(graph, source, destination)
                    print(f"Shortest path: {shortest_path} with total cost: {cost}")

                    # Redraw the graph and the shortest path in green
                    draw_graph()  # Redraw the graph with black connections
                    draw_path(shortest_path)  # Highlight the shortest path in green
                    pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

