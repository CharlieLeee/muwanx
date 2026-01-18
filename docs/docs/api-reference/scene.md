# Scene API Reference

Scenes represent individual simulations with MuJoCo models and optional policies.

## Class: SceneHandle

```python
class SceneHandle(scene: SceneConfig, builder: Builder)
```

Handle for configuring a scene. Returned by [`ProjectHandle.add_scene()`](project.md#add_scene).

## Methods

### add_policy

```python
def add_policy(
    path: str | Path,
    observation_config: dict,
    action_config: dict
) -> SceneHandle
```

Add an ONNX policy to control this scene.

**Parameters:**

- **path** (`str | Path`): Path to the ONNX model file
- **observation_config** (`dict`): Configuration for observations
- **action_config** (`dict`): Configuration for actions

**Returns:**

- `SceneHandle`: Returns self for method chaining

**Example:**

```python
scene = project.add_scene(model=model, name="Robot")

scene.add_policy(
    path="policy.onnx",
    observation_config={
        "qpos": True,
        "qvel": True
    },
    action_config={
        "type": "position",
        "actuators": ["motor1", "motor2"]
    }
)
```

## Class: SceneConfig

```python
class SceneConfig(
    model: mujoco.MjModel,
    name: str,
    initial_qpos: dict[str, float] | None = None,
    initial_qvel: dict[str, float] | None = None,
    id: str | None = None
)
```

Internal configuration object for a scene.

**Attributes:**

- **model** (`mujoco.MjModel`): The MuJoCo physics model
- **name** (`str`): Display name shown in the UI
- **initial_qpos** (`dict[str, float] | None`): Initial joint positions
- **initial_qvel** (`dict[str, float] | None`): Initial joint velocities
- **id** (`str | None`): URL identifier
- **policy** (`PolicyConfig | None`): Attached policy configuration

## Observation Configuration

The `observation_config` dictionary defines what data is extracted from the simulation.

### Boolean Flags

```python
observation_config = {
    "qpos": True,        # All joint positions
    "qvel": True,        # All joint velocities
    "qacc": False,       # Joint accelerations
    "sensordata": False  # Sensor readings
}
```

### Specific Selection

```python
observation_config = {
    "qpos": ["joint1", "joint2", "joint3"],  # Specific joints
    "qvel": ["joint1", "joint2", "joint3"],
    "sensors": ["touch", "imu"]               # Specific sensors
}
```

### With Normalization

```python
observation_config = {
    "qpos": True,
    "qvel": True,
    "normalize": {
        "qpos_mean": [0.0, 0.5, -0.2],
        "qpos_std": [0.1, 0.2, 0.15],
        "qvel_mean": [0.0, 0.0, 0.0],
        "qvel_std": [1.0, 1.0, 1.0]
    }
}
```

### With Clipping

```python
observation_config = {
    "qpos": True,
    "qvel": True,
    "clip": [-10.0, 10.0]  # Clip all observations to this range
}
```

## Action Configuration

The `action_config` dictionary defines how policy outputs are applied.

### Position Control

```python
action_config = {
    "type": "position",
    "actuators": ["motor1", "motor2", "motor3"]
}
```

### Velocity Control

```python
action_config = {
    "type": "velocity",
    "actuators": ["motor1", "motor2", "motor3"]
}
```

### Torque Control

```python
action_config = {
    "type": "torque",
    "actuators": ["motor1", "motor2", "motor3"]
}
```

### With Scaling and Clipping

```python
action_config = {
    "type": "position",
    "actuators": ["motor1", "motor2", "motor3"],
    "scale": 2.0,           # Scale all actions
    "bias": 0.5,            # Add bias to all actions
    "clip": [-1.0, 1.0]     # Clip all actions
}
```

### Per-Actuator Configuration

```python
action_config = {
    "type": "position",
    "actuators": ["motor1", "motor2"],
    "scale": [1.0, 2.0],      # Different scale per actuator
    "bias": [0.0, 0.5],       # Different bias per actuator
    "clip": [
        [-1.0, 1.0],          # Clip range for motor1
        [-2.0, 2.0]           # Clip range for motor2
    ]
}
```

## Examples

### Scene Without Policy

```python
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

scene = project.add_scene(
    model=model,
    name="Free Falling Ball"
)
```

### Scene With Policy

```python
model = mujoco.MjModel.from_xml_path("robot.xml")

scene = project.add_scene(
    model=model,
    name="Controlled Robot",
    initial_qpos={
        "hip": 0.0,
        "knee": -0.5,
        "ankle": 0.2
    }
)

scene.add_policy(
    path="robot_policy.onnx",
    observation_config={
        "qpos": True,
        "qvel": True,
        "sensors": ["imu", "contact"]
    },
    action_config={
        "type": "position",
        "actuators": ["hip", "knee", "ankle"],
        "scale": 0.5,
        "clip": [-1.0, 1.0]
    }
)
```

### Multiple Scenes with Different Policies

```python
model = mujoco.MjModel.from_xml_path("robot.xml")

# Conservative policy
conservative = project.add_scene(
    model=model,
    name="Conservative Policy",
    id="conservative"
)
conservative.add_policy(
    path="conservative.onnx",
    observation_config={"qpos": True, "qvel": True},
    action_config={"type": "position", "scale": 0.3}
)

# Aggressive policy
aggressive = project.add_scene(
    model=model,
    name="Aggressive Policy",
    id="aggressive"
)
aggressive.add_policy(
    path="aggressive.onnx",
    observation_config={"qpos": True, "qvel": True},
    action_config={"type": "position", "scale": 1.0}
)
```

### Chaining Configuration

```python
# Method chaining
project.add_scene(
    model=model,
    name="Robot Demo"
).add_policy(
    path="policy.onnx",
    observation_config={"qpos": True, "qvel": True},
    action_config={"type": "position"}
)
```

### Complex Observation Setup

```python
scene = project.add_scene(model=model, name="Advanced")

scene.add_policy(
    path="policy.onnx",
    observation_config={
        # Select specific joints
        "qpos": ["hip_fl", "hip_fr", "hip_bl", "hip_br",
                 "knee_fl", "knee_fr", "knee_bl", "knee_br"],
        "qvel": ["hip_fl", "hip_fr", "hip_bl", "hip_br",
                 "knee_fl", "knee_fr", "knee_bl", "knee_br"],

        # Include sensors
        "sensors": ["base_imu", "base_gyro", "base_accel"],

        # Normalize observations
        "normalize": {
            "qpos_mean": [0.0] * 8,
            "qpos_std": [0.5] * 8,
            "qvel_mean": [0.0] * 8,
            "qvel_std": [2.0] * 8
        },

        # Clip extreme values
        "clip": [-50.0, 50.0]
    },
    action_config={
        "type": "position",
        "actuators": ["motor_fl", "motor_fr", "motor_bl", "motor_br",
                      "motor_fl_k", "motor_fr_k", "motor_bl_k", "motor_br_k"]
    }
)
```

## Notes

### Joint Names

Joint and actuator names must exactly match those defined in your MuJoCo model:

```xml
<mujoco>
  <worldbody>
    <body>
      <joint name="hip_joint"/>  <!-- Use "hip_joint" in config -->
      <joint name="knee"/>       <!-- Use "knee" in config -->
    </body>
  </worldbody>
</mujoco>
```

### Initial State

- `initial_qpos`: Sets joint positions at the start
- `initial_qvel`: Sets joint velocities at the start
- Both are optional; defaults to zero if not specified
- Useful for starting in specific configurations

### Policy Requirement

- Scenes can exist without policies (passive simulation)
- Only one policy per scene
- Policy must be in ONNX format

### Observation Order

The observation vector is constructed in this order:

1. `qpos` values
2. `qvel` values
3. `qacc` values (if enabled)
4. `sensordata` values (if enabled)

Ensure your policy expects inputs in this order.

### Action Application

Actions are applied to actuators in the order specified in the `actuators` list.

## Best Practices

1. **Match Training**: Ensure observation/action configs match how the policy was trained
2. **Test Policies**: Verify policy behavior before deployment
3. **Meaningful Names**: Use descriptive scene names
4. **Stable Initials**: Choose stable initial states
5. **Document Configs**: Comment complex observation/action configurations

## See Also

- [ProjectHandle](project.md) - Adding scenes to projects
- [PolicyConfig](policy.md) - Policy configuration details
- [Adding Policies Guide](../user-guide/adding-policies.md) - Detailed guide
- [Creating Scenes Guide](../user-guide/creating-scenes.md) - Scene creation guide
