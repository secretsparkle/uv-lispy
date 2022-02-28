
def first(lst):
    if len(lst) == 0:
        return None
    else:
        return lst[0]

def rest(lst):
    if len(lst) <  2:
        return None
    else:
        return lst[1:]
