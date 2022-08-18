MY DEVELOPMENT PROCESS, WHAT WORKED, WHAT DIDN'T DECISIONS I MADE ALONG THE WAY

Notes:
- I was confused by the algo not making blocking moves in some circumstances until I realised this was because if both players played optimally it would lose, and therefore all nodes had the same value (equally bad) and it was choosing the first node rather than the one which would string out the game longer (and therefore open possibility of bad opponent move). I ranked nodes on path depth to correct for this
- It was too ambitious to both implement the full game rules of go and alpha beta pruning, so I had to scale back a lot. If I were doing this again I'd probably have done connect four or tic tac toe
- I did a lot of TDD, but also found coding and manually testing helped (and helped me to develop tests)
- logging helped unpick what was happening (give examples of logs showing the computer's path down the game)
- It was interesting to learn Django, however I could have done this project on the command-line and that might have bought back enough time to develop move of the game of go instead
- I knew it was probably working when I started seeing ladders
- Larger board increases complexity quite a lot, as does more stones in a row to win
- Stones to win equalling board size reduces complexity, but also makes game play less interesting
