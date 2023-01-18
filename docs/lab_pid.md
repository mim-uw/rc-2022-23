---
title: Lab 11
---

```bash
git clone https://github.com/mim-uw/rc-2022-23
```

All needed files are located in the `docs/lab_pid_files/` directory.

# PID

This simulation will give you the chance to understand the concepts of PID control through a virtual setup that includes a motor, a freely rotating arm, and a freely sliding cart. The arm's angle is controlled by adjusting the propeller thrust at the arm's end. The cart's movement is determined by the angle of the arm. If the angle of the arm is above the horizontal, the cart will accelerate in one direction, and if the angle is below the horizontal, the cart will accelerate in the opposite direction (note that we use the word accelerate and not move, as the cart has its momentum).

![img](https://user-images.githubusercontent.com/7950377/212520117-7c9829f8-fdb7-423f-b228-d0d6b532edcb.png)

![img](https://user-images.githubusercontent.com/7950377/212520130-c348ba35-a2b4-42e2-8c23-8b5b6fc0926e.png)


You will not have to write the code for the PID control algorithm, it's already been done for you. Your role is to make adjustments to the algorithm's parameters to optimize its performance. This includes changing the proportional, integral, and derivative gain values to find the settings that work best for the system. Through experimenting with different parameter values, you will see the impact they have on the system's response and learn how to achieve the desired behavior.

The simulation will begin with the cart at a standstill, to make it easier for you to get started. You will first focus on fine-tuning the PID parameters for the arm angle control, and once you have mastered that, you can move on to the second layer of control for the cart's position. This multi-layer PID control is achieved by using the output of one PID controller as the setpoint of another. In this case, one PID controller will control the angle of the pole with the thrust of the motor, while the other will control the position of the cart with the angle of the pole, which is now assumed to be maintained by the first controller. The difference between the desired position and the actual position will be used to adjust the angle and move the cart to the desired position.

To help you evaluate the system's performance, the PID controllers will output data to CSV files after each run. This will enable you to monitor changes in the system's behavior over time and make more informed decisions about how to adjust the parameters. You can analyze the CSVs using your preferred tool or use [this tool](https://chart-studio.plotly.com/create/?fid=pieniacy%3A1)
(click Import and upload your csv) to make it easier to understand the data.

It's important to keep in mind that the PID controllers have limits on their output that need to be tuned. This will help prevent the system from overdriving and guarantee its stability. Additionally, there are specific limits on the integral control to prevent windup, a situation where the integral term accumulates a high value, resulting in a large control output.

It's worth mentioning that the PID controllers have low-pass filters on their derivatives. However, that will not be important for this particular simulation.

This task provides you with the ability to monitor the real-time data of the system such as the arm angle, cart position, control output, and error which will aid you in tuning the parameters. Through this simulation, you will learn how to adjust the parameters to make the system respond quickly, accurately, and stably.

In todays scenario you should:
1. Explore the simulation environment by using manual control.
Notice that the system is stable below horizontal (certain thrust makes the system hover at certain angle).
2. Modify the `main()` function to run the variant you want, in this case comment out manual control.
3. Make the system work by tuning parameters of the angle PID and make sure you can control the system
with the setpoint slider in the gui. It does not have to be very fast, reaching and holding the setpoint is important.
4. Run `test_solution(True)` and try to tune layered controller so that you can set the position
and the system responds correctly and eventually the position is reached and held.
Again, it does not have to be very fast.

Here is a basic guide to PID tuning:
1. Start with a small value for the proportional gain (P) and gradually increase it
until the system starts responding to the setpoint changes. The goal is to find the point at which the system starts oscillating.
2. Once the optimal P value is found, move on to the derivative gain (D). Start with a small value for D and gradually increase it.
The goal is to smooth the operation and dampen any oscillation.
3. Next, if there is a problem with steady state error tune the integral gain (I).
Start with a small value for I and gradually increase it. Integral limits might be useful to prevent windup.

Repeat steps 1 through 3 for several test scenarios.
Once the optimal values for P, D, and I are found, test the system with different setpoints to ensure
that it can handle different situations and it is stable.

Monitor the real-time data of the system, such as the arm angle, control output,
and the error, this will help you adjust the parameters more precisely.

Keep in mind that the optimal values for P, D, and I will depend on the specific
characteristics of the system and the desired behavior, so they may need to be adjusted as the system evolves.
You might to choose to accept some overshoot or to tune a smoother controller.

Finally, it is a good practice to adjust the limits of the controllers, such as output limit and integral windup limit,
to have a stable and safe operation.
