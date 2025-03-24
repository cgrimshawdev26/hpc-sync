import hydra
from omegaconf import DictConfig
from pathlib import Path
from typing import Optional

from .sync import HPCSync

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig, pull: bool = False) -> None:
    """
    Sync files between local machine and HPC server using rsync.
    Configuration is loaded from the config.yaml file.
    
    Args:
        cfg: Configuration from Hydra
        pull: If True, pull from HPC to local. If False, push from local to HPC.
    """
    source_dir = Path(cfg.sync.source_dir)
    target_dir = Path(cfg.sync.target_dir) / source_dir.name

    syncer = HPCSync(
        host=cfg.hpc.host,
        user=cfg.hpc.user,
        port=cfg.hpc.port,
        source_dir=str(source_dir),
        target_dir=str(target_dir),
        exclude=cfg.sync.exclude,
        options=cfg.sync.options,
    )
    
    success = syncer.sync(pull=pull)
    if not success:
        exit(1)

if __name__ == "__main__":
    main() 