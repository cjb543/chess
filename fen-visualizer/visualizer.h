#include <stdbool.h>

void processBoardAppearance(char FENString[], char finishedBoard[]);

void processGameState(char FENString[], int *whitePieceCount,
                      int *blackPieceCount, char whiteFiftyMoveTracker[],
                      char blackFiftyMoveTracker[], bool *whiteToMove,
                      bool *whiteCanCastle, bool *blackCanCastle,
                      bool *hasEnPassant);

void printGame(char FENString[], char finishedBoard[], int whitePieceCount,
               int blackPieceCount, bool whiteToMove, bool whiteCanCastle,
               bool blackCanCastle, char whiteFiftyMoveTracker[],
               char blackFiftyMoveTracker[], bool hasEnPassant);
