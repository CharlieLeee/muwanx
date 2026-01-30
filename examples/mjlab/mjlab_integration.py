"""MJLab Integration Example - All Tasks Policy Observation Explorer

This script loads EVERY task registered in mjlab and collects
detailed policy observation information into variables/dictionaries.
"""

from typing import Any, Dict

from mjlab.tasks.registry import list_tasks, load_env_cfg, load_rl_cfg
from rich.console import Console
from rich.table import Table

import muwanx


def get_all_policy_observations() -> Dict[str, Dict[str, Any]]:
    """
    Collect policy observation information for ALL mjlab registered tasks.

    Returns:
        Dict[task_id → {
            'terms': dict[term_name → term_cfg],
            'policy_group': ObservationGroupCfg,
            'error': str or None
        }]
    """
    all_policy_info: Dict[str, Dict[str, Any]] = {}
    console = Console()

    for task_id in list_tasks():
        try:
            env_cfg = load_env_cfg(task_id)
            policy_group = (
                env_cfg.observations.get("policy")
                if isinstance(env_cfg.observations, dict)
                else None
            )

            if policy_group is None:
                all_policy_info[task_id] = {
                    "terms": {},
                    "policy_group": None,
                    "error": "No policy observation group found",
                }
                continue

            all_policy_info[task_id] = {
                "terms": policy_group.terms,
                "policy_group": policy_group,
                "error": None,
            }

        except Exception as e:
            console.print(f"[yellow]Warning: Failed to load {task_id}: {e}[/yellow]")
            all_policy_info[task_id] = {
                "terms": {},
                "policy_group": None,
                "error": str(e),
            }

    return all_policy_info


def print_policy_observation_summary(all_obs_info: Dict[str, Dict[str, Any]]):
    """Print a beautiful summary table of policy observations for all tasks"""
    console = Console()
    table = Table(
        title="MJLab Tasks - Policy Observation Summary",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Task ID", style="magenta", no_wrap=True)
    table.add_column("Num Terms", justify="right")
    table.add_column("Concatenated?", justify="center")
    table.add_column("Status", style="dim")

    for task_id, info in sorted(all_obs_info.items()):
        status = "[green]OK[/green]" if info["error"] is None else "[red]Error[/red]"

        if info["policy_group"] is not None:
            num_terms = len(info["terms"])
            concatenated = info["policy_group"].concatenate_terms
        else:
            num_terms = 0
            concatenated = False

        table.add_row(
            task_id,
            str(num_terms),
            "Yes" if concatenated else "No",
            status,
        )

    console.print(table)


def print_detailed_observation_info(task_id: str, obs_info: Dict[str, Any]):
    """Print detailed information about observation configuration for a task"""
    console = Console()

    if obs_info["error"] is not None:
        console.print(f"[red]Error loading task {task_id}: {obs_info['error']}[/red]")
        return

    policy_group = obs_info["policy_group"]
    terms = obs_info["terms"]

    if policy_group is None or not terms:
        console.print(f"[yellow]No observation data for {task_id}[/yellow]")
        return

    # Print group-level configuration
    console.print("\n[bold cyan]ObservationGroupCfg (Group-level Settings)[/bold cyan]")
    console.print(f"  concatenate_terms:    {policy_group.concatenate_terms}")
    console.print(f"  concatenate_dim:      {policy_group.concatenate_dim}")
    console.print(f"  enable_corruption:    {policy_group.enable_corruption}")
    console.print(f"  history_length:       {policy_group.history_length}")
    console.print(f"  flatten_history_dim:  {policy_group.flatten_history_dim}")
    console.print(f"  nan_policy:           {policy_group.nan_policy}")
    console.print(f"  nan_check_per_term:   {policy_group.nan_check_per_term}")

    # Print each term's configuration
    console.print(f"\n[bold cyan]ObservationTermCfg × {len(terms)} Terms[/bold cyan]")

    for idx, (term_name, term_cfg) in enumerate(terms.items(), 1):
        console.print(f"\n  [{idx}] {term_name}")

        # Compute function
        compute_fn = getattr(term_cfg, "func", None)
        fn_name = compute_fn.__name__ if compute_fn else "Unknown"
        console.print(f"      compute_fn:           {fn_name}")

        # Noise
        noise = getattr(term_cfg, "noise", None)
        if noise is None:
            console.print("      noise:                None")
        else:
            noise_type = type(noise).__name__
            console.print(f"      noise:                {noise_type}")
            # Show some noise details if available
            if hasattr(noise, "n_min"):
                console.print(
                    f"                          range: [{noise.n_min}, {noise.n_max}]"
                )

        # Clip and scale
        clip = getattr(term_cfg, "clip", None)
        scale = getattr(term_cfg, "scale", None)
        console.print(f"      clip:                 {clip}")
        console.print(f"      scale:                {scale}")

        # Delay parameters
        console.print(
            f"      delay_min_lag:        {getattr(term_cfg, 'delay_min_lag', 0)}"
        )
        console.print(
            f"      delay_max_lag:        {getattr(term_cfg, 'delay_max_lag', 0)}"
        )
        console.print(
            f"      delay_per_env:        {getattr(term_cfg, 'delay_per_env', True)}"
        )
        console.print(
            f"      delay_hold_prob:      {getattr(term_cfg, 'delay_hold_prob', 0.0)}"
        )
        console.print(
            f"      delay_update_period:  {getattr(term_cfg, 'delay_update_period', 0)}"
        )
        console.print(
            f"      delay_per_env_phase:  {getattr(term_cfg, 'delay_per_env_phase', True)}"
        )

        # History
        console.print(
            f"      history_length:       {getattr(term_cfg, 'history_length', 0)}"
        )
        console.print(
            f"      flatten_history_dim:  {getattr(term_cfg, 'flatten_history_dim', True)}"
        )


def get_all_rl_configs() -> Dict[str, Dict[str, Any]]:
    """
    Collect RL configuration information for ALL mjlab registered tasks.

    Returns:
        Dict[task_id → {
            'rl_cfg': RslRlOnPolicyRunnerCfg,
            'error': str or None
        }]
    """
    all_rl_info: Dict[str, Dict[str, Any]] = {}
    console = Console()

    for task_id in list_tasks():
        try:
            rl_cfg = load_rl_cfg(task_id)

            if rl_cfg is None:
                all_rl_info[task_id] = {
                    "rl_cfg": None,
                    "error": "No RL configuration found",
                }
                continue

            all_rl_info[task_id] = {
                "rl_cfg": rl_cfg,
                "error": None,
            }

        except Exception as e:
            console.print(
                f"[yellow]Warning: Failed to load RL config for {task_id}: {e}[/yellow]"
            )
            all_rl_info[task_id] = {
                "rl_cfg": None,
                "error": str(e),
            }

    return all_rl_info


def print_rl_config_summary(all_rl_info: Dict[str, Dict[str, Any]]):
    """Print a summary table of RL configurations for all tasks"""
    console = Console()
    table = Table(
        title="MJLab Tasks - RL Configuration Summary",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Task ID", style="magenta", no_wrap=True)
    table.add_column("Algorithm", justify="center")
    table.add_column("Num Steps", justify="right")
    table.add_column("Max Iters", justify="right")
    table.add_column("Learning Rate", justify="right")
    table.add_column("Status", style="dim")

    for task_id, info in sorted(all_rl_info.items()):
        status = "[green]OK[/green]" if info["error"] is None else "[red]Error[/red]"

        if info["rl_cfg"] is not None:
            rl_cfg = info["rl_cfg"]
            algorithm = getattr(rl_cfg, "algorithm", None)
            algorithm_name = (
                getattr(algorithm, "class_name", "Unknown")
                if algorithm is not None
                else "N/A"
            )

            num_steps = str(getattr(rl_cfg, "num_steps_per_env", "N/A"))
            max_iters = str(getattr(rl_cfg, "max_iterations", "N/A"))

            learning_rate = "N/A"
            if algorithm is not None:
                learning_rate = str(getattr(algorithm, "learning_rate", "N/A"))
        else:
            algorithm_name = "N/A"
            num_steps = "N/A"
            max_iters = "N/A"
            learning_rate = "N/A"

        table.add_row(
            task_id,
            algorithm_name,
            num_steps,
            max_iters,
            learning_rate,
            status,
        )

    console.print(table)


def print_detailed_rl_config_info(task_id: str, rl_info: Dict[str, Any]):
    """Print detailed information about RL configuration for a task"""
    console = Console()

    if rl_info["error"] is not None:
        console.print(
            f"[red]Error loading RL config for {task_id}: {rl_info['error']}[/red]"
        )
        return

    rl_cfg = rl_info["rl_cfg"]

    if rl_cfg is None:
        console.print(f"[yellow]No RL configuration for {task_id}[/yellow]")
        return

    # Print RslRlOnPolicyRunnerCfg (top-level config)
    console.print(
        "\n[bold cyan]RslRlOnPolicyRunnerCfg (Top-level Settings)[/bold cyan]"
    )
    runner_attrs = [
        "seed",
        "num_steps_per_env",
        "max_iterations",
        "save_interval",
        "experiment_name",
        "run_name",
        "logger",
        "wandb_project",
        "resume",
        "load_run",
        "load_checkpoint",
        "clip_actions",
    ]
    for attr in runner_attrs:
        val = getattr(rl_cfg, attr, None)
        if val is not None:
            console.print(f"  {attr:25} {val}")

    # Print Policy configuration
    policy = getattr(rl_cfg, "policy", None)
    if policy is not None:
        console.print("\n[bold cyan]RslRlPpoActorCriticCfg[/bold cyan]")
        console.print(
            f"  class_name:                {getattr(policy, 'class_name', 'N/A')}"
        )

        policy_attrs = [
            "init_noise_std",
            "noise_std_type",
            "actor_obs_normalization",
            "critic_obs_normalization",
            "actor_hidden_dims",
            "critic_hidden_dims",
            "activation",
        ]
        for attr in policy_attrs:
            val = getattr(policy, attr, None)
            if val is not None:
                console.print(f"  {attr:25} {val}")

    # Print Algorithm configuration
    algorithm = getattr(rl_cfg, "algorithm", None)
    if algorithm is not None:
        console.print("\n[bold cyan]RslRlPpoAlgorithmCfg[/bold cyan]")
        console.print(
            f"  class_name:                {getattr(algorithm, 'class_name', 'N/A')}"
        )

        algorithm_attrs = [
            "num_learning_epochs",
            "num_mini_batches",
            "learning_rate",
            "schedule",
            "gamma",
            "lam",
            "entropy_coef",
            "desired_kl",
            "max_grad_norm",
            "value_loss_coef",
            "use_clipped_value_loss",
            "clip_param",
            "normalize_advantage_per_mini_batch",
        ]
        for attr in algorithm_attrs:
            val = getattr(algorithm, attr, None)
            if val is not None:
                console.print(f"  {attr:30} {val}")

    # Print observation groups
    obs_groups = getattr(rl_cfg, "obs_groups", {})
    if obs_groups:
        console.print("\n[bold cyan]Observation Groups[/bold cyan]")
        for group_name, group_dims in obs_groups.items():
            console.print(f"  {group_name:25} {group_dims}")


def main():
    # Create muwanx project
    builder = muwanx.Builder()
    project = builder.add_project(name="MJLab All Tasks Observation & RL Explorer")  # noqa: F841

    # target_task_id = "Mjlab-Velocity-Flat-Unitree-G1"
    target_task_id = "Mjlab-Tracking-Flat-Unitree-G1"

    # ═══════════════════════════════════════════════════════════════════════════════
    # SECTION 1: OBSERVATIONS
    # ═══════════════════════════════════════════════════════════════════════════════

    # 1. Load ALL policy observation info into a variable
    all_policy_obs_info = get_all_policy_observations()

    # 2. Print nice summary
    print("\n" + "=" * 80)
    print("MJLab All Registered Tasks - Policy Observation Overview")
    print("=" * 80)
    print_policy_observation_summary(all_policy_obs_info)

    # Example: Unitree G1 Velocity task - detailed observation view
    print("\n" + "=" * 80)
    print("DETAILED EXAMPLE: Unitree G1 Velocity Task - Observations")
    print("=" * 80)
    g1_velocity_obs = all_policy_obs_info.get(target_task_id)
    if g1_velocity_obs:
        print_detailed_observation_info(target_task_id, g1_velocity_obs)

    # ═══════════════════════════════════════════════════════════════════════════════
    # SECTION 2: RL CONFIGURATIONS
    # ═══════════════════════════════════════════════════════════════════════════════

    # 1. Load ALL RL config info into a variable
    all_rl_info = get_all_rl_configs()

    # 2. Print nice summary
    print("\n\n" + "=" * 80)
    print("MJLab All Registered Tasks - RL Configuration Overview")
    print("=" * 80)
    print_rl_config_summary(all_rl_info)

    # Example: Unitree G1 Velocity task - detailed RL config view
    print("\n" + "=" * 80)
    print("DETAILED EXAMPLE: Unitree G1 Velocity Task - RL Configuration")
    print("=" * 80)
    g1_velocity_rl = all_rl_info.get(target_task_id)
    if g1_velocity_rl:
        print_detailed_rl_config_info(target_task_id, g1_velocity_rl)


if __name__ == "__main__":
    main()
