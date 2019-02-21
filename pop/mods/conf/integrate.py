'''
Integrate is used to pull config data from multiple sources and merge it into
the hub. Once it is merged then when a sub is loaded the respective config data
is loaded into the sub as `OPTS`
'''
# Take an *args list of modules to import and look for config.py
# Import config.py if present
# After gathering all dicts, modify them to merge CLI options
# Include subs so that cli_confgis can be loaded into respective named subs
#
# Import python libs
import importlib


def _ex_final(confs, final, override, key_to_ref, ops_to_ref, globe=False):
    '''
    Scan the configuration datasets, create the final config
    value, and detect collisions
    '''
    for arg in confs:
        for key in confs[arg]:
            ref = f'global.{key}' if globe else f'{arg}.{key}'
            if ref in override:
                s_key = override[ref]['key']
                s_opts = override[ref]['options']
            else:
                s_key = key
                s_opts = confs[arg][key].get('options', [])
            s_opts.append(f'--{s_key}')
            final[s_key] = confs[arg][key]
            if s_opts:
                final[s_key]['options'] = s_opts
            if s_key in key_to_ref:
                key_to_ref[s_key].append(ref)
            else:
                key_to_ref[s_key] = [ref]
            for opt in s_opts:
                if opt in ops_to_ref:
                    ops_to_ref[opt].append(ref)
                else:
                    ops_to_ref = [ref]


def _sub_final(subs, final, subs_final, sub_map):
    '''
    '''
    for imp in subs:
        desc = f'CLI Options for {imp}'
        subs_final[imp] = {'desc': desc, 'help': desc}
        for key in subs[imp]:
            f_key = f'sub.{imp}.{key}'
            final[f_key] = subs[imp][key]
            final[f_key]['sub'] = imp


def load(hub, imports, override=None):
    '''
    This function takes a list of python packages to load and look for
    respective configs. The configs are then loaded in a non-collision
    way modifying the cli options dynamically.
    The args look for the named <package>.config python module and then
    looks for dictonaries named after the following convention:

    override = {'<package>.key': 'key': 'new_key', 'options': ['--option1', '--option2']}

    CONFIG: The main configuration for this package - loads to hub.<sub>.OPTS
    GLOBAL: Global configs to be used by other packages - loads to hub.OPTS
    CLI_CONFIG: Loaded into a subcommand named after the package
    '''
    if override is None:
        override = {}
    if isinstance(imports, str):
        imports = [imports]
    confs = {}
    subs = {}
    globe = {}
    final = {}
    collides = []
    key_to_ref = {}
    ops_to_ref = {}
    subs_final = {}
    sub_map = {}
    for imp in imports:
        cmod = importlib.import_module(f'{imp}.config')
        if hasattr(cmod, 'CONFIG'):
            confs[imp] = cmod.CONFIG
        if hasattr(cmod, 'CLI_CONFIG'):
            subs[imp] = cmod.CLI_CONFIG
        if hasattr(cmod, 'GLOBAL'):
            globe[imp] = cmod.GLOBAL
    _ex_final(confs, final, override, key_to_ref, ops_to_ref)
    _ex_final(globe, final, override, key_to_ref, ops_to_ref, True)
    _sub_final(subs, final, subs_final, sub_map)
    for opt in ops_to_ref:
        g_count = 0
        if len(ops_to_ref[opt]) > 1:
            collides.append({opt: ops_to_ref[opt]})
    for key in key_to_ref:
        col = []
        for ref in key_to_ref[key]:
            if not ref.startswith('global.'):
                col.append(ref)
        if len(col) > 1:
            collides.append({key: key_to_ref[key]})
    if collides:
        raise KeyError(collides)
    opts = hub.conf.reader.read(final, subs_final)
    # seperate the opts into subs
    f_opts = {}  # I don't want this to be a defaultdict,
    # if someone tries to add a key willy nilly it should fail
    for key in opts:
        if key.startswith('sub.'):
            imp = key[key.index('.')+1:key.rindex('.')]
            if imp not in f_opts:
                f_opts[imp] = {}
            f_key = key[key.rindex('.')+1:]
            f_opts[imp][f_key] = opts[key]
            continue
        for ref in key_to_ref[key]:
            imp = ref[:ref.rindex('.')]
            if imp not in f_opts:
                f_opts[imp] = {}
            f_opts[imp][key] = opts[key]
    hub.OPT = f_opts