import agentpy as ap
import random
import numpy as np
from typing import Tuple
import CuboA
import Forklift
import PlanoCubos
import pygame


FRAMES_PER_STEP: int = 5
NUMBER_OF_DIRECTIONS: int = 4
NUMBER_OF_AGENTS: int = 5


class ForkliftRobotAgent(ap.Agent):
    def setup(self) -> None:
        self.prev_fork_height: int = 0
        self.fork_height: int = 0
        self.prev_direction: Tuple[int, int, int] = random.choice(
            [(1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
        )
        self.direction: Tuple[int, int, int] = self.prev_direction
        self.prev_position: Tuple[int, int] = (-1, -1, -1)
        self.position: Tuple[int, int] = (-1, -1, -1)
        while True:
            x: int = random.randint(0, self.model.warehouse_dimensions[0] - 1)
            y: int = 0
            z: int = random.randint(0, self.model.warehouse_dimensions[2] - 1)
            if (
                not self.model.is_in_storage_zone((x, y, z))
                and not self.model.ocupied_initial_positions[x, y, z]
            ):
                self.prev_position: Tuple[int, int] = (x, y, z)
                self.position: Tuple[int, int] = self.prev_position
                self.model.ocupied_initial_positions[x, y, z] = True
                break
        self.boxes_in_neighbor_positions: Tuple[int, int, int, int] = (0, 0, 0, 0)
        self.any_robot_in_neighbor_positions: Tuple[bool, bool, bool, bool] = (
            False,
            False,
            False,
            False,
        )
        self.any_wall_in_neighbor_positions: Tuple[bool, bool, bool, bool] = (
            False,
            False,
            False,
            False,
        )
        self.is_storage_zone_in_neighbor_positions: Tuple[bool, bool, bool, bool] = (
            False,
            False,
            False,
            False,
        )
        self.in_loading_position: bool = False
        self.is_loaded: bool = False
        self.g_forklift: Forklift.Forklift = Forklift.Forklift()
        self.g_forklift.draw(
            self.position, self.direction, self.fork_height, self.is_loaded
        )

    def relative_position(self, direction_index: int) -> Tuple[int, int, int]:
        relative_directions = [
            (self.direction[0], self.direction[1], self.direction[2]),  # Front
            (-self.direction[2], self.direction[1], self.direction[0]),  # Left
            (-self.direction[0], self.direction[1], -self.direction[2]),  # Back
            (self.direction[2], self.direction[1], -self.direction[0]),  # Right
        ]
        delta = relative_directions[direction_index]
        return (
            self.position[0] + delta[0],
            self.position[1] + delta[1],
            self.position[2] + delta[2],
        )

    def boxes_in_direction(self, direction_index: int) -> int:
        x, y, z = self.relative_position(direction_index)
        if (
            0 <= x < self.model.warehouse_dimensions[0]
            and 0 <= y < self.model.warehouse_dimensions[1]
            and 0 <= z < self.model.warehouse_dimensions[2]
        ):
            return self.model.warehouse[x, y, z]
        return 0

    def any_robot_in_direction(self, direction_index: int) -> bool:
        x, y, z = self.relative_position(direction_index)
        for agent in self.model.agents:
            if agent.position == (x, y, z):
                return True
        return False

    def any_wall_in_direction(self, direction_index: int) -> bool:
        x, y, z = self.relative_position(direction_index)
        return (
            x < 0
            or x >= self.model.warehouse_dimensions[0]
            or y < 0
            or y >= self.model.warehouse_dimensions[1]
            or z < 0
            or z >= self.model.warehouse_dimensions[2]
            or self.model.is_in_storage_zone((x, y, z))
        )

    def is_storage_zone_in_position(self, direction_index: int) -> bool:
        x, y, z = self.relative_position(direction_index)
        return self.model.is_in_storage_zone((x, y, z))

    def see(self) -> None:
        self.boxes_in_neighbor_positions = tuple(
            self.boxes_in_direction(i) for i in range(NUMBER_OF_DIRECTIONS)
        )
        self.any_robot_in_neighbor_positions = tuple(
            self.any_robot_in_direction(i) for i in range(NUMBER_OF_DIRECTIONS)
        )
        self.any_wall_in_neighbor_positions = tuple(
            self.any_wall_in_direction(i) for i in range(NUMBER_OF_DIRECTIONS)
        )
        self.is_storage_zone_in_neighbor_positions = tuple(
            self.is_storage_zone_in_position(i) for i in range(NUMBER_OF_DIRECTIONS)
        )

    def next(self) -> None:
        self.prev_position = self.position
        self.prev_direction = self.direction
        self.prev_fork_height = self.fork_height
        if (
            self.fork_height % 6 != 0
            and not self.is_loaded
            and not self.in_loading_position
        ):
            return "reset_fork"
        if not self.is_loaded:
            if (
                self.boxes_in_neighbor_positions[0] > 0
                and not self.any_wall_in_neighbor_positions[0]
            ):
                if self.fork_height % 6 == 0:
                    self.in_loading_position = True
                    return "prepare_fork_to_load"
                self.is_loaded = True
                return "load"
            if (self.boxes_in_neighbor_positions[3] > 0) and not (
                self.any_wall_in_neighbor_positions[3]
            ):
                return "turnright"
            for i in range(1, 3):
                if (
                    self.boxes_in_neighbor_positions[i] > 0
                    and not self.any_wall_in_neighbor_positions[i]
                ):
                    return "turnleft"
        else:
            if self.in_loading_position:
                self.in_loading_position = False
                return "lift_fork"
            if (
                self.is_storage_zone_in_neighbor_positions[0]
                and self.boxes_in_neighbor_positions[0] < 5
            ):
                if self.fork_height % 6 == 0:
                    return "prepare_fork_to_unload"
                self.is_loaded = False
                return "unload"
            if (
                self.is_storage_zone_in_neighbor_positions[3]
                and self.boxes_in_neighbor_positions[3] < 5
            ):
                return "turnright"
            for i in range(1, 3):
                if (
                    self.is_storage_zone_in_neighbor_positions[i]
                    and self.boxes_in_neighbor_positions[i] < 5
                ):
                    return "turnleft"
        if random.random() < 0.75:
            if (
                not self.any_wall_in_neighbor_positions[0]
                and not self.any_robot_in_neighbor_positions[0]
                and self.boxes_in_neighbor_positions[0] == 0
            ):
                return "move"
        if random.random() < 0.5:
            return "turnleft"
        return "turnright"

    def action(self, command: str) -> None:
        if command == "prepare_fork_to_load":
            self.fork_height = -1
        if command == "load":
            self.model.warehouse[self.relative_position(0)] -= 1
        if command == "lift_fork":
            self.fork_height = 6
        elif command == "prepare_fork_to_unload":
            self.fork_height = 6 * self.boxes_in_neighbor_positions[0] - 1
        elif command == "unload":
            self.model.warehouse[self.relative_position(0)] += 1
            self.model.remaining_boxes_to_sort -= 1
        elif command == "reset_fork":
            self.fork_height = 0
        elif command == "move":
            self.position = self.relative_position(0)
        elif command == "turnleft":
            self.prev_direction = self.direction
            self.direction = (
                -self.direction[2],
                self.direction[1],
                self.direction[0],
            )
        elif command == "turnright":
            self.prev_direction = self.direction
            self.direction = (
                self.direction[2],
                self.direction[1],
                -self.direction[0],
            )

    def update(self, interpolation_factor: float = 0.0) -> None:
        self.g_forklift.draw(
            (
                self.prev_position[0]
                + (self.position[0] - self.prev_position[0]) * interpolation_factor,
                self.prev_position[1]
                + (self.position[1] - self.prev_position[1]) * interpolation_factor,
                self.prev_position[2]
                + (self.position[2] - self.prev_position[2]) * interpolation_factor,
            ),
            (
                self.prev_direction[0]
                + (self.direction[0] - self.prev_direction[0]) * interpolation_factor,
                self.prev_direction[1]
                + (self.direction[1] - self.prev_direction[1]) * interpolation_factor,
                self.prev_direction[2]
                + (self.direction[2] - self.prev_direction[2]) * interpolation_factor,
            ),
            self.prev_fork_height
            + (self.fork_height - self.prev_fork_height) * interpolation_factor,
            self.is_loaded,
        )

    def step(self) -> None:
        self.see()
        self.action(self.next())


class WarehouseOrganizingRobotsModel(ap.Model):
    def is_in_storage_zone(self, position: Tuple[int, int, int]) -> bool:
        x, y, z = position
        start_x: int = (
            self.warehouse_dimensions[0] - self.storage_zone_dimensions[0]
        ) // 2
        start_y: int = 0
        start_z: int = (
            self.warehouse_dimensions[2] - self.storage_zone_dimensions[2]
        ) // 2
        end_x: int = start_x + self.storage_zone_dimensions[0] - 1
        end_y: int = start_y + self.storage_zone_dimensions[1] - 1
        end_z: int = start_z + self.storage_zone_dimensions[2] - 1
        return start_x <= x <= end_x and start_y <= y <= end_y and start_z <= z <= end_z

    def setup(self) -> None:
        self.remaining_boxes_to_sort: int = self.p["K"]
        self.warehouse_dimensions: Tuple[int, int, int] = (
            self.p["N_OVER_8"] * 8,
            1,
            self.p["M_OVER_8"] * 8,
        )
        self.storage_zone_dimensions: Tuple[int, int, int] = (
            self.warehouse_dimensions[0] // 4,
            1,
            self.warehouse_dimensions[2] // 4,
        )
        PlanoCubos.Init(self.warehouse_dimensions, self.storage_zone_dimensions)
        self.ocupied_initial_positions: np.ndarray = np.zeros(
            self.warehouse_dimensions, dtype=bool
        )
        self.warehouse: np.ndarray = np.zeros(self.warehouse_dimensions, dtype=int)
        for _ in range(self.p["K"]):
            while True:
                x: int = random.randint(0, self.warehouse_dimensions[0] - 1)
                y: int = 0
                z: int = random.randint(0, self.warehouse_dimensions[2] - 1)
                if (
                    not self.is_in_storage_zone((x, y, z))
                    and not self.ocupied_initial_positions[x, y, z]
                ):
                    self.warehouse[x, y, z] = 1
                    self.ocupied_initial_positions[x, y, z] = True
                    break
        self.agents: ap.AgentList = ap.AgentList(
            self, NUMBER_OF_AGENTS, ForkliftRobotAgent
        )

    def step(self) -> None:
        self.agents.step()
        if self.remaining_boxes_to_sort == 0:
            self.stop()

    def update(self) -> None:
        for i in range(FRAMES_PER_STEP):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    global done
                    done = True
                    self.stop()
            PlanoCubos.display(self.warehouse_dimensions, self.storage_zone_dimensions)
            self.agents.update(i / FRAMES_PER_STEP)
            for x in range(self.warehouse_dimensions[0]):
                for y in range(self.warehouse_dimensions[1]):
                    for z in range(self.warehouse_dimensions[2]):
                        for i in range(self.warehouse[x, y, z]):
                            CuboA.CuboA().draw((x, y + i, z), (1 / 6, 1 / 6, 1 / 6))

            pygame.display.flip()
            pygame.time.wait(1)

    def end(self) -> None:
        self.report("steps", self.t)


parameters: dict = {
    "N_OVER_8": 3,
    "M_OVER_8": 3,
    "K": 20,
}

done: bool = False
model = WarehouseOrganizingRobotsModel(parameters)
model.run()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
pygame.quit()
