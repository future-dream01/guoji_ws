# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/jetson/github/guoji_ws/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/jetson/github/guoji_ws/build

# Utility rule file for main_geneus.

# Include any custom commands dependencies for this target.
include main/CMakeFiles/main_geneus.dir/compiler_depend.make

# Include the progress variables for this target.
include main/CMakeFiles/main_geneus.dir/progress.make

main_geneus: main/CMakeFiles/main_geneus.dir/build.make
.PHONY : main_geneus

# Rule to build all files generated by this target.
main/CMakeFiles/main_geneus.dir/build: main_geneus
.PHONY : main/CMakeFiles/main_geneus.dir/build

main/CMakeFiles/main_geneus.dir/clean:
	cd /home/jetson/github/guoji_ws/build/main && $(CMAKE_COMMAND) -P CMakeFiles/main_geneus.dir/cmake_clean.cmake
.PHONY : main/CMakeFiles/main_geneus.dir/clean

main/CMakeFiles/main_geneus.dir/depend:
	cd /home/jetson/github/guoji_ws/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jetson/github/guoji_ws/src /home/jetson/github/guoji_ws/src/main /home/jetson/github/guoji_ws/build /home/jetson/github/guoji_ws/build/main /home/jetson/github/guoji_ws/build/main/CMakeFiles/main_geneus.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : main/CMakeFiles/main_geneus.dir/depend

