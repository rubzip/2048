# Solving 2048 via Reinforcement Learning
My goal in this project was to implement a solution of 2048 via RL.

## 🔧Setup
The whole game is implemented using `numpy` and `pygame`, so you should install them.
```
pip install -m requiremts.txt
```
 
## 🚀Running the Game

```
python -u game.py
```

## 🕹️About the game

### 💡Game Logic
All the game logic is implemented in the class `Board`.

### 🏗️Game Implementation


### Reinforcement Learning
The reinforcement learning model consists of a DQN model based on [Playing Atari with Deep Reinforcement Learning paper](https://arxiv.org/pdf/1312.5602.pdf).
In this case the variables of the Q algorithm:
 * A: Set of possible actions (UP, RIGHT, DOWN, LEFT).
 * S: Current state, a 4x4 matrix that consist on the actual game state.
 * R: The reward function.

### Reward Function
#### Punctuation
How near to a maximal punctuation we are.

##### Logarithm Scale
$\displaystyle \dfrac{log(punt + 1)}{log(punt_{max})} \in [0,1]$

##### Linear Scale
$\displaystyle \dfrac{punt}{punt_{max})} \in [0,1]$

#### Num of Zeros
How many zeroes there are on grid over a maximal amount.

$\displaystyle \dfrac{num_{zeros}}{max_{zeros})} \in [0,1]$

#### Distribution
How well distributed there are boxes (ideally the frequency of every number is 1 excepting 0).

$\displaystyle 2 - \frac{1}{N}\sum_{i=1}^{N}f_{i}$

$\displaystyle \left \{ x_{i}: f_{i} \ \ \ \forall x_{i} \neq 0 \right \}$

#### Weights
