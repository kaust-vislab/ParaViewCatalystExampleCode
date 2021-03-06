cmake_minimum_required(VERSION 2.8.8)
project(CatalystCxxFullExample)

set(USE_CATALYST ON CACHE BOOL "Link the simulator with Catalyst")
if(USE_CATALYST)
  find_package(ParaView 4.1 REQUIRED COMPONENTS vtkPVPythonCatalyst)
  include("${PARAVIEW_USE_FILE}")
  set(Adaptor_SRCS
    FEAdaptor.cxx
    )
  add_library(CxxFullExampleAdaptor ${Adaptor_SRCS})
  target_link_libraries(CxxFullExampleAdaptor vtkPVPythonCatalyst vtkParallelMPI)
  add_definitions("-DUSE_CATALYST")
  if(NOT PARAVIEW_USE_MPI)
    message(SEND_ERROR "ParaView must be built with MPI enabled")
  endif()
else()
  find_package(MPI REQUIRED)
  include_directories(${MPI_C_INCLUDE_PATH})
endif()

add_executable(CxxFullExample FEDriver.cxx FEDataStructures.cxx)
if(USE_CATALYST)
  target_link_libraries(CxxFullExample LINK_PRIVATE CxxFullExampleAdaptor)
  include(vtkModuleMacros)
  include(vtkMPI)
  vtk_mpi_link(CxxFullExample)
else()
  target_link_libraries(CxxFullExample LINK_PRIVATE ${MPI_LIBRARIES})
endif()

option(BUILD_TESTING "Build Testing" OFF)
# Setup testing.
if (BUILD_TESTING)
  include(CTest)
  add_test(CxxFullExampleTest CxxFullExample ${CMAKE_CURRENT_SOURCE_DIR}/SampleScripts/feslicescript.py)
  add_test(CxxFullExampleCinemaTest CxxFullExample ${CMAKE_CURRENT_SOURCE_DIR}/SampleScripts/feslicecinema.py)
endif()
