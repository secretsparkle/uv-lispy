
def first(lst):
    if type(lst) is list and len(lst) > 0:
        return lst[0]
    else:
        return None

def rest(lst):
    if type(lst) is list and len(lst) < 2:
        return lst[1:]
    else:
        return None

def cons(elt, lst):
    if type(lst) is list:
        return lst.insert(0, elt)
    else:
        return None
