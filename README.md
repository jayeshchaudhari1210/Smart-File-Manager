# Smart File Manager

An early Python desktop file-management application built with Tkinter and ttkbootstrap. It explores file navigation, colored tags and common file operations through a graphical interface.

**Status:** implemented application source, with known reliability and platform limitations. This is a learning/early project rather than a polished replacement for your operating system's file manager.

## Implemented interface and operations

- List files/directories, sort columns and navigate locations/drives.
- Create, rename and open files/directories.
- Copy files/directories with a progress dialog and background copying.
- Store colored/time-based file tags in JSON.
- Search names and offer ordinary, tag-based and content-based duplicate comparison and Trash dialogs.

These features are visible in source; complete interactive behavior has not been verified on a desktop during this documentation update.

## Stack and platform status

- Python, Tkinter, ttkbootstrap and Pillow.
- JSON tag storage under `res/tag_files.json`.
- `psutil` is declared in requirements, though no use was found in the two source modules.
- Native opening is implemented for Windows, Linux and macOS. Full interactive behavior on each platform remains unverified.

## Installation

Use a desktop Python distribution with Tk support. The dependency/import checks below were performed with Python 3.11.16 on Linux; that does not establish Windows or Linux GUI correctness.

```bash
git clone https://github.com/jayeshchaudhari1210/Smart-File-Manager.git
cd Smart-File-Manager
python -m venv .venv
```

Activate `.venv/bin/activate` on Linux, or `.venv\Scripts\Activate.ps1` in Windows PowerShell, then:

```bash
python -m pip install -r requirements.txt
python -c "import tkinter, ttkbootstrap; from PIL import Image; print('Dependencies import')"
python src/main.py
```

Pillow and Send2Trash are declared directly in requirements.txt. On Linux, install your distribution's Tk package if `import tkinter` fails; a desktop display is needed to open the window.

Keep the `icons/` directory with the source. The application creates/uses tag data under `res/`; the checkout must be writable. The initial listing uses the process's current directory. Use a disposable folder with copies of files when evaluating the app.

## Safety and reliability updates

- Duplicate selection now compares file sizes and SHA-256 contents, ignores directories/symlinks and prefers non-copy-looking original names. Contents are checked again after confirmation.
- Deletion moves items to the operating system Trash using Send2Trash. A Trash error is reported without falling back to permanent deletion. Confirmation is still required.
- Empty search results remain empty. The Delete shortcut calls the correct popup signature.
- Copy-progress widgets remain on the GUI thread, using timer polling; existing destinations are not silently overwritten and copy errors are shown.
- Native opening uses the platform's launcher; tag paths use platform-aware joins. These changes do not establish complete Windows/Linux/macOS compatibility.

Use disposable copies when evaluating the GUI. Large-folder content hashing can take time. The application remains early software; no full interactive cross-platform validation has been performed.

## Verification and screenshots

On 28 October 2026, seven regression tests passed on Python 3.11.16. They cover differing content under copy-like names, content-identical files, rechecks after mutation, Trash delegation/failure, empty results, the Delete shortcut and nonblocking progress callbacks. GUI dependencies import successfully. File operation tests run on pushes and pull requests. No real user files were deleted or moved during tests.

```bash
python -m unittest discover -s tests -v
```

No verified GUI screenshot is supplied. Browser screenshots of the portfolio are separate from validation of this desktop application.

## Source layout

```text
src/main.py       GUI, navigation, tags and file operations
src/ext.py        Extension-label helper
icons/            Interface assets
res/              Tag data
requirements.txt  Existing dependency list
```

## Next steps

Next priorities are broader interactive platform testing, responsiveness for very large folders and further filesystem edge-case coverage. Content comparison, Trash behavior and targeted regression tests are now implemented. Source provenance and licensing should be established before inviting external reuse; no root LICENSE was found in the reviewed tree.
