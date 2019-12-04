'''
Integrate is used to pull config data from multiple sources and merge it into
the hub. Once it is merged then when a sub is loaded the respective config data
is loaded into the sub as `OPTS`
'''
# Take an *args list of modules to import and look for conf.py
# Import conf.py if present
# After gathering all dicts, modify them to merge CLI options
#
# Import python libs
import importlib
import copy


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


def load(
        hub,
        imports,
        override=None,
        cli=None,
        roots=False,
        loader='json',
        logs=True):
    '''
    This function takes a list of python packages to load and look for
    respective configs. The configs are then loaded in a non-collision
    way modifying the cli options dynamically.
    The args look for the named <package>.conf python module and then
    looks for dictionaries named after the following convention:

    override = {'<package>.key': 'key': 'new_key', 'options': ['--option1', '--option2']}

    CONFIG: The main configuration for this package - loads to hub.OPT['<import>']
    GLOBAL: Global configs to be used by other packages - loads to hub.OPT['global]
    CLI_CONFIG: Loaded only if this is the only import or if specified in the cli option
    SUBS: Used to define the subcommands, only loaded if this is the cli config
    '''
    if override is None:
        override = {}
    if isinstance(imports, str):
        if cli is None:
            cli = imports
        imports = [imports]
    primary = imports[0] if cli is not None else cli
    confs = {}
    globe = {}
    final = {}
    collides = []
    key_to_ref = {}
    ops_to_ref = {}
    subs = {}
    for imp in imports:
        cmod = importlib.import_module(f'{imp}.conf')
        if hasattr(cmod, 'CONFIG'):
            confs[imp] = copy.deepcopy(cmod.CONFIG)
        if cli == imp:
            if hasattr(cmod, 'CLI_CONFIG'):
                confs[imp].update(copy.deepcopy(cmod.CLI_CONFIG))
            if hasattr(cmod, 'SUBS'):
                subs = copy.deepcopy(cmod.SUBS)
        if hasattr(cmod, 'GLOBAL'):
            globe[imp] = copy.deepcopy(cmod.GLOBAL)
    if logs:
        lconf = hub.conf.log.init.conf(primary)
        lconf.update(confs[primary])
        confs[primary] = lconf
    _ex_final(confs, final, override, key_to_ref, ops_to_ref)
    _ex_final(globe, final, override, key_to_ref, ops_to_ref, True)
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
    opts = hub.conf.reader.read(final, subs, loader=loader)
    f_opts = {}  # I don't want this to be a defaultdict,
    # if someone tries to add a key willy nilly it should fail
    for key in opts:
        if key == '_subparser_':
            f_opts['_subparser_'] = opts['_subparser_']
            continue
        for ref in key_to_ref[key]:
            imp = ref[:ref.rindex('.')]
            if imp not in f_opts:
                f_opts[imp] = {}
            f_opts[imp][key] = opts[key]
    if roots:
        root_dir = f_opts.get(cli, {}).get('root_dir')
        hub.conf.dirs.roots(final.get('root_dir', {}).get('default', '/'), f_opts, root_dir)
        for imp in f_opts:
            hub.conf.dirs.verify(f_opts[imp])
    hub.OPT = f_opts
    if logs:
        log_plugin = hub.OPT[primary].get('log_plugin')
        getattr(hub, f'conf.log.{log_plugin}.setup')(hub.OPT[primary])
