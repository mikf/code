#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys

def list_absolute_links():
    for link in filter(os.path.islink, sys.argv[1:] or os.listdir()):
        target = os.readlink(link)
        if os.path.isabs(target):
            yield target, os.path.abspath(link)

for target, link in list_absolute_links():
    link_dir = os.path.dirname(link)
    os.unlink(link)
    os.symlink( os.path.relpath(target, link_dir), link )
    # print(target, link, os.path.relpath(target, link_dir))
