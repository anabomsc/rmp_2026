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
    pkg_nav2 = get_package_share_directory('nav2_bringup')

    # Setup robot simulation
    start_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_project, 'launch', 'sim_coord_robot.launch.py')),
    )
    ld.add_action(start_sim)

    # SLAM Toolbox Localization
    slam_params_file = os.path.join(pkg_project,'config','mapper_params_online_async.yaml')
    serial_map_file = '/home/anaomscosta/maps_and_bags/ambiente_0_serial'
    start_async_slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
          slam_params_file,
          {'map_frame': 'map'},
          {'mode': 'localization'},
          {'map_file_name': serial_map_file},
          {'map_start_at_dock': True},
          {'use_sim_time': use_sim_time}
        ],
    )
    ld.add_action(start_async_slam_toolbox_node)

    # Nav2 Navigation
    nav2_params_file = os.path.join(pkg_project, 'config', 'nav2_params.yaml')
    start_navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2, 'launch', 'navigation_launch.py')),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': nav2_params_file,
        }.items(),
    )
    ld.add_action(start_navigation)

    # Twist Mux
    twist_mux_params_file = os.path.join(pkg_project, 'config', 'twist_mux.yaml')
    start_twist_mux = Node(
            package="twist_mux",
            executable="twist_mux",
            parameters=[
                twist_mux_params_file,
                {'use_sim_time': True}
            ],
            remappings=[('/cmd_vel_out','/artbot/cmd_vel')]
    )
    ld.add_action(start_twist_mux)
    
    # Launch!
    return ld