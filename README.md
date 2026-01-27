# filesnap

A simple CLI to manage files.

## Commands

### `scan`

Scan all the files in the path.

**Usage:**

```bash
filesnap scan [PATH] [OPTIONS]
```

**Arguments:**

*   `[PATH]`: Path to scan. [default: current directory]

**Options:**

*   `--recursive`: Recursive search to list files in subfolders.
*   `--pretty`: Pretty table to show all the files. Note: this take more time if the path have a lot files.

### `count`

Count all the files by extension.

**Usage:**

```bash
filesnap count [PATH] [OPTIONS] 
```

**Arguments:**

* `[PATH]`: Path to count. [default: current directory]

**Options:**

*   `--recursive`: Recursive search to list files in subfolders.
