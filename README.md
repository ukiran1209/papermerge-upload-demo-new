# Papermerge upload demo

A local Python fixture for the three routine names in
[CVE-2026-105314](https://nvd.nist.gov/vuln/detail/CVE-2026-105314).
The demo stores a small sample in a temporary directory and verifies the bytes
before removing the directory. It needs no database or web server.

## Run

Use Python 3.13 and Git. PyPI does not publish `papermerge-core==3.5.3`.
The manifest declares that exact version for the scanner fixture. For the
source-based demo, install the remaining entries and run the pinned checkout.

```sh
python3.13 -m venv .venv
. .venv/bin/activate
awk '$0 != "papermerge-core==3.5.3"' requirements.txt | python -m pip install -r /dev/stdin
./run.sh
```

`requirements.txt` pins the commit behind the
[papermerge-core 3.5.3 release](https://github.com/papermerge/papermerge-core/releases/tag/3.5.3).
The runner reads the source pin from `requirements.txt` and imports the checked
out modules directly. Pip installs the dependencies used by those modules.
The runner removes its temporary source checkout when it exits.

## Routine mapping

| Routine | Where the demo gets it |
| --- | --- |
| `upload_document` | Demo adapter that accepts a filename and bytes. The 3.5.3 router exposes [`upload_file`](https://github.com/papermerge/papermerge-core/blob/3.5.3/papermerge/core/features/document/router.py#L128-L189). |
| `docver_path` | [Imported from Papermerge 3.5.3](https://github.com/papermerge/papermerge-core/blob/3.5.3/papermerge/core/pathlib.py). |
| `LocalBackend.upload` | Demo adapter that delegates to [`copy_file`](https://github.com/papermerge/papermerge-core/blob/3.5.3/papermerge/core/utils/misc.py), the writer used by the [3.5.3 upload implementation](https://github.com/papermerge/papermerge-core/blob/3.5.3/papermerge/core/features/document/db/api.py). The release has no `papermerge.storage.backends.local` module. |

The demo exercises local storage with a fixed sample filename. It models the
call chain independently of the HTTP endpoint and database.

## Build and scanner inputs

`pyproject.toml` is the Python build manifest. It packages `demo.py`
and reads its dependency list from `requirements.txt`.

Point the scanner at the directory containing `pyproject.toml`. To build a
wheel, run `python -m pip wheel --no-deps .` from that directory.

The Papermerge source pin is read by `run.sh`. To scan the upstream Python
files as well, include a checkout of that pinned revision in the scan.
