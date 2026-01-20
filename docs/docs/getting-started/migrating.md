# Migrating from mjlab

If you're coming from `mjlab`, this guide will help you migrate your projects to Muwanx.

## Key Differences

### API Changes

Muwanx introduces a cleaner, more structured API compared to mjlab:

| mjlab | Muwanx |
|-------|--------|
| Not available | `muwanx.Builder()` - Central builder pattern |
| Direct model creation | Project-based organization |
| Limited scene management | Explicit scene and project management |

### New Concepts

Muwanx introduces several new concepts:

- **Builder**: Central API for creating applications
- **Projects**: Organize related scenes together
- **Scenes**: Individual simulation instances within projects

## Migration Steps

### 1. Update Installation

First, install Muwanx:

```bash
pip install muwanx
```

### 2. Update Imports

Replace mjlab imports:

```python
# Old (mjlab)
import mjlab

# New (Muwanx)
import muwanx as muwanx
```

### 3. Use the Builder Pattern

Muwanx uses a builder pattern for creating applications:

```python
# Create a builder
builder = muwanx.Builder()

# Add a project
project = builder.add_project(name="My Project")

# Add scenes to the project
project.add_scene(model=my_model, name="Scene 1")

# Build and launch
app = builder.build()
app.launch()
```

### 4. Organize Code into Projects

Group related scenes into projects for better organization:

```python
# Create multiple projects
training_project = builder.add_project(name="Training")
testing_project = builder.add_project(name="Testing")

# Add scenes to each project
training_project.add_scene(model=train_model, name="Environment 1")
testing_project.add_scene(model=test_model, name="Test Run")
```

## Example Migration

Here's a complete example showing the migration:

### Before (mjlab)

```python
import mjlab
import mujoco

model = mujoco.MjModel.from_xml_string(xml_string)
# mjlab-specific code...
```

### After (Muwanx)

```python
import muwanx as muwanx
import mujoco

# Create builder
builder = muwanx.Builder()

# Add project
project = builder.add_project(name="My Simulation")

# Create model
model = mujoco.MjModel.from_xml_string(xml_string)

# Add scene
project.add_scene(model=model, name="Main Scene")

# Build and launch
app = builder.build()
app.launch()
```

## Benefits of Migration

- **Better Organization**: Projects and scenes provide clear structure
- **Improved API**: More intuitive and consistent API
- **Enhanced Features**: Access to new features like policy integration
- **Active Development**: Regular updates and improvements

## Need Help?

If you encounter issues during migration, please open an issue on [GitHub](https://github.com/ttktjmt/muwanx/issues).
