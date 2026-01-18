# Policy API Reference

Policies are ONNX neural networks that control simulations in real-time.

## Class: PolicyConfig

```python
class PolicyConfig(
    path: str | Path,
    observation_config: dict,
    action_config: dict
)
```

Configuration for an ONNX policy attached to a scene.

**Attributes:**

- **path** (`str | Path`): Path to the ONNX model file
- **observation_config** (`dict`): Observation extraction configuration
- **action_config** (`dict`): Action application configuration

You typically don't create `PolicyConfig` directly - use [`SceneHandle.add_policy()`](scene.md#add_policy) instead.

## Observation Configuration Reference

### Structure

```python
observation_config = {
    # State observations (boolean or list)
    "qpos": bool | list[str],
    "qvel": bool | list[str],
    "qacc": bool | list[str],

    # Sensor observations
    "sensors": list[str],
    "sensordata": bool,

    # Preprocessing
    "normalize": dict,
    "clip": list[float] | float
}
```

### Fields

#### qpos

Joint positions.

- **Type**: `bool | list[str]`
- **Default**: `False`
- **Examples**:
  ```python
  "qpos": True                          # All joint positions
  "qpos": ["hip", "knee", "ankle"]      # Specific joints
  ```

#### qvel

Joint velocities.

- **Type**: `bool | list[str]`
- **Default**: `False`
- **Examples**:
  ```python
  "qvel": True                          # All joint velocities
  "qvel": ["hip", "knee", "ankle"]      # Specific joints
  ```

#### qacc

Joint accelerations.

- **Type**: `bool | list[str]`
- **Default**: `False`
- **Examples**:
  ```python
  "qacc": True                          # All joint accelerations
  "qacc": ["hip", "knee"]               # Specific joints
  ```

#### sensors

Specific sensor names to include.

- **Type**: `list[str]`
- **Default**: `[]`
- **Examples**:
  ```python
  "sensors": ["imu", "gyro", "touch"]   # Include these sensors
  ```

#### sensordata

Include all sensor data.

- **Type**: `bool`
- **Default**: `False`
- **Examples**:
  ```python
  "sensordata": True                    # All sensors
  ```

#### normalize

Normalization parameters.

- **Type**: `dict`
- **Fields**:
  - `qpos_mean`: Mean values for qpos
  - `qpos_std`: Standard deviation for qpos
  - `qvel_mean`: Mean values for qvel
  - `qvel_std`: Standard deviation for qvel
- **Examples**:
  ```python
  "normalize": {
      "qpos_mean": [0.0, 0.5, -0.3],
      "qpos_std": [0.1, 0.2, 0.15],
      "qvel_mean": [0.0, 0.0, 0.0],
      "qvel_std": [1.0, 1.0, 1.0]
  }
  ```

#### clip

Clip observations to a range.

- **Type**: `list[float]` (two elements) or `float`
- **Examples**:
  ```python
  "clip": [-10.0, 10.0]    # Clip to [-10, 10]
  "clip": 10.0             # Clip to [-10, 10] (symmetric)
  ```

## Action Configuration Reference

### Structure

```python
action_config = {
    # Required
    "type": str,
    "actuators": list[str] | None,

    # Optional scaling/transformation
    "scale": float | list[float],
    "bias": float | list[float],
    "clip": list[float] | list[list[float]]
}
```

### Fields

#### type

Type of control.

- **Type**: `str`
- **Required**: Yes
- **Options**: `"position"`, `"velocity"`, `"torque"`
- **Examples**:
  ```python
  "type": "position"    # Position control
  "type": "velocity"    # Velocity control
  "type": "torque"      # Torque/force control
  ```

#### actuators

List of actuator names to control.

- **Type**: `list[str] | None`
- **Required**: Yes (unless controlling all actuators)
- **Examples**:
  ```python
  "actuators": ["motor1", "motor2", "motor3"]
  "actuators": None  # All actuators (not recommended)
  ```

#### scale

Scale factor applied to actions.

- **Type**: `float | list[float]`
- **Default**: `1.0`
- **Examples**:
  ```python
  "scale": 2.0               # Scale all by 2
  "scale": [1.0, 2.0, 0.5]   # Per-actuator scaling
  ```

#### bias

Bias added to actions.

- **Type**: `float | list[float]`
- **Default**: `0.0`
- **Examples**:
  ```python
  "bias": 0.5                # Add 0.5 to all
  "bias": [0.0, 0.5, -0.2]   # Per-actuator bias
  ```

#### clip

Clip actions to a range.

- **Type**: `list[float]` or `list[list[float]]`
- **Examples**:
  ```python
  "clip": [-1.0, 1.0]              # Clip all to [-1, 1]
  "clip": [[-1, 1], [-2, 2]]       # Per-actuator clipping
  ```

## Complete Configuration Examples

### Minimal Configuration

```python
observation_config = {
    "qpos": True,
    "qvel": True
}

action_config = {
    "type": "position",
    "actuators": ["motor1", "motor2"]
}
```

### Full Featured Configuration

```python
observation_config = {
    # State
    "qpos": ["hip_fl", "hip_fr", "knee_fl", "knee_fr"],
    "qvel": ["hip_fl", "hip_fr", "knee_fl", "knee_fr"],

    # Sensors
    "sensors": ["imu", "gyro", "touch_fl", "touch_fr"],

    # Preprocessing
    "normalize": {
        "qpos_mean": [0.0, 0.0, 0.5, 0.5],
        "qpos_std": [0.2, 0.2, 0.3, 0.3],
        "qvel_mean": [0.0, 0.0, 0.0, 0.0],
        "qvel_std": [1.0, 1.0, 1.0, 1.0]
    },
    "clip": [-50.0, 50.0]
}

action_config = {
    "type": "position",
    "actuators": ["motor_fl", "motor_fr", "motor_bl", "motor_br"],
    "scale": [1.0, 1.0, 0.8, 0.8],
    "bias": [0.0, 0.0, 0.1, 0.1],
    "clip": [
        [-1.0, 1.0],
        [-1.0, 1.0],
        [-0.8, 0.8],
        [-0.8, 0.8]
    ]
}
```

### Humanoid Robot Example

```python
observation_config = {
    "qpos": [
        # Torso
        "abdomen_x", "abdomen_y", "abdomen_z",
        # Left leg
        "hip_l", "knee_l", "ankle_l",
        # Right leg
        "hip_r", "knee_r", "ankle_r",
        # Arms
        "shoulder_l", "elbow_l",
        "shoulder_r", "elbow_r"
    ],
    "qvel": True,  # All velocities
    "sensors": ["torso_imu", "foot_l_contact", "foot_r_contact"],
    "normalize": {
        "qpos_mean": [0.0] * 13,
        "qpos_std": [0.5] * 13,
        "qvel_mean": [0.0] * 13,
        "qvel_std": [2.0] * 13
    }
}

action_config = {
    "type": "position",
    "actuators": [
        "motor_abdomen_x", "motor_abdomen_y", "motor_abdomen_z",
        "motor_hip_l", "motor_knee_l", "motor_ankle_l",
        "motor_hip_r", "motor_knee_r", "motor_ankle_r",
        "motor_shoulder_l", "motor_elbow_l",
        "motor_shoulder_r", "motor_elbow_r"
    ],
    "scale": 0.5,
    "clip": [-1.0, 1.0]
}
```

### Quadruped Example

```python
observation_config = {
    "qpos": True,
    "qvel": True,
    "sensors": ["base_imu", "base_gyro"],
    "clip": [-100.0, 100.0]
}

action_config = {
    "type": "position",
    "actuators": [
        # Front legs
        "fl_hip", "fl_upper", "fl_lower",
        "fr_hip", "fr_upper", "fr_lower",
        # Back legs
        "bl_hip", "bl_upper", "bl_lower",
        "br_hip", "br_upper", "br_lower"
    ],
    "scale": 0.3,  # Conservative scaling
    "clip": [-1.0, 1.0]
}
```

## Data Flow

Understanding the data flow helps configure policies correctly:

```
Simulation State
  ↓
Observation Extraction (qpos, qvel, sensors, etc.)
  ↓
Normalization (if configured)
  ↓
Clipping (if configured)
  ↓
ONNX Policy Inference
  ↓
Action Scaling (if configured)
  ↓
Action Bias (if configured)
  ↓
Action Clipping (if configured)
  ↓
Apply to Actuators
```

## Dimension Matching

Ensure dimensions match your trained policy:

```python
# Training dimensions
observation_dim = 24  # e.g., 12 qpos + 12 qvel
action_dim = 8        # e.g., 8 actuators

# Configuration must match
observation_config = {
    "qpos": [...],  # 12 joints
    "qvel": [...]   # 12 joints
}
# Total: 24 observations ✓

action_config = {
    "actuators": [...]  # 8 actuators ✓
}
```

## Testing Policies

### Dimension Check

```python
import numpy as np
import onnxruntime as ort

# Load ONNX model
session = ort.InferenceSession("policy.onnx")

# Check input shape
input_shape = session.get_inputs()[0].shape
print(f"Expected observation dim: {input_shape}")

# Check output shape
output_shape = session.get_outputs()[0].shape
print(f"Expected action dim: {output_shape}")
```

### Test Inference

```python
# Create dummy observation
dummy_obs = np.zeros((1, observation_dim), dtype=np.float32)

# Run inference
action = session.run(None, {session.get_inputs()[0].name: dummy_obs})
print(f"Action shape: {action[0].shape}")
```

## Common Issues

### Dimension Mismatch

**Problem**: Policy expects different observation dimensions.

**Solution**: Ensure observation config matches training:
```python
# If policy trained with 24 observations
observation_config = {
    "qpos": True,  # e.g., 12 joints
    "qvel": True   # e.g., 12 joints
}
# Total: 24 ✓
```

### Value Range Issues

**Problem**: Policy outputs unexpected values.

**Solution**: Apply appropriate scaling/clipping:
```python
action_config = {
    "type": "position",
    "scale": 0.5,        # Scale down if too aggressive
    "clip": [-1.0, 1.0]  # Prevent extreme values
}
```

### Actuator Name Errors

**Problem**: Actuator names don't match model.

**Solution**: Check names in MuJoCo XML:
```xml
<actuator>
  <motor name="hip_motor"/>  <!-- Use "hip_motor" -->
</actuator>
```

## Best Practices

1. **Document Configs**: Comment your observation/action configurations
2. **Test Locally**: Verify policy behavior before deployment
3. **Match Training**: Ensure configs match training environment exactly
4. **Use Clipping**: Always clip actions to safe ranges
5. **Normalize Consistently**: Use same normalization as training

## See Also

- [SceneHandle.add_policy()](scene.md#add_policy) - Adding policies to scenes
- [Adding Policies Guide](../user-guide/adding-policies.md) - Detailed guide
- [Examples](../examples/custom-models.md) - Complete examples
