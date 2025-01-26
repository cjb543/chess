# FEN-visualization

A C script that aims to visualize the hard-to-read FEN notation that is used for chess games and their state. Shows a "board" in 8x8 structure like any other chess board, as well as the state of the game.

## Command Format:
    ./visualizer <"fen_string">

Here's an example:\
``` ./visualizer "4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1" ```

OUTPUT:
```
 Summary of FEN-String:
 4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1

 0 0 0 0 k 0 0 r 
 0 0 0 0 0 0 r 0 
 0 0 0 0 0 0 0 0 
 0 0 0 0 0 0 0 0 
 0 0 0 0 0 0 0 0 
 0 0 0 0 0 0 0 0 
 0 0 0 R 0 0 0 0 
 R 0 0 0 K 0 0 0

 White has 3 pieces. 
 Black has 3 pieces. 
 White to move. 
 White has castling rights.
 Black has castling rights.
 0 Half-Moves
 1 Full-Moves
```
