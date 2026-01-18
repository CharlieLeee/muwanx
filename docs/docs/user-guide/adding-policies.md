# Adding Policies

Learn how to add ONNX policies to control your simulations with neural networks.

## What is a Policy?

A policy is a neural network that:

- Observes the current state of the simulation
- Computes actions based on those observations
- Controls actuators in real-time

In Muwanx, policies are ONNX models that run entirely in the browser using ONNX Runtime Web.

## Prerequisites

Before adding a policy, you need:

1. A trained neural network exported to ONNX format
2. Knowledge of what observations your policy expects
3. Understanding of what actions it outputs

## Basic Policy Addition

```python
scene = project.add_scene(model=model, name="Controlled Robot")

scene.add_policy(
    path="policy.onnx",
    observation_config={
        "qpos": True,
        "qvel": True
    },
    action_config={
        "type": "position"
    }
)
```

## Exporting Policies to ONNX

### From PyTorch

```python
import torch
import torch.onnx

# Assume you have a trained policy
policy = YourPolicyClass()
policy.load_state_dict(torch.load("policy.pth"))
policy.eval()

# Create dummy input matching your observation space
dummy_input = torch.randn(1, observation_dim)

# Export to ONNX
torch.onnx.export(
    policy,
    dummy_input,
    "policy.onnx",
    input_names=["observation"],
    output_names=["action"],
    dynamic_axes={
        "observation": {0: "batch_size"},
        "action": {0: "batch_size"}
    }
)
```

### From TensorFlow

```python
import tf2onnx
import tensorflow as tf

# Load your trained model
model = tf.keras.models.load_model("policy.h5")

# Convert to ONNX
spec = (tf.TensorSpec((None, observation_dim), tf.float32, name="observation"),)
tf2onnx.convert.from_keras(model, input_signature=spec, output_path="policy.onnx")
```

### From JAX

```python
import jax
import jax.numpy as jnp
from jax2onnx import convert

# Your JAX policy function
def policy_fn(params, obs):
    return network_apply(params, obs)

# Convert to ONNX
dummy_obs = jnp.zeros((1, observation_dim))
convert(
    lambda obs: policy_fn(params, obs),
    dummy_obs,
    "policy.onnx"
)
```

## Observation Configuration

The observation configuration defines what data from the simulation is passed to your policy.

### Standard Observations

```python
observation_config = {
    "qpos": True,        # Joint positions
    "qvel": True,        # Joint velocities
    "qacc": False,       # Joint accelerations (optional)
    "sensordata": False  # Sensor readings (optional)
}
```

### Specific Joints

Select specific joints:

```python
observation_config = {
    "qpos": ["hip", "knee", "ankle"],  # Only these joints
    "qvel": ["hip", "knee", "ankle"]
}
```

### Sensor Data

Include sensor readings:

```python
observation_config = {
    "qpos": True,
    "qvel": True,
    "sensors": ["touch_sensor", "imu", "gyro"]
}
```

### Custom Processing

For custom observation processing:

```python
observation_config = {
    "qpos": True,
    "qvel": True,
    "normalize": True,       # Normalize observations
    "clip": [-10.0, 10.0]   # Clip values
}
```

## Action Configuration

The action configuration defines how policy outputs are applied to the simulation.

### Position Control

```python
action_config = {
    "type": "position",
    "actuators": ["motor1", "motor2", "motor3"]
}
```

The policy outputs desired positions for each actuator.

### Velocity Control

```python
action_config = {
    "type": "velocity",
    "actuators": ["motor1", "motor2", "motor3"]
}
```

The policy outputs desired velocities.

### Torque Control

```python
action_config = {
    "type": "torque",
    "actuators": ["motor1", "motor2", "motor3"]
}
```

The policy outputs desired torques directly.

### Action Scaling

Scale policy outputs:

```python
action_config = {
    "type": "position",
    "actuators": ["motor1", "motor2", "motor3"],
    "scale": 2.0,           # Multiply outputs by 2
    "bias": 0.5,            # Add 0.5 to outputs
    "clip": [-1.0, 1.0]     # Clip to range
}
```

## Complete Example

Here's a full example with a locomotion policy:

```python
import mujoco
import muwanx as mwx

# Load model
model = mujoco.MjModel.from_xml_path("quadruped.xml")

# Create builder and project
builder = mwx.Builder()
project = builder.add_project(name="Quadruped Locomotion")

# Add scene
scene = project.add_scene(
    model=model,
    name="Walking Gait",
    initial_qpos={
        "fl_hip": 0.0,
        "fl_knee": 0.5,
        "fr_hip": 0.0,
        "fr_knee": 0.5,
        "bl_hip": 0.0,
        "bl_knee": 0.5,
        "br_hip": 0.0,
        "br_knee": 0.5
    }
)

# Add policy
scene.add_policy(
    path="quadruped_policy.onnx",
    observation_config={
        "qpos": True,
        "qvel": True,
        "sensors": ["base_imu"]
    },
    action_config={
        "type": "position",
        "actuators": [
            "fl_hip", "fl_knee",
            "fr_hip", "fr_knee",
            "bl_hip", "bl_knee",
            "br_hip", "br_knee"
        ],
        "scale": 0.5,
        "clip": [-1.0, 1.0]
    }
)

# Build and launch
app = builder.build()
app.launch()
```

## Policy Testing

### Local Testing

Test your policy locally before deployment:

```python
# Build and test
app = builder.build()
app.launch()
```

Watch for:

- Policy loads correctly
- Actions are applied as expected
- Simulation remains stable
- Performance is acceptable

### Debugging

Common issues:

1. **Dimension Mismatch**: Ensure observation/action dimensions match your policy
2. **Value Range**: Check if your policy expects normalized inputs
3. **Actuator Names**: Verify actuator names match your model
4. **NaN Values**: Check for numerical instabilities

## Advanced Topics

### Multiple Policies

Add different policies to different scenes:

```python
# Conservative policy
scene1 = project.add_scene(model=model, name="Conservative")
scene1.add_policy(path="conservative.onnx", ...)

# Aggressive policy
scene2 = project.add_scene(model=model, name="Aggressive")
scene2.add_policy(path="aggressive.onnx", ...)
```

### Policy Variants

Compare policy versions:

```python
versions = ["v1", "v2", "v3"]
for version in versions:
    scene = project.add_scene(
        model=model,
        name=f"Policy {version}",
        id=version
    )
    scene.add_policy(path=f"policy_{version}.onnx", ...)
```

### Observation Normalization

If your policy was trained with normalized observations:

```python
observation_config = {
    "qpos": True,
    "qvel": True,
    "normalize": {
        "qpos_mean": [0.0, 0.5, ...],
        "qpos_std": [0.1, 0.2, ...],
        "qvel_mean": [0.0, 0.0, ...],
        "qvel_std": [1.0, 1.0, ...]
    }
}
```

### Action Post-processing

Apply transformations to actions:

```python
action_config = {
    "type": "position",
    "actuators": ["motor1", "motor2"],
    "scale": [1.0, 2.0],      # Per-actuator scaling
    "bias": [0.0, 0.5],        # Per-actuator bias
    "clip": [[-1, 1], [-2, 2]] # Per-actuator clipping
}
```

## Best Practices

### Policy Design

1. **Keep it Simple**: Smaller policies run faster in browsers
2. **Normalize Inputs**: Helps with numerical stability
3. **Reasonable Actions**: Avoid extreme action values
4. **Test Thoroughly**: Test on various browsers and devices

### Performance

1. **Model Size**: Smaller ONNX models load and run faster
2. **Inference Frequency**: Match your policy's expected control frequency
3. **Quantization**: Consider quantizing your policy for faster inference

### Compatibility

1. **ONNX Operators**: Ensure your policy uses supported ONNX operators
2. **Browser Support**: Test on target browsers (Chrome, Firefox, Safari)
3. **Mobile**: Consider mobile device constraints

## Troubleshooting

### Policy Not Loading

Check:

- File path is correct
- ONNX file is valid
- File is accessible from the build directory

### Wrong Behavior

Verify:

- Observation dimensions match training
- Action dimensions match model actuators
- Value ranges are appropriate
- Actuator names are correct

### Performance Issues

Consider:

- Reducing policy size
- Simplifying the model
- Adjusting control frequency
- Using WebGL/WebGPU acceleration

## Next Steps

- [Building Projects](building-projects.md) - Learn about deployment
- [API Reference: Policy](../api-reference/policy.md) - Detailed policy API
- [Examples](../examples/custom-models.md) - Complete examples with policies
