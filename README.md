# HPC Sync

A simple tool to sync files between local machine and HPC server using rsync.

## Installation

1. Clone this repository
2. Install the package and its dependencies:
   ```bash
   uv sync
   uv tool install .
   ```

## Configuration

The tool uses a YAML configuration file located at `hpc-sync/conf/config.yaml`. You can override the default configuration by:

1. Editing the default config file
2. Creating a new config file and using it with `--config-path`
3. Overriding specific values via command line: `hpc-sync hpc.host=my.hpc.server`

## Usage

Basic usage:
```bash
# Push current directory to HPC using default configuration
hpc-sync

# Pull from HPC to local machine
hpc-sync pull=true

# Override HPC host
hpc-sync hpc.host=my.cluster.edu

# Override target directory
hpc-sync sync.target_dir=~/my/custom/path
```

The tool will:
1. Read the configuration
2. Build the rsync command with appropriate options
3. Execute the sync operation (push to HPC by default, pull if specified)
4. Show progress and any warnings/errors

## Requirements

- rsync installed on local machine
- SSH access to server
