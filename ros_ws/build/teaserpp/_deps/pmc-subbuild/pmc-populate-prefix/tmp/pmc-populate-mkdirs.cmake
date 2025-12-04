# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/root/ros_workspace/build/teaserpp/_deps/pmc-src"
  "/root/ros_workspace/build/teaserpp/_deps/pmc-build"
  "/root/ros_workspace/build/teaserpp/_deps/pmc-subbuild/pmc-populate-prefix"
  "/root/ros_workspace/build/teaserpp/_deps/pmc-subbuild/pmc-populate-prefix/tmp"
  "/root/ros_workspace/build/teaserpp/_deps/pmc-subbuild/pmc-populate-prefix/src/pmc-populate-stamp"
  "/root/ros_workspace/build/teaserpp/_deps/pmc-subbuild/pmc-populate-prefix/src"
  "/root/ros_workspace/build/teaserpp/_deps/pmc-subbuild/pmc-populate-prefix/src/pmc-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/root/ros_workspace/build/teaserpp/_deps/pmc-subbuild/pmc-populate-prefix/src/pmc-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/root/ros_workspace/build/teaserpp/_deps/pmc-subbuild/pmc-populate-prefix/src/pmc-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
