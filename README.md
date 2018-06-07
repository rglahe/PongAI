# PongAI
Simple GUI for Atari's Pong and an AI that plays it by temporal difference learning

Script uses PyGame to generate the GUI and uses numpy for large data storage.

After you hit "x" on the menu, it takes a while to train the AI, roughly 10 minutes it runs 100 thousand test cases to train- during this time, it will say it is not responding but it is still running training games on the AI

Once it is done training, the GUI will tell you so. Hit the "p" key to watch the AI play.

Once it misses, the game will freeze, hit escape to go back and it will whipe the board state and you can hit 'P' again to watch it play a new game. The ball starts in the same location every game but after it is rebounded updates its x and y velocity randomly along a fixed range. 
To exit the game on the menu, hit 'e'
