#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

def print_usage():
    import sys
    import os.path
    print("Usage:", os.path.basename(sys.argv[0]), "[ips-patch] [file to patch]")

def ips_patch(patch, file):
    p = open(patch, mode="rb")
    if p.read(5) != b"PATCH":
        print("patch file invalid (missing 'PATCH' magic bytes)")
        return False

    f = open(file, mode="r+b")
    num = 0
    while True:
        offset = p.read(3)
        size   = p.read(2)
        if offset == b"EOF" and len(size) == 0:
            break
        if len(offset) != 3 or len(size) != 2:
            print("patch file invalid (premature end of file)")
            return False

        offset = (offset[0] << 16) + (offset[1] << 8) + (offset[2])
        if size != b"\0\0":
            size   = (size[0] << 8) + (size[1])
            diff   = p.read(size)
            if len(diff) != size:
                print("patch file invalid (should read %d bytes, but got only %d)" \
                    % (size, len(diff)))
        else: # rle mode
            size = p.read(2)
            diff = p.read(1)
            if len(size) != 2 or len(diff) != 1:
                print("patch file invalid (premature end of file)")
                return False
            size = (size[0] << 8) + (size[1])
            diff = diff * size
        f.seek(offset)
        f.write(diff)
        num += 1

    print("%d patches applied" % num)
    return True

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print_usage()
        sys.exit()
    else:
        sys.exit(ips_patch(sys.argv[1], sys.argv[2]))
