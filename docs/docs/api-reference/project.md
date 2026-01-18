# Project API Reference

Projects organize related scenes and appear as sections in the web interface.

## Class: ProjectHandle

```python
class ProjectHandle(project: ProjectConfig, builder: Builder)
```

Handle for configuring a project and adding scenes. Returned by [`Builder.add_project()`](builder.md#add_project).

## Methods

### add_scene

```python
def add_scene(
    model: mujoco.MjModel,
    name: str,
    *,
    initial_qpos: dict[str, float] | None = None,
    initial_qvel: dict[str, float] | None = None,
    id: str | None = None
) -> SceneHandle
```

Add a scene to this project.

**Parameters:**

- **model** (`mujoco.MjModel`): MuJoCo model for the simulation
- **name** (`str`): Display name for the scene in the UI
- **initial_qpos** (`dict[str, float] | None`, optional): Initial joint positions
  - Keys are joint names from the model
  - Values are position values
- **initial_qvel** (`dict[str, float] | None`, optional): Initial joint velocities
  - Keys are joint names from the model
  - Values are velocity values
- **id** (`str | None`, optional): URL identifier for the scene
  - If `None`: auto-generated from name
  - If provided: uses the specified ID

**Returns:**

- `SceneHandle`: Handle for further scene configuration (e.g., adding policies)

**Example:**

```python
import mujoco

# Load model
model = mujoco.MjModel.from_xml_path("robot.xml")

# Add scene with initial state
scene = project.add_scene(
    model=model,
    name="Standing Pose",
    initial_qpos={
        "hip_joint": 0.5,
        "knee_joint": -1.0,
        "ankle_joint": 0.3
    },
    initial_qvel={
        "hip_joint": 0.1
    },
    id="standing"
)
```

## Class: ProjectConfig

```python
class ProjectConfig(name: str, id: str | None = None)
```

Internal configuration object for a project. You typically don't create this directly.

**Attributes:**

- **name** (`str`): Display name of the project
- **id** (`str | None`): URL identifier for the project
- **scenes** (`list[SceneConfig]`): List of scenes in this project

## Examples

### Single Scene Project

```python
import mujoco
import muwanx as mwx

builder = mwx.Builder()

# Simple project with one scene
project = builder.add_project(name="Simple Demo")
model = mujoco.MjModel.from_xml_string("""
<mujoco>
  <worldbody>
    <geom type="plane" size="1 1 0.1"/>
    <body pos="0 0 1">
      <joint type="free"/>
      <geom type="box" size="0.1 0.1 0.1"/>
    </body>
  </worldbody>
</mujoco>
""")

project.add_scene(model=model, name="Falling Box")

app = builder.build()
app.launch()
```

### Multiple Scene Project

```python
# Project with multiple related scenes
project = builder.add_project(name="Locomotion Gaits", id="gaits")

# Walking gait
walk_model = mujoco.MjModel.from_xml_path("walk.xml")
walk_scene = project.add_scene(
    model=walk_model,
    name="Walking",
    id="walk",
    initial_qpos={"speed": 1.0}
)
walk_scene.add_policy(path="walk_policy.onnx", ...)

# Running gait
run_model = mujoco.MjModel.from_xml_path("run.xml")
run_scene = project.add_scene(
    model=run_model,
    name="Running",
    id="run",
    initial_qpos={"speed": 2.0}
)
run_scene.add_policy(path="run_policy.onnx", ...)

# Jumping
jump_model = mujoco.MjModel.from_xml_path("jump.xml")
jump_scene = project.add_scene(
    model=jump_model,
    name="Jumping",
    id="jump"
)
jump_scene.add_policy(path="jump_policy.onnx", ...)
```

### Multiple Projects

```python
builder = mwx.Builder()

# Locomotion project
locomotion = builder.add_project(name="Locomotion", id="locomotion")
locomotion.add_scene(...)
locomotion.add_scene(...)

# Manipulation project
manipulation = builder.add_project(name="Manipulation", id="manipulation")
manipulation.add_scene(...)
manipulation.add_scene(...)

# Research experiments
research = builder.add_project(name="Research", id="research")
research.add_scene(...)
research.add_scene(...)

app = builder.build()
```

### Programmatic Scene Generation

```python
# Generate scenes from data
gaits = [
    ("walk", 1.0, "walk_policy.onnx"),
    ("trot", 1.5, "trot_policy.onnx"),
    ("gallop", 2.5, "gallop_policy.onnx")
]

project = builder.add_project(name="Quadruped Gaits")
base_model = mujoco.MjModel.from_xml_path("quadruped.xml")

for gait_name, speed, policy_path in gaits:
    scene = project.add_scene(
        model=base_model,
        name=gait_name.capitalize(),
        id=gait_name,
        initial_qpos={"target_speed": speed}
    )
    scene.add_policy(
        path=policy_path,
        observation_config={"qpos": True, "qvel": True},
        action_config={"type": "position"}
    )
```

## Project Organization

### URL Routing

Projects appear in URLs:

```python
# First project (default route)
project1 = builder.add_project(name="Main")
# URL: /

# Second project
project2 = builder.add_project(name="Advanced", id="advanced")
# URL: /#/advanced

# Third project
project3 = builder.add_project(name="Experiments", id="exp")
# URL: /#/exp
```

### UI Representation

Projects appear as:

- Navigation menu items
- Separate sections in the interface
- Collapsible groups of scenes

### Best Practices

1. **Logical Grouping**: Group related scenes together
   ```python
   locomotion = builder.add_project(name="Locomotion")
   manipulation = builder.add_project(name="Manipulation")
   ```

2. **Clear Names**: Use descriptive project names
   ```python
   # Good
   project = builder.add_project(name="Bipedal Walking Gaits")

   # Less clear
   project = builder.add_project(name="Project 1")
   ```

3. **Consistent IDs**: Use URL-friendly IDs
   ```python
   # Good
   project = builder.add_project(name="My Project", id="my-project")

   # Works but not ideal
   project = builder.add_project(name="My Project", id="MyProject123")
   ```

4. **Reasonable Size**: Don't create too many projects
   - 1-5 projects: Good
   - 10+ projects: Consider reorganizing

## Notes

### Project vs Scene

- **Project**: Container for related scenes, appears in navigation
- **Scene**: Individual simulation with model and optional policy

### Scene Count

- No hard limit on scenes per project
- Consider UX: too many scenes can be overwhelming
- Group very similar scenes or provide clear differentiation

### Model Reuse

You can reuse models across scenes:

```python
model = mujoco.MjModel.from_xml_path("robot.xml")

# Same model, different initial states
project.add_scene(model=model, name="Config A", initial_qpos={...})
project.add_scene(model=model, name="Config B", initial_qpos={...})
```

## See Also

- [Builder](builder.md) - Creating and managing projects
- [SceneHandle](scene.md) - Configuring individual scenes
- [Creating Scenes Guide](../user-guide/creating-scenes.md) - Detailed scene creation guide
