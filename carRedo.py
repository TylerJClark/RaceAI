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
        
        
        
        
        
        
