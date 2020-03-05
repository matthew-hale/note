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
format_choices = ["text"]
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
                         nargs = '?',
                         type = str,
                         default = "all",
                         help = "target ID, or all")

parser_edit = subparsers.add_parser("edit",
                                    help = "edit file by id")
parser_edit.add_argument("target",
                         metavar = "<target>",
                         nargs = '+',
                         type = str,
                         help = "target ID")

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
            current_file["references"] = list(set(current_file["references"]))
        else:
            current_file["id"] = "(none)"

    _files.append(current_file)

# If we have no files, we want to silently exit
if not _files:
    sys.exit()

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
# Tree will display a tree of files based on ID
#
# The tree shows:
#
# + the root file
# + the root file's descendants
# + each of these files' immediate cross references (if applicable)
elif args.subcommand_name == "tree":
    if args.format == "text":
        if args.target != "all":
            tree_list = []
            # First get a list of files which are children of our root 
            # file
            for f in _files:
                result = re.match(args.target, f["id"])
                if result:
                    tree_list.append(f)
            # For each file in our list, we want to do the following:
            #
            # + print the id and the name
            # + indented, print the ids and names of its references
        else:
            tree_list = _files.copy()
        for f in tree_list:
            print("{}				{}".format(f["id"], f["name"]))
            for r in f["references"]:
                ref = get_file_by_id(r)
                if ref:
                    print("	{}			{}".format(ref["id"], ref["name"]))
