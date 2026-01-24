---
icon: octicons/home-16
---

# Welcome to muwanx!

<p align="center">
  <img src="https://github.com/ttktjmt/muwanx/raw/main/assets/banner.png" alt="Muwanx Header" style="width: 80%;">
  <br/>
  <strong><em>Real-time Interactive AI Robot Simulation in Your Browser</em></strong>
</p>

## What is Muwanx?

Muwanx is a powerful framework for creating interactive MuJoCo simulations with real-time policy control, running entirely in the browser. Built on top of [**MU**joco **WA**sm](https://github.com/google-deepmind/mujoco/tree/main/wasm), [on**NX** runtime](https://github.com/microsoft/onnxruntime), and [three.js](https://github.com/mrdoob/three.js/), it enables easy sharing of AI robot simulation demos as static sites, perfect for GitHub Pages hosting.

## Key Features

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Real-time Simulation__

    ---

    Run MuJoCo simulations and policy control in real time

-   :material-cursor-default-click:{ .lg .middle } __Interactive__

    ---

    Change the state of objects by applying forces with intuitive controls

-   :material-server-off:{ .lg .middle } __Client-only__

    ---

    All computation runs in the browser - no server required for simulation

-   :material-share-variant:{ .lg .middle } __Easy Sharing__

    ---

    Host as a static site for effortless demo distribution (e.g., GitHub Pages)

-   :material-devices:{ .lg .middle } __Cross-platform__

    ---

    Works seamlessly on desktop and mobile devices

-   :material-virtual-reality:{ .lg .middle } __VR Support__

    ---

    Native VR viewer support with WebXR API

</div>

## Use Cases

Muwanx is perfect for:

- **Research Demos**: Share your robot learning research with interactive visualizations
- **Education**: Create interactive physics and robotics tutorials
- **Prototyping**: Quickly test and visualize different MuJoCo models and policies
- **Portfolio**: Showcase your robotics projects in an accessible way

## Live Demos

Explore what's possible with Muwanx:

- [Main Demo](https://ttktjmt.github.io/muwanx/python) - Python-generated demos
- [MyoSuite](https://ttktjmt.github.io/muwanx/python/myosuite) - Musculoskeletal models
- [MuJoCo Menagerie](https://ttktjmt.github.io/muwanx/python/menagerie) - Various robot models
- [MuJoCo Playground](https://ttktjmt.github.io/muwanx/python/playground) - Interactive environments

## Quick Example

```py
import mujoco
import muwanx

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

➔ Check out more examples in the [Examples](getting-started/examples.md) section!

## Community

- [GitHub Repository](https://github.com/ttktjmt/muwanx)
- [PyPI Package](https://pypi.org/project/muwanx)
- [npm Package](https://www.npmjs.com/package/muwanx)

## License

Muwanx is licensed under the [Apache-2.0 License](https://github.com/ttktjmt/muwanx/blob/main/LICENSE).
