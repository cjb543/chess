#include "visualizer.h"

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int whitePieceCount = 0, blackPieceCount = 0;

bool whiteToMove = false, whiteCanCastle = false, blackCanCastle = false,
     hasEnPassant = false;

char FENString[92], whiteFiftyMoveTracker[2], blackFiftyMoveTracker[2],
    finishedBoard[100];

int main(int argc, char *argv[]) {
  // Error-checking user input
  if (argc != 2) {
    printf(" Usage: %s <\"FEN string\">\n Enclose your FEN string in quotes.\n",
           argv[0]);
    return 1;
  }

  // Create FENString based off of user input
  strncpy(FENString, argv[1], 90);

  processBoardAppearance(FENString, finishedBoard);

  processGameState(FENString, &whitePieceCount, &blackPieceCount,
                   whiteFiftyMoveTracker, blackFiftyMoveTracker, &whiteToMove,
                   &whiteCanCastle, &blackCanCastle, &hasEnPassant);

  printGame(FENString, finishedBoard, whitePieceCount, blackPieceCount,
            whiteToMove, whiteCanCastle, blackCanCastle, whiteFiftyMoveTracker,
            blackFiftyMoveTracker, hasEnPassant);

  return 0;
}

void processBoardAppearance(char FENString[], char finishedBoard[]) {
  // Create a duplicate of FENString, because strtok is scary and I'm scared of
  // it
  int FENStringLen = strlen(FENString);
  char FENStringCopy[FENStringLen];
  strcpy(FENStringCopy, FENString);

  // Create a readable, finishedBoard array based off of FENString
  int i = 0, j = 0;
  while (FENStringCopy[i] != '\0') {
    if (isdigit(FENStringCopy[i])) {
      int numSpaces = FENStringCopy[i] - '0';
      for (int k = 0; k < numSpaces; k++) {
        finishedBoard[j] = '0';
        ++j;
      }
    } else if (isalpha(FENStringCopy[i])) {
      finishedBoard[j] = FENStringCopy[i];
      ++j;
    } else if (FENStringCopy[i] == '/') {
      finishedBoard[j] = '\n';
      ++j;
    }
    ++i;
  }
  finishedBoard[j] = '\0';
}

void processGameState(char FENString[], int *whitePieceCount,
                      int *blackPieceCount, char whiteFiftyMoveTracker[],
                      char blackFiftyMoveTracker[], bool *whiteToMove,
                      bool *whiteCanCastle, bool *blackCanCastle,
                      bool *hasEnPassant) {
  // Check amount of black and white pieces
  for (size_t i = 0; i < strlen(FENString); i++) {
    if (isspace(FENString[i]))
      break;
    if (isupper(FENString[i]))
      (*whitePieceCount)++;
    if (isupper(FENString[i]) == false && isalpha(FENString[i])) {
      (*blackPieceCount)++;
    }
  }

  bool castlingAssigned = false, halfMoveAssigned = false;

  // Create a duplicate of FENString because strtok is scary and I'm scared of
  // it
  int FENStringLength = strlen(FENString);
  char FENStringCopy[FENStringLength];
  strcpy(FENStringCopy, FENString);

  // Tokenize FENString and start at second token
  char *token = strtok(FENStringCopy, " ");
  token = strtok(NULL, " ");

  while (token != NULL) {
    // Determine who goes next
    if (strcmp(token, "w") == 0)
      *whiteToMove = true;
    else if (strcmp(token, "b") == 0)
      *whiteToMove = false;

    int tokenLength = strlen(token);

    // Determine castling rights
    if (isupper(token[0])) {
      *whiteCanCastle = true;
      castlingAssigned = true;
    } else if (!isupper(token[tokenLength - 1]) && castlingAssigned == false) {
      *blackCanCastle = true;
      castlingAssigned = true;
    }

    // Determine if en passant square exists
    if (strcmp(token, "-") && castlingAssigned == true)
      *hasEnPassant = false;
    else if (!strcmp(token, "-") && castlingAssigned == true)
      *hasEnPassant = true;

    // Half Move Counter and Full Move Counter
    if (isdigit(token[0]) && halfMoveAssigned == false) {
      strcat(whiteFiftyMoveTracker, token);
      halfMoveAssigned = true;
    } else if (isdigit(token[0]) && halfMoveAssigned == true) {
      strcat(blackFiftyMoveTracker, token);
    }
    token = strtok(NULL, " ");
  }

  return;
}

void printGame(char FENString[], char finishedBoard[], int whitePieceCount,
               int blackPieceCount, bool whiteToMove, bool whiteCanCastle,
               bool blackCanCastle, char whiteFiftyMoveTracker[],
               char blackFiftyMoveTracker[], bool hasEnPassant) {
  // Print board summary
  printf("%s", "\n Summary of FEN-String:\n ");
  for (size_t i = 0; i < strlen(FENString); i++) {
    printf("%c", FENString[i]);
  }

  // Print pieces
  printf("%s", "\n\n");
  for (int i = 0; i < 71; i++) {
    printf(" %c", finishedBoard[i]);
  }
  printf("\n\n");

  // Print piece counts
  printf(" White has %d pieces. \n", whitePieceCount);
  printf(" Black has %d pieces. \n", blackPieceCount);

  // Print move turn
  if (whiteToMove)
    printf(" White to move. \n");
  else
    printf(" Black to move. \n");

  // Print castling
  if (whiteCanCastle)
    printf(" White has castling rights.\n");
  else if (!whiteCanCastle)
    printf(" White does not have castling rights.\n");
  if (blackCanCastle)
    printf(" Black has castling rights.\n");
  else if (!blackCanCastle)
    printf(" Black does not have castling rights.\n");

  // Print if En Passant square exists
  if (hasEnPassant == true)
    printf(" En Passant squares possible.\n");

  // Handle 50-move-rule tracking
  printf(" %s Half-Moves\n", whiteFiftyMoveTracker);
  printf(" %s Full-Moves\n", blackFiftyMoveTracker);
}
