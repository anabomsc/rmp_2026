import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
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

    declare_autostart = DeclareLaunchArgument(
        'autostart',
        default_value='true',
        description='Autostart nav2 lifecycle manager if true'
    )
    autostart = LaunchConfiguration('autostart', default='true')
    ld.add_action(declare_autostart)

    lifecycle_nodes = ['map_server', 'amcl']

    # Setup project paths
    pkg_project = get_package_share_directory('rmp_2026')
    map_file = '/home/anaomscosta/maps_and_bags/ambiente_0_save.yaml'

    # Setup for namespaces and frames
    namespace = "/artbot"

    # Nav2 AMCL Localization
    nav2_params_file = os.path.join(pkg_project,'config','nav2_params.yaml')
    start_map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[
            nav2_params_file,
            {'yaml_filename': map_file, 'use_sim_time': use_sim_time}
        ]
    )

    start_amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[
            nav2_params_file,
            {'yaml_filename': map_file, 'use_sim_time': use_sim_time}
        ]
    )
    
    start_map_node_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'autostart': autostart},
            {'node_names': lifecycle_nodes}
        ]
    )

    ld.add_action(start_map_server)
    ld.add_action(start_amcl)
    ld.add_action(start_map_node_manager)

    # Launch!
    return ld