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
        self.pos = np.array([float(0),float(0)])

        #speed
        self.spd = float(0)
        

        #acceleration
        self.acc = float(0)
        
        self.width = 70
        self.height = 200
        self.fps = 30
        self.resistance = 0

        self.angle = 0

    def getPos(self):
        return [self.pos[0],720 - self.pos[1]]

    def getAngle(self):
        return self.angle
    
    #turn left by define amount when left key is pressed
    def turnLeft(self):
        
        #create rotational matrix
        """theta = np.radians(cfg.THETA);
        c, s = np.cos(theta), np.sin(theta)
        R = np.array((c, -s), (s, c))
        
        #rotate direction the car want to the direction it want to turn to
        self.dir = np.multiply(R, self.dir)"""
        self.angle -= 3
        if self.angle < 0:
            self.angle = 359

        
    
    #turn right by define amount when right key is pressed
    def turnRight(self):
        
        #create rotational matrix
        """theta = np.radians(-cfg.THETA);
        c, s = np.cos(theta), np.sin(theta)
        R = np.array((c, -s), (s, c))
        
        #rotate direction the car want to the direction it want to turn to
        self.dir = np.multiply(R, self.dir)"""

        self.angle += 3
        if self.angle > 359:
            self.angle = 0

        
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

        self.pos[0] += self.spd * math.sin(math.radians(self.angle))
        self.pos[1] += self.spd * math.cos(math.radians(self.angle))
        
        """if self.angle < 90:
            self.pos[0] += self.spd * math.sin(math.radians(self.angle))
            self.pos[1] += self.spd * math.cos(math.radians(self.angle))
        elif self.angle < 180:
            self.pos[0] += self.spd * math.cos(math.radians(self.angle - 90))
            self.pos[1] += self.spd * math.sin(math.radians(self.angle - 90))            
        elif self.angle < 270:
            self.pos[0] += self.spd * math.sin(math.radians(self.angle - 180))
            self.pos[1] += self.spd * math.cos(math.radians(self.angle - 180))
        else:
            self.pos[0] += self.spd * math.cos(math.radians(self.angle - 270))
            self.pos[1] += self.spd * math.sin(math.radians(self.angle - 270))"""

            
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


    def handleEvents(self,keys):
        if keys[pygame.K_a]:
            self.turnLeft()
        if keys[pygame.K_d]:
            self.turnRight()
            
        if keys[pygame.K_w]:
            self.accelerate()
            
        if keys[pygame.K_SPACE] or keys[pygame.K_s]:
            self.brake()

        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
