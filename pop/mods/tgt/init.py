__func_alias__ = {'eval_': 'eval'}


def eval_(hub, tgt_type, meta, tgt):
    if hasattr(hub.tgt, tgt_type):
        mod = getattr(hub.tgt, tgt_type)
        return mod.check(meta, tgt)
