---
icon: octicons/download-16
---

# Installation

muwanx can be installed using either Python (pip) or JavaScript (npm), depending on your preferred workflow.

<div class="grid cards" markdown>

-   [:simple-python: &nbsp; __Python package__](#python-installation){ style="text-decoration: none; color: inherit;" }

    ---

    Install via pip to quickly build and share interactive MuJoCo simulations

-   [:simple-javascript: &nbsp; __JavaScript package__](#javascript-installation){ style="text-decoration: none; color: inherit;" }

    ---

    Install via npm for custom web applications with TypeScript support

-   [:simple-github: &nbsp; __GitHub Source__](#github-source){ style="text-decoration: none; color: inherit;" }

    ---

    Clone the repository for development and contributing to the project

>   :simple-docker: &nbsp; __Docker / Cluster__
>   ---
>   Not supported yet.

</div>

## Requirements

- **Python**: Version 3.10 or higher
- **Node.js**: Version 20 or higher (for npm installation)
- **Browser**: Modern browser with WebAssembly and WebGL support

## Python Installation

Install muwanx with pip:

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

Install muwanx with npm:

```bash
npm install muwanx
```

Or with yarn:

```bash
yarn add muwanx
```

## GitHub Source

Clone the repository:

```bash
git clone https://github.com/ttktjmt/muwanx.git
cd muwanx
```

Install dependencies:

```bash
uv sync --all-extras
```
