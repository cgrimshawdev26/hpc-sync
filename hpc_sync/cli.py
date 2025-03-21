import hydra
from omegaconf import DictConfig

from .sync import HPCSync

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    """
    Sync local files with HPC server using rsync.
    Configuration is loaded from the config.yaml file.
    """
    syncer = HPCSync(
        host=cfg.hpc.host,
        user=cfg.hpc.user,
        port=cfg.hpc.port,
        source_dir=cfg.sync.source_dir,
        target_dir=cfg.sync.target_dir,
        exclude=cfg.sync.exclude,
        options=cfg.sync.options,
    )
    
    success = syncer.sync()
    if not success:
        exit(1)

if __name__ == "__main__":
    main() 