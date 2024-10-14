# rotor_thrust_data

Get thrust and moment data with APC 10x4.5 propeller.

Thrust data through YZC-1B with 3 kg capacity.

<img src="figures/weight_front.jpg"/>

Moment data through loadcell which can measure static torque.

Its capacity is 3 Nm.

<img src="figures/moment_front.jpg"/>

https://github.com/user-attachments/assets/2dd4a7c1-820b-4ba2-b6f8-a8fc06fa6466


# Thrust and moment mapping

<img src="/thrust_bag2/mat_folder/thrust_data.png"/>

The mapping between rpm and thrust is like the below:

$T = p_{T,rpm,1} cmd^2 + p_{T,rpm,2} cmd + p_{T,rpm,3}$

where

$p_{T,rpm,1}$ = 1.80883139637315e-09

$p_{T,rpm,2}$ = -1.96222600800466e-006

$p_{T,rpm,3}$ = 1.66928771872563e-003.

# Moment mapping

<img src="/moment_bag2/mat_folder/moment_data.png"/>

The mapping between rpm and moment is 

$M = p_{M,rpm,1} cmd^2 + p_{M,rpm,2} cmd + p_{M,rpm,3}$

where

$p_{M,rpm,1}$ = 2.92066276908551e-09

$p_{M,rpm,2}$ = -5.54473448895723e-006

$p_{M,rpm,3}$ = 18.2016053924933e-03.
