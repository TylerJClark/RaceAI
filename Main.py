import pygame
import math
import random
import time
import numpy as np
from collections import namedtuple
#from itertools import count
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import pygame
from ButtonLib import Button
import os
import threading
from copy import deepcopy
from carRedo import Car

pygame.init()
pygame.mixer.init() #initialises pygame and sound
fps = 30 #the game's frames per second

width = 1280
height = 720

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
grey = (128,128,128)

FONT = pygame.font.Font(None, 32) #fonts used in the game

screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN)
pygame.display.set_caption("RaceAI")


def tanh(number):
    return (math.e**number - math.e**(-number))/(math.e**number + math.e**(-number))

    
def extract_tensors(experiences):
    # Convert batch of Experiences to Experience of batches
    batch = Experience(*zip(*experiences))
    
    #('state', 'action', 'next_state', 'reward'))
    #print(batch.state)
    #print(batch.action)
    #print(batch.state)
    t1 = torch.cat(batch.state)
    #print(t1)
    t2 = torch.cat(batch.action)
    t3 = torch.cat(batch.reward)
    t4 = torch.cat(batch.next_state)
    #print(t3)

    return (t1,t2,t3,t4)


class QValues():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    @staticmethod
    def get_current(policy_net, states, actions):
        #print(states)
        #print(policy_net(states))
        return policy_net(states).gather(dim=1, index=actions.unsqueeze(-1))
    
    @staticmethod
    def get_next(target_net, next_states):
        
        #final_state_locations = next_states.max(dim=1)[0].eq(3).type(torch.bool)
        final_state_locations = next_states.max(dim=1)[0].eq(3).type(torch.ByteTensor)
        #print(final_state_locations)
        
        non_final_state_locations = (final_state_locations == 0)
        non_final_states = next_states[non_final_state_locations]
        
        batch_size = next_states.shape[0]
        values = torch.zeros(batch_size).to(QValues.device)
        #print(non_final_states)
        values[non_final_state_locations] = target_net(non_final_states).max(dim=1)[0].detach()
        #print(values)
        return values


class DQN(nn.Module):
    def __init__(self, inputs, hidden, outputs):
        super().__init__()
        """self.layers = []
        
        learnArgs = []
        self.layers.append(nn.Linear(in_features = inputs, out_features = hidden[0]))
        learnArgs.append(nn.Parameter(torch.tensor([float(inputs),float(hidden[0])])))

        #self.myParameters.append(nn.Linear(in_features = inputs, out_features = hidden[0]))
        
        for i in range(len(hidden) - 1):
            self.layers.append(nn.Linear(in_features = hidden[i], out_features = hidden[i+1]) )
            learnArgs.append(nn.Parameter(torch.tensor([float(hidden[i]),float(hidden[i+1])])))
            #self.myParameters.append(nn.Linear(in_features = hidden[i], out_features = hidden[i+1]))


        self.layers.append(nn.Linear(in_features = hidden[-1], out_features = outputs))
        learnArgs.append(nn.Parameter(torch.tensor([float(hidden[-1]),float(outputs)])))

        self.myParameters = nn.ParameterList(learnArgs)"""
        #self.myParameters.append(nn.Linear(in_features = hidden[-1], out_features = outputs))
        #self.myparameters = nn.ParameterList(Parameter1, Parameter2, ...)
        #print(hidden)
        self.lengthHidden = len(hidden)
        finished = False
        self.fc1 = nn.Linear(in_features=inputs, out_features=hidden[0])
        
        if len(hidden) > 1:
            self.fc2 = nn.Linear(in_features=hidden[0], out_features=hidden[1])
        else:
            self.out = nn.Linear(in_features=hidden[0], out_features=outputs)
            finished = True

        if not finished:
            if len(hidden) > 2:
                self.fc3 = nn.Linear(in_features=hidden[1], out_features=hidden[2])
            else:
                self.out = nn.Linear(in_features=hidden[1], out_features=outputs)
                finished = True

        if not finished:
            if len(hidden) > 3:
                self.fc4 = nn.Linear(in_features=hidden[2], out_features=hidden[3])
            else:
                self.out = nn.Linear(in_features=hidden[2], out_features=outputs)
                finished = True

        if not finished:
            if len(hidden) > 4:
                self.fc5 = nn.Linear(in_features=hidden[3], out_features=hidden[4])
            else:
                self.out = nn.Linear(in_features=hidden[3], out_features=outputs)
                finished = True

        if not finished:
            if len(hidden) > 5:
                self.fc6 = nn.Linear(in_features=hidden[4], out_features=hidden[5])
            else:
                self.out = nn.Linear(in_features=hidden[4], out_features=outputs)
                finished = True            
            

    def forward(self, t):
        """newt = [[]]
        for i in range(len(t)):
            for j in t[i]:
                newt[0].append(j)"""
        #t = newt
        #print(t)
        #t = torch.tensor(t)
        #t.clone().detach()
        #print(t)
        #t = t.flatten(start_dim=1)
        #t = t.reshape(1,-1)
        #t = t.squeeze()
        #print(t)
        
        """for i in range(len(self.layers) - 1):
            
            t = F.relu(self.layers[i](t))
            
        t = self.layers[-1](t)"""
        
        t = F.relu(self.fc1(t))
        if self.lengthHidden > 1:
            t = F.relu(self.fc2(t))
        if self.lengthHidden > 2:
            t = F.relu(self.fc3(t))
        if self.lengthHidden > 3:
            t = F.relu(self.fc4(t))
        if self.lengthHidden > 4:
            t = F.relu(self.fc5(t))
        if self.lengthHidden > 5:
            t = F.relu(self.fc6(t))            
        t = self.out(t)        
        return t

    def forwardSigmoid(self, t):
        t = t.flatten(start_dim=1)
        for i in range(len(self.layers) - 1):
            
            t = F.logsigmoid(self.layers[i](t))
            
        t = self.layers[-1](t)
        return t    

    def forwardTanh(self, t):
          
        #t = F.hardtanh(self.layers[i](t))
        t = F.hardtanh(self.fc1(t))
        if self.lengthHidden > 1:
            t = F.hardtanh(self.fc2(t))
        if self.lengthHidden > 2:
            t = F.hardtanh(self.fc3(t))
        if self.lengthHidden > 3:
            t = F.hardtanh(self.fc4(t))
        if self.lengthHidden > 4:
            t = F.hardtanh(self.fc5(t))
        if self.lengthHidden > 5:
            t = F.hardtanh(self.fc6(t))            
        t = F.hardtanh(self.out(t))      
        return t

class ReplayMemory():
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.push_count = 0


    def push(self, experience):
        if len(self.memory) < self.capacity:
            self.memory.append(experience)
        else:
            self.memory[self.push_count % self.capacity] = experience
        self.push_count += 1


    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def can_provide_sample(self, batch_size):
        return len(self.memory) >= batch_size
    
    def check_copy(self,experience):
        copy = False
        if len(self.memory)!=0:
            for i in self.memory:
                if experience[0].tolist()==i[0].tolist():
                    if experience[3].tolist==i[3].tolist():
                        copy=True
                        break
        return copy


class EpsilonGreedyStrategy():
    def __init__(self, start, end, decay):
        self.start = start
        self.end = end
        self.decay = decay

    def get_exploration_rate(self, current_step):
        return self.end + (self.start - self.end) * \
            math.exp(-1. * current_step * self.decay)



class Agent():
    def __init__(self, strategy, num_actions, device):
        self.current_step = 0
        self.strategy = strategy
        self.num_actions = num_actions
        self.device = device
        print(device)

    def selectAction(self, state, policy_net,actions,exploitChance = -1):
        if exploitChance == -1:
            self.rate = self.strategy.get_exploration_rate(self.current_step)
        else:
            self.rate = exploitChance
        #print(rate)
        self.current_step += 1

        if self.rate > random.random():
            #print("explore")
            return random.choice(actions),None # explore      
        else:
            with torch.no_grad():
                #print("exploit")
                #print(policy_net(state))
                #print(torch.tensor(state).reshape(1,-1))
                #print((policy_net(torch.tensor(state).reshape(1,-1))).tolist()[0])
                probabilities = policy_net(torch.tensor(state).reshape(1,-1))
                best = int(probabilities.argmax(dim=1).to(self.device)[0])
                #best = int(policy_net(torch.tensor(state).reshape(1,-1)).argmax(dim=1).to(self.device)[0]) # exploit
                if best in actions:
                    return best,probabilities.tolist()[0]

                
                ordered = []
                
                #choice = policy_net.forward(state.clone().detach())
                #print("choice",choice)
                for i in range(len(probabilities[0])):
                    ordered.append((float(probabilities[0][i]),i))

                ordered = sorted(ordered, key=lambda x: x[0])
                ordered = ordered[::-1]
                #print("order",ordered)

                for i in ordered:
                    if i[1] in actions:
                        return i[1],probabilities.tolist()[0]

                #print(torch.tensor(currentState))
                print("no move found")
                print("ordered",ordered)
                print("actions",actions)


                
class envManager():
    def __init__(self):
        
        self.env = playGame()
        self.state,self.maxActions,self.maxStates = self.env.startGame()
        
        self.done = False

    def getFFF(self):
        return self.env.getFF()

    def getAdvanceMove(self):
        return self.env.getNext()

    def sendProb(self,probabilities):
        self.env.sendProb(probabilities)

    def setAdvanceMove(self):
        self.env.setNext(True)

    def getFinalState(self):
        return self.env.getFinalState()

    def getFinalReward(self):
        return self.env.getFinalReward()

    def getMaxStates(self):
        return self.maxStates

    def getState(self):
        return self.state

    def getMaxActions(self):
        return self.maxActions
    
    def reset(self):
        self.env = playGame()
        self.state,self.maxActions,self.maxStates = self.env.startGame()
        self.done = False
        
    def render(self):
        self.env.render()

    def getActions(self):
        return self.env.getMoves()

    def take_action(self, action):  
        self.newState,reward,done,nextActions,lastState = self.env.step(action)
        #newState is other players state
        return self.newState,torch.tensor([reward], device=self.device),done,nextActions,lastState

    def increment_turn(self):
        self.state = self.newState

    def getReward(self):
        return self.getFinalReward()

def trainAI(trained):
    global stopGame
    global gamesPlayed
    global policyNetwork
    global targetNetwork
    global Experience
    
    manager = envManager()


class playGame():
    def __init__(self,humanControl,viewing):
        self.humanControl = humanControl
        self.viewing = viewing
        self.map = track()
        self.car = Car()
        self.lastState = None
        self.currentState = None
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder,"images") 
        self.carImage = pygame.image.load(os.path.join(self.img_folder,"car.png")).convert()

    def display(self,screen):
        angle = self.car.getImageAngle()
        newCar = pygame.transform.rotate(self.carImage,360 - angle)
        self.car.draw(screen,newCar)
        
        #pygame.draw.rect(screen, [255, 255, 255], [pos[0] - 6, pos[1] - 15, 12, 30], False)
        self.map.drawMap(screen,white)

    def update(self,screen,agent = None):
        if not self.humanControl:
            actions = self.agent.selectAction()
            self.car.performActions(actions)

        self.car.updatePerFrame(self.map.edges)
        self.car.getState(screen,self.map.edges,True)
        if self.viewing:
            self.display(screen)

    #self.state,self.maxActions,self.maxStates = self.env.startGame()
    def startGame(self):
        self.state = self.car.getState()
        self.maxActions = 4
        self.maxStates = 1800
        return self.state, self.maxActions, self.maxStates
        
        

class track():
    def __init__(self):
        #self.edges = [(12,12,35,36),()] 
        self.edges = [(210,400,210,260),(210,260,230,200),(230,200,250,180),(250,180,310,150),
                      (310,150,590,150),(590,150,650,180),(650,180,670,200),(670,200,700,260),
                      (700,260,700,350),(700,350,730,370),(730,370,780,370),(780,370,800,350),
                      (800,350,800,260),(800,260,830,200),(830,200,850,180),(850,180,910,150),
                      (910,150,1040,150),(1040,150,1100,180),(1100,180,1120,200),(1120,200,1150,260),
                      (1150,260,1150,520),(1150,520,1100,600),(1100,600,1000,630),(1000,630,900,630),
                      (900,630,700,590),(700,590,400,590),(400,590,370,650),(370,650,350,670),
                      (350,670,290,700),(290,700,210,700),(210,700,150,670),(150,670,130,650),
                      (130,650,100,590),(100,590,100,510),(100,510,130,450),(130,450,150,430),
                      (150,430,210,400),(400,510,320,510),(320,510,320,590),(320,590,290,620),
                      (290,620,210,620),(210,620,180,590),(180,590,180,510),(180,510,210,480),
                      (210,480,290,480),(290,480,290,400),(400,510,700,510),(700,510,830,500),
                      (830,500,930,430),(930,430,930,250),(930,250,900,250),(900,250,880,270),
                      (880,270,880,350),(880,350,840,420),(840,420,800,450),(800,450,700,450),
                      (700,450,650,430),(650,430,620,390),(620,390,620,270),(620,270,590,230),
                      (590,230,310,230),(310,230,290,270),(290,270,290,400)]

        #self.edges = [(400,400,600,400)]
                      
        
        self.gates = []
        self.startGate = ()

    def drawMap(self,screen,colour):
        for i in self.edges:
            pygame.draw.line(screen, colour, (i[0], i[1]), (i[2], i[3]),5)

#buttons
quitButton = Button(1220,10,50,50,grey,blue,True,(0,0,0),text = "X")
viewButton = Button(390,310,500,100,grey,blue,True,(0,0,0),text = "View AI")
trainButton = Button(390,190,500,100,grey,blue,True,(0,0,0),text = "Train AI")
playButton = Button(390,430,500,100,grey,blue,True,(0,0,0),text = "Play Game")
saveButton = Button(390,550,500,100,grey,blue,True,(0,0,0),text = "Save Game")



clock = pygame.time.Clock()
running = True

#hyperparams
maxEpisodes = 100
maxSteps = 50
learningRate = 0.01
maxMemory = 5000
targetUpdate = 10 #how often target network copies the policy network
discountRate = 0.99
exploreDecay = 0.0001
batchSize = 256
trained = False
gamesPlayed = 0



game = "home"
while running:
    clock.tick(fps)
    pygame.display.flip()
    screen.fill((0,0,0))
    mouseUp = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouseUp = True
            
    pos = pygame.mouse.get_pos()
    
    quitButton.hovering(pos)
    quitButton.create(screen)
    if quitButton.click(pos,mouseUp):
        running = False
        pygame.quit()


    if game == "home" or game == "training":
        viewButton.hovering(pos)
        viewButton.create(screen)
        if viewButton.click(pos,mouseUp):
            game = "viewing"
            thisGame = playGame(False,True)

        trainButton.hovering(pos)
        trainButton.create(screen)
        if trainButton.click(pos,mouseUp):
            
            if game == "training":
                trainButton = Button(390,190,500,100,red,(150,0,0),True,(0,0,0),text = "Stop Training")
                game = "home"
                trained = True
            else:
                trainButton = Button(390,190,500,100,grey,blue,True,(0,0,0),text = "Train AI")
                game = "training"

                trainingThread = threading.Thread(target=trainAI,
                    args=[trained])

                trainingThread.start()
                

        playButton.hovering(pos)
        playButton.create(screen)
        if playButton.click(pos,mouseUp):
            game = "playing"
            thisGame = playGame(True,True)
            

        saveButton.hovering(pos)
        saveButton.create(screen)
        if saveButton.click(pos,mouseUp):
            saveGame()
        
    elif game == "playing":
        thisGame.update(screen)
        keys = pygame.key.get_pressed()
            
        thisGame.car.handleEvents(keys)

    
 
    


pygame.quit()
