# CMake generated Testfile for 
# Source directory: /root/ros_workspace/src/semantic_inference/semantic_inference_ros
# Build directory: /root/ros_workspace/build/semantic_inference_ros
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(semantic_inference_ros_test "/usr/bin/python3" "-u" "/opt/ros/jazzy/share/ament_cmake_test/cmake/run_test.py" "/root/ros_workspace/build/semantic_inference_ros/test_results/semantic_inference_ros/semantic_inference_ros_test.gtest.xml" "--package-name" "semantic_inference_ros" "--output-file" "/root/ros_workspace/build/semantic_inference_ros/ament_cmake_gtest/semantic_inference_ros_test.txt" "--command" "/root/ros_workspace/build/semantic_inference_ros/semantic_inference_ros_test" "--gtest_output=xml:/root/ros_workspace/build/semantic_inference_ros/test_results/semantic_inference_ros/semantic_inference_ros_test.gtest.xml")
set_tests_properties(semantic_inference_ros_test PROPERTIES  LABELS "gtest" REQUIRED_FILES "/root/ros_workspace/build/semantic_inference_ros/semantic_inference_ros_test" TIMEOUT "60" WORKING_DIRECTORY "/root/ros_workspace/build/semantic_inference_ros" _BACKTRACE_TRIPLES "/opt/ros/jazzy/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/jazzy/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;95;ament_add_test;/opt/ros/jazzy/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/root/ros_workspace/src/semantic_inference/semantic_inference_ros/CMakeLists.txt;102;ament_add_gtest;/root/ros_workspace/src/semantic_inference/semantic_inference_ros/CMakeLists.txt;0;")
subdirs("gtest")
