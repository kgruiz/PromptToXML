import json
import shutil
import subprocess
from pathlib import Path

# Define paths
SVG_ICON: Path = Path("xml.svg")
BACKGROUND: Path = Path("icon-bg.png")
FINAL_ICON: Path = Path("icon-final.png")
ICONS_DIR: Path = Path("icons")
APPICONSET_DIR: Path = Path("../../Shared (App)/Assets.xcassets/AppIcon.appiconset")
EXTENTSION_IMAGES_DIR: Path = Path("../../Shared (Extension)/Resources/images")

# Define icon sizes and mappings for AppIcon.appiconset
ICON_SIZES: list[int] = [16, 32, 48, 64, 96, 128, 256, 384, 512, 1024]
ICON_MAPPING = {
    "16x16@1x": "icon-16.png",
    "16x16@2x": "icon-32.png",
    "32x32@1x": "icon-32.png",
    "32x32@2x": "icon-64.png",
    "128x128@1x": "icon-128.png",
    "128x128@2x": "icon-256.png",
    "256x256@1x": "icon-256.png",
    "256x256@2x": "icon-512.png",
    "512x512@1x": "icon-512.png",
    "512x512@2x": "icon-1024.png",
    # "1024x1024": "icon-1024.png",
}

EXTENSION_SIZES: list[int] = [48, 64, 96, 128, 256, 512]

# Remove and recreate icons directory if it exists
if ICONS_DIR.exists():
    shutil.rmtree(ICONS_DIR)
ICONS_DIR.mkdir(parents=True, exist_ok=True)

if EXTENTSION_IMAGES_DIR.exists():
    shutil.rmtree(EXTENTSION_IMAGES_DIR)
EXTENTSION_IMAGES_DIR.mkdir(parents=True, exist_ok=True)


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
        f'-draw "roundrectangle 0,0 1024,1024 222,222" "{BACKGROUND}"'
    )
    RunCommand(command)


def OverlaySvgOnBackground() -> None:
    """
    Overlay the transparent SVG onto the Apple-style background.

    The function overlays the SVG icon onto the background image using ImageMagick.
    """
    command = (
        f"magick '{BACKGROUND}' '{SVG_ICON}' -gravity center -composite '{FINAL_ICON}'"
    )
    RunCommand(command)


def GenerateResizedIcons() -> None:
    """
    Generate multiple icon sizes and save them to the icons directory.

    For each specified icon size, the function resizes the final icon image using ImageMagick.
    """

    for size in ICON_SIZES:
        outputFile: Path = ICONS_DIR / f"icon-{size}.png"
        command = f"magick '{FINAL_ICON}' -resize {size}x{size} '{outputFile}'"
        RunCommand(command)


def GenerateExtensionIcons() -> None:

    for size in EXTENSION_SIZES:
        outputFile: Path = EXTENTSION_IMAGES_DIR / f"icon-{size}.png"
        command = f"magick '{FINAL_ICON}' -resize {size}x{size} '{outputFile}'"
        RunCommand(command)

    extensionSvgPath: Path = EXTENTSION_IMAGES_DIR / "toolbar-icon.svg"

    shutil.copy(SVG_ICON, extensionSvgPath)


def GenerateAppIconSet() -> None:
    """
    Generate the AppIcon.appiconset folder with properly assigned icons and a Contents.json file.

    Parameters
    ----------
    None
    """

    # Ensure the AppIcon.appiconset directory exists
    APPICONSET_DIR.mkdir(parents=True, exist_ok=True)

    # Copy icons into AppIcon.appiconset
    for sizeKey, filename in ICON_MAPPING.items():

        sourceFile: Path = ICONS_DIR / filename
        targetFile: Path = APPICONSET_DIR / filename
        if sourceFile.exists():

            shutil.copy(sourceFile, targetFile)
        else:

            print(f"⚠️ Warning: Missing '{filename}' in '{ICONS_DIR}'")

    # Create Contents.json
    contents = {"images": [], "info": {"author": "xcode", "version": 1}}

    for sizeKey, filename in ICON_MAPPING.items():

        size, scale = sizeKey.split("@") if "@" in sizeKey else (sizeKey, "1x")
        contents["images"].append(
            {"idiom": "mac", "size": size, "scale": scale, "filename": filename}
        )

    # Write Contents.json file
    with open(APPICONSET_DIR / "Contents.json", "w") as jsonFile:

        json.dump(contents, jsonFile, indent=4)

    print(f"✅ AppIcon.appiconset successfully generated at '{APPICONSET_DIR}'!")


if __name__ == "__main__":

    CreateAppleIconBackground()
    OverlaySvgOnBackground()
    GenerateResizedIcons()
    GenerateAppIconSet()
    GenerateExtensionIcons()

    FINAL_ICON.unlink()
    BACKGROUND.unlink()

    print(
        f"✅ Apple app icons generated successfully in '{ICONS_DIR}' and assigned to AppIcon.appiconset!"
    )
