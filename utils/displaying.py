from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
from rich.align import Align

custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "banner": "bold magenta"
})

console = Console(theme=custom_theme)

BANNER = r"""
  _________ .__                   .___ __________                                  
  \_   ___ \|  |   ____  __ __  __| _/\______   \ ____ _____  ______   ___________ 
  /    \  \/|  |  /  _ \|  |  \/ __ |  |       _// __ \\__  \ \____ \_/ __ \_  __ \
  \     \___|  |_(  <_> )  |  / /_/ |  |    |   \  ___/ / __ \|  |_> >  ___/|  | \/
   \______  /____/\____/|____/\____ |  |____|_  /\___  >____  /   __/ \___  >__|   
          \/                       \/         \/     \/     \/|__|        \/       
"""

def print_banner():
    console.print(Panel(
        Align.center(
            Text(BANNER, style="bold red") + 
            Text("\n\nCloudReaper: The Ultimate Cloudflare Bypass Tool\n", style="bold white") +
            Text("v2.0 Professional Edition", style="bold magenta")
        ),
        border_style="red",
        subtitle="[dim]Author: HUNT3R | Telegram: @hunt3rxxxx[/dim]"
    ))

def print_info(msg):
    console.print(f"[bold blue][INFO][/bold blue] {msg}")

def print_success(msg):
    console.print(Panel(f"[bold green]{msg}[/bold green]", title="[bold green]SUCCESS[/bold green]", border_style="green"))

def print_warning(msg):
    console.print(f"[bold yellow][WARN][/bold yellow] {msg}")

def print_error(msg):
    console.print(Panel(f"[bold red]{msg}[/bold red]", title="[bold red]ERROR[/bold red]", border_style="red"))
