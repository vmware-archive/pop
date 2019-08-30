# Import python libs
import inspect
# Import pop libs
import pop.exc


def contract(hub, raws, mod):  # pylint: disable=unused-argument
    '''
    Verify module level contract - functions only
    '''
    sig_errs = []
    sig_miss = []
    for raw in raws:
        for fun in raw._funcs:
            if fun.startswith('sig_'):
                tfun = fun[4:]
                if tfun not in mod._funcs:
                    sig_miss.append(tfun)
                    continue
                sig_errs.extend(sig(mod._funcs[tfun].func, raw._funcs[fun].func))
    if sig_errs or sig_miss:
        msg = ''
        if sig_errs:
            msg += 'Signature Errors:\n'
            for err in sig_errs:
                msg += f'{err}\n'
        if sig_miss:
            msg += 'Signature Functions Missing:\n'
            for err in sig_miss:
                msg += f'{err}\n'
        msg = msg.strip()
        raise pop.exc.ContractSigException(msg)



def sig(func, ver):
    '''
    Takes 2 functions, the first function is verified to have a parameter signature
    compatible with the second function
    '''
    errors = []
    vsig = inspect.signature(ver)
    fsig = inspect.signature(func)
    vparams = list(vsig.parameters.values())
    fparams = list(fsig.parameters.values())
    vdat = {'args': [], 'v_pos': -1, 'kw': [], 'kwargs': False}
    for ind in range(len(vparams)):
        param = vparams[ind]
        val = param.kind.value
        name = param.name
        if val == 0 or val == 1:
            vdat['args'].append(name)
            if param.default != inspect._empty: # Is a KW, can be inside of **kwargs
                vdat['kw'].append(name)
        elif val == 2:
            vdat['v_pos'] = ind
        elif val == 3:
            vdat['kw'].append(name)
        elif val == 4:
            vdat['kwargs'] = ind
    arg_len = len(vdat['args'])
    v_pos = False
    for ind in range(len(fparams)):
        param = fparams[ind]
        val = param.kind.value
        name = param.name
        has_default = param.default != inspect._empty
        if val == 2:
            v_pos = True
        if val == 0 or val == 1:
            if ind >= arg_len:  # Past available positional args
                if not vdat['v_pos'] == -1:  # Has a *args
                    if ind >= vdat['v_pos'] and v_pos:
                        # Invalid unless it is a kw
                        if not name in vdat['kw']:
                            # Is a kw
                            errors.append(f'Parameter "{name}" is invalid')
                        if vdat['kwargs'] is False:
                            errors.append(f'Parameter "{name}" not defined as kw only')
                        continue
                elif vdat['kwargs'] is not False and not has_default:
                    errors.append(f'Parameter "{name}" is past available positional params')
            else:
                v_param = vdat['args'][ind]
                if v_param != name:
                    errors.append(f'Parameter "{name}" does not have the correct name: {v_param}')
        if val == 2:
            if ind < vdat['v_pos']:
                errors.append(f'Parameter "{name}" is not in the correct position for *args')
        if val == 3:
            if name not in vdat['kw'] and not vdat['kwargs']:
                errors.append(f'Parameter "{name}" is not available as a kwarg')
        if val == 4:
            if vdat['kwargs'] is False:
                errors.append(f'Kwargs are not permitted as a parameter')
    return errors
