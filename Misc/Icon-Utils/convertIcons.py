import subprocess
from pathlib import Path

# Define paths
SVG_ICON: Path = Path("xml.svg")
BACKGROUND: Path = Path("icon-bg.png")
FINAL_ICON: Path = Path("icon-final.png")
ICONS_DIR: Path = Path("icons")
ICON_SIZES: list[int] = [16, 32, 64, 128, 256, 512, 1024]

if ICONS_DIR.exists():

    import shutil

    shutil.rmtree(ICONS_DIR)

# Ensure the output directory exists
ICONS_DIR.mkdir(parents=True, exist_ok=True)


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
        f'-draw "roundrectangle 0,0 1024,1024 222,222" {BACKGROUND}'
    )
    RunCommand(command)


def OverlaySvgOnBackground() -> None:
    """
    Overlay the transparent SVG onto the Apple-style background.

    The function overlays the SVG icon onto the background image using ImageMagick.

    """
    command = f"magick {BACKGROUND} {SVG_ICON} -gravity center -composite {FINAL_ICON}"
    RunCommand(command)


def GenerateResizedIcons() -> None:
    """
    Generate multiple icon sizes and save them to the icons directory.

    For each specified icon size, the function resizes the final icon image using ImageMagick.

    """
    for size in ICON_SIZES:
        outputFile: Path = ICONS_DIR / f"icon-{size}.png"
        command = f"magick {FINAL_ICON} -resize {size}x{size} {outputFile}"
        RunCommand(command)

    FINAL_ICON.unlink()
    BACKGROUND.unlink()


if __name__ == "__main__":
    CreateAppleIconBackground()
    OverlaySvgOnBackground()
    GenerateResizedIcons()
    print(f"✅ Apple app icons generated successfully in '{ICONS_DIR}'!")
