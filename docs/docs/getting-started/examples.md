---
icon: octicons/code-16
---

# Examples

Let's create a simple "Hello World" simulation with a falling box.

## Step 1: Create a Python Script

Create a new file called `hello_world.py`:

```py
import mujoco
import muwanx

# Create a builder instance
builder = muwanx.Builder()

# Add a project
project = builder.add_project(name="Hello World")

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

# Add a scene to the project
project.add_scene(model=model, name="Falling Box")

# Build the application
app = builder.build()

# Launch in browser
app.launch()
```

## Step 2: Run the Script

Execute your script:

```bash
python hello_world.py
```

This will:

1. Build the application in a `dist` directory
2. Start a local web server
3. Open your default browser to view the simulation

You should see an interactive 3D view with a green box falling onto a red plane!

## Understanding the Code

Let's break down what each part does:

### Builder

```python
builder = muwanx.Builder()
```

The `Builder` is the main entry point for creating muwanx applications. It manages projects, scenes, and builds the final application.

### Project

```python
project = builder.add_project(name="Hello World")
```

A project is a collection of related scenes. It appears as a section in the UI and can contain multiple scenes.

### MuJoCo Model

```python
model = mujoco.MjModel.from_xml_string("""...""")
```

You define your physics simulation using MuJoCo's XML format. This example creates a simple scene with a plane (ground) and a box with a free joint that allows it to fall.

### Scene

```python
project.add_scene(model=model, name="Falling Box")
```

A scene represents a single simulation instance. You can add multiple scenes to a project to show different configurations or behaviors.

### Build and Launch

```python
app = builder.build()
app.launch()
```

The `build()` method compiles everything into a static web application, and `launch()` starts a local server and opens it in your browser.

## Troubleshooting

### Port Already in Use

If port 8080 is already in use, muwanx will automatically find an available port. You can also specify a custom port:

```python
app.launch(port=8888)
```

### Browser Doesn't Open

If the browser doesn't open automatically, you can manually navigate to the URL shown in the console output (typically `http://localhost:8080`).

### Build Directory

By default, the application is built to a `dist` directory relative to your script. You can specify a custom output directory:

```python
app = builder.build(output_dir="./my_app")
```

### WebAssembly Not Supported

muwanx requires a modern browser with WebAssembly support. Ensure you're using an up-to-date version of Chrome, Firefox, Safari, or Edge.
