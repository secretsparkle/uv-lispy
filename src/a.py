
def first(lst):
    if type(lst) is list and len(lst) > 0:
        return lst[0]
    else:
        return None

def second(lst):
    if type(lst) is list and len(lst) > 1:
        return lst[1]
    else:
        return None

def third(lst):
    if type(lst) is list and len(lst) > 2:
        return lst[2]
    else:
        return None

def nth(index, lst):
    if type(lst) is list and len(lst) > index:
        return lst[index]
    else:
        return None

def rest(lst):
    if type(lst) is list and len(lst) >= 2:
        return lst[1:]
    else:
        return None

def cons(elt, lst):
    if type(lst) is list:
        return lst.insert(0, elt)
    else:
        return None

def append(elt, lst):
    if type(lst) is list:
        return lst.insert(-1, elt)

def equal(x, y):
    if x == y:
        return True
    else:
        return False

def length(lst):
    if type(lst) is list:
        return len(lst)



if 2 > 1:
    print("True")
print("False"))

    