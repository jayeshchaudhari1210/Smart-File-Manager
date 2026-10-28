"""Content comparison helpers; no filesystem mutation occurs here."""
import hashlib
import re
from pathlib import Path


def digest(path):
    result = hashlib.sha256()
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.digest()


def same_content(first, second):
    a, b = Path(first), Path(second)
    return (a.is_file() and b.is_file() and not a.is_symlink()
            and not b.is_symlink() and a.stat().st_size == b.stat().st_size
            and digest(a) == digest(b))


def duplicate_candidates(directory):
    """Return candidate/original pairs, preferring non-copy-looking originals."""
    paths = [p for p in Path(directory).iterdir() if p.is_file() and not p.is_symlink()]
    paths.sort(key=lambda p: (bool(re.search(r'(?: - Copy(?: \(\d+\))?| \(\d+\))$', p.stem)), p.name.casefold()))
    originals = {}
    result = []
    for path in paths:
        key = (path.stat().st_size, digest(path))
        if key in originals:
            result.append((path, originals[key]))
        else:
            originals[key] = path
    return result
