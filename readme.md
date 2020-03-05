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

+ Implement ID parsing for both the file and cross references

### Why subcommand?
You may be wondering: this script only has one subcommand, so why do 
that at all? Why not just take positional parameters without the "list" 
subcommand?

The answer is mostly because I'd hate to have to refactor it to fit 
into a subcommand architecture later if I wanted to; plus, originally I 
had this idea that there would be multiple subcommands ready to go, but 
the only useful one I came up with was what you see in "list".
