# Smart File Manager

An early Python desktop file-management application built with Tkinter and ttkbootstrap. It explores file navigation, colored tags and common file operations through a graphical interface.

**Status:** implemented application source, with known reliability and platform limitations. This is a learning/early project rather than a polished replacement for your operating system's file manager.

## Implemented interface and operations

- List files/directories, sort columns and navigate locations/drives.
- Create, rename and open files/directories.
- Copy files/directories with a progress dialog and background copying.
- Store colored/time-based file tags in JSON.
- Search names and offer ordinary, tag-based and copy-like-filename deletion dialogs.

These features are visible in source; complete interactive behavior has not been verified on a desktop during this documentation update.

## Stack and platform status

- Python, Tkinter, ttkbootstrap and Pillow.
- JSON tag storage under `res/tag_files.json`.
- `psutil` is declared in requirements, though no use was found in the two source modules.
- The source is Windows-oriented: launching uses `os.startfile` and several tag paths use backslashes. A Linux drive branch exists, but full Linux support is incomplete. macOS handling is not established.

## Installation

Use a desktop Python distribution with Tk support. The dependency/import checks below were performed with Python 3.11.16 on Linux; that does not establish Windows or Linux GUI correctness.

```bash
git clone https://github.com/jayeshchaudhari1210/Smart-File-Manager.git
cd Smart-File-Manager
python -m venv .venv
```

Activate `.venv/bin/activate` on Linux, or `.venv\Scripts\Activate.ps1` in Windows PowerShell, then:

```bash
python -m pip install -r requirements.txt Pillow
python -c "import tkinter, ttkbootstrap; from PIL import Image; print('Dependencies import')"
python src/main.py
```

Pillow is included explicitly because the source imports `PIL`, while requirements.txt does not directly declare Pillow. The requirements file has not been changed. On Linux, install your distribution's Tk package if `import tkinter` fails; a desktop display is needed to open the window.

Keep the `icons/` directory with the source. The application creates/uses tag data under `res/`; the checkout must be writable. The initial listing uses the process's current directory. Use a disposable folder with copies of files when evaluating the app.

## Important limitations

- **Duplicate selection compares names, not file contents or hashes.** Copy-like suffixes can identify unrelated data, including files with different extensions. It is not a reliable duplicate detector.
- Deletion asks for confirmation, then uses `os.remove` or `shutil.rmtree`. It does not provide an application recycle bin or undo. Avoid cleanup operations on valuable data.
- The Delete-key wrapper passes an argument to a zero-argument function and can raise `TypeError`.
- A search with no matches can display the complete directory listing because an empty result is interpreted as a refresh request.
- Some copy-progress GUI work occurs in a worker thread, and copy errors are not clearly surfaced.
- Tag cleanup mutates the list while iterating, which can skip matching entries.
- Windows-only opening/path handling prevents a claim of full cross-platform support.

These are documentation findings, not application fixes.

## Verification and screenshots

On 28 October 2026, both Python source files passed AST parsing and the declared/imported dependencies were checked in an isolated Python 3.11 environment. See the import command above to check your environment. No automated test suite is tracked. No GUI session or file deletion/copy test was performed during this update, and no screenshot is supplied because no verified screenshot was available.

## Source layout

```text
src/main.py       GUI, navigation, tags and file operations
src/ext.py        Extension-label helper
icons/            Interface assets
res/              Tag data
requirements.txt  Existing dependency list
```

## Next steps

Priorities are content-based duplicate checks, recoverable file operations, focused filesystem tests, safer GUI-thread updates and explicit platform support. Source provenance and licensing should be established before inviting external reuse; no root LICENSE was found in the reviewed tree.
