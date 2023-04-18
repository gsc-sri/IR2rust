
def str_till_cp(chaine):
    chaine = chaine.strip(" \n")
    if chaine[0] != '(':
        i = 0
        for char in chaine:
            if char == ' ':
                break
            i += 1
        #print("single", chaine[:i], chaine[i:] )
        return chaine[:i], chaine[i:]
    else :
        count = 0
        i = 0
        for char in chaine:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
            i += 1
            if count == 0:
                #print("good ", 'A', chaine[:i],'A', chaine[i:], 'A' )
                return chaine[:i], chaine[i:]
        #print("error on " + chaine)
        raise Exception("E >> INVALID PARENTHESIS")

def get_els_from_str(chaine):
    #print("getting els from", chaine)

    arr = []
    while len(chaine) > 1:
        el , chaine = str_till_cp(chaine)
        arr.append(el)

    tabl = []
    for els in arr:
        if els.strip()[0] != "(":
            tabl.append(els)
        else:
            tabl.append(get_els_from_str(els.strip(" \n")[1:-1]))
    return tabl
