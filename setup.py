from setuptools import find_packages, setup

package_name = 'uav_mapping'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='SMU Drone Club',
    maintainer_email='drone@smudrones.com',
    description='UAV Occupancy Grid Mapping for autonomous drone navigation',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "uav_mapping_node = uav_mapping.uav_mapping:main"
        ],
    },
)
