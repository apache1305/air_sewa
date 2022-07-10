def querydict_to_dict(qdict):
    """ Return dict for the given QueryDict """

    return {k: v[0] if len(v) == 1 else v for k, v in qdict.lists()}