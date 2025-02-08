# tic-tac-toe
A simple Tic-Tac-Toe game written in Python.
![image](https://github.com/user-attachments/assets/438bab1d-67b9-4da9-b6e2-0c03f2f54e7b)

# Modules Used
- pygame
- random

# How To Use
The program initially starts in "pvp" mode.
The goal of the game is to get three naughts or crosses across the board either horizontally, vertically and or diagonally.
When you are hovering over a tile you can see a white symbol and if you click on the tile it will change colour representing it has been placed.
To refresh the score you need to press the tile with the red cross on it.
To change between the modes you press on the tile with either "pvp", "pvr" and or "rvr" written on it it. To know which mode is selected the writing is green and the background of the mode button is dark.
To exit one must press the exit button and the program will be terminated.

# Modes
Player vs Player ("pvp") -
Played with two players swapping every turn on the same computer.

Player vs Robot ("pvr") -
Played with one player, the other is a bot that decides which tile to use.

Robot vs Robot ("rvr") -
This mode does not require a player. Two bots fight it out. This mode only lasts three games, so the mode doesn't go forever. After three games it goes to menu mode.

Menu Mode
This mode is entered after three games in "rvr" mode. You can see the mode buttons are not selected. This mode only allows the user to interact with the mode buttons.

# About the Bot
The bot decides it's move by weighing certain decisions.
- Firstly checks if the middle tile is taken, if not it takes it.
- Secondly checks if it is one tile off of winning, if so it takes that tile.
- Thirdly checks if the enemy is one tile off of winning, if so it takes it so they can't.
- Fourthly if none of the conditions above apply, it randomly takes a tile.
