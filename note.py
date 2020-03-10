#!/bin/python3
#
# note.py
#
# A simple program to use a directory of plaintext files as a slip-box

import argparse
import os
import sys
from glob import glob
import re
import json

# Our "id" tag regex
_id_re = re.compile("(id[:=] ?[a-zA-Z0-9]+)", re.I)

# Allowed extensions; currently a hardcoded variable, but I may turn it 
# into a parameter
_extensions = ("*.md", "*.txt")

# Given an input string, return a list of all of the id tags as single 
# strings
def get_ids(string):
    result = []
    matches = _id_re.findall(string)
    for match in matches:
        value = match[3:].strip()
        result.append(value)
    return result

# Given an id, return the file from _files (if it exists)
def get_file_by_id(string):
    for f in _files:
        if f["id"] == string:
            return f
    return None

def get_file_by_name(string):
    for f in _files:
        if f["name"] == string:
            return f
    return None

# Arguments will use subcommands.
parser = argparse.ArgumentParser(description = "note management tool")
parser.add_argument("-d", "--directory",
                    dest = "directory",
                    help = "directory in which note will search",
                    type = str)
format_choices = ["text", "json"]
parser.add_argument("-f", "--format",
                    metavar = "<format>",
                    dest = "format",
                    help = "output format; one of: " + str(format_choices),
                    choices = format_choices ,
                    default = "text",
                    type = str)

subparsers = parser.add_subparsers(title = "subcommands",
                                   dest = "subcommand_name")

parser_list = subparsers.add_parser("list",
                                    help = "list notes based on tags/categiries")

parser_tree = subparsers.add_parser("tree",
                                    help = "show a tree of notes (non-recursive, 1 layer deep)")
parser_tree.add_argument("target",
                         metavar = "<target>",
                         type = str,
                         help = "target ID, or all")

parser_get = subparsers.add_parser("get",
                                   help = "get filename(s) by id")
parser_get.add_argument("target",
                        metavar = "<target>",
                        nargs = '+',
                        type = str,
                        help = "target ID(s)")

args = parser.parse_args()

# Need to parse directory first
if args.directory:
    if os.path.isdir(args.directory):
        os.chdir(args.directory)
    else:
        raise OSError(args.directory + " does not exist or is not a directory")

# Gather file names
file_names = []
for extension in _extensions:
    for file in glob(extension):
        file_names.append(file)

# Parse files
#
_files = []
#
# This results in a list of file dictionaries that contain a few 
# things:
#
# + filename
# + file's id
# + any cross references present in the file
for name in file_names:
    current_file = {
        "name": name,
        "id": None,
        "references": []
    }
    
    with open(name) as f:
        # Store the first line, then read and parse the rest, adding 
        # ids to references
        first_line = f.readline()
        current_file["id"] = get_ids(first_line)
        if current_file["id"]:
            current_file["id"] = current_file["id"][0]
            for line in f:
                references = get_ids(line)
                for reference in references:
                    current_file["references"].append(reference)
            # Dedup
            current_file["references"] = sorted(list(set(current_file["references"])))
        else:
            current_file["id"] = "(none)"

    _files.append(current_file)

# If we have no files, we want to silently exit
if not _files:
    sys.exit()

# Sort files by id (makes everything else easier)
_files.sort(key=lambda x: x["id"])

# Argument parsing
#
# List will display files based on IDs and ID references
if args.subcommand_name == "list":
    if args.format == "text":
        for f in _files:
            id_length = len(f["id"])
            left_length = 24-id_length
            outstring = "{}".format(f["id"])
            # Four tab caracters here:
            outstring += "				"
            outstring += f["name"]
            if f["references"]:
                # Again, tabs (3 this time)
                outstring += "			references: " + ", ".join(f["references"])
            print(outstring)
    elif args.format == "json":
        print(json.dumps(_files, indent=4))
#
# Tree will display a tree of files based on ID
#
# The tree shows:
#
# + the root file
# + the root file's linkers (files that link to it), if applicable
# + the root file's descendants and cross references
elif args.subcommand_name == "tree":
    if args.format == "text":
        root_file = get_file_by_id(args.target)
        # First get a list of files which are children of our root 
        # file
        descendants = []
        for r in root_file["references"]:
            f = get_file_by_id(r)
            descendants.append(f)
        # Next, get a list of files which link to our root file
        linkers = []
        for f in _files:
            if root_file["id"] in f["references"]:
                linkers.append(f)
        # Our output should look like this:
        #
        # linker 1        root_file        descendant 1
        # linker 2                         descendant 2
        #                                  descendant 3
        # ...with our root file in the middle column, our linkers on 
        # the left, and our descendants on the right.
        loop_length = max(len(descendants), len(linkers))
        for i in range(0, loop_length):
            if len(descendants) > i:
                desc_string = "{}: {}".format(descendants[i]["id"], descendants[i]["name"])
            else:
                desc_string = "	"
            if len(linkers) > i:
                link_string = "{}: {}".format(linkers[i]["id"], linkers[i]["name"])
            else:
                link_string = "	"
            if i == 0:
                root_string = "{}: {}".format(root_file["id"], root_file["name"])
            else:
                root_string = "	"
            print("{}			{}			{}".format(link_string, root_string, desc_string))

#
# Returns file(s) by id; simple
elif args.subcommand_name == "get":
    targets = []
    for target in args.target:
        f = get_file_by_id(target)
        if f:
            targets.append(f)
    if args.format == "text":
        for target in targets:
            print(target["name"])
    elif args.format == "json":
        print(json.dumps(targets, indent=4))
