#!/bin/python3
#
# note.py
#
# A simple note parser; uses tags based on the PARA method of tagging.
#
# PARA stands for:
#
# + Projects
# + Areas (of responsibility)
# + Resources
# + Archive (past projects)
#
# More specifically, this program uses the "PAR" method, as there's 
# currently no support for any archiving system. The simplest way to 
# put files into an archive would be to simply move them into an 
# archive folder, which you can search separately.

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

# Similar to get_tags, the get_files function will return a list of 
# filenames of those files that contain the given tag.
def get_files(tag, tag_type, files):
    if not tag_type in tags:
        return None
    matches = [file["name"] for file in files if file[tag_type] == tag]
    # We don't need unique values here - in theory, the file system 
    # should take care of that for us - but we would like the result to 
    # be in alphabetical order.
    return matches

# These are our note tags. 
#
tags = ("project", "area", "resource")
#
# Tags in a note file have the following requirements to be parsed 
# correctly:
#
# + Notes are tagged with these tags in the first three lines of a file
# + The tag must start at the beginning of the line
# + The tag must have a colon or an equals sign 
# + The tag may come after a space, or right after the tag definition
# + There must be no whitespace at the end of the line after the tag
#
# Examples of proper tags (ignoring the space after these comment 
# signs; pretend that the '# ' doesn't exist):
#
# project=demo
# area: life
# resource:computer hardware
#
# Now we have the rules for our regular expression searches, as defined 
# here.
project_re = re.compile("(^project[:=])([a-zA-Z0-9 \\-_]*$)", re.I)
area_re = re.compile("(^area[:=])([a-zA-Z0-9 \\-_]*$)", re.I)
resource_re = re.compile("(^resource[:=])([a-zA-Z0-9 \\-_]*$)", re.I)


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
        "resource": None
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
            resource = resource_re.match(line)
            if project:
                current_file["project"] = project.group(2).strip()
            if area:
                current_file["area"] = area.group(2).strip()
            if resource:
                current_file["resource"] = resource.group(2).strip()
    files.append(current_file)

# With all of the work done getting the formatted file data, it's time 
# to parse user input. Everything else will depend on what parameters 
# the user has defined.
#
# First, we'll define a simple argument parser:
#
parser = argparse.ArgumentParser(description = "note management tool")
#
# Next, we'll define a subparser object for our subcommands, giving 
# it a destination variable of 'subcommand_name' so that we can test 
# based on which subcommand was provided:
#
subparsers = parser.add_subparsers(title = "subcommands",
                                   dest = "subcommand_name")
#
# To this, we'll add our subcommands, followed by any additional 
# arguments for each one
#
#
# # list
#
# This command is used to produce a list of files, filtered by any tags 
# or categories that the user provides. The syntax looks like this:
#
#   $ note list project pythfinder
#   $ note list area "personal development"
#   $ note list resource "sorting algorithms"
#   $ note list category resource
#   $ note list all
#
# etc.
#
parser_list = subparsers.add_parser("list",
                                    add_help = False,
                                    help = "list notes based on tags/categiries")
parser_list.add_argument("target",
                         metavar = "target",
                         choices = ["project", "area", "resource", "category", "all"],
                         help = "type of list target",
                         type = str)
parser_list.add_argument("subject",
                         metavar = "subject",
                         help = "the specific tag/category to list",
                         nargs = "?",
                         default = None,
                         type = str)
parser_list.add_argument("-f", "--format",
                         dest = "format",
                         help = "",
                         choices = ["pretty", "text"],
                         default = "pretty",
                         type = str)
args = parser.parse_args()
#
# Now we enter the logic for parsing user arguments. First, we parse 
# subcommand with a simple if-elif structure on the 'subcommand_name' 
# variable; afterwards, we'll do further parsing of each subcommand's 
# required and optional arguments.
#
if args.subcommand_name == "list":
    target = args.target
    subject = args.subject
    #
    # The only target that doesn't require a subject is "all"; thus, we 
    # test that subject is present if the target is not all. If we're 
    # missing a subject when we need one, we'll throw an error.
    #
    if target != "all" and subject == None:
        raise ValueError("subject is required for targets != 'all'")
    if target == "all":
        print("all")
    # All of the 'project', 'area', 'resource' targets behave the same 
    # way, so we group them here.
    elif target in ("project", "area", "resource"):
        output_files = []
        matching_files = get_files(subject, target, files)
        if matching_files:
            for item in matching_files:
                output_files.append(item)
        if args.format == "pretty":
            print("\n    {}: {}".format(target, subject))
            print("\n    " + "\n    ".join(output_files) + "\n")
        elif args.format == "text":
            for file in output_files:
                print(file)
    elif target == "category":
        print("category")
