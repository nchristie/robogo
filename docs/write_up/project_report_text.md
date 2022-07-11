I. Introduction
The ancient Chinese boardgame Go has attracted lots of media attention in recent years following Google's success in writing Artificial Intelligence capable of beating the world's best human Go player [SOURCE]. While there are many resources to play Go online both against other humans and against computers [SOURCE] there are fewer resources aimed at assisting beginners to understand the rules. Gomoku [https://en.wikipedia.org/wiki/Gomoku] is a variation of the game in which the aim is to place five stones in a row before one's opponent manages to get five in a row. All the other remaining rules of the game were, however, maintained. On investigation this variation of the game appears to be an adaption of Gomoku , in which the capture rules aren't upheld. While there are resources to play Gomoku against computers online [https://gomokuonline.com/, https://gomoku.yjyao.com/] on investigation I could not find this unusual variation in which capture rules are upheld available.

II. Literature Review

- Resources here and how I used them to learn

III. Robogo User Guide
The user should open a terminal at the robogo directory and type in the following command:
./start_game.sh

Note: if you get an error message saying `permission denied: ./start_game.sh` then please run the following command: `chmod u+x start_game.sh` and then try `./start_game.sh` again.

This should open the game in a web browser. The user should see a page showing a simple 9x9 Go board where the intersections are labelled as plus signs, and the coordinates (0-8) are labelled along the top and the right hand side.

[INSERT IMAGE HERE SHOWING BOARD]

A form at the top of the screen will allow the user to state which game they are playing (based on their IP address), which colour player they're playing (human user should always play the black player), and which X and Y coordinates they want to play at. When they give coordinates for their move it will appear on the board, and white's response will be displayed. The human user can then input the coordinates of their next move, and so on. Once the software is complete the game will detect when a user has five stones in a row and then declare that this player as the winner.

Errors:
If the user inputs coordinates which are out of range they will forfeit that move and white will play instead.

IV. Robogo program

i. Overview
Robogo is implemented using the Django web framework for the Python language and a Postgresql database. Docker containerisation has been employed in order to make it easier to run the code from different computers or servers by automating the process of setting up dependencies. The Django framework uses Model, View, Template structure. The Model represents both the classes in the program and the items in the database. The View handles the logic in order to prepare information for the Template, which is the means of viewing the relevant information from a web browser. Django was chosen in order to simplify the coupling of concepts in the code to the database, create some ready-made structure to the code and to ease the rendering of information as a web page. The code to allow the computer to select the best move is stored in `games/minimax.py` and `games/go_minimax_joiner.py` and implements the minimax algorithm.

ii. Minimax with Alpha-Beta Pruning
The minimax algorithm allows the computer to optimise its choice of next move by looking ahead a number of steps in the game by creating a game tree. It then assesses the utility of the moves at this point in the game, and then works back up the tree to establish the most optimal move at each point. For a two-player game such as Go the computer will always choose the move with the minimum utility to its opponent and presume that its opponent will take the move with the maximum utility to themself, and this alternating minimising and maximising of utility is where the term minimax derives. Alpha beta pruning can be layered over minimax to reduce the amount of computing time required to calculate the optimal move. It works by traveling navigating the game tree to the terminal state of one branch and establishing the utility of the optimal move on that branch, now when the next branch is assessed, as soon as the utility breaches the threshold value set by the first branch we can ignore all paths below that level and avoid these calculations.

In this project minimax is implemented using a base class in `games/minimax.py` called `MinimaxNode`. This class creates a node in the game tree, which in turn has a member variable called `leaves` which is a list of MinimaxNodes. 

Note: Alpha-Beta pruning is not yet implemented on this repo.


Database
Front End


TESTS I DID TO MAKE SURE IT WORKS, ERROR HANDLING

CONCLUSION
- What else would improve this program?

References:


