cmake_minimum_required(VERSION 3.5)

project(SERIALTest LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# specify where to look for the Qt5 package
set(CMAKE_PREFIX_PATH "C:\\Qt\\6.5.1\\mingw_64\\lib\\cmake")

find_package(Qt5 COMPONENTS Widgets Multimedia REQUIRED)

add_executable(SerialTest serialtest.cpp)

target_link_libraries(SERIALTest PRIVATE Qt5::Widgets Qt5::Multimedia)
