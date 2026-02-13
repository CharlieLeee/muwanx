"""mjlab Integration Example - Visualize MuJoCo scenes from all mjlab tasks

Extracts the MuJoCo model from each mjlab task and visualizes them
in the browser using muwanx.
"""

from mjlab.scene import Scene
from mjlab.tasks.registry import list_tasks, load_env_cfg

import muwanx


def main():
    builder = muwanx.Builder()
    project = builder.add_project(name="mjlab Examples")

    for task_id in list_tasks():
        env_cfg = load_env_cfg(task_id)
        env_cfg.scene.num_envs = 1
        scene = Scene(env_cfg.scene, device="cpu")
        mj_model = scene.compile()
        project.add_scene(model=mj_model, name=task_id)

    app = builder.build()
    app.launch()


if __name__ == "__main__":
    main()
