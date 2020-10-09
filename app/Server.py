from typing import List, Dict  # import del manejo de listas
from flask import Flask  # import para el funcionamiento general de flask
import mysql.connector  # import de conexion con mysql
import json  # import para el manejo de variables tipo json
from flask import request  ## Import encargado de renderizar las templates 
import random
import sys
import time
from datetime import timedelta, datetime

app = Flask(__name__)  # creacion de la app en python de flask

def find_lines(board, i, j, player):
    lines = []
    for xdir, ydir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], 
                       [-1, 0], [-1, 1]]:
        u = i
        v = j
        line = []

        u += xdir
        v += ydir
        found = False
        while u >= 0 and u < len(board) and v >= 0 and v < len(board):
            if board[v][u] == 0:
                break
            elif board[v][u] == player:
                found = True
                break
            else: 
               line.append((u,v))
            u += xdir
            v += ydir
        if found and line: 
            lines.append(line)
    return lines
   

def get_possible_moves(board, player):
    result = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[j][i] == 0:
                lines = find_lines(board,i,j,player)
                if lines: 
                    result.append((i,j))
    return result


def play_move(board, player, i, j):
    new_board = []
    for row in board: 
        new_board.append(list(row[:]))
    lines = find_lines(board, i,j, player)
    new_board[j][i] = player
    for line in lines: 
        for u,v in line: 
           new_board[v][u] = player 
    final = []
    for row in new_board: 
        final.append(tuple(row))
    return tuple(final)



def get_score(board):
    p1_count = 0
    p2_count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                p1_count += 1
            elif board[i][j] == 2:
                p2_count += 1
    return p1_count, p2_coun
corners = [(0,0),(0,7),(7,0),(7,7)]


def get_score_weighted(board):

    score = 0
    
    boardHeuristic  =[
        [1000, -10, 10, 10, 10, 10, -10, 1000], \
        [-10, -10, 10, 1,  1,  10,  -10,  -10], \
        [10,  10, 10,  1,  1,  10,  10,  10], \
        [10,  1, 1,  1,  1,  1,  1,  10], \
        [10,  1, 1,  1,  1,  1,  1,  10], \
        [10,  10, 10,  1,  1,  10,  10,  10], \
        [-10, -10, 10,  1,  1,  10, -10,  -10], \
        [1000, -10, 10, 10, 10, 10, -10, 1000]]

    p1_count = 0
    p2_count = 0
    empty_spaces = 0
    p1_weighted = 0
    p2_weighted = 0
    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                empty_spaces +=1
            elif board[i][j] == 1:
                p1_count += 1
                p1_weighted += boardHeuristic[i][j]
            elif board[i][j] == 2:
                p2_count += 1
                p2_weighted += boardHeuristic[i][j]

    if empty_spaces > 0:
        return p1_weighted, p2_weighted
    else:
        return p1_count, p2_count

def minimax_min_node(board, color, depth, end_time):
    possible_moves = get_possible_moves(board, color)
    current_time = datetime.now()
    if possible_moves == [] or depth==0 or current_time >= end_time:
        score = get_score_weighted(board) #get_score(board)
        if color == 1: #then ai player is white
            return score[1]-score[0] #score for ai black
        else:
            return score[0]-score[1] #score for ai white
    else:
        if color == 1: 
            next_color = 2
        else:
            next_color = 1
        best_min_score = 1000000
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            move_score = minimax_max_node(new_board, next_color, depth-1, end_time)
            if move_score < best_min_score:
                best_min_score = move_score
        return best_min_score
    return None


def minimax_max_node(board, color, depth, end_time):
    possible_moves = get_possible_moves(board, color)
    current_time = datetime.now()
    if possible_moves == [] or depth==0 or current_time >= end_time:
        score = get_score_weighted(board) #get_score(board)
        if color == 1: #then ai player is black
            return score[0]-score[1] #score for ai black
        else:
            return score[1]-score[0] #score for ai white
    else:
        if color == 1: 
            next_color = 2
        else:
            next_color = 1
        
        best_max_score = -1000000
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            move_score = minimax_min_node(new_board, next_color, depth-1, end_time)
            if move_score > best_max_score:
                best_max_score = move_score
        return best_max_score
    return None 

    
def select_move_minimax(board, color, depth, end_time):
    best_max_score = -10000000
    possible_moves = get_possible_moves(board, color)
    if color == 1: 
        next_color = 2
    else:
        next_color = 1
    for move in possible_moves:
        new_board = play_move(board, color, move[0], move[1])
        move_score = minimax_min_node(new_board, next_color, depth-1, end_time)
        if move_score > best_max_score:
            best_max_score = move_score
            best_move = move
    return best_move

def alphabeta_min_node(board, color, depth, alpha, beta, end_time):

    possible_moves = get_possible_moves(board, color)
    current_time = datetime.now()
    if possible_moves == [] or depth==0 or current_time >= end_time:
        score = get_score_weighted(board) 
        if color == 1:
            return score[1]-score[0]
        else:
            return score[0]-score[1] 
    else:
        if color == 1: 
            next_color = 2
        else:
            next_color = 1
        best_min_score = 1000000
        for move in possible_moves:
            if move in corners:
                new_board = play_move(board, color, move[0], move[1])
                score = get_score_weighted(new_board)
                if color == 1: 
                		return score[1]-score[0]
                else:
                		return score[0]-score[1] 
            new_board = play_move(board, color, move[0], move[1])
            move_score = alphabeta_max_node(new_board, next_color, depth-1, alpha, beta, end_time)
            if move_score < best_min_score:
                best_min_score = move_score
                beta = min(beta, move_score)
            if beta <= alpha:
                break
        return best_min_score
    return None

def alphabeta_max_node(board, color, depth, alpha, beta, end_time):
    possible_moves = get_possible_moves(board, color)
    current_time = datetime.now()
    if possible_moves == [] or depth==0 or current_time >= end_time:
        score = get_score_weighted(board)
        if color == 1: 
            return score[0]-score[1] 
        else:
            return score[1]-score[0] 
    else:
        if color == 1: 
            next_color = 2
        else:
            next_color = 1
        
        best_max_score = -1000000
        for move in possible_moves:
            if move in corners:
                new_board = play_move(board, color, move[0], move[1])
                score = get_score_weighted(new_board)
                if color == 1: 
                		return score[0]-score[1] 
                else:
                		return score[1]-score[0] 
            new_board = play_move(board, color, move[0], move[1])
            move_score = alphabeta_min_node(new_board, next_color, depth-1, alpha, beta, end_time)
            if move_score > best_max_score:
                best_max_score = move_score
                alpha = max(alpha, move_score)
            if beta <= alpha:
                break
        return best_max_score
    return None

def select_move_alphabeta(board, color, depth, end_time): 
    best_max_score = -10000000
    alpha = -1000000
    beta = 1000000
    best_move = []
    
    possible_moves = get_possible_moves(board, color)        
    if color == 1: 
        next_color = 2
    else:
        next_color = 1
    
    for move in possible_moves:
        if move in corners:
            return move
        new_board = play_move(board, color, move[0], move[1])
        move_score = alphabeta_min_node(new_board, next_color, depth-1, alpha, beta, end_time)
        if move_score > best_max_score:
            best_max_score = move_score
            best_move = move
    return best_move

@app.route('/')
def index():
    turno = request.args.get('turno')
    turno = int(turno)
    estado = request.args.get('estado')#1212121212121211
    response = 24
    lista = list(estado)#['1','2','2']
    contador = 1
    tablero = []
    fila = []
    for i in lista:
        if i == '2':
            fila.append(0)
        elif i == '1':
            fila.append(2)
        elif i == '0':
            fila.append(1)
        if contador%8==0:
            tablero.append(fila)
            fila=[]
        contador=contador+1
    board =[
                    [0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 2, 1, 0, 0, 0], 
                    [0, 0, 0, 1, 2, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0],                        
                    [0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0]]
    print (board)
    print (tablero)
    board = tablero
    color = 1
    if turno==1:
       color = 2
    current_time = datetime.now()
    end_time = current_time + timedelta(seconds=15)
    movei, movej = select_move_minimax(board, color, 2, end_time)
    response=str(movej)+''+str(movei)#24
    return str(response)


if __name__ == '__main__':
    # comando para configurar la ip del servicio
    app.run(host='0.0.0.0')

