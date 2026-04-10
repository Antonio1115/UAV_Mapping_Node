# UAV Occupancy Grid Mapping

This ROS 2 package builds and publishes a 2D occupancy grid map for navigation.
The node consumes obstacle inputs and publishes a map topic for downstream nodes
such as path planning.

## Current Interface

- Subscribes: `/obstacles` (`geometry_msgs/PoseArray`)
- Publishes: `/map` (`nav_msgs/OccupancyGrid`)

Obstacle mapping convention from `PoseArray`:

- `pose.position.x` -> obstacle x (meters, world/map frame)
- `pose.position.y` -> obstacle y (meters, world/map frame)
- `pose.position.z` -> optional obstacle radius (meters, `0.0` if unused)

## Occupancy Encoding

- `-1` unknown
- `0` free
- `100` occupied

## Project Structure

```
uav-mapping/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
│   └── uav_mapping
├── uav_mapping/
│   ├── __init__.py
│   ├── uav_mapping.py
│   └── occupancy_grid.py
├── test/
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
└── README.md
```

## Build And Run

Run from your ROS 2 workspace root (for example `~/SMU-Drone-Club/uav_nodes`):

```bash
source /opt/ros/<your_distro>/setup.bash
colcon build --packages-select uav_mapping
source install/setup.bash
ros2 run uav_mapping uav_mapping_node
```

## Quick Topic Test

In one terminal, run the node. In a second terminal, publish test obstacles:

```bash
ros2 topic pub /obstacles geometry_msgs/msg/PoseArray \
"{poses: [{position: {x: 1.0, y: 1.5, z: 0.3}}, {position: {x: -1.2, y: 0.4, z: 0.0}}]}" -r 2
```

Then verify map output:

```bash
ros2 topic echo /map
```
