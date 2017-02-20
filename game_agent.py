"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    """
    #Heuristic 1: Aggressive Improved Score
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves - 2*opp_moves)

    """

    """
    #Heuristic 2: Border/Non-Border Differentiated Moves Scoring
    border_moves = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6),
                    (1,0), (1,6), (2,0), (2,6), (3,0), (3,6), (4,0),
                    (4,6), (5,0), (5,6), (6,0), (6,1), (6,2), (6,3),
                    (6,4), (6,5), (6,6)]
    own_score = 0
    opp_score = 0
    for each_move in game.get_legal_moves(player):
        if each_move in border_moves:
            own_score = own_score + 1
        else:
            own_score = own_score + 1.5

    for each_move in game.get_legal_moves(game.get_opponent(player)):
        if each_move in border_moves:
            opp_score = opp_score + 1
        else:
            opp_score = opp_score + 1.5

    return float(own_score - opp_score)
    """

    #Heuristic 3: Advanced Differentiated Board scoring
    border_moves = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6),
                    (1,0), (1,6), (2,0), (2,6), (3,0), (3,6), (4,0),
                    (4,6), (5,0), (5,6), (6,0), (6,1), (6,2), (6,3),
                    (6,4), (6,5), (6,6)]

    next_to_border_moves = [(1,1), (1,2), (1,3), (1,4), (1,5), (2,1),
                            (2,5), (3,1), (3,5), (4,1), (4,5),
                            (5,1), (5,2), (5,3), (5,4), (5,5)]

    own_score = 0
    opp_score = 0

    for move in game.get_legal_moves(player):
        if move in border_moves:
            own_score += 1
        elif move in next_to_border_moves:
            own_score += 1.2
        else:
            own_score += 1.5

    for move in game.get_legal_moves(game.get_opponent(player)):
        if move in border_moves:
            opp_score += 1
        elif move in next_to_border_moves:
            opp_score += 1.2
        else:
            opp_score += 1.5

    return float(own_score - opp_score)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left
        move = (-1, -1) #Default

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        max_depth = 0
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative:
                #Perform iterative search
                num_of_remaining_moves = len(game.get_blank_spaces())
                for depth in range(1,num_of_remaining_moves):
                    if self.time_left() <= self.TIMER_THRESHOLD:
                        return move

                    if self.method == 'alphabeta':
                        iterative_best_score, iterative_best_move = self.alphabeta(game, depth)
                    else:
                        iterative_best_score, iterative_best_move = self.minimax(game, depth)

                    #Stores score and move of the deepest search
                    score = iterative_best_score
                    move = iterative_best_move
                    max_depth = depth
            else:
                #Perform fixed-depth search
                if self.method == 'alphabeta':
                    score, move = self.alphabeta(game, self.search_depth)
                else:
                    score, move = self.minimax(game, self.search_depth)

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        return move


    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        legal_moves = game.get_legal_moves()

        best_move = (-1, -1)
        if maximizing_player:
            score = float("-inf")
        else:
            score = float("inf")

        #At bottom of minimax tree
        if depth == 1:
            for each_move in legal_moves:
                new_game = game.forecast_move(each_move)
                if maximizing_player and self.score(new_game, self) > score:
                        score = self.score(new_game, self)
                        best_move = each_move
                elif not maximizing_player and self.score(new_game, self) < score:
                        score = self.score(new_game, self)
                        best_move = each_move

            return score, best_move

        #Not at bottom of minimax tree
        for each_move in legal_moves:
            #Return each_move that gets the highest score
            new_game = game.forecast_move(each_move)
            new_score , new_move = self.minimax(new_game, depth-1, not maximizing_player)
            if maximizing_player and new_score > score:
                score = new_score
                best_move = each_move
            elif not maximizing_player and new_score < score:
                score = new_score
                best_move = each_move

        return score, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        ""
        legal_moves = game.get_legal_moves()

        best_move = (-1, -1)
        if maximizing_player:
            score = float("-inf")
        else:
            score = float("inf")

        #At bottom of minimax tree
        if depth == 1:
            for each_move in legal_moves:
                new_game = game.forecast_move(each_move)
                new_score = self.score(new_game, self)
                if maximizing_player:
                    #Pruning of max nodes
                    if new_score >= beta:
                        return beta, each_move
                    if new_score > score:
                        score = new_score
                        best_move = each_move
                else:
                    #Pruning of min nodes
                    if new_score <= alpha:
                        return alpha, each_move
                    if new_score < score:
                        score = new_score
                        best_move = each_move

            return score, best_move

        #Not at bottom of minimax tree
        for each_move in legal_moves:
            #Return each_move that gets the highest score
            new_game = game.forecast_move(each_move)
            new_score , new_move = self.alphabeta(new_game, depth-1, alpha, beta, not maximizing_player)
            if maximizing_player:
                #Pruning of max nodes
                if new_score >= beta:
                    return beta, each_move
                elif new_score > alpha:
                    #Update alpha for pruning in next for iteration
                    alpha = new_score

                if new_score > score:
                    score = new_score
                    best_move = each_move
            else:
                #Pruning of min nodes
                if new_score <= alpha:
                    return alpha, each_move
                elif new_score < beta:
                    #Update beta for pruning in next for iteration
                    beta = new_score

                if new_score < score:
                    score = new_score
                    best_move = each_move

        return score, best_move
