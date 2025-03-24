import hydra
from omegaconf import DictConfig
from pathlib import Path

from .sync import HPCSync

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    """
    Sync local files with HPC server using rsync.
    Configuration is loaded from the config.yaml file.
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
    
    success = syncer.sync()
    if not success:
        exit(1)

if __name__ == "__main__":
    main() 