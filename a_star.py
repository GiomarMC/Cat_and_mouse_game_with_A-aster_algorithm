import heapq


def a_star(start, goal, grid):
    rows, cols = len(grid), len(grid[0])
    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
                new_cost = cost_so_far[current] + 1
                neighbor = (nx, ny)
                if (neighbor not in cost_so_far or
                        new_cost < cost_so_far[neighbor]):
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + abs(goal[0]-nx) + abs(goal[1]-ny)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

    # Reconstruir el camino
    path = []
    current = goal
    while current and current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
