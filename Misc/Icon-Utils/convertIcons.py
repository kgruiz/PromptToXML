import json
import shutil
import subprocess
from pathlib import Path

# ------------------------------------------------------------------------------
# MACRO_CASE CONSTANTS
# ------------------------------------------------------------------------------
SVG_ICON = Path("xml.svg")
DARK_SVG_ICON = Path("dark-xml.svg")
BACKGROUND = Path("icon-bg.png")
FINAL_ICON = Path("icon-final.png")

# Temporary directory for generated mac icons
ICONS_DIR = Path("icons")

# The AppIcon.appiconset directory – all icons (mac, iOS, and watchOS) will be copied here.
APPICONSET_DIR = Path("../../Shared (App)/Assets.xcassets/AppIcon.appiconset")

# Extension images directory (unchanged)
EXTENTSION_IMAGES_DIR = Path("../../Shared (Extension)/Resources/images")

# Mac icon sizes and mapping (original functionality)
ICON_SIZES = [16, 32, 48, 64, 96, 128, 256, 384, 512, 1024]
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
    # "1024x1024": "icon-1024.png",  # Uncomment if needed
}

# ------------------------------------------------------------------------------
# FINAL SPECIFICATIONS FOR CONTENTS.JSON
# (Each spec includes a "pixels" key for internal calculations.)
# ------------------------------------------------------------------------------
IOS_FINAL_SPECS = [
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "2x",
        "size": "20x20",
        "pixels": 40,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "3x",
        "size": "20x20",
        "pixels": 60,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "2x",
        "size": "29x29",
        "pixels": 58,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "3x",
        "size": "29x29",
        "pixels": 87,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "2x",
        "size": "38x38",
        "pixels": 76,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "3x",
        "size": "38x38",
        "pixels": 114,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "2x",
        "size": "40x40",
        "pixels": 80,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "3x",
        "size": "40x40",
        "pixels": 120,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "2x",
        "size": "60x60",
        "pixels": 120,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "3x",
        "size": "60x60",
        "pixels": 180,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "2x",
        "size": "64x64",
        "pixels": 128,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "3x",
        "size": "64x64",
        "pixels": 192,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "2x",
        "size": "68x68",
        "pixels": 136,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "2x",
        "size": "76x76",
        "pixels": 152,
    },
    {
        "idiom": "universal",
        "platform": "ios",
        "scale": "2x",
        "size": "83.5x83.5",
        "pixels": 167,
    },
    {"idiom": "universal", "platform": "ios", "size": "1024x1024", "pixels": 1024},
]

MAC_FINAL_SPECS = [
    {"idiom": "mac", "scale": "1x", "size": "16x16", "pixels": 16},
    {"idiom": "mac", "scale": "2x", "size": "16x16", "pixels": 32},
    {"idiom": "mac", "scale": "1x", "size": "32x32", "pixels": 32},
    {"idiom": "mac", "scale": "2x", "size": "32x32", "pixels": 64},
    {"idiom": "mac", "scale": "1x", "size": "128x128", "pixels": 128},
    {"idiom": "mac", "scale": "2x", "size": "128x128", "pixels": 256},
    {"idiom": "mac", "scale": "1x", "size": "256x256", "pixels": 256},
    {"idiom": "mac", "scale": "2x", "size": "256x256", "pixels": 512},
    {"idiom": "mac", "scale": "1x", "size": "512x512", "pixels": 512},
    {"idiom": "mac", "scale": "2x", "size": "512x512", "pixels": 1024},
]

WATCHOS_FINAL_SPECS = [
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "22x22",
        "pixels": 44,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "24x24",
        "pixels": 48,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "27.5x27.5",
        "pixels": 55,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "29x29",
        "pixels": 58,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "30x30",
        "pixels": 60,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "32x32",
        "pixels": 64,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "33x33",
        "pixels": 66,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "40x40",
        "pixels": 80,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "43.5x43.5",
        "pixels": 87,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "44x44",
        "pixels": 88,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "46x46",
        "pixels": 92,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "50x50",
        "pixels": 100,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "51x51",
        "pixels": 102,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "54x54",
        "pixels": 108,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "86x86",
        "pixels": 172,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "98x98",
        "pixels": 196,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "108x108",
        "pixels": 216,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "117x117",
        "pixels": 234,
    },
    {
        "idiom": "universal",
        "platform": "watchos",
        "scale": "2x",
        "size": "129x129",
        "pixels": 258,
    },
    {"idiom": "universal", "platform": "watchos", "size": "1024x1024", "pixels": 1024},
]

# ------------------------------------------------------------------------------
# DIRECTORY PREPARATION
# ------------------------------------------------------------------------------
for directory in [ICONS_DIR, EXTENTSION_IMAGES_DIR, APPICONSET_DIR]:
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------------------
# UTILITY FUNCTIONS
# ------------------------------------------------------------------------------
def RunCommand(command):
    """
    Run a shell command using subprocess.

    Parameters
    ----------
    command : str
        The shell command to be executed.
    """
    subprocess.run(command, shell=True, check=True)


def GenerateImage(spec, variantPrefix):
    """
    Generate an icon image by resizing the master icon.

    Parameters
    ----------
    spec : dict
        A dictionary with keys "size", optionally "scale", and "pixels".
    variantPrefix : str
        A prefix for the output filename (e.g., "ios", "mac", or "watchos").

    Returns
    -------
    str
        The generated output filename.
    """
    # Use the provided "pixels" value.
    pixels = spec["pixels"]

    scalePart = spec.get("scale", "")
    if scalePart:
        filename = f"{variantPrefix}_{spec['size']}_{scalePart}.png"
    else:
        filename = f"{variantPrefix}_{spec['size']}.png"
    outputFile = APPICONSET_DIR / filename
    command = f"magick '{FINAL_ICON}' -resize {pixels}x{pixels} '{outputFile}'"
    RunCommand(command)
    return filename


# ------------------------------------------------------------------------------
# ORIGINAL ICON GENERATION FUNCTIONS (for mac icons and extension icons)
# ------------------------------------------------------------------------------
def CreateAppleIconBackground():
    """
    Create a rounded Apple-style background using ImageMagick.

    Returns
    -------
    None
    """
    command = (
        f"magick -size 1024x1024 xc:none -fill white "
        f'-draw "roundrectangle 0,0 1024,1024 222,222" "{BACKGROUND}"'
    )
    RunCommand(command)


def OverlaySvgOnBackground():
    """
    Overlay the transparent SVG onto the Apple-style background.

    Returns
    -------
    None
    """
    command = (
        f"magick '{BACKGROUND}' '{SVG_ICON}' -gravity center -composite '{FINAL_ICON}'"
    )
    RunCommand(command)


def GenerateResizedIcons():
    """
    Generate mac icons by resizing the final icon image.
    The generated images are stored temporarily in ICONS_DIR.

    Returns
    -------
    None
    """
    for size in ICON_SIZES:
        outputFile = ICONS_DIR / f"icon-{size}.png"
        command = f"magick '{FINAL_ICON}' -resize {size}x{size} '{outputFile}'"
        RunCommand(command)


def GenerateExtensionIcons():
    """
    Generate extension icons and copy the toolbar SVG.

    Returns
    -------
    None
    """
    extensionSizes = [48, 64, 96, 128, 256, 512]
    for size in extensionSizes:
        outputFile = EXTENTSION_IMAGES_DIR / f"icon-{size}.png"
        command = f"magick '{FINAL_ICON}' -resize {size}x{size} '{outputFile}'"
        RunCommand(command)
    extensionSvgPath = EXTENTSION_IMAGES_DIR / "toolbar-icon.svg"
    shutil.copy(SVG_ICON, extensionSvgPath)


# ------------------------------------------------------------------------------
# FINAL CONTENTS.JSON GENERATION FUNCTION
# ------------------------------------------------------------------------------
def GenerateFinalContents():
    """
    Generate the final Contents.json file in APPICONSET_DIR using the specified
    iOS, mac, and watchOS icon specifications. Also generate the corresponding
    image files (by resizing the master icon). Each image entry will include a
    "filename" attribute.

    The final JSON structure will be as follows:

    {
      "images": [
        { "idiom": "universal", "platform": "ios", "scale": "2x", "size": "20x20", "filename": "<name>" },
        { "idiom": "universal", "platform": "ios", "scale": "3x", "size": "20x20", "filename": "<name>" },
        ... (remaining iOS entries) ...,
        { "idiom": "mac", "scale": "1x", "size": "16x16", "filename": "<name>" },
        ... (remaining mac entries) ...,
        { "idiom": "universal", "platform": "watchos", "scale": "2x", "size": "22x22", "filename": "<name>" },
        ... (remaining watchOS entries) ...
      ],
      "info": {
         "author": "Kaden Gruizenga",
         "version": 0.1
      }
    }

    Returns
    -------
    None
    """
    finalEntries = []

    # Generate iOS icons and add entries
    for spec in IOS_FINAL_SPECS:
        filename = GenerateImage(spec, "ios")
        entry = {k: v for k, v in spec.items() if k != "pixels"}
        entry["filename"] = filename
        finalEntries.append(entry)

    # Generate mac icons and add entries
    for spec in MAC_FINAL_SPECS:
        filename = GenerateImage(spec, "mac")
        entry = {k: v for k, v in spec.items() if k != "pixels"}
        entry["filename"] = filename
        finalEntries.append(entry)

    # Generate watchOS icons and add entries
    for spec in WATCHOS_FINAL_SPECS:
        filename = GenerateImage(spec, "watchos")
        entry = {k: v for k, v in spec.items() if k != "pixels"}
        entry["filename"] = filename
        finalEntries.append(entry)

    contents = {
        "images": finalEntries,
        "info": {"author": "Kaden Gruizenga", "version": 0.1},
    }

    with open(APPICONSET_DIR / "Contents.json", "w") as jsonFile:
        json.dump(contents, jsonFile, indent=2)

    print(f"✅ Final Contents.json generated at '{APPICONSET_DIR}'!")


# ------------------------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Step 1: Create the master icon image.
    CreateAppleIconBackground()
    OverlaySvgOnBackground()

    # Step 2: Generate the mac icons (temporary) and copy them to APPICONSET_DIR.
    GenerateResizedIcons()

    # Step 3: Generate extension icons (remain in their designated folder).
    GenerateExtensionIcons()

    # Step 4: Generate the final Contents.json (with iOS, mac, and watchOS entries including filename)
    GenerateFinalContents()

    # Cleanup temporary files.
    FINAL_ICON.unlink()
    BACKGROUND.unlink()

    print(
        f"✅ Apple app icons generated successfully and placed in '{APPICONSET_DIR}'!"
    )
