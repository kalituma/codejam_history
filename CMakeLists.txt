cmake_minimum_required(VERSION 3.16)
project(codejam_history)

set(CMAKE_CXX_STANDARD 17)

add_library(codejam_2017
        2017/round_q/oversizedpancakeflipper.cpp
        2017/round_q/tidynumbers.cpp
        2017/round_q/bathroomstalls.cpp
        2017/round_q/fasionshow.cpp
        2017/round_1a/alphabetcake.cpp
        2017/round_1a/ratatouille.cpp
        2017/round_1a/playthedragon.cpp
        2017/round_1b/cruisecontrol.cpp
        2017/round_1b/stableneighbors.cpp
        2017/round_1b/ponyexpress.cpp
        2017/round_1c/amplesyrup.cpp
        2017/round_1c/parentingpartnering.cpp
        2017/round_1c/coretraining.cpp
        2017/round_2/freshchocolate.cpp
        2017/round_2/rollercoasterscheduling.cpp
        2017/round_2/beamingwithjoy.cpp
        2017/round_2/_shoottheturrets.cpp)
add_library(codejam_2018
        2018/round_q/saving_the_universe_again.cpp
        2018/round_q/trouble_sort.cpp
        2018/round_q/go_gopher.cpp
        2018/round_q/cubic_ufo.cpp
        )