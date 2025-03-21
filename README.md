# HPC Sync

A simple tool to sync local files with an HPC server using rsync.

## Installation

1. Clone this repository
2. Install the package and its dependencies:
   ```bash
   uv sync
   uv pip install -e .
   ```

## Configuration

The tool uses a YAML configuration file located at `hpc_sync/conf/config.yaml`. You can override the default configuration by:

1. Editing the default config file
2. Creating a new config file and using it with `--config-path`
3. Overriding specific values via command line: `hpc-sync hpc.host=my.hpc.server`

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
