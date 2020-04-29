# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:40:07 2020

@author: gouna
"""

""" PRACTICAL 6"""

import random

"""GAME DRIVER, CALL TO START GAME. CAN SPECIFY PLAYER VS AI OR AI VS AI"""
def nim():
    global gstate
    print("Let's play nim!")
    num_piles = int(input("How many piles initially? "))
    max_sticks = int(input("Maximum number of sticks? "))
    piles = createState(num_piles, max_sticks)
    print("The initial state is", piles)
    
    gameType = input("Do you want to play or watch two AIs play? Type 'me' for you or 'ai' for AI. ")
    
    if gameType == "me":
        player = int(input("Do you want to go first or second? "))
        
        gstate = (piles, 1)
        while gstate[0] != []:
            print("\nThe current state is:", gstate)
            if (gstate[-1] == player) & (gstate[-1] == 1):
                pile = int(input("Which pile will you remove from? "))
                num = int(input("How many sticks do you wish to remove? (1, 2 or 3) "))
                gstate[0][pile-1] -= num
                if gstate[0][pile-1] <= 0:
                    gstate[0].pop(pile-1)
                gstate = (gstate[0], 2)
                
            elif (player == 2) & (gstate[-1] == 1):
                print("\nAI's turn..")
                maxVal_prune_game(gstate, float("-inf"), float("inf"))
            
            elif (gstate[-1] == player) & (gstate[-1] == 2):
                pile = int(input("Which pile will you remove from? "))
                num = int(input("How many sticks do you wish to remove? (1, 2 or 3) "))
                gstate[0][pile-1] -= num
                if gstate[0][pile-1] <= 0:
                    gstate[0].pop(pile-1)
                gstate = (gstate[0], 1)
                
            elif (player == 1) & (gstate[-1] == 2):
                print("\nAI's turn..")
                minVal_prune_game(gstate, float("-inf"), float("inf"))
                
        if(gstate[-1] != player):
            print("\nYou lose, AI wins!")
        else:
            print("\nYOU WIN! AI LOSES!")
    elif gameType == "ai":
        gstate = (piles, 1)
        while gstate[0] != []:
            print("\nThe current state is:", gstate)
            if gstate[-1] == 1:
                print("\nMAX AI's turn..")
                maxVal_prune_game(gstate, float("-inf"), float("inf"))
                
            elif gstate[-1] == 2:
                print("\nMIN AI's turn..")
                minVal_prune_game(gstate, float("-inf"), float("inf"))
                
        if(gstate[-1] == 1):
            print("\nFINAL STATE IS:", gstate, "\nMAX AI wins!")
        else:
            print("\nFINAL STATE IS:", gstate, "\nMIN AI wins!")
     
"""CREATES INITIAL STATE FROM USER INPUT"""
def createState(num_piles, max_sticks):
    piles = []
    for i in range(0,num_piles):
        rand = random.randint(1,max_sticks)
        piles.append(rand)
    return piles

"""FINDS OPTIMAL MAX MOVE USING ALPHA PRUNING"""
def maxVal_prune_game(state, alpha, beta):
    global gstate
    if terminal_test(state):
        return utility(state)
    v = float("-inf")
    node = state
    for s in successors(state):
        vp =  minVal_prune_game(s, alpha, beta)
        if vp > v:
            v = vp
            node = s
        if vp >= beta:
            if terminal_test(s):
                return utility(s)
            return v
        if vp > alpha:
            alpha = vp
    gstate = node
    return v

"""FINDS OPTIMAL MAX MOVE USING BETA PRUNING"""
def minVal_prune_game(state, alpha, beta):
    global gstate
    if terminal_test(state):
        return utility(state)
    v = float("inf")
    node = state
    for s in successors(state):
        vp = maxVal_prune_game(s, alpha, beta)
        if vp < v:
            v = vp
            node = s
        if vp <= alpha:
            if terminal_test(s):
                return utility(s)
            return v
        if vp < beta:
            beta = vp
    gstate = node
    return v

"""RETURNS LIST OF POSSIBLE NEXT STATES"""
def successors(state):
    l = []
    index = 0
    player = state[-1]
    if player == 1:
        player = 2
    else:
        player = 1
        
    for pile in state[0]:
        num = 1
        while num < 4:
            if pile - num == 0:
                temp = state[0][:]
                temp.remove(pile)
                l.append((temp, player))
                
            if pile - num > 0:
                temp = state[0][:]
                temp[index] = pile - num
                l.append((temp, player))
            num += 1
        index += 1
    return l

"""RETURNS 1 IF MAX WINS, -1 IF MIN WINS"""
def utility(state):
    if state[-1] == 1:
        return 1
    elif state[-1] == 2:
        return -1

"""CHECKS IF GAME IS OVER"""
def terminal_test(state):
    if state[0] == []:
        return True
    else:
        return False