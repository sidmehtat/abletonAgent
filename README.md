# Ableton Project Packager

**Author:** Siddharth Mehta

## What it is

A small desktop app that packs an Ableton Live project into one folder. The folder holds the project file and every audio file it uses, so the project can be moved to another computer or shared with someone else.

## What it solves

An Ableton project (`.als`) doesn't contain its audio. It only stores the paths to samples and recordings saved elsewhere on your computer, such as your Splice folder or the project's `Samples/Recorded` folder. Send someone just the `.als` and they open a project full of missing files. Gathering every sample by hand is slow and easy to get wrong. This app reads the project and collects the files for you.

## How it works (for the user)

1. Open Ableton, use **File → Collect All and Save** on your project, and close it.
2. Start the app. You need Python 3.11, which has tkinter built in:
   ```
   cd codingFiles
   python3.11 main.py
   ```
3. If your Splice samples aren't in `~/Splice`, click **Choose Splice folder** and pick the right one.
4. Click **Select file** and choose your `.als` file in Finder.
5. The app creates a `selectedFile` folder in the project with this layout:
   ```
   selectedFile/
     yourProject.als
     samplesUsed/      Splice and other samples the project uses
     recordedFiles/    audio you recorded in Ableton
   ```
   The window lists everything that was copied and any third-party plugins the project uses.

Your original project is never changed. Each new selection replaces the `selectedFile` folder. MIDI isn't copied separately because it's stored inside the `.als` file. Ableton's built-in sounds are skipped because every Ableton install already has them.

## What's done so far

- **Parser:** opens the `.als` file (gzip-compressed XML) and lists every sample it uses and which track uses it.
- **Plugin list:** shows every third-party plugin (VST2, VST3 and Audio Unit) and the track it's on.
- **Packager:** copies the project file into `selectedFile/`, recordings into `recordedFiles/`, and all other samples into `samplesUsed/`. If two samples have the same name, the second is saved as `name (2)` so it doesn't overwrite the first.
- **Desktop app:** a plain window built with tkinter, with a button to pick the project and a button to pick the Splice folder.
- **Testing:** tested on one real project made in Ableton Live 11.3. It copied 22 audio files: 12 recordings and 10 samples.

## What's left

- **Test on more projects:** run it on 3 to 5 of my own projects and record how many samples each one has.
- **Samples saved anywhere:** find samples that have been moved by searching for their file name, and include frozen, flattened and consolidated audio from `Samples/Processed`.
- **Fix the paths:** rewrite the paths inside the copied `.als` so the samples load automatically on another computer, with no "missing files" prompt.
- **Plugin warning:** tell the user which tracks use third-party plugins and should be frozen or flattened before sharing.
- **Drag-and-drop interface:** drop a project onto the window and see live progress, like "Copying 12 of 40".
