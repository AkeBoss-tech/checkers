# Checkers
This program is a checkers program.
The program has the following rules:
1. Pieces that take other pieces in the same turn can take as many pieces as they can
2. Normal Pieces can only move forward diagonally
3. Kings can move forwards or backwards diagonally
4. Once a piece reaches the end of the board it becomes a king
5. Pieces take diagonally

# Program
This program is split into two files.
~~~
main.py
Pieces.py
~~~
In order to run the game, you must run main.py.
You should probably go into the help menu before you start just to read how the game works.

## Libraries
The program requires multiple libraries
~~~
os, sys, pygame, pickle, datetime, copy, random, pathlib, time
~~~

You can install them by running

~~~
pip install library_you_need_to_install
~~~

## Playing the Game
### Human Player
If you are playing a human player, you can click the undo button.
~~~
<-
~~~
At the top of the screen to allow the other person to start.
While playing, if you select pieces or squares that the current player can not select you will enter counting mode. In this mode you will see green or aqua circles in squares and pieces. To exit this mode, click outside of the board.


### Computer Player
The computer has 4 different modes.
1. Random
2. Easy
3. Medium
4. Hard

The computer uses a mini max algorithm to search all possible future moves to find the best one.

1. Random mode chooses a random move for the computer. There is no logic involved.
2. Easy looks one move ahead (one move for the computer and another for the user)
3. Medium looks two moves ahead.
4. Hard looks three moves ahead, but it takes a really long to decide the move because there are thousands of possible game states.

### Closing the Game
The user can click the quit button whenever they want. If they are using the terminal they can type quit to leave. 

# Features
1. Player can undo or take back moves in human vs. human and human vs. computer mode
2. Players can save and view previous games. Games are saved by the time they are finished.
3. Help screen to give a short crash course of the program.
4. Smooth GUI
5. Players can select and deselect pieces without making a move
6. Possible moves are shown on the screen. (Sometimes the program may give hints for possible move locations)
