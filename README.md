# Discovering User Types: _Mapping User Traits by Task-Specific Behaviors in Reinforcement Learning_

Source code for experiments for [our paper](https://arxiv.org/pdf/2307.08169.pdf) at the [ICML 2023](https://icml.cc/Conferences/2023) workshops on [AI & Human-Computer Interaction](https://sites.google.com/view/aihci/home) (best paper runner-up), [Theory of Mind](https://tomworkshop.github.io/), and [Interactive Learning with Implicit Human Feedback](https://interactive-learning-implicit-feedback.github.io/).

[Read the paper](https://arxiv.org/pdf/2307.08169.pdf) and consider citing our work if you find it helpful:

```bibtex
@article{ankile2023discovering,
  title={Discovering User Types: Mapping User Traits by Task-Specific Behaviors in Reinforcement Learning},
  author={Ankile, Lars L and Ham, Brian S and Mao, Kevin and Shin, Eura and Swaroop, Siddharth and Doshi-Velez, Finale and Pan, Weiwei},
  journal={arXiv preprint arXiv:2307.08169},
  year={2023}
}
```

**Abstract:**

_When assisting human users in reinforcement learning (RL), we can represent users as RL agents and study key parameters, called user traits, to inform intervention design. We study the relationship between user behaviors (policy classes) and user traits. Given an environment, we introduce an intuitive tool for studying the breakdown of "user types": broad sets of traits that result in the same behavior. We show that seemingly different real-world environments admit the same set of user types and formalize this observation as an equivalence relation defined on environments. By transferring intervention design between environments within the same equivalence class, we can help rapidly personalize interventions._



## Quickstart

(This current quickstart assumes a Unix-based OS, if you're on Windows, please adapt the steps to the appropriate Windows analog.)

**Clone the repo to your local machine.**

If you're authorizing the `git` cli with an app password, you can use HTTPS:

`git clone https://github.com/ankile/discovering-user-types.git`

Otherwise, SSH is probably advisable:

`git clone git@github.com:ankile/discovering-user-types.git`


**Make a virtual environment**

Make sure you have Python 3 installed (preferably 3.10 or above). If you do not, may I suggest using [Homebrew](brew.sh) to install it?

To create the virtual environment, run (I prefer to explicitly write the version, e.g., `python3.11`, to avoid surprises):

`python3 -m venv venv`

**Activate the environment**

`source venv/bin/activate && pip install --upgrade pip`

(This command also upgrades `pip` because it _always_ complains about being outdated, so why wait?)


**Install the required packages**

`pip install -r requirements.txt`


**Run experiments**

If you want to run, let's say, the perturbation plot for the Cliff world, you can first edit the relevant fields in the `src/param_sweeps/cliff_world.py`:

```python
  run_parallel = True

  # Set the number of subplots per row
  cols = 4  # 5, 7, 9

  # Define the default parameters
  default_params = {
      "height": 5,
      "width": 9,
      "reward_mag": 1e2,
      "neg_mag": -1e8,
      "latent_reward": 0,
  }

  # Define the search space
  search_parameters = {
      "width": np.linspace(4, 10, cols).round().astype(int),
      "height": np.linspace(4, 10, cols).round().astype(int),
      "reward_mag": np.linspace(100, 500, cols),
  }

  # Set the number of scales and gammas to use
  granularity = 20  # 5, 10, 20

  # Set up parameters to search over
  probs = np.linspace(0.4, 0.99, granularity)
  gammas = np.linspace(0.4, 0.99, granularity)
```

When you're happy with all the settings, run the code in the `if __name__ == "__main__":` block:

`python -m src.param_sweeps.cliff_world`

(Mark the lack of `.py` at the end.)

**Next steps**

Happy `hacking`!

