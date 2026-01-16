# Tripo3D Jewelry Generator

A robust CLI tool for generating high-quality 3D jewelry models using the Tripo3D API. This tool supports creating full jewelry pieces, segmenting existing models, and a unique "Modular Assembly" workflow for combining separate bands and gemstones.

## Features

- **Text-to-3D Generation**: Create detailed jewelry models from text prompts.
- **Modular Assembly**: Generate ring bands and gemstones separately for higher quality control, then merge them.
- **Automatic Segmentation**: Segment generated models into component parts.
- **Enhanced Prompts**: Built-in prompt engineering with professional 3D rendering keywords (Octane, Ray Tracing, PBR).
- **Integrated Viewer**: View your generated `.glb` models directly from the CLI.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- A Tripo3D API Key

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mesh-generator
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   TRIPO_API_KEY=your_tripo_api_key_here
   ```

## Usage

### Run the Generator
Start the interactive CLI:
```bash
uv run main.py
```

**Options:**
1. **Generate New Jewelry Piece**: Creates a single, complete jewelry model.
2. **Segment Existing Model**: Breaking a model down into its sub-meshes.
3. **Modular Assembly**: The recommended workflow for rings. Generates a high-quality band and a specific gemstone separately, giving you two distinct files (and an option to merge).

### View Models
View any generated model (GLB format) using the built-in viewer:
```bash
uv run view_model.py output/<filename>.glb
```

## Project Structure

- `main.py`: Entry point and CLI logic.
- `tripo_client.py`: Async wrapper for the Tripo3D API, handling distinct parameters like `negative_prompt`.
- `jewelry_prompts.py`: Prompt engineering logic for jewelry-specific attributes.
- `mesh_processor.py`: Utilities for inspecting and handling 3D mesh files.
- `view_model.py`: Lightweight 3D viewer using `trimesh` and `pyglet`.
- `output/`: Directory where generated models are saved.