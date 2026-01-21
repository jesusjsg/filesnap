# filesnap

A simple CLI to manage files.

## Commands

### `scan`

Scan all the files in the path.

**Usage:**

```bash
filesnap scan [OPTIONS] [PATH]
```

**Arguments:**

*   `[PATH]`: Path to scan. [default: current directory]

**Options:**

*   `--recursive`: Recursive search to list files in subfolders.
*   `--pretty`: Pretty table to show all the files. Note: this take more time if the path have a lot files.
*   `--help`: Show this message and exit.

### `sync`

This command is not implemented yet.
