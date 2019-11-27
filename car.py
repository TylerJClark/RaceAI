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
        self.pos = np.array([0,0])
        self.pointerVector = np.array([0,0])

        self.dir = np.array([0,1])

        #speed
        self.spdX = 0
        self.spdY = 0
        

        #acceleration
        self.accX = 0
        self.accY = 0
        
        self.width = 70
        self.height = 200
        self.fps = 30
        self.resistance = 0

        self.angle = 0

    def getPos(self):
        return self.pos
    
    #turn left by define amount when left key is pressed
    def turnLeft():
        
        #create rotational matrix
        """theta = np.radians(cfg.THETA);
        c, s = np.cos(theta), np.sin(theta)
        R = np.array((c, -s), (s, c))
        
        #rotate direction the car want to the direction it want to turn to
        self.dir = np.multiply(R, self.dir)"""
        angle -= 1
        if angle < 0:
            angle = 359
        
    
    #turn right by define amount when right key is pressed
    def turnRight(self):
        
        #create rotational matrix
        """theta = np.radians(-cfg.THETA);
        c, s = np.cos(theta), np.sin(theta)
        R = np.array((c, -s), (s, c))
        
        #rotate direction the car want to the direction it want to turn to
        self.dir = np.multiply(R, self.dir)"""

        angle += 1
        if angle > 359:
            angle = 0
        
    #accelerate
    def accelerate(self):
        self.acc = cfg.Amax


        
    #decelerate
    def resist(self):
        pass
        #slows the speeds at a flat value
        """if self.spd > cfg.NA * 2:
            self.spd -= cfg.NA
            
        elif self.spd < -cfg.NA * 2:
            self.spd += cfg.NA

        else:
            self.spd = 0"""

        
    def brake(self):
        self.acc = cfg.B
        
    
    #update velocity every frame
    def updateVelocity(self):
        # v = u + at
        self.spd = self.spd + self.acc
        if self.spd > 5:
            self.spd = 5
        elif self.spd < 3:
        
    
    #update position every frame
    def updatePos(self):
        #self.pos = np.add(self.pos, self.dir * self.spd)

        self.pos[0] += self.spd * math.sin(math.radians(self.angle))
        self.pos[1] -= self.spd * math.cos(math.radians(self.angle))
    
    #update the pivot point every frame
    def updatePivot(self):
        self.pivot = np.add(self.pos, self.pointerVector)
        
    
    def updatePerFrame(self):
        self.updatePos()
        self.updateVelocity()
        self.resist()
        print("pos",self.pos)
        print("vel",self.spd)
        print("acc",self.acc)


    def handleEvents(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.turnLeft()
            if event.key == pygame.K_d:
                self.turnRight()
            if event.key == pygame.K_w:
                self.accelerate()
            if event.key == pygame.K_SPACE:
                self.brake()
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
