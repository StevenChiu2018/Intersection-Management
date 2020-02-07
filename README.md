# Intersection management
This implementation is referenced from the paper
`Ismail H. Zohdy, Raj Kishore Kamalanathsharma, Hesham Rakha, Member, IEEE, “Intersection Management for Autonomous Vehicles using iCACC”, 2012 15th International IEEE Conference on Intelligent Transportation Systems`
and we have modified the constraints slightly in our implementation, the modification will be shown in document.

## Simulation Controlling

The objective of paper is to find an efficient way to control the intersection under the environment with CACC mode. And there are 2 points of requirement should be achieved:

- Given a designated time, the vehicle should arrive at the stop-line in front of intersection. (CACC mode should adjust the speed to reduce fuel consumption)

- Vehicles should keep at a fixed speed in intersection. (35 miles/hr in paper)

However, we found we couldn't designate the arrival time of vehicle at the stop-line. Therefore, to solve this problem and simplify the procedures in controlling, we have the 2 following adjustments:

- Once we obtain the delay time for incoming vehicles in optimization, we transform it into the delaying period of departure.

- Vehicles should keep at a fixed speed all the way in the map of simulation. (15 m/s)

With these 2 adjustments, we could still verify the correctness of constraints. (Simulator would give us warning of potential collisions.)

## Simulation Results

- Youtube: Simulation of Intersection Management

[![](http://img.youtube.com/vi/mhBlxEJIuzI/0.jpg)](http://www.youtube.com/watch?v=mhBlxEJIuzI "Simulation of Intersection Management") 
