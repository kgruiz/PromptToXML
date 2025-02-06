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

DARK_BACKGROUND = Path("dark-icon-bg.png")
DARK_FINAL_ICON = Path("dark-icon-final.png")

# Temporary directory for generated mac icons
ICONS_DIR = Path("icons")

# The AppIcon.appiconset directory – all icons (mac, iOS, watchOS) will be copied here.
APPICONSET_DIR = Path("../../Shared (App)/Assets.xcassets/AppIcon.appiconset")

# Extension images directory (unchanged)
EXTENTSION_IMAGES_DIR = Path("../../Shared (Extension)/Resources/images")

# Original mac icon sizes and mapping (used for legacy functionality)
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
# (Each spec includes a "pixels" key for internal resizing calculations.)
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

# Create dark iOS specs by copying IOS_FINAL_SPECS and adding an appearance entry.
IOS_DARK_FINAL_SPECS = []
for spec in IOS_FINAL_SPECS:
    darkSpec = spec.copy()
    darkSpec["appearances"] = [{"appearance": "luminosity", "value": "dark"}]
    IOS_DARK_FINAL_SPECS.append(darkSpec)

# Create tinted iOS specs similarly.
IOS_TINTED_FINAL_SPECS = []
for spec in IOS_FINAL_SPECS:
    tintedSpec = spec.copy()
    tintedSpec["appearances"] = [{"appearance": "luminosity", "value": "tinted"}]
    IOS_TINTED_FINAL_SPECS.append(tintedSpec)

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


def GenerateImage(spec, variantPrefix, master=FINAL_ICON, tint=False):
    """
    Generate an icon image by resizing the master icon.

    Parameters
    ----------
    spec : dict
        A dictionary with keys "size", optionally "scale", and "pixels".
    variantPrefix : str
        A prefix for the output filename (e.g., "ios", "ios_dark", "ios_tinted", "mac", or "watchos").
    master : Path, optional
        The master image file to use, by default FINAL_ICON.
    tint : bool, optional
        If True, apply a tint effect using a predefined color, by default False.

    Returns
    -------
    str
        The generated output filename.
    """
    pixels = spec["pixels"]
    scalePart = spec.get("scale", "")
    if scalePart:
        filename = f"{variantPrefix}_{spec['size']}_{scalePart}.png"
    else:
        filename = f"{variantPrefix}_{spec['size']}.png"
    outputFile = APPICONSET_DIR / filename
    if tint:
        command = f"magick '{master}' -resize {pixels}x{pixels} -fill '#007aff' -colorize 30 '{outputFile}'"
    else:
        command = f"magick '{master}' -resize {pixels}x{pixels} '{outputFile}'"
    RunCommand(command)
    return filename


# ------------------------------------------------------------------------------
# DARK/TINTED MASTER IMAGE FUNCTIONS
# ------------------------------------------------------------------------------
def CreateAppleDarkIconBackground():
    """
    Create a dark (black) rounded background using ImageMagick.

    Returns
    -------
    None
    """
    command = (
        f"magick -size 1024x1024 xc:none -fill black "
        f'-draw "roundrectangle 0,0 1024,1024 222,222" "{DARK_BACKGROUND}"'
    )
    RunCommand(command)


def OverlayDarkSvgOnBackground():
    """
    Overlay the dark SVG onto the dark background without a white backing.

    Returns
    -------
    None
    """
    # The addition of "-background none" prevents the dark SVG from being placed on a white background.
    command = f"magick '{DARK_BACKGROUND}' '{DARK_SVG_ICON}' -background none -gravity center -composite '{DARK_FINAL_ICON}'"
    RunCommand(command)


# ------------------------------------------------------------------------------
# ORIGINAL ICON GENERATION FUNCTIONS (for mac icons and extension icons)
# ------------------------------------------------------------------------------
def CreateAppleIconBackground():
    """
    Create a light rounded background using ImageMagick.

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
    Overlay the light SVG onto the light background.

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
    Generate mac icons by resizing the light master icon.
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
    default iOS, dark iOS, tinted iOS, mac, and watchOS icon specifications. For each image,
    generate the corresponding image file (by resizing the appropriate master icon)
    and include a "filename" attribute.

    Returns
    -------
    None
    """
    finalEntries = []

    # Generate default iOS icons using the light master icon.
    for spec in IOS_FINAL_SPECS:
        filename = GenerateImage(spec, "ios", master=FINAL_ICON, tint=False)
        entry = {k: v for k, v in spec.items() if k != "pixels"}
        entry["filename"] = filename
        finalEntries.append(entry)

    # Generate dark iOS icons using the dark master icon.
    for spec in IOS_DARK_FINAL_SPECS:
        filename = GenerateImage(spec, "ios_dark", master=DARK_FINAL_ICON, tint=False)
        entry = {k: v for k, v in spec.items() if k != "pixels"}
        entry["filename"] = filename
        finalEntries.append(entry)

    # Generate tinted iOS icons using the light master icon with a tint effect.
    for spec in IOS_TINTED_FINAL_SPECS:
        filename = GenerateImage(spec, "ios_tinted", master=FINAL_ICON, tint=True)
        entry = {k: v for k, v in spec.items() if k != "pixels"}
        entry["filename"] = filename
        finalEntries.append(entry)

    # Generate mac icons.
    for spec in MAC_FINAL_SPECS:
        filename = GenerateImage(spec, "mac", master=FINAL_ICON, tint=False)
        entry = {k: v for k, v in spec.items() if k != "pixels"}
        entry["filename"] = filename
        finalEntries.append(entry)

    # Generate watchOS icons.
    for spec in WATCHOS_FINAL_SPECS:
        filename = GenerateImage(spec, "watchos", master=FINAL_ICON, tint=False)
        entry = {k: v for k, v in spec.items() if k != "pixels"}
        entry["filename"] = filename
        finalEntries.append(entry)

    contents = {"images": finalEntries, "info": {"author": "xcode", "version": 1}}

    with open(APPICONSET_DIR / "Contents.json", "w") as jsonFile:
        json.dump(contents, jsonFile, indent=2)

    print(f"✅ Final Contents.json generated at '{APPICONSET_DIR}'!")


# ------------------------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Step 1: Create the light master icon.
    CreateAppleIconBackground()
    OverlaySvgOnBackground()

    # Step 2: Create the dark master icon.
    CreateAppleDarkIconBackground()
    OverlayDarkSvgOnBackground()

    # Step 3: (Original functionality) Generate the mac icons (temporary) and extension icons.
    GenerateResizedIcons()
    GenerateExtensionIcons()

    # Step 4: Generate the final Contents.json (with default, dark, tinted iOS icons, mac, and watchOS entries).
    GenerateFinalContents()

    # Cleanup temporary master files.
    # FINAL_ICON.unlink()
    # BACKGROUND.unlink()
    # DARK_FINAL_ICON.unlink()
    # DARK_BACKGROUND.unlink()

    print(
        f"✅ Apple app icons generated successfully and placed in '{APPICONSET_DIR}'!"
    )
