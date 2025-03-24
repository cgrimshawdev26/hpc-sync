import subprocess
from pathlib import Path
from typing import List

from rich.console import Console
from rich.panel import Panel

console = Console()

class HPCSync:
    def __init__(
        self,
        host: str,
        user: str,
        port: int,
        source_dir: str,
        target_dir: str,
        exclude: List[str],
        options: List[str],
    ):
        self.host = host
        self.user = user
        self.port = port
        self.source_dir = Path(source_dir).expanduser().resolve()
        self.target_dir = target_dir
        self.exclude = exclude
        self.options = options

    def build_rsync_command(self, pull: bool = False) -> List[str]:
        """Build the rsync command with all options.
        
        Args:
            pull: If True, pull from remote to local. If False, push from local to remote.
        """
        cmd = ["rsync"]
        
        # Add standard options
        cmd.extend(self.options)
        
        # Add exclude patterns
        for pattern in self.exclude:
            cmd.extend(["--exclude", pattern])
        
        # Ensure .git is always excluded
        cmd.extend(["--exclude", ".git", "--exclude", ".git/**"])
        
        # Add SSH options
        cmd.extend(["-e", f"ssh -p {self.port}"])
        
        # Add source and destination based on direction
        if pull:
            source = f"{self.user}@{self.host}:{self.target_dir}/"
            destination = str(self.source_dir)
        else:
            source = str(self.source_dir) + "/"  # Trailing slash to sync contents
            destination = f"{self.user}@{self.host}:{self.target_dir}"
            
        cmd.extend([source, destination])
        
        # Print the command for debugging
        console.print(f"[dim]Running command: {' '.join(cmd)}[/dim]")
        
        return cmd

    def sync(self, pull: bool = False) -> bool:
        """Execute the sync operation.
        
        Args:
            pull: If True, pull from remote to local. If False, push from local to remote.
        """
        cmd = self.build_rsync_command(pull=pull)
        
        if pull:
            from_path = f"{self.user}@{self.host}:{self.target_dir}"
            to_path = str(self.source_dir)
        else:
            from_path = str(self.source_dir)
            to_path = f"{self.user}@{self.host}:{self.target_dir}"
        
        console.print(
            Panel(
                f"[bold blue]{'Pulling' if pull else 'Pushing'}[/bold blue]\n"
                f"From: [green]{from_path}[/green]\n"
                f"To: [green]{to_path}[/green]"
            )
        )
        
        try:
            process = subprocess.run(
                cmd,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            
            console.print(process.stdout)
            
            if process.stderr:
                console.print(f"[yellow]Warnings:[/yellow]\n{process.stderr}")
            
            console.print("[bold green]✓ Sync completed successfully![/bold green]")
            return True
            
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Error during sync:[/bold red]")
            console.print(e.stderr)
            return False
        except Exception as e:
            console.print(f"[bold red]Unexpected error:[/bold red] {str(e)}")
            return False 