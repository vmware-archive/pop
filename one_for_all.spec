# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

def Entrypoint(dist, group, name, **kwargs):
    import pkg_resources

    # get toplevel packages of distribution from metadata
    def get_toplevel(dist):
        try:
            distribution = pkg_resources.get_distribution(dist)
        except:
            return []
        if distribution.has_metadata('requirements.txt'):
            return list(distribution.get_metadata('requirements.txt').split())
        else:
            return []

    kwargs.setdefault('hiddenimports', ['pop', 'pop.mods', 'pop.mods.pop'])
    packages = []
    for distribution in kwargs['hiddenimports']:
        packages += get_toplevel(distribution)

    kwargs.setdefault('pathex', [])
    # get the entry point
    ep = pkg_resources.get_entry_info(dist, group, name)
    assert ep, 'Could not find the entry point'
    # insert path of the egg at the verify front of the search path
    kwargs['pathex'] = [ep.dist.location] + kwargs['pathex']
    # script name must not be a valid module name to avoid name clashes on import
    script_path = os.path.join(workpath, name + '-script.py')
    print("creating script for entry point", dist, group, name)
    with open(script_path, 'w') as fh:
        print("import", ep.module_name, file=fh)
        print("%s.%s()" % (ep.module_name, '.'.join(ep.attrs)), file=fh)
        for package in packages:
            print("import", package, file=fh)

    return Analysis(
        [script_path] + kwargs.get('scripts', []),
        **kwargs
    )

a = Entrypoint('heis', 'console_scripts', 'heis')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='heis',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=True,
               upx=True,
               upx_exclude=[],
               name='heis')
