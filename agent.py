import tensorflow as tf

from tf_agents.agents.dqn import dqn_agent
from tf_agents.networks import sequential
from tf_agents.utils import common
from tf_agents.trajectories import TimeStep
from tf_agents.specs import BoundedArraySpec
from tf_agents.specs import ArraySpec

q_net = sequential.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(4)
])

optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
train_step_counter = tf.Variable(0)

time_step_spec = TimeStep(
    step_type=ArraySpec(shape=(), dtype='int32', name='step_type'),
    reward=ArraySpec(shape=(), dtype='int32', name='reward'),
    discount=BoundedArraySpec(shape=(), dtype='float32', name='discount', minimum=0., maximum=1.),
    observation=BoundedArraySpec(shape=(16,), dtype='int32', name='observation', minimum=[0 for _ in range(16)], maximum=[20 for _ in range(16)])
)

action_spec = BoundedArraySpec(
    shape=(), dtype='int32', name='action', minimum=0, maximum=3
)


agent = dqn_agent.DqnAgent(
    time_step_spec,
    action_spec,
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=train_step_counter)

agent.initialize()

class Agent:
    def __init__(self) -> None:
        self.n_states = 16
        self.n_actions = 4
        self.fc_layers = [64, 32, 16]

    def init_qmodel(self):
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Input(shape=(16,)),
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dense(32, activation='relu'),
                tf.keras.layers.Dense(4, activation='softmax')
            ])
        return model

