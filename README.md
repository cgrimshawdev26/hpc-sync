# HPC Sync

A simple tool to sync local files with an HPC server using rsync.

## Installation

1. Clone this repository
2. Install dependencies using uv:
   ```bash
   uv pip install -r requirements.txt
   ```
3. Install the package in development mode:
   ```bash
   uv pip install -e .
   ```

## Configuration

The tool uses a YAML configuration file located at `hpc_sync/conf/config.yaml`. You can override the default configuration by:

1. Editing the default config file
2. Creating a new config file and using it with `--config-path`
3. Overriding specific values via command line: `hpc-sync hpc.host=my.hpc.server`

Default configuration:
```yaml
hpc:
  host: "your.hpc.server"  # HPC server hostname
  user: "${oc.env:USER}"   # Default to current user
  port: 22                 # SSH port

sync:
  source_dir: "${hydra:runtime.cwd}"  # Current working directory
  target_dir: "~/projects/${hydra:runtime.cwd:name}"  # Remote directory
  exclude:
    - ".git/"
    - "__pycache__/"
    # ... (see config.yaml for full list)
  options:
    - "--archive"
    - "--compress"
    - "--verbose"
    - "--delete"
```

## Usage

Basic usage:
```bash
# Sync current directory using default configuration
hpc-sync

# Override HPC host
hpc-sync hpc.host=my.cluster.edu

# Override target directory
hpc-sync sync.target_dir=~/my/custom/path
```

The tool will:
1. Read the configuration
2. Build the rsync command with appropriate options
3. Execute the sync operation
4. Show progress and any warnings/errors

## Requirements

- Python 3.9+
- rsync installed on local machine
- SSH access to HPC server
