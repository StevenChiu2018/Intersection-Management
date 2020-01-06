import math
import random
# import sys

# simulation setting
SimulationStepLength = 0.1
StepPerSecond = math.ceil(1/SimulationStepLength)
MinimumGap = 1.0
VehicleLength = 5.0
LaneDistance = 150
FixedSpeed = 15.0


class Scheduler:

    # dictionary storing the last vehicle in each lane
    __Last_Vehicle_Arrival_Time = {}
    __Last_Vehicle_Arrival_Time["route_WN"] = 0.0
    __Last_Vehicle_Arrival_Time["route_WS"] = 0.0
    __Last_Vehicle_Arrival_Time["route_EW"] = 0.0
    __Last_Vehicle_Arrival_Time["route_WE"] = 0.0
    __Last_Vehicle_Arrival_Time["route_EN"] = 0.0
    __Last_Vehicle_Arrival_Time["route_ES"] = 0.0
    __Last_Vehicle_Arrival_Time["route_NE"] = 0.0
    __Last_Vehicle_Arrival_Time["route_NW"] = 0.0
    __Last_Vehicle_Arrival_Time["route_NS"] = 0.0
    __Last_Vehicle_Arrival_Time["route_SE"] = 0.0
    __Last_Vehicle_Arrival_Time["route_SN"] = 0.0
    __Last_Vehicle_Arrival_Time["route_SW"] = 0.0

    # nested dictionary storing occupied timestep for each conflict point
    __Conflict_Point = {}
    __Conflict_Point_temp = {}

    # conflict point of each lane tuple(index of point, period traveling from stop-line)
    __Lane_Conflict = {}
    __Lane_Conflict["route_WN"] = []
    __Lane_Conflict["route_WS"] = []    # none
    __Lane_Conflict["route_EW"] = []
    __Lane_Conflict["route_WE"] = []
    __Lane_Conflict["route_EN"] = []    # none 
    __Lane_Conflict["route_ES"] = []
    __Lane_Conflict["route_NE"] = []
    __Lane_Conflict["route_NW"] = []    # none
    __Lane_Conflict["route_SW"] = []
    __Lane_Conflict["route_NS"] = []
    __Lane_Conflict["route_SE"] = []    # none 
    __Lane_Conflict["route_SN"] = []

    # some constant
    __OPTP = LaneDistance/FixedSpeed

    __MiniLaneDistance = MinimumGap
    __Hmin = math.ceil((__MiniLaneDistance/FixedSpeed)*StepPerSecond)       # same lane safe distance

    __MiniIntersectionDistance = VehicleLength + __MiniLaneDistance
    __Delta = math.ceil((__MiniIntersectionDistance/FixedSpeed)*StepPerSecond)      #intersection safe distance

    __StraightLength = 21.0
    __LeftLength = 19.24
    __S1 = 5.25
    __S2 = 5.43
    __S3 = 11.07
    __S4 = 6.63
    __ConflictDistanceStraight = [__S1, (__StraightLength-__S3), __S3, (__StraightLength-__S1)]
    __ConflictDistanceLeft = [__S2, __S4, (__LeftLength-__S4), (__LeftLength-__S2)]

    __StraightPeriod = []
    __LeftPeriod = []

    # state of optimizer
    __TotalDelay = 0.0
    __VehicleNumber = 0

    # random nomber generator
    x=123456789
    y=362436069
    z=521288629
    t=0
    def __random(self):
        self.x ^= (self.x << 16)
        self.x ^= (self.x >> 5)
        self.x ^= (self.x << 1)

        self.t = self.x
        self.x = self.y
        self.y = self.z

        self.z = self.t ^ self.x ^ self.y
        return self.z

    def __init__(self):
        # init of dictionary of each conflict point
        for i in range(16):
            self.__Conflict_Point[i+1] = {}
            self.__Conflict_Point_temp[i+1] = {}

        for dis in self.__ConflictDistanceStraight:
            self.__StraightPeriod.append((dis/FixedSpeed)*StepPerSecond)
            # print(dis)

        for dis in self.__ConflictDistanceLeft:
            self.__LeftPeriod.append((dis/FixedSpeed)*StepPerSecond)
            # print(dis)
        
        # turning Left=====================================================
        # west to north
        self.__Lane_Conflict["route_WN"].append((10, self.__LeftPeriod[0]))
        self.__Lane_Conflict["route_WN"].append((8, self.__LeftPeriod[1]))
        self.__Lane_Conflict["route_WN"].append((6, self.__LeftPeriod[2]))
        self.__Lane_Conflict["route_WN"].append((3, self.__LeftPeriod[3]))
        # print(self.__Lane_Conflict["route_WN"])
        # west to north
        self.__Lane_Conflict["route_SW"].append((15, self.__LeftPeriod[0]))
        self.__Lane_Conflict["route_SW"].append((11, self.__LeftPeriod[1]))
        self.__Lane_Conflict["route_SW"].append((8, self.__LeftPeriod[2]))
        self.__Lane_Conflict["route_SW"].append((5, self.__LeftPeriod[3]))
        # east to south
        self.__Lane_Conflict["route_ES"].append((7, self.__LeftPeriod[0]))
        self.__Lane_Conflict["route_ES"].append((9, self.__LeftPeriod[1]))
        self.__Lane_Conflict["route_ES"].append((11, self.__LeftPeriod[2]))
        self.__Lane_Conflict["route_ES"].append((14, self.__LeftPeriod[3]))
        # north to east
        self.__Lane_Conflict["route_NE"].append((2, self.__LeftPeriod[0]))
        self.__Lane_Conflict["route_NE"].append((6, self.__LeftPeriod[1]))
        self.__Lane_Conflict["route_NE"].append((9, self.__LeftPeriod[2]))
        self.__Lane_Conflict["route_NE"].append((12, self.__LeftPeriod[3]))

        # going straight =====================================================
        # west to north
        self.__Lane_Conflict["route_WE"].append((13, self.__StraightPeriod[0]))
        self.__Lane_Conflict["route_WE"].append((14, self.__StraightPeriod[1]))
        self.__Lane_Conflict["route_WE"].append((15, self.__StraightPeriod[2]))
        self.__Lane_Conflict["route_WE"].append((16, self.__StraightPeriod[3]))
        # print(self.__StraightPeriod)
        # print(self.__Lane_Conflict["route_WE"])
        # South to north
        self.__Lane_Conflict["route_SN"].append((16, self.__StraightPeriod[0]))
        self.__Lane_Conflict["route_SN"].append((12, self.__StraightPeriod[1]))
        self.__Lane_Conflict["route_SN"].append((7, self.__StraightPeriod[2]))
        self.__Lane_Conflict["route_SN"].append((4, self.__StraightPeriod[3]))
        # east to west
        self.__Lane_Conflict["route_EW"].append((4, self.__StraightPeriod[0]))
        self.__Lane_Conflict["route_EW"].append((3, self.__StraightPeriod[1]))
        self.__Lane_Conflict["route_EW"].append((2, self.__StraightPeriod[2]))
        self.__Lane_Conflict["route_EW"].append((1, self.__StraightPeriod[3]))
        # north to south
        self.__Lane_Conflict["route_NS"].append((1, self.__StraightPeriod[0]))
        self.__Lane_Conflict["route_NS"].append((5, self.__StraightPeriod[1]))
        self.__Lane_Conflict["route_NS"].append((10, self.__StraightPeriod[2]))
        self.__Lane_Conflict["route_NS"].append((13, self.__StraightPeriod[3]))

    def __Clear_Temp(self):
        for i in range(16):
            self.__Conflict_Point_temp[i+1].clear()
            # print(self.__Conflict_Point_temp[i+1])

    def __GenerateValiidSolution(self, IncomingVehicle, CurrentTimeStep):
        MaxDelay = 20*StepPerSecond
        TempSol = []
        SumTempDelay = 0
        TempDelay = 0
        successful = False
        
        for v in IncomingVehicle:
            # print("schedule for "+ str(v))
            successful = False
            while not successful:
                TempDelay =  random.randint(0, MaxDelay)#self.__random() % MaxDelay
                #print(TempDelay)
                T_stop_line = CurrentTimeStep  + self.__OPTP + TempDelay
                
                while(T_stop_line < self.__Hmin + self.__Last_Vehicle_Arrival_Time[v[0]]):
                    # print("violate __Hmin")
                    TempDelay += random.randint(0, MaxDelay)#self.__random() % MaxDelay
                    T_stop_line = CurrentTimeStep  + self.__OPTP + TempDelay

                SubValid = True     # some routes have no conflict point
                if(len(self.__Lane_Conflict[v[0]]) == 0):   # scheduling for the lane which has no conflict point
                    TempDelay = 0
                # print(self.__Lane_Conflict[v[0]])
                for Cpoint in self.__Lane_Conflict[v[0]]:
                    # print(Cpoint)
                    SubValid = False
                    upper_bound = math.ceil(T_stop_line + Cpoint[1] + self.__Delta)
                    lower_bound = math.floor(T_stop_line + Cpoint[1] - self.__Delta)
                    # print("UL: "+str(upper_bound)+", "+str(lower_bound))

                    for t in range(lower_bound, upper_bound+1):
                        if(t in self.__Conflict_Point[Cpoint[0]].keys() or t in self.__Conflict_Point_temp[Cpoint[0]].keys()):
                            # print("not valid")
                            SubValid = False
                            break
                        elif(t == upper_bound):
                            SubValid = True
                    if(not SubValid):
                        break
                if(not SubValid):
                    continue
                else:
                    successful = True
            for Cpoint in self.__Lane_Conflict[v[0]]:
                upper_bound = math.ceil(T_stop_line + Cpoint[1])
                lower_bound = math.floor(T_stop_line + Cpoint[1])
                self.__Conflict_Point_temp[Cpoint[0]][upper_bound] = True
                self.__Conflict_Point_temp[Cpoint[0]][lower_bound] = True
            TempSol.append((v[0], v[1], TempDelay))
            SumTempDelay += TempDelay

        return (SumTempDelay, TempSol)

    def Simulated_Annealing(self, IncomingVehicle, CurrentTimeStep):     # list of tupe (lane, vehicle id)       
        BestSol = []    # list of answer
        BestDelay = math.inf    # setting infinity
        Iteration = 3000

        if(len(IncomingVehicle)==0):
            return BestSol

        TempSol = []
        SumTempDelay = 0
        LastDelay = 0

        for i in range(Iteration):
            # print("Iteration: " + str(i))
            self.__Clear_Temp()
            SumTempDelay, TempSol = self.__GenerateValiidSolution(IncomingVehicle, CurrentTimeStep)
            if(SumTempDelay < BestDelay):
                BestSol = TempSol
                BestDelay = SumTempDelay
                LastDelay = SumTempDelay
            else:
                Temperature = Iteration / i
                difference = LastDelay - SumTempDelay
                average = float(difference) / len(IncomingVehicle)
                average /= StepPerSecond
                if(random.random() <= math.exp(-average / Temperature)):
                    LastDelay = SumTempDelay        

        self.__TotalDelay += BestDelay
        self.__VehicleNumber += len(IncomingVehicle)
        self.__Clear_Temp()
        Ans = []
        for index in range(len(IncomingVehicle)):
            T_stop_line = CurrentTimeStep + self.__OPTP + BestSol[index][2]
            Ans.append((BestSol[index][0], BestSol[index][1], CurrentTimeStep + BestSol[index][2]))
            v = IncomingVehicle[index]
            self.__Last_Vehicle_Arrival_Time[v[0]] = T_stop_line    # update time point of the last vehicle in each lane
            for Cpoint in self.__Lane_Conflict[v[0]]:               # update occupied time point of each conflict point
                upper_bound = math.ceil(T_stop_line + Cpoint[1])
                lower_bound = math.floor(T_stop_line + Cpoint[1])
                self.__Conflict_Point[Cpoint[0]][upper_bound] = True
                self.__Conflict_Point[Cpoint[0]][lower_bound] = True

        return Ans
    
    def QueryTotalDelay(self):
        if self.__VehicleNumber == 0:
            return (self.__TotalDelay/StepPerSecond)
        else:
            return ((self.__TotalDelay/StepPerSecond)/self.__VehicleNumber)

if __name__ == "__main__":
    optimizer = Scheduler()


    N = 36000
    # demand per second from different directions (probabilities)
    pWE = 3. / (5*7)   # vehicles from west lane
    pWN = 1. / (5*7)
    pWS = 1. / (5*7)
    pEW = 3. / (5*7)   # vehicles from east lane
    pEN = 1. / (5*7)
    pES = 1. / (5*7)
    pNE = 1. / (5*7)   # vehicles from north lane
    pNW = 1. / (5*7)
    pNS = 3. / (5*7)
    pSE = 1. / (5*7)   # vehicles from south lane
    pSN = 3. / (5*7)
    pSW = 1. / (5*7)

    vehNr = 0

    for i in range(N):
        if(i%10):
            continue
        # vehicles dirving from west
        vehicles = []
        if random.uniform(0, 1) < pWE:
            vehicles.append(("route_WE", vehNr))
            vehNr += 1
        if random.uniform(0, 1) < pWN:
            vehicles.append(("route_WN", vehNr))
            vehNr += 1
        if random.uniform(0, 1) < pWS:
            vehicles.append(("route_WS", vehNr))
            vehNr += 1

        # vehicles dirving from east
        if random.uniform(0, 1) < pEW:
            vehicles.append(("route_EW", vehNr))
            vehNr += 1
        if random.uniform(0, 1) < pEN:
            vehicles.append(("route_EN", vehNr))
            vehNr += 1
        if random.uniform(0, 1) < pES:
            vehicles.append(("route_ES", vehNr))
            vehNr += 1

        # vehicles dirving from south
        if random.uniform(0, 1) < pSE:
            vehicles.append(("route_SE", vehNr))
            vehNr += 1
        if random.uniform(0, 1) < pSN:
            vehicles.append(("route_SN", vehNr))
            vehNr += 1
        if random.uniform(0, 1) < pSW:
            vehicles.append(("route_SW", vehNr))
            vehNr += 1

        # vehicles dirving from north
        if random.uniform(0, 1) < pNE:
            vehicles.append(("route_NE", vehNr))
            vehNr += 1
        if random.uniform(0, 1) < pNS:
            vehicles.append(("route_NS", vehNr))
            vehNr += 1
        if random.uniform(0, 1) < pNW:
            vehicles.append(("route_NW", vehNr))
            vehNr += 1
        print("--------------------------")
        print(vehicles)
        best = optimizer.Simulated_Annealing(vehicles, i)
        print(best)

        for (x, y, z) in best:
            if(len(best)==0):
                print("wtf")


    print(optimizer.QueryTotalDelay())


