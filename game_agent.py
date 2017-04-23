"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import sys

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score_3(game, player):
    """
    Results: 42.86%
    ----------
    Discussion:
    This scoring function just blindly evalue the number of possible legal moves left as if
    the player can make move immediately insteading of waiting for the opponent to finish.
    So it doesn't consider locations, nor the future board after opponenet's move.
    It's actually surpiringly win the MM_Improved by 11 to 9.
    """
    return float(len(game.get_legal_moves(player)))
    
def custom_score(game, player):
    """
    Results: 85.00%
    ----------
    Discussion:
    Borrowing from the improved score from lecture, I heavily weighted the number of opponent
    moves left in the game by multiplying by 100.
    """
    if game.is_winner(player):
        return float('inf')
    elif game.is_loser(player):
        return float('-inf')
    else:
        own_moves = len(game.get_legal_moves(player))
        opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
        return float(own_moves - 3*opp_moves)

def custom_score_2(game, player):
    """
    Results: 76.43%
    ----------            
    Discussion:
    This heuristic was an attempt to weight the number of moves left to the player with their
    respective position on the board. By multiplying by the absolute value of the difference
    between their x and y positions and the total width of the board, I am penalizing positions
    in the center of the board and rewarding positions closer to the edges. I am also using the 
    100 weight from custom_score. Weighting the position on the board resulted in an over 6%
    increase over custom_score.
    """
    if game.is_winner(player):
        return float('inf')
    elif game.is_loser(player):
        return float('-inf')
    else:
        width = game.width/2
        position = game.get_player_location(player)
        opp_position = game.get_player_location(game.get_opponent(player))

        own_moves = len(game.get_legal_moves(player))
        opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
        
        position_width_weight = abs(width - position[0])
        position_height_weight = abs(width - position[1])
        
        opp_position_width_weight = abs(width - opp_position[0])
        opp_position_width_height = abs(width - opp_position[1])
        
        return float((own_moves + position_width_weight + position_height_weight) - 100*((opp_moves + opp_position_width_weight + opp_position_width_height)))   
 
 
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
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!
        best_score = float('-inf')
        
        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if not legal_moves:
            return (-1,-1)
        best_move = legal_moves[0]
        
        if game.move_count < 1:   # opening book
            x, y = random.randint(0, game.width), random.randint(0, game.height)
            return (x, y)

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative:
                for i in range (1, sys.maxsize):
                    if self.method == 'alphabeta':
                        if self.time_left() < self.TIMER_THRESHOLD:
                            raise Timeout()
                        score, move = self.alphabeta(game, i)
                        if score > best_score:
                            best_score = score
                            best_move = move
                    else:
                        if self.time_left() < self.TIMER_THRESHOLD:
                            raise Timeout()
                        score, move = self.minimax(game, i)
                        if score > best_score:
                            best_score = score
                            best_move = move            
            else:
                if self.method == 'minimax':
                    best_score, best_move = self.minimax(game, self.search_depth)
                else:
                    best_score, best_move = self.alphabeta(game, self.search_depth)
                     
        except Timeout:
            return best_move

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
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
            
        legal_moves = game.get_legal_moves(game.active_player)
        best_score = float('-inf')
        best_move = (-1, -1)
        
        if not maximizing_player:
            best_score = float('inf')
            
        if not legal_moves:
            return self.score(game, self), best_move
        
        if depth == 0:
            return self.score(game, self), legal_moves[0]
        else:
            for move in legal_moves:
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise Timeout()
                    
                clone = game.forecast_move(move)
                score, _ = self.minimax(clone, depth-1, not maximizing_player)
                if maximizing_player:
                    if score > best_score:
                        best_score = score
                        best_move = move
                else:
                    if score < best_score:
                        best_score = score
                        best_move = move

        return (best_score, best_move)
    
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
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() <= self.TIMER_THRESHOLD:
            raise Timeout()
            
        legal_moves = game.get_legal_moves(game.active_player)
        best_score = float('-inf')

        if not maximizing_player:
            best_score = float('inf')

        if not legal_moves:
            return self.score(game, self), (-1, -1)
        best_move = legal_moves[0]
        
        if depth == 0:
            return self.score(game, self), best_move

        else:
            for move in legal_moves:
                if self.time_left() <= self.TIMER_THRESHOLD:
                    raise Timeout()
                    
                clone = game.forecast_move(move)
                score, _ = self.alphabeta(clone, depth-1, alpha, beta, not maximizing_player)

                if maximizing_player:
                    if score > best_score:
                        best_score = score
                        best_move = move
                    if score >= beta:
                        return score, move
                    alpha = max(alpha, score)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = move
                    if score <= alpha:
                        return score, move
                    beta = min(beta, score)
                    
        return best_score, best_move