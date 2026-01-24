---
icon: octicons/download-16
---

# Installation

Muwanx can be installed using either Python (pip) or JavaScript (npm), depending on your preferred workflow.

## Python Installation

Install Muwanx with pip:

```bash
pip install muwanx
```

For development work, you can install with optional dependencies:

```bash
pip install muwanx[dev]
```

For running examples:

```bash
pip install muwanx[examples]
```

## JavaScript Installation

Install Muwanx with npm:

```bash
npm install muwanx
```

Or with yarn:

```bash
yarn add muwanx
```

## Requirements

- **Python**: Version 3.10 or higher
- **Node.js**: Version 20 or higher (for npm installation)
- **Browser**: Modern browser with WebAssembly and WebGL support

### Python Dependencies

The following are automatically installed with Muwanx:

- `mujoco>=3.4.0` - MuJoCo physics engine
- `nodeenv>=1.9.1` - Node.js environment management
- `onnx>=1.20.0` - ONNX model format support
- `wandb>=0.23.1` - Experiment tracking (optional)

## Verify Installation

After installation, you can verify that Muwanx is installed correctly:

```python
import muwanx
print(muwanx.__version__)
```
