

def file_read_lines(Fname):
    with open(Fname, 'r') as F:
        return F.readlines()

def is_dict(Obj):
    return isinstance(Obj, dict)

def is_float(Obj):
    return isinstance(Obj, float)

def is_fun(Obj):
    return callable(Obj)

def is_int(Obj):
    return isinstance(Obj, int)

def is_list(Obj):
    return isinstance(Obj, list)

def is_class_user_defined(Obj):
    return callable(Obj)

def is_none(Obj):
    return Obj == None

def is_bool(Obj):
    return isinstance(Obj, bool)

def is_str(Obj):
    return isinstance(Obj, str)

def is_tuple(Obj):
    return isinstance(Obj, tuple)

def is_simple(Obj):
    return is_int(Obj) or is_float(Obj) or is_str(Obj) or is_none(Obj) or is_bool(Obj)
