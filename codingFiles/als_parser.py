import gzip
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SPLICE_FOLDER = Path.home() / "Splice"


def get_value(element, tag):
    if element is None:
        return ""
    child = element.find(tag)
    if child is None:
        return ""
    return child.get("Value", "")


def track_name(track):
    name = track.find("Name")
    return get_value(name, "EffectiveName") or get_value(name, "UserName") or track.tag


def plugin_info(info):
    if info.tag == "VstPluginInfo":
        return {"name": get_value(info, "PlugName"), "format": "VST2"}
    elif info.tag == "Vst3PluginInfo":
        return {"name": get_value(info, "Name"), "format": "VST3"}
    else:
        return {"name": get_value(info, "Name"), "format": "AU"}


def sample_status(path, project_folder, splice_folder):
    p = Path(path)
    if not p.exists():
        return "missing"
    elif p.is_relative_to(splice_folder):
        return "splice"
    elif p.is_relative_to(project_folder):
        return "project"
    elif p.is_relative_to("/Applications") and "Ableton" in p.parts[2]:
        return "builtin"
    else:
        return "outside"


def parse_project(als_path, splice_folder=SPLICE_FOLDER):
    als_path = Path(als_path)
    splice_folder = Path(splice_folder)
    project_folder = als_path.parent

    with gzip.open(als_path) as f:
        root = ET.parse(f).getroot()

    live_set = root.find("LiveSet")
    tracks = list(live_set.find("Tracks"))
    for tag in ("MasterTrack", "MainTrack"):
        if live_set.find(tag) is not None:
            tracks.append(live_set.find(tag))

    samples = {}
    plugins = []
    for track in tracks:
        name = track_name(track)

        for ref in track.iter("SampleRef"):
            path = get_value(ref.find("FileRef"), "Path")
            if not path:
                continue
            if path not in samples:
                samples[path] = {
                    "path": path,
                    "name": Path(path).name,
                    "status": sample_status(path, project_folder, splice_folder),
                    "tracks": [],
                }
            if name not in samples[path]["tracks"]:
                samples[path]["tracks"].append(name)

        for tag in ("VstPluginInfo", "Vst3PluginInfo", "AuPluginInfo"):
            for info in track.iter(tag):
                plugin = plugin_info(info)
                plugin["track"] = name
                plugins.append(plugin)

    return {
        "project": str(als_path),
        "samples": list(samples.values()),
        "plugins": plugins,
    }


if __name__ == "__main__":
    result = parse_project(sys.argv[1])
    for s in result["samples"]:
        print(s["status"], s["name"])
    for p in result["plugins"]:
        print(p["name"], p["format"], p["track"])
