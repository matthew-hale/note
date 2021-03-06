# What is Note?

Note is a tool that enables a slip-box-based note workflow with 
plaintext files. It parses note IDs and cross-references, allowing this 
network to be displayed and explored.

## Features

+ Notes are plain text - markdown makes for easy rendering
+ Output formats include:
    + Plain text
    + JSON (TODO)

## Example usage

```
$ note list
(none)				readme.md
1				git.md
1a				git-syntax.md
1b				git-config.md
1c				git-server-setup.md
1d				git-workstation-setup.md
1d1				git-workstation-setup2.md
1e				git-rebase.md
1f				git-workflow.md
2				routines.md
3				meme.txt
4				project-outline.md
5				meetings.md
6a				program-ideas.md
```

## Roadmap

+ ~~ID parsing for both the file and cross references~~
+ ~~`tree` subcommand~~
+ ~~`get` subcommand~~
+ ~~JSON output format~~
