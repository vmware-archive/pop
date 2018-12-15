# Import python libs
import fnmatch


def check(meta, tgt):
    for key in tgt:
        if key in meta:
            return fnmatch(meta[key], tgt[key])
    return False
