# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 13:04:38 2019

@author: shume
"""
import numpy as np

import config as cfg
import pygame
import math

class Car(object):
    def __init__(self):
        #displacement
        #this is the middle of the car
        self.pos = np.array([float(0),float(0)])

        #speed
        self.spd = float(0)
        

        #acceleration
        self.acc = float(0)
        
        self.width = 12
        self.height = 30
        self.fps = 30
        self.resistance = 0

        self.angle = float(0)
        self.drifting = False
        self.driftingOffset = 0

        self.sensorAngles = [0,15,30,45,75,90,180,270,285,315,330,345]
        #self.sensorAngles = [0]


    def getEquation(self,p1,p2):

        if (p2[0] - p1[0]) == 0:

            #supposed to be the case where
            #x = ?
            return ["x=?",p1[0]]
        
        gradient = (p2[1] - p1[1])/(p2[0] - p1[0])

        #c is y intercept
        c = p1[1] - gradient * p1[0]

        return [gradient,c]

    #returns false if lines do
    #not intersect
    def findPoint(self,e1,e2):
        #e1[0] is gradient
        #e1[1] is y intercept

        
        #print("hhiya",e1,e2)
        #this is for the case equation is x = ?
        if e1[0] == "x=?" and e2[0] == "x=?":
            return False
        
        if (e1[0] == "x=?"):

            #this is the ? in "x = ?"
            x = e1[1]

            #sub x value into y = mx + c
            y = e1[1] * e2[0] + e2[1]
            return [x,y]

        elif (e2[0] == "x=?"):
            x = e2[1]
            y = e2[1] * e1[0] + e1[1]
            return [x,y]

        if (e1[0] - e2[0]) == 0:
            return False

        #print("fddrgfdgf")
        x = (e2[1] - e1[1])/(e1[0] - e2[0])

        y = x * e1[0] + e1[1]

        return [x,y]

    def getDistance(self,p1,p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        
        
        
    def getState(self,screen,edges,displaySensors = False):
        #inter is intersection

        for j in self.sensorAngles:
            closestWall = 999999999
            closestInt = None
            for i in edges:

                edgeP1 = (i[0],i[1])
                edgeP2 = (i[2],i[3])

                edgeEquation = self.getEquation(edgeP1,edgeP2)


                """if edgeEquation[0] != "x=?":
                    pygame.draw.line(screen, (0,0,200), (edgeP1[0],edgeEquation[0] * edgeP1[0] + edgeEquation[1]),
                                 (edgeP2[0],edgeEquation[0] * edgeP2[0] + edgeEquation[1]),10)     """           
                
                #equations in form [gradient,y intercept]

                carPos = (self.pos[0],720 - self.pos[1])

                #arbitrery constant
                a = 1000

                #point opposite car
                oppCar = [carPos[0] + a * math.sin(math.radians(j - self.angle - self.driftingOffset + 180)),carPos[1] +
                          a * math.cos(math.radians(j - self.angle - self.driftingOffset + 180))]
                
                #pygame.draw.line(screen, (0,150,0), (carPos[0], carPos[1]), (oppCar[0],oppCar[1]),2)

                carEquation = self.getEquation(carPos,oppCar)

                """if carEquation[0] != "x=?":
                    pygame.draw.line(screen, (0,0,200), (carPos[0],carEquation[0] * carPos[0] + carEquation[1]),
                                 (oppCar[0],carEquation[0] * oppCar[0] + carEquation[1]),10)"""
                

                intersect = self.findPoint(edgeEquation,carEquation)
                #print(intersect)
                #edgeP1[0] = 3
                #edgeP1[1] = 10
                
                #edgeP2[0] = 3
                #edgeP2[1] = 5

                
                #edgeP1[0] means x coord
                if intersect != False:
                    if edgeP1[0] > edgeP2[0]:
                        bigCoordX = edgeP1[0]
                        littleCoordX = edgeP2[0]
                    else:
                        bigCoordX = edgeP2[0]
                        littleCoordX = edgeP1[0]

                    if edgeP1[1] > edgeP2[1]:
                        bigCoordY = edgeP1[1]
                        littleCoordY = edgeP2[1]
                    else:
                        bigCoordY = edgeP2[1]
                        littleCoordY = edgeP1[1]
                        

                    if carPos[0] > oppCar[0]:
                        bigCoordX2 = carPos[0]
                        littleCoordX2 = oppCar[0]
                    else:
                        bigCoordX2 = oppCar[0]
                        littleCoordX2 = carPos[0]

                    if carPos[1] > oppCar[1]:
                        bigCoordY2 = carPos[1]
                        littleCoordY2 = oppCar[1]
                    else:
                        bigCoordY2 = oppCar[1]
                        littleCoordY2 = carPos[1]
                        
                    if ((intersect[0] >= littleCoordX and intersect[0] <= bigCoordX and
                        intersect[1] >= littleCoordY and intersect[1] <= bigCoordY) and
                        (intersect[0] >= littleCoordX2 and intersect[0] <= bigCoordX2 and
                        intersect[1] >= littleCoordY2 and intersect[1] <= bigCoordY2)):

                        
                        distance = self.getDistance(intersect,carPos)
                        if distance < closestWall:
                            closestWall = distance
                            closestInt = intersect
                    
            if displaySensors and closestInt != None:
                pygame.draw.line(screen, (150,0,0), (carPos[0], carPos[1]), (closestInt[0],closestInt[1]),2)
        
    def getPos(self):
        #to make it so upwards is positive
        return [self.pos[0],720 - self.pos[1]]

    def getImageAngle(self):
        return self.angle + self.driftingOffset
    
    #turn left by define amount when left key is pressed
    def turnLeft(self,drift = False):
        
        #create rotational matrix
        """theta = np.radians(cfg.THETA);
        c, s = np.cos(theta), np.sin(theta)
        R = np.array((c, -s), (s, c))
        
        #rotate direction the car want to the direction it want to turn to
        self.dir = np.multiply(R, self.dir)"""
        if not drift:
            self.decreaseAngle(cfg.THETA)
        else:
            self.decreaseAngle(cfg.DRIFT_THETA)

        
    
    #turn right by define amount when right key is pressed
    def turnRight(self,drift = False):
        
        #create rotational matrix
        """theta = np.radians(-cfg.THETA);
        c, s = np.cos(theta), np.sin(theta)
        R = np.array((c, -s), (s, c))
        
        #rotate direction the car want to the direction it want to turn to
        self.dir = np.multiply(R, self.dir)"""
        if not drift:
            self.increaseAngle(cfg.THETA)
        else:
            self.increaseAngle(cfg.DRIFT_THETA)

        
    #accelerate
    def accelerate(self):
        self.acc = float(cfg.Amax)


        
    #decelerate
    def resist(self):
        pass
        #slows the speeds at a flat value
        if self.spd > cfg.NA * 2:
            self.spd -= cfg.NA
            
        elif self.spd < -cfg.NA * 2:
            self.spd += cfg.NA

        else:
            self.spd = float(0)

        
    def brake(self):
        self.acc = float(cfg.B)
        
    
    #update velocity every frame
    def updateVelocity(self):
        # v = u + at
        self.spd = self.spd + self.acc
        
        if self.spd > 5:
            self.spd = float(5)
        elif self.spd < -5:
            self.spd = float(-5)
    
    #update position every frame
    def updatePos(self):
        #self.pos = np.add(self.pos, self.dir * self.spd)

        #makes them move in given direction
        self.pos[0] += self.spd * math.sin(math.radians(self.angle))
        self.pos[1] += self.spd * math.cos(math.radians(self.angle))

            
    #update the pivot point every frame
    def updatePivot(self):
        self.pivot = np.add(self.pos, self.pointerVector)
        
    
    def updatePerFrame(self):
        #print("accP",self.acc)
        self.updatePos()
        self.updateVelocity()
        self.resist()
        self.acc = float(0)
        #print("pos",self.pos)
        #print("vel",self.spd)
        #print("acc",self.acc)

    def increaseAngle(self,amount):
        self.angle += amount
        if self.angle > 359:
            self.angle = 0 + (self.angle - 359)        

    def decreaseAngle(self,amount):
        self.angle -= amount
        if self.angle < 0:
            self.angle = 359 + self.angle 

    def handleEvents(self,keys):
        
        if self.drifting == False:
            
            if self.driftingOffset != 0:
                
                if self.driftingOffset > 0:
                    
                    if self.driftingOffset > cfg.DRIFT_OFFSET:
                        self.increaseAngle(self.driftingOffset - cfg.DRIFT_OFFSET)
                    else:
                        self.decreaseAngle(self.driftingOffset)
                        
                elif self.driftingOffset < 0:
                    
                    if self.driftingOffset < -cfg.DRIFT_OFFSET:
                        self.decreaseAngle(abs(self.driftingOffset) - cfg.DRIFT_OFFSET)
                        
                    else:
                        self.decreaseAngle(abs(self.driftingOffset))
                    
                self.driftingOffset = 0
                
            if keys[pygame.K_a] and keys[pygame.K_SPACE] and self.spd > 3:
                self.drifting = "left"

                #rotate clockwise

                self.driftingOffset = -cfg.DRIFT_INITIAL

            elif keys[pygame.K_d] and keys[pygame.K_SPACE] and self.spd > 3:
                self.drifting = "right"

                
                self.driftingOffset = cfg.DRIFT_INITIAL
                
            elif keys[pygame.K_a]:
                self.turnLeft()
                
            elif keys[pygame.K_d]:
                self.turnRight()
                

                
            elif keys[pygame.K_SPACE] or keys[pygame.K_s]:
                self.brake()

            
            if keys[pygame.K_w]:
                self.accelerate()

        elif self.drifting == "right":
            if self.driftingOffset < 45:
                self.driftingOffset += 1
            self.accelerate()
            if not keys[pygame.K_SPACE]:
                self.drifting = False
                
            elif keys[pygame.K_d]:
                self.turnRight(drift = True)            
            
        elif self.drifting == "left":
            if self.driftingOffset > -45:
                self.driftingOffset -= 1
            self.accelerate()
            
            if not keys[pygame.K_SPACE]:
                self.drifting = False
        
            elif keys[pygame.K_a]:
                self.turnLeft(drift = True)          
        
        
        
        
        
        
