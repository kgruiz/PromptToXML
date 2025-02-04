import subprocess
from pathlib import Path

# Define paths
svgIcon: Path = Path("xml.svg")
background: Path = Path("icon-bg.png")
finalIcon: Path = Path("icon-final.png")
iconsDir: Path = Path("icons")
iconSizes: list[int] = [16, 32, 64, 128, 256, 512, 1024]

# Ensure the output directory exists
iconsDir.mkdir(parents=True, exist_ok=True)


def RunCommand(command: str) -> None:
    """
    Run a shell command using subprocess.

    Parameters
    ----------
    command : str
        Shell command to be executed.

    """
    subprocess.run(command, shell=True, check=True)


def CreateAppleIconBackground() -> None:
    """
    Create a rounded Apple-style background.

    This function generates a rounded background image using ImageMagick.

    """
    command = (
        f"magick -size 1024x1024 xc:none -fill white "
        f'-draw "roundrectangle 0,0 1024,1024 222,222" {background}'
    )
    RunCommand(command)


def OverlaySvgOnBackground() -> None:
    """
    Overlay the transparent SVG onto the Apple-style background.

    The function overlays the SVG icon onto the background image using ImageMagick.

    """
    command = f"magick {background} {svgIcon} -gravity center -composite {finalIcon}"
    RunCommand(command)


def GenerateResizedIcons() -> None:
    """
    Generate multiple icon sizes and save them to the icons directory.

    For each specified icon size, the function resizes the final icon image using ImageMagick.

    """
    for size in iconSizes:
        outputFile: Path = iconsDir / f"icon-{size}.png"
        command = f"magick {finalIcon} -resize {size}x{size} {outputFile}"
        RunCommand(command)


if __name__ == "__main__":
    CreateAppleIconBackground()
    OverlaySvgOnBackground()
    GenerateResizedIcons()
    print(f"✅ Apple app icons generated successfully in '{iconsDir}'!")
