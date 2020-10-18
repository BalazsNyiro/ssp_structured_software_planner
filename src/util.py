def file_write_simple(Fname, Content, Mode="w"):
    if "b" not in Mode: # fixed unix style end of line
        with open(Fname, Mode, newline="\n") as f:
            f.write(Content)
    else:
        with open(Fname, Mode) as f:
            f.write(Content)


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

def diff_dicts(Old, New):
    Diff = {}
    for Key, Val in New.items():
        if Key not in Old:
            Diff[Key] = New[Key]
        else:
            if Old[Key] != New[Key]:
                Diff[Key] = diff_objects(Old[Key], New[Key])

def diff_lists(Old, New):
    Diff = []
    for Id, Elem in enumerate(New):
        Difference = diff_objects(Old[Id], New[Id])
        Diff.append(Difference)
    return Diff

# return with difference.
def diff_objects(Old, New, FirstCall=True):
    if type(Old) == type(New):
        if is_simple(Old) and is_simple(New):
            if Old == New:
                return ""
            else:
                return New

        else:  # not simple types
            if is_dict(Old):
                return diff_dicts(Old, New)

            if is_list(Old):
               return diff_lists(Old, New)

    else: # different types, New is total different
        return New

    return f"can't create diff of objects: {str(A)} {str(B)}"
