import shutil
from pathlib import Path

PACKAGE_FOLDER = Path(__file__).parent.parent / "selectedFile"


def unique_path(dest):
    n = 2
    new_dest = dest
    while new_dest.exists():
        new_dest = dest.with_name(f"{dest.stem} ({n}){dest.suffix}")
        n += 1
    return new_dest


def package(scan, out=PACKAGE_FOLDER):
    if out.exists():
        shutil.rmtree(out)
    (out / "samplesUsed").mkdir(parents=True)
    (out / "recordedFiles").mkdir()
    shutil.copy2(scan["project"], out)

    copied = []
    for sample in scan["samples"]:
        if sample["status"] in ("builtin", "missing"):
            continue

        if "Recorded" in Path(sample["path"]).parts:
            folder = "recordedFiles"
        else:
            folder = "samplesUsed"

        dest = unique_path(out / folder / sample["name"])
        shutil.copy2(sample["path"], dest)
        copied.append(folder + "/" + dest.name)

    return {"folder": str(out), "copied": copied}
