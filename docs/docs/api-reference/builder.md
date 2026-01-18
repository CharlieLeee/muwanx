# Builder API Reference

The `Builder` class is the main entry point for creating Muwanx applications.

## Class: Builder

```python
class Builder(base_path: str = "/")
```

The Builder manages the construction of Muwanx applications, coordinating projects, scenes, and the build process.

### Parameters

- **base_path** (`str`, optional): Base path for the application deployment. Defaults to `"/"`.
  - Use `"/"` for root domain deployment
  - Use `"/subdirectory/"` for subdirectory deployment
  - Use `"/repo-name/"` for GitHub Pages project pages

### Example

```python
import muwanx as mwx

# For root deployment
builder = mwx.Builder()

# For subdirectory deployment
builder = mwx.Builder(base_path="/myapp/")

# For GitHub Pages
builder = mwx.Builder(base_path="/my-repo/")
```

## Methods

### add_project

```python
def add_project(
    name: str,
    *,
    id: str | None = None
) -> ProjectHandle
```

Add a new project to the builder.

**Parameters:**

- **name** (`str`): Display name for the project shown in the UI
- **id** (`str | None`, optional): URL identifier for routing
  - If `None` and this is the first project: uses `None` (default/home route)
  - If `None` and not the first project: auto-generated from name
  - If provided: uses the specified ID

**Returns:**

- `ProjectHandle`: Handle for configuring the project and adding scenes

**Example:**

```python
# First project (default route)
project1 = builder.add_project(name="Main Demo")

# Second project (auto-generated ID)
project2 = builder.add_project(name="Advanced Demos")
# URL: /#/advanced-demos

# Custom ID
project3 = builder.add_project(name="My Project", id="custom")
# URL: /#/custom
```

### build

```python
def build(
    output_dir: str | Path | None = None
) -> MuwanxApp
```

Build the application from configured projects.

**Parameters:**

- **output_dir** (`str | Path | None`, optional): Directory to save application files
  - If `None`: defaults to `dist` in the caller's directory
  - If provided: saves to the specified directory

**Returns:**

- `MuwanxApp`: Built application ready to launch or deploy

**Raises:**

- `ValueError`: If no projects have been added

**Example:**

```python
# Build to default 'dist' directory
app = builder.build()

# Build to custom directory
app = builder.build(output_dir="./deploy")

# Build to absolute path
from pathlib import Path
app = builder.build(output_dir=Path.home() / "my_app")
```

### get_projects

```python
def get_projects() -> list[ProjectConfig]
```

Get the list of configured projects.

**Returns:**

- `list[ProjectConfig]`: List of project configurations

**Example:**

```python
projects = builder.get_projects()
print(f"Total projects: {len(projects)}")
for project in projects:
    print(f"  - {project.name}")
```

## Complete Example

```python
import mujoco
import muwanx as mwx

# Create builder
builder = mwx.Builder(base_path="/")

# Add multiple projects
locomotion = builder.add_project(name="Locomotion", id="locomotion")
manipulation = builder.add_project(name="Manipulation", id="manipulation")

# Add scenes to first project
model1 = mujoco.MjModel.from_xml_path("quadruped.xml")
scene1 = locomotion.add_scene(model=model1, name="Walking")
scene1.add_policy(path="walk_policy.onnx", ...)

# Add scenes to second project
model2 = mujoco.MjModel.from_xml_path("arm.xml")
scene2 = manipulation.add_scene(model=model2, name="Picking")
scene2.add_policy(path="pick_policy.onnx", ...)

# Build and launch
app = builder.build(output_dir="./dist")
app.launch(port=8080)
```

## Notes

### Project Organization

- The first project added becomes the default route (`/`)
- Subsequent projects are accessible via their IDs (`/#/project-id`)
- Project IDs must be unique
- Empty builders (no projects) cannot be built

### Path Resolution

- All file paths (models, policies) are resolved relative to the calling script
- The builder automatically handles asset copying during build
- Mesh files referenced in MuJoCo models are included automatically

### Build Output

The build process creates:

```
output_dir/
├── index.html              # Main HTML entry point
├── assets/
│   ├── models/            # MuJoCo XML/MJCF files
│   ├── policies/          # ONNX policy files
│   └── meshes/            # 3D mesh files
├── js/                    # JavaScript bundles
├── css/                   # Stylesheets
└── config.json            # Application configuration
```

### Performance Considerations

- Builder operations are lightweight (no heavy computation)
- Build time depends on number of assets and their sizes
- Large ONNX models or high-poly meshes increase build time and application size

## See Also

- [ProjectHandle](project.md) - Project configuration
- [MuwanxApp](app.md) - Launching and running applications
- [Building Projects Guide](../user-guide/building-projects.md) - Build and deployment guide
