# Basic Concepts

This guide introduces the core concepts and architecture of Muwanx.

## Architecture Overview

Muwanx follows a hierarchical structure:

```
Builder
  └── Project(s)
        └── Scene(s)
              └── Policy (optional)
```

### Builder

The [`Builder`](../api-reference/builder.md) is the top-level object that orchestrates the entire application. It manages projects and handles the build process.

```python
builder = mwx.Builder(base_path="/")
```

**Key responsibilities:**

- Managing multiple projects
- Configuring deployment paths
- Building the final application

### Project

A [`Project`](../api-reference/project.md) is a collection of related scenes. Projects help organize your simulations logically and appear as sections in the web interface.

```python
project = builder.add_project(name="Robot Experiments", id="robots")
```

**Key features:**

- Groups related scenes together
- Has a display name shown in the UI
- Has an optional ID for URL routing
- First project is the default/home page

### Scene

A [`Scene`](../api-reference/scene.md) represents a single simulation instance with a MuJoCo model and optional policy.

```python
scene = project.add_scene(
    model=mujoco_model,
    name="Walking Gait",
    initial_qpos={...}
)
```

**Key features:**

- Contains a MuJoCo physics model
- Can have custom initial states
- May include an ONNX policy for control
- Appears as a selectable option in the UI

### Policy

A [`Policy`](../api-reference/policy.md) is an ONNX neural network that controls the simulation based on observations.

```python
scene.add_policy(
    path="policy.onnx",
    observation_config={...},
    action_config={...}
)
```

**Key features:**

- Runs inference in real-time in the browser
- Processes observations from the simulation
- Outputs actions to control the model
- Fully client-side (no server required)

## Data Flow

Understanding how data flows through a Muwanx application:

```
MuJoCo Simulation → Observations → ONNX Policy → Actions → MuJoCo Simulation
```

1. **Simulation Step**: MuJoCo physics engine advances the simulation
2. **Observation Extraction**: Configured sensors/states are extracted
3. **Policy Inference**: ONNX model processes observations
4. **Action Application**: Policy outputs are applied to actuators
5. **Repeat**: Process continues in real-time

## Browser Execution

One of Muwanx's key features is that everything runs in the browser:

### WebAssembly

MuJoCo is compiled to WebAssembly (Wasm), allowing native-speed physics simulation directly in the browser without plugins.

### ONNX Runtime

Policies are executed using ONNX Runtime Web, which supports:

- CPU execution
- WebGL acceleration
- WebGPU acceleration (when available)

### Three.js Rendering

Visualization is powered by Three.js, providing:

- Real-time 3D rendering
- Interactive camera controls
- VR support via WebXR

## Configuration Philosophy

Muwanx uses a declarative configuration approach:

### Python API (Programmatic)

Build applications using Python code:

```python
builder = mwx.Builder()
project = builder.add_project(name="Demo")
project.add_scene(model=model, name="Scene 1")
app = builder.build()
```

**Advantages:**

- Dynamic generation from code
- Integration with ML training pipelines
- Programmatic customization
- Python ecosystem integration

### JSON Configuration (Advanced)

Under the hood, configurations are represented as JSON:

```json
{
  "projects": [
    {
      "name": "Demo",
      "scenes": [
        {
          "name": "Scene 1",
          "model": "model.xml",
          "policy": "policy.onnx"
        }
      ]
    }
  ]
}
```

This enables advanced use cases like editing configurations directly or generating them from other tools.

## File Structure

A built Muwanx application has this structure:

```
dist/
├── index.html              # Main entry point
├── assets/
│   ├── models/            # MuJoCo XML models
│   ├── policies/          # ONNX policy files
│   └── meshes/            # 3D meshes (if used)
├── js/                    # JavaScript bundles
├── css/                   # Stylesheets
└── config.json            # Application configuration
```

All files are static, making deployment to services like GitHub Pages, Netlify, or Vercel straightforward.

## Deployment Modes

### Local Development

Use `app.launch()` for local testing:

```python
app = builder.build()
app.launch(port=8080, open_browser=True)
```

### Static Deployment

Build to a directory and deploy:

```python
app = builder.build(output_dir="./deploy")
# Then upload the ./deploy directory to your hosting service
```

### GitHub Pages

Configure the builder with the correct base path:

```python
builder = mwx.Builder(base_path="/my-repo/")
```

This ensures assets load correctly when deployed to `https://username.github.io/my-repo/`.

## Best Practices

### Project Organization

- Use one project for closely related scenes
- Create separate projects for different experiments or use cases
- Give projects descriptive names

### Scene Design

- Keep models reasonably sized for browser performance
- Test on target devices (mobile, desktop)
- Use appropriate simulation timesteps

### Policy Configuration

- Ensure observation/action dimensions match your policy
- Normalize inputs if your policy expects normalized data
- Test policies before deployment

### Performance

- Optimize MuJoCo models (reduce unnecessary contacts, simplify meshes)
- Use appropriate rendering quality settings
- Consider mobile device constraints

## Next Steps

- [Creating Scenes](creating-scenes.md) - Learn scene configuration in detail
- [Adding Policies](adding-policies.md) - Add AI control to your simulations
- [Building Projects](building-projects.md) - Advanced build configuration
