# What is Note?
Note is a simple tool that interacts with a notes directory, and parses 
notes based on tags to show you relevant notes.

## Features

+ Uses the PARA system for tags and interfacing
+ Notes are plain text - markdown makes for easy rendering
+ Displays all tags hierarchically according to PARA
+ Output formats include:
    + Pretty printing (default)
    + Plain text (filenames)

## Example usage

Say you have four files, with the following first few lines:

todo.txt:
```
project: strucure future projects
area: personal development
resource: project management
...
```

project1.txt:
```
project: project1
area: health
...
```

note.md:
```
resource: git commands
```

empty.txt (an empty file)

Here's what would happen with a bunch of different `note` commands.

### List all

```
$ note list all

    project
        project1
            project1.txt
        structure future projects
            todo.txt
    area
        health
            project1.txt
        personal development
            todo.txt
    resource
        git commands
            note.md
        project management
            todo.txt
    untagged
        empty.txt

$ note list all --format text
empty.txt
note.md
project1.txt
todo.txt
$
```

### List all projects/areas/resources

```
$ note list category project

    projects:
        project1
        structure future projects

$ note list category project -f text
project1
structure future projects
```

### List specific project/area/resource

```
$ note list project project1

    project: project1
        project1.txt

$ note list project project1 --format text
project1.txt
$ note list area health

    area: health
        project1.txt

$ note list area health --format=text
project1.txt
# etc...
```

### Using note in a script
Here's a little example of a script that uses `note` to produce a list 
of files with a given project tag, piping that list to `dmenu` so that 
the user can use `vim` (or their $EDITOR of choice) on the chosen file.

```sh
#!/bin/sh

if [ -z "$1" ]; then
    echo "Usage: $0 <project name>"
    exit 1
fi

selection=$(note.py list project "$1" --format=text | dmenu)

if [ -n "$selection" ]; then
    "$EDITOR" "$selection"
fi
```

## Roadmap

+ Add basic subcommand argument structure:
    + ~~note list~~
    + ~~note search~~
        + I think this is better served with a simple grep, or small 
        script that uses note to produce a list of files to search with 
        grep. Don't rewrite the wheel, as it were.
    + If I think of any other subcommands that this should have, I'll 
    add them here.
+ ~~Add parameter for specific directory (current behavior: note only 
searches the current working directory)~~ - complete
+ ~~Allow multiple "resource" tags (current behavior: only one resource 
tag per document)~~ - complete
+ ~~Allow multiple "area" tags (current behavior: only one area tag per 
document)~~ - complete

### Why subcommand?
You may be wondering: this script only has one subcommand, so why do 
that at all? Why not just take positional parameters without the "list" 
subcommand?

The answer is mostly because I'd hate to have to refactor it to fit 
into a subcommand architecture later if I wanted to; plus, originally I 
had this idea that there would be multiple subcommands ready to go, but 
the only useful one I came up with was what you see in "list".
