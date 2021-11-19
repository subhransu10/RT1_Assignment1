from __future__ import print_function

import time
from sr.robot import *


a_th = 2.0
""" float: Threshold for the control of the linear distance"""
d_th = 0.4
""" float: Threshold for the control of the orientation"""
g_th = 2.0
""" float: Threshold for the control of direction"""
s_th = 0.9
""" float: Threshold for linear distance between robot and gold"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token(angle,length):
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
#angle signifies the angle between the silver token and the robot
#length signifies the length of the field visible ahead    
    dist=100
    for token in R.see():
       if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and angle+length>=token.rot_y>=angle-length:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
      return -1,-1
    else:
      return dist,rot_y

def find_golden_token(angle,length):
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
#angle signifies the angle between the silver token and the robot
#length signifies the length of the field visible ahead   
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and  angle+length>=token.rot_y>=angle-length:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

def left_winger():
   dist_l,rot_yl = find_golden_token(-90,30)
   dist_r,rot_yr = find_golden_token(90,30)
   ##it will check whether the distance to the left is more or right
   print("left distance=",dist_l)
   print("right distance=",dist_r)
   if dist_l>dist_r:
            return True
   else:
       return False

def avoid_gold_wall():
    dist,rot_y=find_golden_token(0,70)
    if dist==-1:
       return
    elif dist<s_th:
         left=left_winger()
         if left:
            while(rot_y<g_th):
                 turn(-20,0.1)
                 dist,rot_y=find_golden_token(0,5)
         else :
              while(rot_y<g_th):
                   turn(+20,0.1)
                   dist,rot_y=find_golden_token(0,5)

def pick_silver():
    dist,rot_y=find_silver_token(0,50)
    dist_g,rot_yg=find_golden_token(rot_y,50)
    if dist==-1:
       return
    
    elif dist<d_th:
         R.grab()
         turn(-20,2.5)
         R.release()
         turn(20,2.5)
         return
    elif -a_th<=rot_y<=a_th:
         drive(50,0.1)
    elif -a_th>rot_y:
         turn(-1,0.1)
    elif a_th<rot_y:
         turn(1,0.1)
    return
         
while 1:
      drive(35,0.1)
      pick_silver()
      avoid_gold_wall()
      
    
