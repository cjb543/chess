board_widget = None

def set_board(board):
    global board_widget
    board_widget = board

def processPGN(pgn_content):
    if board_widget:
        board_widget.parsePGN(pgn_content)
        board_widget.resetToStart()
        print("PGN processed successfully!")
    else:
        print("Board widget not set!")

def nextMove():
    if board_widget and board_widget.nextMove():
        print(f"Showing move {board_widget.current_move_index + 1}")
    else:
        print("No more moves!")

def previousMove():
    if board_widget:
        if board_widget.previousMove():
            if board_widget.current_move_index == -1:
                print("Showing initial position")
            else:
                print(f"Showing move {board_widget.current_move_index + 1}")
        else:
            print("Already at the initial position!")
    else:
        print("Board widget not set!")