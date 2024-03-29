from Board import Board, Player
from Game import Game
from math import inf
import time

class Bot(object):
    
    bail = False
    transposition_table: dict[int, tuple[int, int, tuple[int, int]]] = {}
    """Hashmap that stores the state of the game as hash(board) : (depth, score, move)
    """

    def __minimax(self, board: Board, depth: int, alpha: int, beta: int, maximizingPlayer: bool, player: Player, start_time: float) -> tuple[float, tuple[int, int]]:
        """Minimax algorithm that uses alpha beta pruning. 

        Args:
            board (Board): state of the board
            depth (int): depth
            alpha (int): alpha
            beta (int): beta
            maximizingPlayer (bool): is maximising player
            player (Player): player

        Returns:
            tuple[float, tuple[int, int]]: score and the best move found
        """
        if time.time() - start_time >= 3.0:
            Bot.bail = True
        board_hash: int = hash((board.color, board.occupied))
        transposition: tuple[int, int, tuple[int, int]] | None = Bot.transposition_table.get(board_hash)
        if transposition and transposition[0] >= depth:
            return transposition[1], transposition[2]

        moves: dict[tuple[int, int], list[tuple[int, int]]] = Game.get_moves(board, player)

        if depth == 0 or len(moves) == 0 or Bot.bail:
            score: float = Game.get_board_score(board, player)
            return score, None
        
        if maximizingPlayer:
            max_eval: int = -inf
            eval: int = -inf
            best_move: tuple[int, int] = ()
            for move in moves:
                next_state: Board = board.deepcopy()
                Game.play(next_state, player, move, moves, True)
                eval, _ = self.__minimax(next_state, depth - 1, alpha, beta, False, Player.get_opponent(player), start_time)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            Bot.transposition_table[board_hash] = (depth, max_eval, best_move)
            return max_eval, best_move
        else:
            min_eval: int = inf
            eval: int = inf
            best_move: tuple[int, int] = ()
            for move in moves:
                next_state: Board = board.deepcopy()
                Game.play(next_state, player, move, moves, True)
                eval, _ = self.__minimax(next_state, depth - 1, alpha, beta, True, Player.get_opponent(player), start_time)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            Bot.transposition_table[board_hash] = (depth, min_eval, best_move)
            return min_eval, best_move        
    
    def bot_move(self, board: Board, time_limit: float = 3.0, depth_limit: int = 7) -> tuple[int, int]:
        """Finds the best possible move using minimax and iterative deeping.

        Args:
            board (Board): game state
            time_limit (float, optional): Time limit. Defaults to 3.0
            deth_limit (int, optional): Depth limit. Defaults to 7

        Returns:
            tuple[int, int]: best possible move found
        """
        best_score: int = -inf
        best_move: tuple[int, int] = ()
        depth: int = 1

        move_count: int = len(Game.get_moves(board, Player.WHITE))

        if move_count == 0:
            return None

        Bot.bail = False
        search_limit: float = (time_limit - 0.25) / move_count
        start_time: float = time.time()
        
        while time.time() - start_time < search_limit and depth <= depth_limit:
            score, move = self.__minimax(board, depth, -inf, inf, True, Player.WHITE, start_time)
            if score > best_score:
                best_score = score
                best_move = move
            if move_count == 1:
                break
            depth += 1            

        
        print(f"Time: {time.time() - start_time}")
        print(f"Depth: {min(depth, depth_limit)}")
        print(f"Move: {best_move}")
                
        return best_move
        