# Building Projects

Learn how to build and deploy your Muwanx applications.

## Build Process

The build process compiles your Python configuration into a static web application.

## Basic Build

```python
# Create your application
builder = mwx.Builder()
project = builder.add_project(name="My Project")
project.add_scene(model=model, name="Scene 1")

# Build
app = builder.build()
```

By default, this creates a `dist` directory containing your application.

## Custom Output Directory

Specify where to build:

```python
app = builder.build(output_dir="./my_app")
```

The directory structure:

```
my_app/
├── index.html
├── assets/
│   ├── models/
│   ├── policies/
│   └── meshes/
├── js/
├── css/
└── config.json
```

## Deployment Paths

### Root Path Deployment

For deployment at a domain root (`example.com`):

```python
builder = mwx.Builder(base_path="/")
```

### Subdirectory Deployment

For deployment in a subdirectory (`example.com/myapp/`):

```python
builder = mwx.Builder(base_path="/myapp/")
```

This ensures all asset paths are correct.

### GitHub Pages

For GitHub Pages deployment:

```python
# For user/org pages: https://username.github.io/
builder = mwx.Builder(base_path="/")

# For project pages: https://username.github.io/repo-name/
builder = mwx.Builder(base_path="/repo-name/")
```

## Local Development

### Launch Server

```python
app = builder.build()
app.launch()
```

This starts a local server (default port 8080) and opens your browser.

### Custom Port

```python
app.launch(port=3000)
```

### Custom Host

```python
app.launch(host="0.0.0.0", port=8080)  # Accessible on network
```

### No Browser

```python
app.launch(open_browser=False)
```

## Static Deployment

Once built, deploy the output directory to any static hosting service.

### GitHub Pages

1. Build with correct base path:

```python
builder = mwx.Builder(base_path="/repo-name/")
app = builder.build(output_dir="./docs")
```

2. Push to GitHub
3. Enable GitHub Pages in repository settings
4. Select the `docs` folder as source

### Netlify

1. Build the application:

```python
app = builder.build(output_dir="./dist")
```

2. Deploy via Netlify CLI:

```bash
netlify deploy --dir=dist --prod
```

Or connect your GitHub repository and configure:

- Build command: `python build_script.py`
- Publish directory: `dist`

### Vercel

1. Build the application:

```python
app = builder.build(output_dir="./public")
```

2. Deploy via Vercel CLI:

```bash
vercel --prod
```

Or use the Vercel dashboard to connect your repository.

### AWS S3

1. Build:

```python
app = builder.build(output_dir="./dist")
```

2. Upload to S3:

```bash
aws s3 sync dist/ s3://your-bucket-name/
```

3. Enable static website hosting in S3 settings

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install muwanx

      - name: Build application
        run: python build_script.py

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

### GitLab CI

Create `.gitlab-ci.yml`:

```yaml
pages:
  image: python:3.10
  script:
    - pip install muwanx
    - python build_script.py
    - mv dist public
  artifacts:
    paths:
      - public
  only:
    - main
```

## Build Script

Create a reusable build script `build.py`:

```python
#!/usr/bin/env python3
"""Build script for Muwanx application."""

import mujoco
import muwanx as mwx

def build():
    # Create builder
    builder = mwx.Builder(base_path="/")

    # Add projects
    project = builder.add_project(name="My Project")

    # Add scenes
    model = mujoco.MjModel.from_xml_path("models/robot.xml")
    scene = project.add_scene(model=model, name="Robot Demo")

    # Add policies
    scene.add_policy(
        path="policies/robot_policy.onnx",
        observation_config={"qpos": True, "qvel": True},
        action_config={"type": "position"}
    )

    # Build
    app = builder.build(output_dir="./dist")
    print("Build complete! Output in ./dist")

    return app

if __name__ == "__main__":
    app = build()

    # Launch for local testing
    import sys
    if "--launch" in sys.argv:
        app.launch()
```

Usage:

```bash
# Build only
python build.py

# Build and launch
python build.py --launch
```

## Multiple Projects

Organize complex applications:

```python
def build_demo():
    builder = mwx.Builder()

    # Project 1: Locomotion
    locomotion = builder.add_project(name="Locomotion", id="locomotion")
    locomotion.add_scene(...)

    # Project 2: Manipulation
    manipulation = builder.add_project(name="Manipulation", id="manipulation")
    manipulation.add_scene(...)

    # Project 3: Experiments
    experiments = builder.add_project(name="Experiments", id="experiments")
    experiments.add_scene(...)

    return builder.build()
```

## Asset Management

### Organizing Assets

```
project/
├── build.py
├── models/
│   ├── robot1.xml
│   ├── robot2.xml
│   └── meshes/
│       ├── body.stl
│       └── arm.stl
├── policies/
│   ├── robot1_policy.onnx
│   └── robot2_policy.onnx
└── dist/  (generated)
```

### Relative Paths

Muwanx handles paths relative to your build script:

```python
# All paths relative to build script location
model = mujoco.MjModel.from_xml_path("models/robot.xml")
scene.add_policy(path="policies/policy.onnx", ...)
```

## Optimization

### Reduce Build Size

1. **Optimize ONNX Models**: Use ONNX optimizer

```python
import onnx
from onnxoptimizer import optimize

model = onnx.load("policy.onnx")
optimized = optimize(model)
onnx.save(optimized, "policy_optimized.onnx")
```

2. **Simplify Meshes**: Use lower-poly versions for web

3. **Remove Unused Assets**: Only include necessary files

### Improve Loading Speed

1. **Compress Assets**: Enable gzip compression on your server
2. **Use CDN**: Serve static assets via CDN
3. **Lazy Loading**: Only load policies when needed (future feature)

## Testing Builds

### Pre-deployment Checklist

- [ ] Test on multiple browsers (Chrome, Firefox, Safari)
- [ ] Test on mobile devices
- [ ] Verify all scenes load correctly
- [ ] Check policy behavior
- [ ] Confirm asset paths are correct
- [ ] Test on slow network connections
- [ ] Verify VR functionality (if used)

### Automated Testing

```python
def test_build():
    """Test that build succeeds and produces expected files."""
    import os
    from pathlib import Path

    app = build()

    # Check files exist
    dist = Path("dist")
    assert (dist / "index.html").exists()
    assert (dist / "config.json").exists()
    assert (dist / "assets").exists()

    print("✓ Build test passed!")
```

## Troubleshooting

### Build Failures

**Error: No projects added**

```python
# Bad
builder = mwx.Builder()
app = builder.build()  # Error!

# Good
builder = mwx.Builder()
builder.add_project(name="Project").add_scene(...)
app = builder.build()
```

**Error: Model file not found**

Check file paths are correct and relative to the build script.

### Deployment Issues

**Assets not loading (404 errors)**

Check `base_path` matches your deployment:

```python
# Wrong
builder = mwx.Builder(base_path="/")  # But deployed to /myapp/

# Correct
builder = mwx.Builder(base_path="/myapp/")
```

**CORS errors**

Ensure your server sends correct CORS headers for ONNX and model files.

## Best Practices

1. **Version Control**: Include build scripts in git, not built files
2. **Environment**: Use virtual environments for dependencies
3. **Documentation**: Document build process in README
4. **Automation**: Automate builds with CI/CD
5. **Testing**: Test builds before deploying

## Next Steps

- [Deployment Guide](../advanced/deployment.md) - Advanced deployment topics
- [VR Support](../advanced/vr-support.md) - Enable VR features
- [Examples](../examples/custom-models.md) - See complete examples
