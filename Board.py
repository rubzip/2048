import numpy as np
from tf_agents.trajectories import TimeStep 
import tensorflow as tf

class Board:
    def __init__(self, N: int=4, grid: np.array=None) -> None:
        if grid is None:
            self.N = N
            self.grid = np.zeros([N, N], np.int8)
            self.add_2()
        else:
            self.N = len(grid)
            self.grid = grid

        self.possible_moves, self.results = self.check_possible_moves(return_values=True)
        self.game_over = self.is_game_over(return_values=True)
        self.win = self.is_win(return_values=True)

        self.POINTS = {n: (n-1)*(2**n) for n in range(1, 20)}
        self.POINTS[0] = 0

        self.punctuation = self.get_punctuation(return_values=True)
        self.t_step = 0
    
    def add_2(self, return_values=False) -> bool:
        possible = self.grid==0
        indexes = np.where(possible)
        n = len(indexes[0])
        self.game_over = n==0
        if not self.game_over:
            m = np.random.randint(n)
            i, j = indexes[0][m], indexes[1][m]
            self.grid[i, j] = 1
        
        if return_values:
            return self.game_over, self.grid
        
    def __str__(self):
        return str(self.grid)
    
    def __eq__(self, other_board=None, other_grid: np.array=None):
        """
            Compares the Board with other Board, or with a grid
        """
        if other_board is not None:
            return (self.grid==other_board.grid).all()
        else:
            return (self.grid==other_grid).all()
    
    def left_slide(self, v: np.array) -> np.array:
        # Remove zeros
        v_z = v[v!=0]
        # Join between equal numbers
        n = len(v_z)
        for i in range(n-1):
            if v_z[i]==v_z[i+1]:
                v_z[i] += 1
                v_z[i+1] = 0
        # Remove zeros
        v_z = v_z[v_z!=0]
        n = len(v_z)
        # Padding
        return np.pad(v_z, (0, self.N-n))

    def right_slide(self, v: np.array) -> np.array:
        # Remove zeros
        v_z = v[v!=0]
        # Join between equal numbers
        n = len(v_z)
        for i in range(n-1, 0, -1):
            if v_z[i]==v_z[i-1]:
                v_z[i] += 1
                v_z[i-1] = 0
        # Remove zeros
        v_z = v_z[v_z!=0]
        n = len(v_z)
        # Padding
        return np.pad(v_z, (self.N-n, 0))

    def move_left(self) -> np.array:
        grid_copy = self.grid.copy()
        for i in range(self.N):
            grid_copy[i, :] = self.left_slide(grid_copy[i, :])
        return grid_copy
  
    def move_right(self) -> np.array:
        grid_copy = self.grid.copy()
        for i in range(self.N):
            grid_copy[i, :] = self.right_slide(grid_copy[i, :])
        return grid_copy
    
    def move_up(self) -> np.array:
        grid_copy = self.grid.copy()
        for i in range(self.N):
            grid_copy[:, i] = self.left_slide(self.grid[:, i])
        return grid_copy

    def move_down(self) -> np.array:
        grid_copy = self.grid.copy()
        for i in range(self.N):
            grid_copy[:, i] = self.right_slide(grid_copy[:, i])
        return grid_copy
    
    def check_possible_moves(self, return_values=False) -> list:
        self.results = {
            'up': self.move_up(),
            'down': self.move_down(),
            'left': self.move_left(),
            'right': self.move_right(),
            }
        self.possible_moves = []
        for fun_name, result in self.results.items():
            if not (result==self.grid).all():
                self.possible_moves.append(fun_name)
        
        if return_values:
            return self.possible_moves, self.results
    
    def is_game_over(self, return_values=False) -> bool:
        self.game_over = (len(self.possible_moves)==0)
        if return_values:
            return self.game_over
    
    def is_win(self, return_values=False, goal=11) -> bool:
        self.win = (self.grid >= goal).any()
        if return_values:
            return self.win

    def move(self, movement: str, return_values=False):
        if movement in self.possible_moves:
            self.grid = self.results[movement]
        else:
            # raise Exception(f"Movement {movement} is not allowed, try with: {self.possible_moves}")
            print(f"Movement {movement} is not allowed, try with: {self.possible_moves}")
        if return_values:
            return self.grid
    
    def get_punctuation(self, return_values=False):
        vals, freqs = np.unique(self.grid, return_counts=True)
        self.punctuation = sum([self.POINTS.get(val, 0)*freq for val, freq in zip(vals, freqs)])

        if return_values:
            return self.punctuation

    def get_reward(self, max_punctuation: int, max_zeros: int, weights: dict, logarithmic_punctuation: bool=True):
        total_reward = 0.

        if self.win:
            total_reward += weights.get('win', 0)
        elif self.game_over:
            total_reward += weights.get('game over', 0)
        
        vals, freqs = np.unique(self.grid, return_counts=True)
        num_zeros = freqs[vals==0].sum()
        avg_freq = freqs[vals!=0].mean()

        if logarithmic_punctuation:
            total_reward += between_0_and_1(np.log(self.punctuation + 1)/np.log(max_punctuation)) * weights.get('punctuation', 0)
        else:
            total_reward += between_0_and_1(self.punctuation/max_punctuation) * weights.get('punctuation', 0)
        
        total_reward += between_0_and_1(num_zeros/max_zeros) * weights.get('zeros', 0)
        total_reward += between_0_and_1(2 - avg_freq) * weights.get('distribution', 0)

        return total_reward
    
    def get_time_step(self):
        discount = int(not (self.is_game_over() or self.is_win()))
        
        return TimeStep(
            step_type=tf.constant(self.t_step),
            reward=tf.constant(self.get_reward()),
            discount=tf.constant(discount),
            observation=self.grid.reshape(-1)
        )


def between_0_and_1(num):
    return max(0, min(1, num))