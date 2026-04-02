#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from .occupancy_grid import OccupancyGridMap


class UavMappingNode(Node):
    """
    UAV Mapping Node for occupancy grid generation and management.
    Displays obstacles on the grid and handles ArUco marker tracking.
    """

    def __init__(self):
        super().__init__('uav_mapping_node')
        self.get_logger().info('UAV Mapping Node initialized')

    def run_mapping(self):
        """
        Execute the UAV mapping algorithm with test data.
        """
        self.get_logger().info('Starting UAV mapping...')

        grid = OccupancyGridMap(
            width_meters=8,
            height_meters=8,
            resolution=.2,
            inflation_meters=0.0
        )

        obstacles = [
            {"x": -1.0, "y": 1.2, "radius_m": 0.65},
            {"bbox": [-2.8, -1.6, -1.6, -0.2], "radius_m": 0.0},
            {"bbox": [1.0, 0.2, 2.2, 1.4], "radius_m": 0.0},
            {"x": 2.4, "y": -1.8, "radius_m": 0.45}
        ]
        grid.update_from_obstacles(obstacles)

        aruco_marker = {"x": -2.6, "y": 1.6, "size_m": 0.6, "yaw_rad": 0.0}
        grid.update_from_aruco_marker(aruco_marker)

        grid.visualize_grid()
        self.get_logger().info('Mapping complete. Grid visualization saved.')


def main(args=None):
    rclpy.init(args=args)

    node = UavMappingNode()
    node.run_mapping()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
