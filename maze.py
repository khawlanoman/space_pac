def move_ghosts(self, td) -> None:
    for ghost in self.ghosts:

        if ghost.state == Ghost_state.EATEN:
            ghost.x, ghost.y = ghost.my_corner
            ghost.state = Ghost_state.SCATTER
            continue

        ghost_x = round(ghost.x)
        ghost_y = round(ghost.y)

        center = (
            abs(ghost.x - ghost_x) < 0.1
            and abs(ghost.y - ghost_y) < 0.1
        )

        if center:

            if ghost.state == Ghost_state.SCATTER:
                target_x, target_y = self.check_ghost(ghost)

                best_distance = float('inf')
                best_direction = None
                opposite = Directions[
                    Opposite[ghost.direction.name].value
                ]

                for direction in Directions:
                    if direction == opposite:
                        continue

                    if not loader.can_move(
                        self.maze, ghost_x, ghost_y, direction
                    ):
                        continue

                    dx, dy = direction.value[:2]
                    next_x = ghost_x + dx
                    next_y = ghost_y + dy

                    distance = (
                        abs(target_x - next_x)
                        + abs(target_y - next_y)
                    )

                    if distance < best_distance:
                        best_distance = distance
                        best_direction = direction

                if best_direction is not None:
                    ghost.direction = best_direction

                elif loader.can_move(
                    self.maze, ghost_x, ghost_y, opposite
                ):
                    ghost.direction = opposite
                else:
                    continue

            elif ghost.state == Ghost_state.CHASE:
                grid = self.grid

                grid._entryx = ghost_x
                grid._entryy = ghost_y
                grid._exitx = round(self.player.x)
                grid._exity = round(self.player.y)

                grid._shortest_path = False
                grid._find_short_path()

                path = grid.shortest_path

                directions_map = {
                    'N': Directions.UP,
                    'S': Directions.DOWN,
                    'W': Directions.LEFT,
                    'E': Directions.RIGHT
                }

                if path:
                    direction = directions_map[path[0]]

                    if loader.can_move(
                        self.maze, ghost_x, ghost_y, direction
                    ):
                        ghost.direction = direction
                    else:
                        continue
                else:
                    continue

            elif ghost.state == Ghost_state.FRIGHTENED:
                continue

        dx, dy = ghost.direction.value[:2]

        target_x = ghost_x + dx
        target_y = ghost_y + dy

        distance = ghost.speed * td

        if dx > 0:
            ghost.x = min(ghost.x + distance, target_x)
        elif dx < 0:
            ghost.x = max(ghost.x - distance, target_x)

        if dy > 0:
            ghost.y = min(ghost.y + distance, target_y)
        elif dy < 0:
            ghost.y = max(ghost.y - distance, target_y)