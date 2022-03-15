cmake_minimum_required(VERSION 3.21.4)
project(CppLib)

file(GLOB_RECURSE FILE_SOURCES RELATIVE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/src/Hello.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/Hello.cpp
)

# Solution Filters
foreach(source IN LISTS FILE_SOURCES)
    get_filename_component(source_path "${source}" PATH)
    string(REPLACE "/" "\\" source_path_msvc "${source_path}")
    string(REPLACE "src" "" source_path_final "${source_path_msvc}")
    source_group("${source_path_final}" FILES "${source}")
endforeach()

######### 3rdparty #########
include_directories(3rdparty)

add_library(${PROJECT_NAME} ${FILE_SOURCES})
target_include_directories(${PROJECT_NAME} PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/src/
    ${CMAKE_CURRENT_SOURCE_DIR}/3rdparty # 公开第三方库头文件
)

################################ 设置项目编译属性 #################################
# 设置项目属性
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/export/lib)

# 设置C++版本
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 17)
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD_REQUIRED ON)

# 设置C语言版本
set_property(TARGET ${PROJECT_NAME} PROPERTY C_STANDARD 99)
set_property(TARGET ${PROJECT_NAME} PROPERTY C_STANDARD_REQUIRED ON)

if(WIN32)
    # 关闭代码页警告
    add_definitions(-DUNICODE -D_UNICODE)
    set_target_properties(${PROJECT_NAME} PROPERTIES COMPILE_FLAGS "/wd4819")
endif()

## 3rdParty
set(3rdPartyDir ${CMAKE_CURRENT_SOURCE_DIR}/3rdparty)