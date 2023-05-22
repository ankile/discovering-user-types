import numpy as np
from src.utils.param_sweep import run_param_sweep
from src.utils.riverswim import make_riverswim_experiment, make_riverswim_transition


def get_start_state(height, width):
    return 1


# Setting the parameters
default_params = dict(
    height=1,
    width=7,
    prob=0.8,
    gamma=0.9,
    big_r=5,
    small_r=1,
)


if __name__ == "__main__":
    """
    River Swim World:
    1D world with a desired reward on right and smaller reward on left.
    Taking the left action is deterministic, but the right action depends on the confidence.
    Default right transitions: 0.6 to the same state, 0.05 to the left, 0.35 to the right state.
    """

    # === Set up the experiment === #
    setup_name = "Riverswim World"

    run_parallel = True

    # Set the number of subplots per row
    cols = 9  # 5, 7, 9

    # Set the number of scales and gammas to use
    granularity = 20  # 5, 10, 20

    # Set up parameters to search over
    probs = np.linspace(0.4, 0.99, granularity)
    gammas = np.linspace(0.4, 0.99, granularity)

    search_parameters = {
        # `cols` number of consecutive integers centered around the default value
        "width": np.arange(5, 5+cols, 1),
        "big_r": np.arange(2, 2+cols, 1),
    }

    rows = len(search_parameters)

    # === End of setup === #

    run_param_sweep(
        setup_name=setup_name,
        default_params=default_params,
        search_parameters=search_parameters,
        create_experiment_func=make_riverswim_experiment,
        transition_matrix_func=make_riverswim_transition,
        rows=rows,
        cols=cols,
        get_start_state=get_start_state,
        granularity=granularity,
        gammas=gammas,
        probs=probs,
        run_parallel=run_parallel,
    )
