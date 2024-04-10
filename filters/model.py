from autonomous import log


def defined(obj, attr):
    return any(attr in key for key in obj.attributes.keys())
