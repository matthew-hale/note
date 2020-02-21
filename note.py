#!/bin/python3
#
# note.py
#
# A simple note parser; uses tags based on the PARA method of tagging.
#
# PARA stands for:
#
# * Projects
# * Areas (of responsibility)
# * Research topics
# * Archive (past projects)

import argparse
from glob import glob
import re

# This function returns a list of all the unique tags present in the 
# list of file dictionaries provided. If a tag is provided as an 
# argument that isn't "allowed", the function will simply return a null 
# value; the same thing happens when there are no tags of the given tag 
# in the file dictionaries provided.
def get_tags(tag, files):
    if not tag in tags:
        return None
    # This clever line simply says:
    # "For each file, if the tag has content, return that tag's content"
    matches = [file[tag] for file in files if file[tag] != None]

    # Finally, we sort and return our output if there is one
    return sorted(set(matches)) if matches else None

# These are our note tags. Tags in a note file have the following 
# requirements to be parsed correctly:
#
tags = ("project", "area", "research")
#
# * Notes are tagged with these tags in the first three lines of a file
# * The tag must start at the beginning of the line
# * The tag must have a colon or an equals sign 
# * The tag may come after a space, or right after the tag definition
# * There must be no whitespace at the end of the line after the tag
#
# Examples of proper tags (ignoring the space after these comment 
# signs; pretend that the '# ' doesn't exist):
#
# project=demo
# area: life
# research:computer hardware
#
# Now we have the rules for our regular expression searches, as defined 
# here.
project_re = re.compile("(^project[:=])([a-zA-Z0-9 \\-_]*$)", re.I)
area_re = re.compile("(^area[:=])([a-zA-Z0-9 \\-_]*$)", re.I)
research_re = re.compile("(^research[:=])([a-zA-Z0-9 \\-_]*$)", re.I)


# This grabs files of extensions "*.md" and "*.txt" in the same 
# directory as where the script was called. Future version of this 
# script can add supported extensions simply by adding string globs to 
# the extensions tuple.
file_names = []
extensions = ("*.md", "*.txt")
for extension in extensions:
    for file in glob(extension):
        file_names.append(file)

# Now we come to the meat of the program. We're gathering a list of 
# dictionaries containing the following:
#
# * The filename
# * The values of that file's tags, if any
#
# First, we create our empty list of file dicts:
#
files = []
#
# Now we can iterate through each file, creating a dictionary, 
# populating its keys, and appending it to this list.
#
for file in file_names:
    # This is what each dictionary looks like
    current_file = {
        "name": file,
        "project": None,
        "area": None,
        "research": None
    }
    # We open the file, and read the first 3 lines. Then, we iterate 
    # through the lines, pulling out the values of any matching tags we 
    # find. One thing to note here: any leading whitespace in a tag's 
    # value is stripped. For example, if I have a tag that looks like 
    # this:
    #
    # project: demo
    #
    # The space after the colon ':' will not be included in the tag's 
    # value of "demo".
    with open(file) as f:
        content = []
        for i in range(0, 4):
            content.append(f.readline())
        for line in content:
            project = project_re.match(line)
            area = area_re.match(line)
            research = research_re.match(line)
            if project:
                current_file["project"] = project.group(2).strip()
            if area:
                current_file["area"] = area.group(2).strip()
            if research:
                current_file["research"] = research.group(2).strip()
    files.append(current_file)

# With all of the work done getting the formatted file data, it's time to parse user input.
