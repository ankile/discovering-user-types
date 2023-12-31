import os

import numpy as np
import seaborn as sns
from src.utils.enums import TransitionMode

from src.worlds.mdp2d import Experiment_2D


def wall_reward(
    height: int,
    width: int,
    wall_width: int,
    wall_height: int,
    neg_mag: float,
    reward_mag: float,
    latent_cost: float = 0,
) -> dict:
    """
    Creates a wall in the middle of the gridworld.

    returns a dictionary of rewards for each state in the gridworld.
    """

    reward_dict = {}
    for i in range(height * width):
        reward_dict[i] = latent_cost  # add latent cost
    wall_end_x = width - 1
    wall_begin_x = wall_end_x - wall_width
    wall_end_y = wall_height
    wall_begin_y = 0
    for i in range(wall_begin_x, wall_end_x):
        for j in range(wall_begin_y, wall_end_y):
            reward_dict[width * j + i] = neg_mag
    reward_dict[width - 1] = reward_mag
    return reward_dict


def make_wall_experiment(
    height,
    width,
    neg_mag,
    reward_mag,
    latent_cost=0,
) -> Experiment_2D:
    wall_dict = wall_reward(
        height,
        width,
        wall_width=width - 2,
        wall_height=height - 1,
        neg_mag=neg_mag,
        reward_mag=reward_mag,
        latent_cost=latent_cost,
    )

    experiment = Experiment_2D(
        height,
        width,
        rewards_dict=wall_dict,
        transition_mode=TransitionMode.SIMPLE,
    )

    return experiment


if __name__ == "__main__":
    default_prob = 0.8
    sns.set()

    setup_name = "Wall"
    setup_name = setup_name.replace(" ", "_").lower()

    if not os.path.exists(f"images/{setup_name}"):
        os.makedirs(f"images/{setup_name}")

    height = 10
    width = 5

    wall_dict = wall_reward(
        height,
        width,
        wall_width=3,
        wall_height=9,
        neg_mag=-10,
        reward_mag=100,
        latent_cost=-1,
    )
    test = Experiment_2D(10, 5, rewards_dict=wall_dict)
    test.mdp.solve(setup_name=setup_name, policy_name="Baseline World")
    test.mdp.reset()

    # MYOPIC EXPERIMENT RUNS:
    for gamma in np.arange(0.5, 0.99, 0.1):
        test.mdp.reset()
        myopic = test.myopic(gamma=gamma)
        test.mdp.solve(
            setup_name=setup_name,
            policy_name="Myopic Agent: \u03B3={:.3f}".format(gamma),
        )

    # UNDERCONFIDENT + OVERCONFIDENT EXPERIMENT RUNS:
    for prob in np.arange(0.05, 0.5, 0.05):
        test.mdp.reset()
        confident = test.confident(action_success_prob=prob)
        if prob < default_prob:
            test.mdp.solve(
                setup_name=setup_name,
                policy_name="Underconfident Agent: p={:.3f}".format(prob),
            )
        elif prob > default_prob:
            test.mdp.solve(
                setup_name=setup_name,
                policy_name="Overconfident Agent: p={:.3f}".format(prob),
            )
