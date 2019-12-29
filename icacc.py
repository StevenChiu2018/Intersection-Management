#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2019 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @date    2009-03-26

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa


SimulationStepLength = 0.05
SimulationPeriod = 1800
SimulationEnding = 2000
SimulationDuration = SimulationEnding/SimulationStepLength
print("Duration of Simulation(steps): " + str(SimulationDuration))

def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = SimulationPeriod  # number of time steps
    # demand per second from different directions (probabilities)
    pWE = 1. / 10   # vehicles from west lane
    pWN = 1. / 12
    pWS = 1. / 30
    pEW = 1. / 12   # vehicles from east lane
    pEN = 1. / 16
    pES = 1. / 25
    pNE = 1. / 14   # vehicles from north lane
    pNW = 1. / 16
    pNS = 1. / 18
    pSE = 1. / 12   # vehicles from south lane
    pSN = 1. / 16
    pSW = 1. / 20
    with open("data/cross.rou.xml", "w") as routes:
        print("""<routes>""", file = routes)
        # vehicle configuration of simulation
        print("""
        <vType id="VehicleA" accel="3.5" decel="5.0" sigma="0" length="5" minGap="1.0" maxSpeed="15.0" speedFactor="1.0"
        guiShape="passenger" speedDev="0" />
        <vType id="VehicleB" accel="3.5" decel="5.0" sigma="0" length="5" minGap="1.0" maxSpeed="15.0" speedFactor="1.0"
        guiShape="passenger" speedDev="0" />
        """, file=routes)
        #speedFactor="1.0"   speedDev="0"
        # route configuration of simulation
        print("""
        <route id="route_WE" edges="L1 L2 L11 L12" />
        <route id="route_WN" edges="L1 L2 L15 L16" />
        <route id="route_WS" edges="L1 L2 L7 L8" />
        <route id="route_EW" edges="L9 L10 L3 L4" />
        <route id="route_EN" edges="L9 L10 L15 L16" />
        <route id="route_ES" edges="L9 L10 L7 L8" />
        <route id="route_NE" edges="L13 L14 L11 L12" />
        <route id="route_NW" edges="L13 L14 L3 L4" />
        <route id="route_NS" edges="L13 L14 L7 L8" />
        <route id="route_SE" edges="L5 L6 L11 L12" />
        <route id="route_SN" edges="L5 L6 L15 L16" />
        <route id="route_SW" edges="L5 L6 L3 L4" />
        """, file=routes)

        # generate vehicles randomly
        # vehNr = 0
        # for i in range(N):
        #     # vehicles dirving from west
        #     if random.uniform(0, 1) < pWE:
        #         print('    <vehicle id="vWE_%i" type="VehicleA" route="route_WE" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1
        #     if random.uniform(0, 1) < pWN:
        #         print('    <vehicle id="vWN_%i" type="VehicleA" route="route_WN" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1
        #     if random.uniform(0, 1) < pWS:
        #         print('    <vehicle id="vWS_%i" type="VehicleA" route="route_WS" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1

        #     # vehicles dirving from east
        #     if random.uniform(0, 1) < pEW:
        #         print('    <vehicle id="vEW_%i" type="VehicleA" route="route_EW" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1
        #     if random.uniform(0, 1) < pEN:
        #         print('    <vehicle id="vEN_%i" type="VehicleA" route="route_EN" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1
        #     if random.uniform(0, 1) < pES:
        #         print('    <vehicle id="vES_%i" type="VehicleA" route="route_ES" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1

        #     # vehicles dirving from south
        #     if random.uniform(0, 1) < pSE:
        #         print('    <vehicle id="vSE_%i" type="VehicleA" route="route_SE" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1
        #     if random.uniform(0, 1) < pSN:
        #         print('    <vehicle id="vSN_%i" type="VehicleA" route="route_SN" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1
        #     if random.uniform(0, 1) < pSW:
        #         print('    <vehicle id="vSW_%i" type="VehicleA" route="route_SW" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1

        #     # vehicles dirving from north
        #     if random.uniform(0, 1) < pNE:
        #         print('    <vehicle id="vNE_%i" type="VehicleA" route="route_NE" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1
        #     if random.uniform(0, 1) < pNS:
        #         print('    <vehicle id="vNS_%i" type="VehicleA" route="route_NS" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1
        #     if random.uniform(0, 1) < pNW:
        #         print('    <vehicle id="vNW_%i" type="VehicleA" route="route_NW" depart="%i" />' % (
        #             vehNr, i), file=routes)
        #         vehNr += 1
        print("</routes>", file=routes)
        
# The program looks like this
#    <tlLogic id="0" type="static" programID="0" offset="0">
# the locations of the tls are      NESW
#        <phase duration="31" state="GrGr"/>
#        <phase duration="6"  state="yryr"/>
#        <phase duration="31" state="rGrG"/>
#        <phase duration="6"  state="ryry"/>
#    </tlLogic>


def run():
    """execute the TraCI control loop"""
    random.seed(42)
    step = 0
    # we start with phase 2 where EW has green
    # traci.trafficlight.setPhase("0", 2)
    traci.vehicle.add("newVeh", "route_WN", typeID="VehicleA", departSpeed="15.0", departLane="2")
    traci.vehicle.setSpeedMode("newVeh", 0)
    # traci.vehicle.add("newVeh2", "route_WE", typeID="VehicleA", departSpeed="10.0", departLane="1")
    # traci.vehicle.setSpeedMode("newVeh2", 0)
    # traci.vehicle.add("newVeh3", "route_WS", typeID="VehicleA", departSpeed="10.0", departLane="0")
    # traci.vehicle.setSpeedMode("newVeh3", 0)
    # traci.vehicle.add("newVeh4", "route_WE", typeID="VehicleB", departSpeed="15.0", departLane="1", depart="2")
    # traci.vehicle.setSpeedMode("newVeh4", 0)
    while step < 1000:
        traci.simulationStep()
        # traci.vehicle.setSpeed("newVeh", 10.0)
        # traci.vehicle.setSpeedMode("newVeh", 0)
        # traci.vehicle.setSpeed("newVeh2", 10.0)
        # # traci.vehicle.setSpeedMode("newVeh2", 0)
        # traci.vehicle.setSpeed("newVeh3", 10.0)
        # # traci.vehicle.setSpeedMode("newVeh3", 0)
        # traci.vehicle.setSpeed("newVeh4", 15.0)
        # traci.vehicle.setSpeedMode("newVeh4", 0)
        # if step % 10 == 0:
        #     traci.vehicle.setSpeed("0", random.uniform(30, 50))
        step += 1
    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
