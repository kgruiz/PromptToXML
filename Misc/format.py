import json
from pathlib import Path

# fullRecordingPath = Path("send-button-record.json")

# jsonFiles = Path(__file__).parent.glob("*.json")

# for jsonFile in jsonFiles:;

#     with jsonFile.open("r") as file:

#         fullRecording = json.load(file)

#     with jsonFile.open("w") as file:

#         json.dump(fullRecording, file, indent=4)

currentDir = Path(__file__).parent

jsonFiles = currentDir.glob("*.json")

for jsonFile in jsonFiles:

    print(jsonFile.relative_to(currentDir))

    with jsonFile.open("r") as file:

        fullRecording = json.load(file)

    recording = fullRecording["recording"]

    print(recording.keys())

    raise SystemExit

    # with jsonFile.open("w") as file:

    #     json.dump(fullRecording, file, indent=4)
