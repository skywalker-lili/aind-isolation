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

    # TODO: finish this function!
    
    # Heuristic function 1: # of available moves
    return float(len(game.get_legal_moves(player)))


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
        current state.)  This parameter should be ignored when iterative = True.

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).  When True, search_depth should
        be ignored and no limit to search depth.

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
            DEPRECATED -- This argument will be removed in the next release

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

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        
        if len(legal_moves) == 0:
            return (-1, -1)
        
        best_move = legal_moves[0] # default use first legal move as the best move
            
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            
            # TODO: finish this function!
            
            if self.method == "minimax":
                best_score, best_move = self.minimax(game, self.search_depth, 
                                                     maximizing_player=True)
                return best_move
            
            elif self.method == "alphabeta":
                best_socre, best_move = self.alphabeta(
                    game, self.search_depth, maximizing_player=True,
                    alpha=float("-inf"), beta=float("inf"))
                return best_move
            
            else:
                raise Exception("Method:{}, isn't valid. Only 'minimax' or 'alphabeta' is valid."
                                .format(self.method))

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move # return the best move before time out

        # Return the best move from the last completed search iteration
        return best_move

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

        # TODO: finish this function!
        possible_moves = game.get_legal_moves()
        print("Initial possible moves are:{}".format(possible_moves))
        
        if maximizing_player:
            value, move = self.max_value(game, 1, depth)
            return value, move
            
        else:
            value, move = self.min_value(game, 1, depth)
            return value, move
        # raise NotImplementedError
    
    def terminate_minimax(self, game, current_depth, max_depth, maximizing_player=True):
        """
        Determine whether minimax search should stop
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        current_depth : int
            An integer indicating the current number of plies to search in the game tree
        
        max_depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)
            
        Returns
        -------
        boolean :
            Whether should stop the minimax search
        """
        
        # Situation 1: current depth is deeper than maximeum depth
        if current_depth > max_depth:
            # print("This game reaches max depth:{}!".format(max_depth))
            return True
        
        # Situation 2: there is no legal moves for active player to perform
        if len(game.get_legal_moves()) == 0:
            # print("This game has to end since no legal move for {}!"
            #       .format(game.active_player))
            return True
        
        return False  # otherwise should return False to continue the search
    
    def max_value(self, game, current_depth, max_depth):
        """
        Find the maximum value given the game board
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        current_depth : int
            An integer indicating the current number of plies to search in the game tree
        
        max_depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
                   
        Returns
        -------
        float :
            maximum value of the given board
        
        int :
            index of the move that maximize the value in possible legal moves; intialized as -1
        """
        
        if self.terminate_minimax(game, current_depth, max_depth):
            return self.score(game, self), -1
        
        else:
           max_val = float("-inf")
           max_move_id = -1
           possible_moves = game.get_legal_moves()
           # print("possible_moves are {}".format(possible_moves))
           
           # Iterate through all possible moves and find maximum one
           for id, move in enumerate(possible_moves):
               attempt_board = game.forecast_move(move)
               attempt_max, _ = self.min_value(attempt_board, current_depth+1, max_depth)
               # print("Trying move {}, its score is {}".format(move, attempt_max))
               if attempt_max > max_val:
                   # print("Move {} has score:{}, larger than current:{}".format(move, attempt_max, max_val))
                   max_val = attempt_max
                   max_move_id = id
           # print("Max move decided: {} with value of {}".format(possible_moves[max_move_id], max_val))
           return max_val, possible_moves[max_move_id]
    
    def min_value(self, game, current_depth, max_depth):
        """
        Find the minimum value given the game board
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        current_depth : int
            An integer indicating the current number of plies to search in the game tree
        
        max_depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
   
        Returns
        -------
        float :
            the minimum value of the given board
        
        int :
            index of the move that minimize the value in possible legal moves; intialized as -1
        """
        
        if self.terminate_minimax(game, current_depth, max_depth):
            return self.score(game, self), -1
        
        else:
            min_val = float("inf")
            min_move_id = -1
            possible_moves = game.get_legal_moves()
            
            # Iterate through all possible moves to find the minimum one
            for id, move in enumerate(possible_moves):
                attempt_board = game.forecast_move(move)
                attempt_min, _ = self.max_value(attempt_board, current_depth+1, max_depth)
                if attempt_min < min_val:
                    min_val = attempt_min
                    min_move_id = id
            
            return min_val, possible_moves[min_move_id]
    
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

        # TODO: finish this function!
        possible_moves = game.get_legal_moves()
        alpha_beta = {"alpha": float("-inf"), "beta": float("inf")}
        
        if maximizing_player:
            value, move_id = self.max_value_ab(game, 1, depth, alpha_beta)
            return value, possible_moves[move_id]
            
        else:
            value, move_id = self.min_value_ab(game, 1, depth, alpha_beta)
            return value, possible_moves[move_id]
        # raise NotImplementedError
    
    def max_value_ab(self, game, current_depth, max_depth,\
                     alpha_beta={"alpha": float("-inf"), "beta": float("inf")}):
        """
        Find the maximum value given the game board using alpha-beta pruning
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        current_depth : int
            An integer indicating the current number of plies to search in the game tree
        max_depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha_beta : dict(string:float)
            alpha and beta value stored in the dictionary to allow recursive call to modify them.
            two keys: "alpha" and "beta".
        
        Returns
        -------
        float :
            maximum value of the given board
        
        int :
            index of the move that maximize the value in possible legal moves; intialized as -1
        """
        
        if self.terminate_minimax(game, current_depth, max_depth):
           return self.score(game, self), -1
        
        else:
           max_val = float("-inf")
           max_move_id = -1
           possible_moves = game.get_legal_moves()
           
           # Iterate through all possible moves and find maximum one
           for id, move in enumerate(possible_moves):
               attempt_board = game.forecast_move(move)
               attempt_max, _ = self.min_value_ab(attempt_board, current_depth+1, max_depth, alpha_beta)
               if attempt_max > max_val:
                   max_val = attempt_max
                   max_move_id = id
                   
                   # Only difference with simple minimax: compare with current beta and update alpha
                   if max_val > alpha_beta["beta"]:
                       return max_val, max_move_id
                   alpha_beta["alpha"] = max(alpha_beta["alpha"], max_val)
                      
           
           return max_val, max_move_id
    
    def min_value_ab(self, game, current_depth, max_depth,\
                    alpha_beta={"alpha": float("-inf"), "beta": float("inf")}):
        """
        Find the minimum value given the game board using alpha-beta pruning
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        current_depth : int
            An integer indicating the current number of plies to search in the game tree
        max_depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha_beta : dict(string:float)
            alpha and beta value stored in the dictionary to allow recursive call to modify them.
            two keys: "alpha" and "beta".
        
        Returns
        -------
        float :
            minimum value of the given board
        
        int :
            index of the move that minimize the value in possible legal moves; intialized as -1
        """
        
        if self.terminate_minimax(game, current_depth, max_depth):
           return self.score(game, self), -1
        
        else:
           min_val = float("inf")
           min_move_id = -1
           possible_moves = game.get_legal_moves()
           
           # Iterate through all possible moves and find minimum one
           for id, move in enumerate(possible_moves):
               attempt_board = game.forecast_move(move)
               attempt_min, _ = self.max_value_ab(attempt_board, current_depth+1, max_depth, alpha_beta)
               if attempt_min < min_val:
                   min_val = attempt_min
                   min_move_id = id
                   
                   # Only difference with simple minimax: compare with current alpha and update beta
                   if min_val < alpha_beta["alpha"]:
                       return min_val, min_move_id
                   alpha_beta["beta"] = min(alpha_beta["beta"], min_val)
                      
           return min_val, min_move_id