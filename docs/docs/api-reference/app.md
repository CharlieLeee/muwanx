# MuwanxApp API Reference

The `MuwanxApp` class represents a built application ready to be launched or deployed.

## Class: MuwanxApp

```python
class MuwanxApp(app_dir: Path)
```

A built Muwanx application that can be launched in a web browser or deployed to a static hosting service.

### Parameters

- **app_dir** (`Path`): Directory containing the built application files

You typically don't create `MuwanxApp` instances directly - they're returned by [`Builder.build()`](builder.md#build).

## Methods

### launch

```python
def launch(
    *,
    host: str = "localhost",
    port: int = 8080,
    open_browser: bool = True
) -> None
```

Launch the application on a local web server.

**Parameters:**

- **host** (`str`, optional): Host to bind the server to. Defaults to `"localhost"`.
  - Use `"localhost"` for local-only access
  - Use `"0.0.0.0"` to allow network access
- **port** (`int`, optional): Port to run the server on. Defaults to `8080`.
  - If the port is unavailable, automatically finds the next available port
- **open_browser** (`bool`, optional): Whether to automatically open the default browser. Defaults to `True`.

**Raises:**

- `RuntimeError`: If the application directory doesn't exist
- `RuntimeError`: If no available port is found

**Example:**

```python
# Basic usage
app = builder.build()
app.launch()

# Custom port
app.launch(port=3000)

# Allow network access
app.launch(host="0.0.0.0", port=8080)

# Don't open browser
app.launch(open_browser=False)

# All options
app.launch(host="0.0.0.0", port=9000, open_browser=False)
```

### Behavior

- Starts a local HTTP server serving the application files
- Prints the server URL to the console
- If `open_browser=True`, opens the URL in the default browser
- Runs until interrupted (Ctrl+C)
- Automatically handles port conflicts by finding an available port

**Server Output:**

```
Starting server at http://localhost:8080
```

Or if port is unavailable:

```
Port 8080 unavailable — using port 8081 instead.
Starting server at http://localhost:8081
```

To stop the server, press `Ctrl+C`:

```
^C
Server stopped.
```

## Complete Examples

### Basic Workflow

```python
import mujoco
import muwanx as mwx

# Build application
builder = mwx.Builder()
project = builder.add_project(name="Demo")
model = mujoco.MjModel.from_xml_path("robot.xml")
project.add_scene(model=model, name="Robot")

# Build and launch
app = builder.build()
app.launch()
```

### Development Server

```python
# Development with custom settings
app = builder.build(output_dir="./dev_build")
app.launch(
    host="0.0.0.0",      # Accessible from other devices
    port=8000,
    open_browser=True
)
```

### Production Build

```python
# Build for production (don't launch)
app = builder.build(output_dir="./dist")

# Manually test if needed
if args.test:
    app.launch()
```

### Automated Testing

```python
import subprocess
import time
import requests

# Build and launch in background
app = builder.build()

# Start server in subprocess
proc = subprocess.Popen(
    ["python", "-c", "app.launch(open_browser=False)"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
time.sleep(2)

# Test endpoint
response = requests.get("http://localhost:8080")
assert response.status_code == 200

# Cleanup
proc.terminate()
```

## Deployment

For static deployment (GitHub Pages, Netlify, etc.), you don't use `launch()`. Instead, just build and deploy the output directory:

```python
# Build only
app = builder.build(output_dir="./dist")

# Deploy the ./dist directory to your hosting service
# No need to call app.launch()
```

## Notes

### Server Type

The server is a simple HTTP server suitable for:

- Local development
- Testing
- Demo purposes

For production, deploy as static files to a proper hosting service.

### Port Selection

If the requested port is unavailable, the server automatically tries the next port and continues until it finds an available one (up to 1000 attempts).

### Network Access

- `host="localhost"`: Only accessible from your machine
- `host="0.0.0.0"`: Accessible from other devices on your network
  - Useful for testing on mobile devices
  - Find your IP with `ipconfig` (Windows) or `ifconfig` (Unix)
  - Access from other devices: `http://YOUR_IP:8080`

### Browser Compatibility

The application requires a modern browser with:

- WebAssembly support
- WebGL support
- ES6+ JavaScript support

Supported browsers:

- Chrome/Edge (version 91+)
- Firefox (version 89+)
- Safari (version 15+)

### Security Considerations

- The built-in server is not hardened for production use
- Use proper hosting services for public deployment
- Be cautious when using `host="0.0.0.0"` on public networks

## Troubleshooting

### Port Already in Use

The server automatically handles this:

```
Port 8080 unavailable — using port 8081 instead.
```

Or manually specify a different port:

```python
app.launch(port=9000)
```

### Application Directory Not Found

Ensure you've built the application first:

```python
# Wrong
app = mwx.MuwanxApp(Path("nonexistent"))  # Error!
app.launch()

# Correct
app = builder.build()  # Creates the directory
app.launch()
```

### Browser Doesn't Open

If automatic browser opening fails:

1. Check the console output for the URL
2. Manually open the URL in your browser
3. Or disable automatic opening:

```python
app.launch(open_browser=False)
```

### Permission Denied

If you get permission errors on the port:

- Ports below 1024 require root/admin privileges
- Use ports ≥ 1024 (recommended: 8080, 8000, 3000)

## See Also

- [Builder.build()](builder.md#build) - Building applications
- [Building Projects Guide](../user-guide/building-projects.md) - Build and deployment
- [Deployment Guide](../advanced/deployment.md) - Production deployment
