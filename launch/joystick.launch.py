import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument

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

    declare_use_twist_mux = DeclareLaunchArgument(
        'use_twist_mux',
        default_value='false',
        description='Prepare for twist_mux use if true'
    )
    use_twist_mux = LaunchConfiguration('use_twist_mux', default='false')
    ld.add_action(declare_use_twist_mux)

    # Setup project paths
    pkg_project = get_package_share_directory('rmp_2026')

    # Setup namespaces
    namespace = "/artbot"

    # External joystick teleop setup
    joy_params = os.path.join(pkg_project,'config','joystick.yaml')

    joy_node = Node(
        package='joy',
        executable='joy_node',
        parameters=[joy_params, {'use_sim_time': use_sim_time}], #
    )
    ld.add_action(joy_node)

    cmd_vel_remap = PythonExpression([
        "'", namespace, "/cmd_vel_joy' if '", use_twist_mux, "' == 'true' else '", namespace, "/cmd_vel'"
    ])

    teleop_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_node',
        parameters=[joy_params, {'use_sim_time': use_sim_time}],
        remappings=[('/cmd_vel', cmd_vel_remap)]
    )
    ld.add_action(teleop_node)

    # Launch!
    return ld      