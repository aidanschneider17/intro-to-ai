from MinMax import minimax_search
from TicTacToe import TicTacToe


def game_loop(game, player):
    """
    Main game loop. Runs until the game until a terminal
    state and then prints the result
    """
    player_id = 0 #id of the current player
    game_over = False
    while not game_over:

        print("-------START TURN------")
        print("Board:")
        game.print_board(game.board)
        print("Current player: " + str(game.symbol[player_id])+" ("+player[player_id]+")")

        if player[player_id] == "human":
            move = int(input("Enter a move (1-9): "))
        elif player[player_id] == "minimax":
            [value, move] = minimax_search(game,game.board,player_id)
             # print(value,move)
        else:
            move = game.random_move(game.board)

        print("Action: "+str(move))
        actions = game.actions(game.board)
        if move in actions:
            game.board = game.result(game.board, move)
            if game.terminal(game.board):
                game_over = True
            else:
                # toggle the player from 1 to 0 or 0 to 1
                player_id = 1 if player_id == 0 else 0
        else:
            print("Invalid move. Spot already taken.")

    game.print_game_over(player_id, player)


def set_players(players):
    """
    Allows you to set player 0 and 1 to either a human, random move, or minimax move
    :param players:
    :return:
    """
    for i in range(len(players)):
        prompt = "Set Player " + str(i+1) + ":" + "\n\t1:Human" + "\n\t2:Random\n" + "\t3:Minimax\n"
        option = int(input(prompt))
        if option == 1:
            players[i] = "human"
        elif option == 2:
            players[i] = "random"
        elif option == 3:
            players[i] = "minimax"

    print("")


def program_loop():
    """
    Allows you to set the players and run the game.
    :return:
    """
    player = ["human", "random"]
    run_program = True

    print("Welcome to Tic-Tac-Toe.")
    print("Would you like to play a game?")
    print("------------------------------\n")

    while run_program:
        print("Current players:")
        print("\tPlayer1:"+player[0]+"\n\tPlayer2:"+player[1]+"\n")
        prompt = "Options:" + "\n\t1.Set Players" + "\n\t2.Play Game\n"

        option = int(input(prompt))
        if option == 0:
            run_program = False
        elif option == 1:
            set_players(player)
        elif option == 2:
            game_loop(TicTacToe(), player)
        else:
            "Invalid choice "+str(option)


if __name__ == '__main__':
    program_loop()
