# Creating Scenes

Learn how to create and configure scenes in Muwanx.

## What is a Scene?

A scene is a single simulation instance that combines:

- A MuJoCo physics model
- Initial state configuration
- Optional ONNX policy for control
- Visualization settings

## Basic Scene Creation

The simplest way to create a scene:

```python
import mujoco
import muwanx as mwx

# Create a MuJoCo model
model = mujoco.MjModel.from_xml_string("""
<mujoco>
  <worldbody>
    <geom type="plane" size="1 1 0.1"/>
    <body pos="0 0 1">
      <joint type="free"/>
      <geom type="sphere" size="0.1"/>
    </body>
  </worldbody>
</mujoco>
""")

# Add to a project
builder = mwx.Builder()
project = builder.add_project(name="My Project")
scene = project.add_scene(model=model, name="Bouncing Ball")
```

## Loading Models from Files

### From XML File

```python
model = mujoco.MjModel.from_xml_path("path/to/model.xml")
scene = project.add_scene(model=model, name="My Scene")
```

### From MJCF File

```python
model = mujoco.MjModel.from_xml_path("robot.mjcf")
scene = project.add_scene(model=model, name="Robot Scene")
```

## Setting Initial State

### Initial Joint Positions

Set initial positions for specific joints:

```python
scene = project.add_scene(
    model=model,
    name="Standing Robot",
    initial_qpos={
        "hip_joint": 0.5,
        "knee_joint": -0.8,
        "ankle_joint": 0.3
    }
)
```

Joint names must match those defined in your MuJoCo model.

### Initial Velocities

Set initial velocities:

```python
scene = project.add_scene(
    model=model,
    name="Running Start",
    initial_qvel={
        "root_joint": 1.0  # Moving forward
    }
)
```

## Scene Configuration Options

The `add_scene()` method accepts several configuration options:

```python
scene = project.add_scene(
    model=model,                    # Required: MuJoCo model
    name="Advanced Scene",          # Required: Display name
    initial_qpos={...},            # Optional: Initial positions
    initial_qvel={...},            # Optional: Initial velocities
    id="advanced-scene"            # Optional: URL identifier
)
```

### Scene ID

The scene ID is used in URL routing. If not provided, it's automatically generated from the name:

```python
# Explicit ID
scene = project.add_scene(model=model, name="My Scene", id="custom-id")
# URL: /#/project-id/custom-id

# Auto-generated ID (name converted to lowercase-with-hyphens)
scene = project.add_scene(model=model, name="My Scene")
# URL: /#/project-id/my-scene
```

## Complex Models

### Models with Meshes

If your model references external mesh files:

```python
# Ensure the model's XML has correct relative paths
model = mujoco.MjModel.from_xml_path("models/robot/robot.xml")

# Muwanx will automatically include referenced mesh files
scene = project.add_scene(model=model, name="Robot with Meshes")
```

### Models with Assets

For models with multiple assets (textures, meshes):

```
my_project/
├── script.py
└── assets/
    ├── robot.xml
    ├── meshes/
    │   ├── body.stl
    │   └── arm.stl
    └── textures/
        └── skin.png
```

MuJoCo automatically resolves relative paths from the XML file location.

## Multiple Scenes in One Project

Create variations of a simulation:

```python
builder = mwx.Builder()
project = builder.add_project(name="Gait Experiments")

# Scene 1: Walking
model_walk = mujoco.MjModel.from_xml_path("walk.xml")
project.add_scene(model=model_walk, name="Walk", id="walk")

# Scene 2: Running
model_run = mujoco.MjModel.from_xml_path("run.xml")
project.add_scene(model=model_run, name="Run", id="run")

# Scene 3: Jumping
model_jump = mujoco.MjModel.from_xml_path("jump.xml")
project.add_scene(model=model_jump, name="Jump", id="jump")
```

Users can switch between scenes using the UI.

## Scene with Policy

Add an ONNX policy to control the simulation:

```python
scene = project.add_scene(
    model=model,
    name="Controlled Robot"
)

# Add policy to the scene
scene.add_policy(
    path="policy.onnx",
    observation_config={
        "qpos": True,
        "qvel": True
    },
    action_config={
        "type": "position",
        "actuators": ["actuator1", "actuator2"]
    }
)
```

Learn more in [Adding Policies](adding-policies.md).

## Tips and Best Practices

### Model Design

1. **Keep it Simple**: Browser performance is limited compared to desktop applications
2. **Optimize Contacts**: Reduce unnecessary collision meshes
3. **Use Appropriate Timesteps**: Balance accuracy and performance

### Initial States

1. **Test Stability**: Ensure initial configurations are physically stable
2. **Use Meaningful Defaults**: Set initial states that demonstrate the desired behavior
3. **Document Joint Names**: Keep a reference of joint names from your model

### Scene Organization

1. **Logical Grouping**: Group related scenes in the same project
2. **Clear Naming**: Use descriptive names that explain what each scene demonstrates
3. **Consistent Styling**: Maintain consistent visual styling across scenes

### Performance Considerations

Browser-based simulation has limitations:

- **Model Complexity**: Keep models reasonably sized
- **Contact Points**: Limit the number of contacts
- **Rendering**: High-poly meshes can impact performance
- **Mobile Devices**: Test on mobile if targeting those platforms

### Testing

Always test your scenes before deployment:

```python
app = builder.build()
app.launch()  # Test locally first
```

Check:

- Model loads correctly
- Initial state is stable
- Physics behaves as expected
- Performance is acceptable
- Works on target devices

## Examples

### Example 1: Simple Pendulum

```python
model = mujoco.MjModel.from_xml_string("""
<mujoco>
  <worldbody>
    <body pos="0 0 1">
      <joint name="hinge" type="hinge" axis="1 0 0"/>
      <geom type="capsule" size="0.02" fromto="0 0 0 0 0 -0.5"/>
      <body pos="0 0 -0.5">
        <geom type="sphere" size="0.1" mass="1"/>
      </body>
    </body>
  </worldbody>
</mujoco>
""")

scene = project.add_scene(
    model=model,
    name="Pendulum",
    initial_qpos={"hinge": 1.0}  # Start at angle
)
```

### Example 2: Quadruped Robot

```python
model = mujoco.MjModel.from_xml_path("quadruped.xml")

scene = project.add_scene(
    model=model,
    name="Quadruped Standing",
    initial_qpos={
        "fl_hip": 0.2,
        "fl_knee": -0.4,
        "fr_hip": 0.2,
        "fr_knee": -0.4,
        "bl_hip": 0.2,
        "bl_knee": -0.4,
        "br_hip": 0.2,
        "br_knee": -0.4
    }
)
```

### Example 3: Multiple Variations

```python
base_model = mujoco.MjModel.from_xml_path("robot.xml")

# Light robot
project.add_scene(
    model=base_model,
    name="Light Configuration",
    id="light"
)

# Heavy robot
project.add_scene(
    model=base_model,
    name="Heavy Configuration",
    id="heavy",
    initial_qpos={"body_mass": 2.0}
)
```

## Next Steps

- [Adding Policies](adding-policies.md) - Add AI control to your scenes
- [API Reference: Scene](../api-reference/scene.md) - Detailed scene API documentation
- [Examples](../examples/custom-models.md) - More complete examples
