# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 13:04:38 2019

@author: shume
"""
import numpy as np

import config as cfg

class Car(object):
    def __init__(self):
        self.pos = numpy.array([0,0])
        self.pointerVector = numpy.array([0,0])
        self.velocity = numpy.array([0.0,0.0])
        self.acceleration = numpy.array([0,0])
        self.width = 70
        self.height = 200
        self.pivot = numpy.array([0,0])
        self.fps = 30
        self.resistance = 0
    
    #turn left by define amount when left key is pressed
    def turnLeft():
        
        #create rotational matrix
        theta = np.radians(cfg.THETA);
        c, s = np.cos(theta), np.sin(theta)
        R = np.array((c, -s), (s, c))
        
        #rotate direction the car want to the direction it want to turn to
        self.acceleration = np.multiply(R, self.acceleration)
    
    #turn right by define amount when right key is pressed
    def turnRight(self):
        
        #create rotational matrix
        theta = np.radians(-cfg.THETA);
        c, s = np.cos(theta), np.sin(theta)
        R = np.array((c, -s), (s, c))
        
        #rotate direction the car want to the direction it want to turn to
        self.acceleration = np.multiply(R, self.acceleration)
        
    #accelerate
    def accelerate():
        self.acceleration = self.acceleration * cfg.A
        
    #decelerate
    def resistance():
        self.acceleration = self.acceleration * cfg.NA
        
    def brake():
        self.acceleration = self.acceleration * cfg.B
        
    
    #update velocity every frame
    def updateVelocity(self):
        # v = u + at
        self.velocity = np.add(self.velocity, self.acceleration / 30)
    
    #update position every frame
    def updatePos(self):
        self.pos = np.add(self.pos, self.velocity)
    
    #update the pivot point every frame
    def updatePivot(self):
        self.pivot = np.add(self.pos, self.pointerVector)
        
    def startEngine(self):
        self.velocity = numpy.array([0.0, 0.0])
        
    
    def updatePerFrame():
        self.updatePos()
        self.updateVelocity()
        self.resistance()
        self.
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        