# Welcome to muwanx!

<div align="center">
  <strong><em>Real-time Interactive AI Robot Simulation in Your Browser</em></strong>
</div>

## What is Muwanx?

Muwanx is a powerful framework for creating interactive MuJoCo simulations with real-time policy control, running entirely in the browser. Built on top of [**MU**joco **WA**sm](https://github.com/google-deepmind/mujoco/tree/main/wasm), [on**NX** runtime](https://github.com/microsoft/onnxruntime), and [three.js](https://github.com/mrdoob/three.js/), it enables easy sharing of AI robot simulation demos as static sites, perfect for GitHub Pages hosting.

## Key Features

- **Real-time Simulation**: Run MuJoCo simulations and policy control in real time
- **Interactive**: Change the state of objects by applying forces with intuitive controls
- **Cross-platform**: Works seamlessly on desktop and mobile devices
- **VR Support**: Native VR viewer support with WebXR API
- **Client-only**: All computation runs in the browser - no server required for simulation
- **Easy Sharing**: Host as a static site for effortless demo distribution (e.g., GitHub Pages)
- **Customizable**: Visualize your MuJoCo models and ONNX policies quickly

## Quick Example

```python
import mujoco
import muwanx as muwanx

# Create a builder
builder = muwanx.Builder()

# Add a project
project = builder.add_project(name="My Robot")

# Create a MuJoCo model
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

# Add a scene
project.add_scene(model=model, name="My Scene")

# Build and launch
app = builder.build()
app.launch()
```

## Getting Started

Get up and running with Muwanx in minutes:

- [Installation](getting-started.md#installation) - Install Muwanx with pip or npm
- [Quick Start](getting-started.md#quick-start) - Create your first simulation
- [Basic Concepts](user-guide/basic-concepts.md) - Understand the core concepts

## Use Cases

Muwanx is perfect for:

- **Research Demos**: Share your robot learning research with interactive visualizations
- **Education**: Create interactive physics and robotics tutorials
- **Prototyping**: Quickly test and visualize different MuJoCo models and policies
- **Portfolio**: Showcase your robotics projects in an accessible way

## Live Demos

Explore what's possible with Muwanx:

- [Main Demo](https://ttktjmt.github.io/muwanx/) - Interactive examples
- [Python Demo](https://ttktjmt.github.io/muwanx/python) - Python-generated demos
- [MyoSuite Demo](https://ttktjmt.github.io/muwanx/#/myosuite) - Musculoskeletal models
- [MuJoCo Menagerie](https://ttktjmt.github.io/muwanx/#/menagerie) - Various robot models
- [MuJoCo Playground](https://ttktjmt.github.io/muwanx/#/playground) - Interactive environments

## Community

- [GitHub Repository](https://github.com/ttktjmt/muwanx)
- [Issue Tracker](https://github.com/ttktjmt/muwanx/issues)
- [PyPI Package](https://pypi.org/project/muwanx)
- [npm Package](https://www.npmjs.com/package/muwanx)

## License

Muwanx is licensed under the [Apache-2.0 License](https://github.com/ttktjmt/muwanx/blob/main/LICENSE).
