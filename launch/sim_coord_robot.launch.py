import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # Launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use sim time if true'
    )
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    ld.add_action(declare_use_sim_time)

    # Setup project paths
    pkg_project = get_package_share_directory('rmp_2026')

    # Setup gazebo simulation
    gz_simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_project, 'launch', 'world.launch.py')),
    )
    ld.add_action(gz_simulation)

    # Setup single robot spawn and details
    single_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_project, 'launch', 'robot_spawn.launch.py')),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )
    ld.add_action(single_robot)

    # Setup single robot teleop
    teleop = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_project, 'launch', 'joystick.launch.py')),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )
    ld.add_action(teleop)

    # Launch!
    return ld