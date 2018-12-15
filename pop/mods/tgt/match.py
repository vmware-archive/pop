def check(meta, tgt):
    for key in tgt:
        if key in meta:
            return meta[key] == tgt[key]
    return False
