"""
PW2 Lab B Part 2 -- three routes to a minimum.

Compare gradient descent, Newton, and SLSQP on two functions:
  2A: f(x) = (x-3)**2 + 1          (easy, one minimum at x=3)
  2B: g(x) = x**4 - 3*x**2 + x + 5 (harder, several stationary points)
Run:  python warmup.py
"""
import numpy as np
from scipy.optimize import newton, minimize

# ---------- 2A: easy convex function ----------
def f(x):   
  return (x-3)**2 + 1
def df(x):  
  return 2*(x-3)
def d2f(x): 
  return 2.0


x = 0.0
lr = 0.1 #it is defined by us, because choosing step size small, makes good optimization to x(min)



#FIrst method for calculating f(min) -- Gradient Descent
while (abs(df(x)) > 1e-8):
  x = x - lr*df(x)

print("Gradient descent by hand result: ")
print("x = ",x )
print("f(x) = ", f(x))



#Second method for calculating f(min) -- Newton Method
x_newton = newton(df, x0 = 0.0, fprime = d2f)
print("Newton result: ")
print("x = ", x_newton)
print("f(x) = ", f(x_newton))


# Sequential Least Squares Programming - SLSQP
result = minimize(f, x0= 0.0 , method = "SLSQP")
print("SLSQP-(Sequential Least Squares Programming): ")
print(result)

# ---------- 2B: harder landscape ----------
def g(x):   
  return x**4 - 3*x**2 + x + 5
def dg(x):  
  return 4*x**3 - 6*x + 1
def d2g(x): 
  return 12*x**2 - 6

#Gradient descent for complex equation
def gradient_descent(start):
  x = start #because it has 2 initial values given in the task: 0 and 2;

  while abs(dg(x)) > 1e-8:
    x = x - lr*dg(x)
  return x

gd_0 = gradient_descent(0.0)
gd_2 = gradient_descent(2.0)

print("Gradient descent from 0:", gd_0, g(gd_0))
print("Gradient descent from 2:", gd_2, g(gd_2))
## With lr = 0.1, both starting points converge to the same minimum

#Newton's method for complex equation
starting_point1 = 0
starting_point2 = 2

result1 = newton(dg, x0 = starting_point1, fprime = d2g) 
result2 = newton(dg, x0 = starting_point2, fprime = d2g)

print("Newton result: ")
print("Result 1 and ddg(x) ", result1, d2g(result1)) #local maximum because d2g(x) is not greater than zero (<0)
print("Result 2 and ddg(x) ", result2, d2g(result2)) #local minimum because d2g(x) is greater than zero

print("If ddg(x) (or d2g(x) is less than zero it is local maximum")
print("If ddg(x) (or d2g(x) is greater than zero it is local minimum")


#SLSQP for complex function
result1 = minimize(g, x0= 0.0, method="SLSQP")
result2 = minimize(g, x0= 2.0, method="SLSQP")

print(result1)
print(result2)

