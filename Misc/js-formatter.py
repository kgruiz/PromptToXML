from pathlib import Path

import jsbeautifier
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text


def humanReadableSize(size: int) -> str:
    """
    Converts bytes into a human-readable format.

    Parameters
    ----------
    size : int
        File size in bytes.

    Returns
    -------
    str
        Human-readable file size.
    """
    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.2f} {units[index]}"


def FormatJsFile(jsFilePath: Path | str, outputPath: Path | str = None) -> None:
    """
    Formats a JavaScript file and displays statistics.

    Parameters
    ----------
    jsFilePath : Path | str
        Path to the JavaScript file to be formatted.
    outputPath : Path | str, optional
        Path to save the formatted file. Defaults to input file path.

    Returns
    -------
    None
    """

    console = Console()
    jsPath = Path(jsFilePath)

    if not jsPath.is_file():
        console.print(
            Panel(
                f"[bold red]Error:[/bold red] File not found: {jsFilePath}",
                title="Error",
                style="bold red",
            )
        )
        return

    outputPath = Path(outputPath) if outputPath else jsPath

    # Read original JS file
    with jsPath.open("r", encoding="utf-8") as file:
        jsCode = file.read()

    originalSize = humanReadableSize(jsPath.stat().st_size)
    originalLines = len(jsCode.splitlines())

    # Beautify JavaScript code
    formattedJs = jsbeautifier.beautify(jsCode)

    formattedLines = len(formattedJs.splitlines())

    # Save formatted file
    with outputPath.open("w", encoding="utf-8") as file:
        file.write(formattedJs)

    formattedSize = humanReadableSize(outputPath.stat().st_size)

    # Display results
    table = Table(title="JavaScript File Formatting Results", style="bold cyan")
    table.add_column("Metric", style="bold yellow")
    table.add_column("Before", style="bold white")
    table.add_column("After", style="bold green")

    table.add_row("File Size", originalSize, formattedSize)
    table.add_row("Line Count", str(originalLines), str(formattedLines))

    console.print(table)
    console.print(f"[bold green]Formatted:[/bold green] {outputPath}")

    if formattedLines <= 100:

        syntax = Syntax(formattedJs, "javascript", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="Formatted Code", style="bold blue"))


if __name__ == "__main__":

    # jsFilePath = Path("Misc/ebd5ewokhsa7ru1i.js")
    jsFilePath = Path("test.js")

    FormatJsFile(jsFilePath)
