#!/usr/bin/env python
# coding: utf-8

# Submitted By :
#   Navpreet Singh
#   ns4767@nyu.edu

# define the class of states for both terminal and non terminal

class state:
    
    top = 0
    bottom = 10**6
    
    def __init__(self,t,n,r):
        self.terminal = t
        self.reward = r
        self.state_no = n
        self.actions = 0
        self.t_p = []
        
        if t:
            if r<state.bottom:
                state.bottom=r
            if r>state.top:
                state.top=r
        
    def add_action(self):
        self.actions+=1
        self.t_p.append({})
    
    def add_tp(self,a,s,p):
        self.t_p[s][a]=p
    

# choosing an action randomly factoring M for explore/exploit tradeoff

def chooseAction(s,count,total,M):
    n = s.actions
    for i in range(0,n):
        if count[s.state_no][i]==0:
            return i
    avg = []
    for i in range(0,n):
        avg.append(total[s.state_no][i]/count[s.state_no][i])
    bottom = state.bottom
    top = state.top
    savg = []
    for i in range(0,n):
        savg.append(0.25 + 0.75*(avg[i]-bottom)/(top-bottom))
    c = 0
    for i in range(0,n):
        c += count[s.state_no][i]
    up = []
    for i in range(0,n):
        up.append(savg[i]**(c/M))
    norm = 0
    for i in range(0,n):
        norm += up[i]
    p = []
    for i in range(0,n):
        p.append(up[i]/norm)
    
    choice = random.choices(p,weights=p)
    return p.index(choice[0])


# play 1 round given the state and choosing a random action and saving its performance result to exploit later.

def play_round(states,s,count,total,M):
    pairs = []
    while not s.terminal:
        a = chooseAction(s,count,total,M)
        pairs.append((s.state_no,a))
        s1 = random.choices(list(s.t_p[a].keys()),weights=list(s.t_p[a].values()))
        s = states[s1[0]]
    for k in pairs:
        i,j=k
        count[i][j]+=1
        total[i][j]+=s.reward
    

# print the output in the given format as described in the problem statement

def print_output(count,total,rn):
    if rn==0:
        return
    print("After {} rounds\n".format(rn))
    print("Count:")
    for i in range(len(count)):
        for j in range(len(count[i])):
            print("[{},{}]={}. ".format(i,j,count[i][j]),end="")
        print("")
    print("\nTotal:")
    for i in range(len(count)):
        for j in range(len(count[i])):
            print("[{},{}]={}. ".format(i,j,total[i][j]),end="")
        print("")
    print("\nBest Action :  ",end="")
    for i in range(len(count)):
        if 0 in count[i]:
            print("{}:U. ".format(i),end="")
        else:
            print("{}:{}. ".format(i,count[i].index(max(count[i]))),end="")
    print("\n")
    

# main function for using reinforcement learning to solve mdp playing r rounds.

def rl_mdp(states,count,total,M,v,r):
    
    for i in range(r):
        play_round(states,random.choices(states[:n])[0],count,total,M)
        if v != 0 and i%v == 0 :
            print_output(count,total,i)
            print("")
    print_output(count,total,r)



import random

if __name__ == "__main__":

    # take inputs
    
    with open('input.txt', 'r') as file:
        inputs = file.readlines()
    
    n,t,r,v,M = list(map(int,inputs[0].split()))
    states = []
    
    for s in range(n):
        states.append(state(False,s,0))
    
    inp = list(map(int,inputs[1].split()))
    i=0
    while i < len(inp):
        states.append(state(True,inp[i],inp[i+1]))
        i+=2
        
        
    for i in range(2,len(inputs)):
        inp = list(inputs[i].split())
        s1 = int(inp[0][0])
        a = int(inp[0][2])
        states[s1].add_action()
        j=1
        while(j<len(inp)):
            s2=int(inp[j])
            tp=float(inp[j+1])
            j+=2
            states[s1].add_tp(s2,a,tp)

    # define data structure to keep track of learning process
        
    count = []
    total = []
    
    for s in range(n):
        count.append([])
        total.append([])
        for _ in range(states[s].actions):
            count[s].append(0)
            total[s].append(0)
    
    
    # start the reinforcement learning for n rounds and according to M parameter
    
    rl_mdp(states,count,total,M,v,r)





