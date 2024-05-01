# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "main: 2 messages, 0 services")

set(MSG_I_FLAGS "-Imain:/home/jetson/github/guoji_ws/src/main/msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(main_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg" NAME_WE)
add_custom_target(_main_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "main" "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg" ""
)

get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg" NAME_WE)
add_custom_target(_main_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "main" "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(main
  "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/main
)
_generate_msg_cpp(main
  "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/main
)

### Generating Services

### Generating Module File
_generate_module_cpp(main
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/main
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(main_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(main_generate_messages main_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg" NAME_WE)
add_dependencies(main_generate_messages_cpp _main_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg" NAME_WE)
add_dependencies(main_generate_messages_cpp _main_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(main_gencpp)
add_dependencies(main_gencpp main_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS main_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(main
  "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/main
)
_generate_msg_eus(main
  "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/main
)

### Generating Services

### Generating Module File
_generate_module_eus(main
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/main
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(main_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(main_generate_messages main_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg" NAME_WE)
add_dependencies(main_generate_messages_eus _main_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg" NAME_WE)
add_dependencies(main_generate_messages_eus _main_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(main_geneus)
add_dependencies(main_geneus main_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS main_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(main
  "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/main
)
_generate_msg_lisp(main
  "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/main
)

### Generating Services

### Generating Module File
_generate_module_lisp(main
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/main
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(main_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(main_generate_messages main_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg" NAME_WE)
add_dependencies(main_generate_messages_lisp _main_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg" NAME_WE)
add_dependencies(main_generate_messages_lisp _main_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(main_genlisp)
add_dependencies(main_genlisp main_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS main_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(main
  "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/main
)
_generate_msg_nodejs(main
  "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/main
)

### Generating Services

### Generating Module File
_generate_module_nodejs(main
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/main
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(main_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(main_generate_messages main_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg" NAME_WE)
add_dependencies(main_generate_messages_nodejs _main_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg" NAME_WE)
add_dependencies(main_generate_messages_nodejs _main_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(main_gennodejs)
add_dependencies(main_gennodejs main_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS main_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(main
  "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/main
)
_generate_msg_py(main
  "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/main
)

### Generating Services

### Generating Module File
_generate_module_py(main
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/main
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(main_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(main_generate_messages main_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_data.msg" NAME_WE)
add_dependencies(main_generate_messages_py _main_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jetson/github/guoji_ws/src/main/msg/Yolox_action.msg" NAME_WE)
add_dependencies(main_generate_messages_py _main_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(main_genpy)
add_dependencies(main_genpy main_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS main_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/main)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/main
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(main_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(main_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/main)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/main
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(main_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(main_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/main)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/main
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(main_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(main_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/main)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/main
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(main_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(main_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/main)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/main\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/main
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(main_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(main_generate_messages_py std_msgs_generate_messages_py)
endif()
