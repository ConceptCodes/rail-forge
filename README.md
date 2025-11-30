# Parametric Roller Coaster Track Generator

A powerful Python and OpenSCAD toolchain for generating 3D-printable roller coaster tracks. This tool accepts 3D coordinates (via CSV or algorithms), turns them into smooth track geometry, and intelligently slices the model into printable segments with interlocking connectors.

## Features

- **Parametric Geometry**: Generates realistic track profiles with rails, crossties, and a spine.
- **Intelligent Slicing**: Automatically partitions long tracks into segments that fit your 3D printer's build volume.
- **Interlocking Connectors**: Automatically generates male/female connectors (pegs and sockets) with configurable tolerance for easy assembly.
- **Banking & Orientation**: Calculates correct banking and frame orientation vectors (Forward, Up, Right) for every point on the track.
- **CSV Support**: Import your own track designs from simple CSV files.
- **Automated Rendering**: Renders all segments to STL files in one command.

## Prerequisites

1.  **OpenSCAD**: This tool relies on OpenSCAD for 3D generation.
    *   **macOS**: Install via `brew install --cask openscad` or download from [openscad.org](https://openscad.org/).
    *   **Windows/Linux**: Install from [openscad.org](https://openscad.org/).
2.  **Python 3.11+**
3.  **uv** (Recommended): A fast Python package and project manager.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/conceptcodes/rail-forge.git
    cd rail-forge
    ```

2.  Initialize the environment:
    ```bash
    uv sync
    ```

## Usage

The primary interface is `generate.py`.

### 1. Generate a Demo Track
If no input file is provided, the tool generates a demo helix/loop track.

```bash
uv run generate.py --render
```

### 2. Generate from CSV
You can provide a CSV file containing `x, y, z` coordinates.

```bash
# or use one of the example tracks
uv run generate.py tracks/left_turn.csv --scale 100 --render
```

### 3. Slicing for Your Printer
Use the `--max-length` argument to specify your printer's bed size (in mm). The tool will split the track into segments that fit.

```bash
# For a printer with a 256mm build plate
uv run generate.py tracks/helix.csv --scale 100 --max-length 250 --output-dir my_coaster --render
```

This will produce files named `track_segment_01_of_XX.stl` inside the `my_coaster/` directory.

### Command Line Arguments

| Argument | Description | Default |
| :--- | :--- | :--- |
| `file` | Input CSV file (optional). | Demo Helix |
| `--scale` | Scale factor for input points. | `1.0` |
| `--max-length` | Maximum length of a track segment in mm. | `250.0` |
| `--render` | Automatically render STL files using OpenSCAD. | `False` |
| `--openscad` | Path to OpenSCAD executable. | `openscad` |
| `--output-dir` | Directory to save generated STL files. | `.` |

## CSV Format

Your CSV files should contain 3 columns (X, Y, Z). Headers are optional (the parser skips lines that aren't numeric).

```csv
0.0, 0.0, 0.0
10.0, 5.0, 2.0
20.0, 10.0, 5.0
...
```

See the `tracks/` directory for examples:
- `straight.csv`: Basic straight track
- `helix.csv`: Unit-circle spiral (requires scaling)
- `airtime_hill.csv`: Parabolic hill
- `left_turn.csv` / `right_turn.csv`: 90-degree turns

## Project Structure

This project is structured as a modular Python package:

```text
generate.py           # CLI entry point
track.scad            # OpenSCAD geometry definition
spline_data.scad      # (generated) data file passed to OpenSCAD
tracks/               # Example CSV tracks
src/
│   └── roller_coaster/
│       ├── geometry.py   # Vector math & path generation algorithms
│       ├── track.py      # Slicing & partitioning logic
│       ├── io.py         # File I/O (CSV reading, SCAD writing)
│       └── render.py     # OpenSCAD process orchestration
└── pyproject.toml        # Project configuration
```

## Customizing the Track Design

You can modify `track.scad` to change the aesthetic of the coaster:
- `track_gauge`: Width between rails.
- `rail_diameter`: Thickness of the rails.
- `crosstie_spacing`: Distance between ties.
- `tolerance`: Fit tolerance for connectors (default 0.2mm).
