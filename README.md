# filesnap

`filesnap` is a command-line tool for managing files and directories.

## Motivation
filesnap was born out of necessity in a professional production environment. Dealing with massive directory structures and thousands of assets manually is error-prone and slow.

I built this tool to:
    - Automate Database Seeding: Quickly export entire folders of images or assets into structured formats (CSV, JSON) to sync filenames with database records.
    - Bulk Audit: Count and scan files by extension.
    - Smart Cleanup: Safely prune specific file types or filenames across nested directories using --dry-run to prevent accidental data loss.

## Installation

you can install it globally using uv by [astral](https://github.com/astral-sh/uv)
```bash
uv tool install filesnap
```

or with pip
```bash
pip3 install filesnap
```

## Commands

### `filesnap scan`

Scans all the files in the path.

| Argument | Description | Default |
|---|---|---|
| `path` | Path to scan | Current directory |

| Option | Alias | Description |
|---|---|---|
| `--recursive` | `-r` | Recursive search. |
| `--pretty` | `-p` | Pretty print the output in a table. |
| `--exclude` | | Exclude files/directories from scanning. |
| `--ext` | `-e` | Scan only files with these extensions. |

### `filesnap count`

Counts all the files by extension in the path selected.

| Argument | Description | Default |
|---|---|---|
| `path` | Path to count | Current directory |

| Option | Alias | Description |
|---|---|---|
| `--recursive` | `-r` | Recursive search. |
| `--exclude` | | Exclude files/directories from counting. |

### `filesnap clean`

Cleans the content of a path.

| Argument | Description |
|---|---|
| `path` | Path to clean |

| Option | Alias | Description |
|---|---|---|
| `--recursive` | `-r` | Recursive cleaning. |
| `--contain` | `-c` | Clean only files containing this string. |
| `--ext` | `-e` | Clean only files with these extensions. |
| `--exclude` | | Exclude files/directories from cleaning. |
| `--force` | `-f` | Force deletion without confirmation. |
| `--dry-run` | `--dry` | Simulate cleaning without deleting files. |

### `filesnap export`

Exports the filenames to a file.

| Argument | Description |
|---|---|
| `path` | Path to scan for filenames |

| Option | Alias | Description |
|---|---|---|
| `--type` | `-t` | The type of file to export to (e.g., `txt`, `csv`, `json`). |
| `--recursive` | `-r` | Recursive scanning. |
| `--output` | `-o` | The output file name. |
| `--format` | `-f` | The format of the output. |
| `--column` | `-c` | The column to export (defaults to `file_name`). |

