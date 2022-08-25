# Robogo Description

This document is designed to help the developer understand how to structure the code based on the requirements of the software. 

In the project definition we've already separated out these concepts which I'll bear in mind while describing the software:

1) code to handle game moves and storing of game position
2) code containing algorithm to choose next move
3) code for visual user interface for the human to interact with
4) code for test suite including unit tests, integration tests and system tests

Robogo is a software application which allows a human user to play five-in-a-row Go against a computer opponent. The user should be able to start the application from the command line and then get a visual respresentation of a 9x9 Go board. The user will always start the game, and therefore their stones will be black and the computer's stones will be white (following Go conventions). The user will place their first stone on the board using the mouse to choose their position. The computer will then respond by placing a stone. The computer will decide how to place its stone using an algorithm. If either player's stone placement is an illegal move the UI won't show that stone as placed and will display a warning and prompt to select the move again. Either player should also be able to indicate they want to pass their move. If both the human and the computer pass then the game will end. As this is five-in-a-row an early end to the game will be scored as a draw. If either player places a stone which causes a capture, the captured stones will be removed from the board, but we won't tally up the number of captures as this isn't part of five-in-a-row go. If either player places the fifth stone in a row the game will end with a message declaring that player to be the winner.

Classes:
Go board
Game moves




