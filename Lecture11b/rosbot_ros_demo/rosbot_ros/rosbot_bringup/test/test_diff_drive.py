# Copyright 2021 Open Source Robotics Foundation, Inc.
# Copyright 2023 Intel Corporation. All Rights Reserved.
# Copyright 2024 Husarion sp. z o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import launch_pytest
import pytest
import rclpy
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from test_utils import BringupTestNode, readings_data_test


@launch_pytest.fixture
def generate_test_description():
    rosbot_bringup = FindPackageShare("rosbot_bringup")
    bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    rosbot_bringup,
                    "launch",
                    "bringup.launch.py",
                ]
            )
        ),
        launch_arguments={
            "healthcheck": "False",
            "use_sim": "False",
        }.items(),
    )

    return LaunchDescription([bringup_launch])


@pytest.mark.launch(fixture=generate_test_description)
def test_bringup_startup_success():
    rclpy.init()
    try:
        node = BringupTestNode("test_bringup")
        node.create_test_subscribers_and_publishers()
        node.start_publishing_fake_hardware()

        node.start_node_thread()
        readings_data_test(node)

    finally:
        rclpy.shutdown()
