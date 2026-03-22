from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    AppendEnvironmentVariable,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
import os
import xacro
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    share_dir = get_package_share_directory("autonomous_drive")

    set_env_vars = AppendEnvironmentVariable(
        "IGN_GAZEBO_RESOURCE_PATH", os.path.join(share_dir, "meshes")
    )

    set_model_path = AppendEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH", os.path.join(share_dir, "meshes")
    )

    xacro_file = os.path.join(share_dir, "urdf", "diff_drive.xacro")
    robot_description_config = xacro.process_file(xacro_file)
    robot_urdf = robot_description_config.toxml()

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[{"robot_description": robot_urdf}, {"use_sim_time": True}],
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        parameters=[{"use_sim_time": True}],
    )

    # Ignition Gazebo server launch
    ignition_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]
                )
            ]
        ),
        launch_arguments={
            "gz_args": ["-r -s ", os.path.join(share_dir, "worlds", "cone_world.sdf")],
            "on_exit_shutdown": "true",
        }.items(),
    )

    # Ignition Gazebo client launch
    ignition_gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]
                )
            ]
        ),
        launch_arguments={"gz_args": "-g "}.items(),
    )

    urdf_spawn_node = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-name", "diff_drive", "-topic", "robot_description"],
        output="screen",
    )

    joint_state_broadcaster_spawner = TimerAction(
        period=8.0,
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[
                    "joint_state_broadcaster",
                    "--controller-manager",
                    "/controller_manager",
                ],
                output="screen",
            )
        ],
    )

    diff_drive_spawner = TimerAction(
        period=10.0,
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[
                    "autonomous_drive_controller",
                    "--controller-manager",
                    "/controller_manager",
                ],
                output="screen",
            )
        ],
    )

    # Bridge from ROS2 to Gazebo
    bridge = TimerAction(
        period=5.0,
        actions=[
            Node(
                package="ros_gz_bridge",
                executable="parameter_bridge",
                name="bridge",
                parameters=[
                    {
                        "config_file": os.path.join(
                            share_dir, "config", "autonomous_drive_bridge.yaml"
                        ),
                        "use_sim_time": True,
                    }
                ],
                output="screen",
            )
        ],
    )

    cmd_vel_relay = TimerAction(
        period=12.0,
        actions=[
            Node(
                package="autonomous_drive",
                executable="cmd_vel_relay",
                name="cmd_vel_relay",
                output="screen",
            )
        ],
    )

    rtabmap = Node(
        package="rtabmap_slam",
        executable="rtabmap",
        name="rtabmap",
        output="screen",
        parameters=[
            {
                "use_sim_time": True,
                "subscribe_depth": True,
                "subscribe_rgb": True,
                "subscribe_scan": False,
                "frame_id": "base_link",
                "odom_frame_id": "odom",
                "map_frame_id": "map",
                "publish_tf_map": True,
                "approx_sync": True,
                "visual_odometry": False,
                "wait_for_transform": 0.5,
                "topic_queue_size": 10,
                "sync_queue_size": 10,
                "camera_frame_id": "camera_optical_link",
                # RTAB-Map parameters
                "RGBD/LinearUpdate": "0.05",
                "RGBD/AngularUpdate": "0.05",
                "RGBD/NeighborLinkRefining": "true",
                "RGBD/ProximityBySpace": "true",
                "RGBD/LoopClosureReextractFeatures": "true",
                "Grid/CellSize": "0.05",
                "Grid/RangeMax": "4.0",
                "Grid/RangeMin": "0.2",
                "Grid/Sensor": "1",
                "Mem/STMSize": "30",
                "Vis/MinInliers": "5",
                "Kp/MaxFeatures": "400",
                "Kp/DetectorStrategy": "6",
            }
        ],
        remappings=[
            ("rgb/image", "/camera/color/image_raw"),
            ("depth/image", "/camera/depth/image_raw"),
            ("rgb/camera_info", "/camera/color/camera_info"),
            ("odom", "/odom"),
        ],
        arguments=['--delete_db_on_start'],
        namespace="rtabmap",
    )

    return LaunchDescription(
        [
            set_env_vars,
            set_model_path,
            robot_state_publisher_node,
            joint_state_publisher_node,
            ignition_gazebo_server,
            ignition_gazebo_client,
            urdf_spawn_node,
            bridge,
            joint_state_broadcaster_spawner,
            diff_drive_spawner,
            cmd_vel_relay,
            rtabmap,
        ]
    )
