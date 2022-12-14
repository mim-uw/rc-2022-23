---
title: Lab 9
title:  "test"
usemathjax: true
date:   2022-07-05 12:00:00 +0200
---

<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>

# Camera coordinates calculations 

## Problem 1


Determine the matrix that describes the intrinsic parameters of the two identical pinhole cameras, which have focal lengths of 1 and optical centers at `(300.5, 300.5)`.

## Problem 2

Find the 2D coordinates of the projection of the 3D point `(10, 10, 5)` onto the images captured by any of the two cameras.

## Problem 3

Given that the optic axes of the two cameras are parallel and the second camera is displaced by `(x=1, y=0, z=0)` relative to the first camera, estimate the distance from the first camera to the point whose coordinates are `(303, 303)` on the image captured by the first camera and `(298, 303)` on the image captured by the second camera.

# Linearizing non-linear dynamics around fixed points


Find fixed points of the following system and linearize its dynamics around those fixed points, i.e., 

- given a system \\( \dot{x} = f(x) \\), find \\(\overline{x}\\) such that \\(f(\overline{x})=0\\) and 
- formulate approximate dynamics \\(\dot{\Delta x} = A ⋅ \Delta x\\), where \\(A\\) is the matrix you need to find and \\(\Delta x=x-\overline{x}\\).

## System 1

Consider the following 1-dimensional system that can be used to model population growth \\(x\\) is the population size, \\(P_{max}\\) is population limit above which the environment becomes resource scarse.

$$\dot{x} = f(x) = x(P_{max}-x)$$

## System 2

Damped pendulum (\\(\delta\\) is the damping coefficient), where \\(\theta\\) denotes the angle.

$$\ddot{\theta} = -\sin(\theta) - \delta\dot{\theta}$$

Denote

$$x = \begin{pmatrix} x_1 \\ x_2\end{pmatrix} = \begin{pmatrix} \theta\\ \dot{\theta} 
\end{pmatrix} $$


$$\dot{x} =  \begin{pmatrix}\dot{x_1} \\ \dot{x_2}\end{pmatrix} = \begin{pmatrix}x_2 \\ -\sin(x_1) - \delta x_2 \end{pmatrix}$$ 

which is non-linear due to the \\(\sin\\) function.

## System 3

In the following system you can assume \\(-\pi \le \theta \le \pi\\)


$$\dot{r} = r^2 - r$$

$$\dot{\theta} = \sin^2(\theta / 2)$$


## System 4

$$\begin{pmatrix}\dot{x} \\ \dot{y}\end{pmatrix} = 
\begin{pmatrix}x(3-x-2y)\\ y(2-x-y)\end{pmatrix}$$
