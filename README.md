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


### Reward Function
#### Punctuation
##### Logarithm Scale
$\displaystyle \dfrac{log(punt + 1)}{log(punt_{max})} \in [0,1]$
##### Linear Scale
$\displaystyle \dfrac{punt}{punt_{max})} \in [0,1]$
#### Weights
#### Num of Zeros
#### 
