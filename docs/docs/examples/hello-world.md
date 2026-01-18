# Hello World Example

A simple example to get started with Muwanx.

## Overview

This example creates a basic scene with a box falling onto a plane, demonstrating the fundamental workflow of Muwanx.

## Complete Code

```python
"""Hello World - Simplest Muwanx Example

This example creates a basic scene with a box falling onto a plane.
"""

import mujoco
import muwanx as mwx


def main():
    # Create a builder
    builder = mwx.Builder()

    # Add a project
    hello_world_project = builder.add_project(name="Hello World")

    # Define a simple MuJoCo model
    model = mujoco.MjModel.from_xml_string("""
    <mujoco>
      <worldbody>
        <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
        <geom type="plane" size="1 1 0.1" rgba=".9 0 0 1"/>
        <body pos="0 0 1">
          <joint type="free"/>
          <geom type="box" size=".1 .2 .3" rgba="0 .9 0 1"/>
        </body>
      </worldbody>
    </mujoco>
    """)

    # Add the scene
    hello_world_project.add_scene(
        model=model,
        name="Box over Plane",
    )

    # Build the application
    app = builder.build()

    # Launch in browser
    app.launch()

    print("✓ Hello World example completed successfully!")


if __name__ == "__main__":
    main()
```

## Running the Example

1. Save the code to a file (e.g., `hello_world.py`)
2. Run it:

```bash
python hello_world.py
```

3. Your browser will open automatically showing the simulation

## What You'll See

- A red plane (ground)
- A green box falling from above
- The box bouncing and settling on the plane
- Interactive 3D camera controls

## Understanding the Code

### 1. Builder Creation

```python
builder = mwx.Builder()
```

The builder is your starting point for creating Muwanx applications.

### 2. Project Creation

```python
hello_world_project = builder.add_project(name="Hello World")
```

Projects organize related scenes. Here we create a single project.

### 3. MuJoCo Model

```python
model = mujoco.MjModel.from_xml_string("""
<mujoco>
  <worldbody>
    <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
    <geom type="plane" size="1 1 0.1" rgba=".9 0 0 1"/>
    <body pos="0 0 1">
      <joint type="free"/>
      <geom type="box" size=".1 .2 .3" rgba="0 .9 0 1"/>
    </body>
  </worldbody>
</mujoco>
""")
```

This defines the physics simulation:

- `<light>`: Adds lighting to the scene
- `<geom type="plane">`: Creates a ground plane (red)
- `<body pos="0 0 1">`: Creates a body 1 meter above the plane
- `<joint type="free"/>`: Allows the body to move freely
- `<geom type="box">`: Adds a box shape (green)

### 4. Scene Addition

```python
hello_world_project.add_scene(
    model=model,
    name="Box over Plane",
)
```

Adds the scene to the project with a descriptive name.

### 5. Build and Launch

```python
app = builder.build()
app.launch()
```

Builds the application and launches it in your browser.

## Variations

### Different Shapes

Change the box to a sphere:

```python
<geom type="sphere" size="0.15" rgba="0 .9 0 1"/>
```

Or a capsule:

```python
<geom type="capsule" size="0.1 0.3" rgba="0 .9 0 1"/>
```

### Multiple Objects

Add more falling objects:

```python
model = mujoco.MjModel.from_xml_string("""
<mujoco>
  <worldbody>
    <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
    <geom type="plane" size="1 1 0.1" rgba=".9 0 0 1"/>

    <!-- First box -->
    <body pos="-0.3 0 1">
      <joint type="free"/>
      <geom type="box" size=".1 .1 .1" rgba="0 .9 0 1"/>
    </body>

    <!-- Second box -->
    <body pos="0 0 1.5">
      <joint type="free"/>
      <geom type="box" size=".08 .08 .08" rgba="0 0 .9 1"/>
    </body>

    <!-- Sphere -->
    <body pos="0.3 0 2">
      <joint type="free"/>
      <geom type="sphere" size="0.1" rgba=".9 .9 0 1"/>
    </body>
  </worldbody>
</mujoco>
""")
```

### Different Colors

RGBA format: `[red, green, blue, alpha]` (values 0-1)

```python
rgba=".9 0 0 1"    # Red
rgba="0 .9 0 1"    # Green
rgba="0 0 .9 1"    # Blue
rgba=".9 .9 0 1"   # Yellow
rgba=".9 0 .9 1"   # Magenta
rgba="0 .9 .9 1"   # Cyan
```

### Initial Velocity

Give the box an initial velocity:

```python
hello_world_project.add_scene(
    model=model,
    name="Box with Initial Velocity",
    initial_qvel={
        "free_joint_x": 1.0,  # Move in x direction
        "free_joint_z": 2.0   # Move upward
    }
)
```

## Next Steps

- [Creating Scenes](../user-guide/creating-scenes.md) - Learn more about scene configuration
- [Custom Models Example](custom-models.md) - Work with external model files
- [Basic Concepts](../user-guide/basic-concepts.md) - Understand Muwanx architecture

## Troubleshooting

### Port Already in Use

If you see a port conflict:

```python
app.launch(port=8888)  # Use a different port
```

### Browser Doesn't Open

Manually visit the URL shown in the console (usually `http://localhost:8080`).

### Black Screen

If you see a black screen:

- Check browser console for errors (F12)
- Ensure WebGL is enabled in your browser
- Try a different browser (Chrome, Firefox recommended)
