# rotor_thrust_data

Get thrust and moment data with APC 10x4.5 propeller.

Thrust data through YZC-1B with 3 kg capacity.

<img src="figures/weight_front.jpg"/>

Moment data through loadcell which can measure static torque.

Its capacity is 3 Nm.

<img src="figures/moment_front.jpg"/>

https://github.com/user-attachments/assets/2dd4a7c1-820b-4ba2-b6f8-a8fc06fa6466


# Thrust and moment mapping

<img src="/thrust_bag2/mat_folder/thrust_data_CT.png"/>

The mapping between rpm and thrust is like the below:

$T = C_{T} \omega^2$

where

$C_{T}$ = 1.481e-07 \frac{N}{\text{rpm}^2}$.

# Moment mapping

<img src="/moment_bag2/mat_folder/moment_data_CM.png"/>

The mapping between rpm and moment is 

$M = C_{M} \omega^2$

where

$C_{M} = 2.524e-09 \frac{N\cdot m}{\text{rpm}^2}$.
