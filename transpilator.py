import os

FN_NAME = "is_prime__fibo"
FN_LIST = {"is_prime__fibo":1,
           "nrem":2,
           }


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
        return "INVALID PARENTHESIS", ""

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

# last let subrange rename - <

# on peut partir sur une structure de la forme fonction
# recursive interp qui garde la structure du code lisp

def get_type(t):
    if isinstance(t, str):
        t = t.strip(" \n")
        if t == "mpq":
            raise Exception("Reals unsupported yet")
            return "real"
        elif t == "bool" or t == "boolean":
            return "bool"
        else:
            raise Exception("UKNW STR TYPE : " + t)
    else:
        try:
            assert(t[0] == "subrange")
        except:
            print("INVALID TYPE")
            exit(1)
        if t[1] == '*':
            return 'nat'
        elif int(t[1]) >= 0:
            return 'Integer' #posnat
        else:
            return 'Interger'

def get_var(v):
    # from ['last', ['ivar_1', ['subrange', '0', '*', 'nil', 'nil'], 'n']]
    # to [name='ivar_1', type='Integer']
    if v[0] == "last":
        return get_var(v[1])
    return v[0], get_type(v[1])

def interp(parsed_IR) -> str:
    command = parsed_IR[0]
    if not isinstance(command, str):
        return interp(parsed_IR[0])
    output = ""
    match command:
        case "lambda":
            output += "fn " + FN_NAME + "("
            for var in parsed_IR[1]:
                output += var[0] + " : " + get_type(var[1]) + ","
            output += ") -> " + get_type(parsed_IR[3]) + " {\n"
            output += interp(parsed_IR[4])
            output += "\n}"
            return output
        
        case "let":
            name = parsed_IR[1].strip(" \n")
            t = get_type(parsed_IR[2])

            if isinstance(parsed_IR[3], str) and parsed_IR[3].strip(" \n").isdigit():
                output += "let " + name + " : " + t + " = " + parsed_IR[3].strip(" \n") + ";\n"
            else :
                output += "let " + name + " : " + t + " = {\n"
                output += interp(parsed_IR[3])
                output += "\n};\n"

            output += interp(parsed_IR[4])
            return output
        
        case "<":
            n1, t1 = get_var(parsed_IR[1])
            n2, t2 = get_var(parsed_IR[2])
            # quand on ajoutera les types, il faudra les verifier ici
            output += n1 + " < " + n2
            return output
        
        case "if":
            v, t = get_var(parsed_IR[1])
            output += "if " + v + " {\n"
            output += interp(parsed_IR[2])
            output += "\n}else {\n"
            output += interp(parsed_IR[3])
            output += "\n}\n"
            return output
        
        case "-":
            n1, t1 = get_var(parsed_IR[1])
            n2, t2 = get_var(parsed_IR[2])
            # quand on ajoutera les types, il faudra les verifier ici
            output += n1 + " - " + n2
            return output
        
        case "+":
            n1, t1 = get_var(parsed_IR[1])
            n2, t2 = get_var(parsed_IR[2])
            # quand on ajoutera les types, il faudra les verifier ici
            output += n1 + " + " + n2
            return output

        case "last":
            v, t = get_var(parsed_IR)
            output += v
            return output

        case _:
            if command in FN_LIST.keys():
                output += command + "("
                for i in range(FN_LIST[command]):
                    v,t = get_var(parsed_IR[i+1])
                    output += v + ", "
                output += ")\n"
                return output
            else:
                output += '/*' + parsed_IR.__str__().replace('\n','') + '*/'
                return output


if __name__ == "__main__":
    fichier = open("IR.lisp", 'r')
    src = fichier.read()
    fichier.close()
    parsed = get_els_from_str(src)
    rust = interp(parsed)
    fichier = open("out.rs", "w")
    fichier.write(rust)
    fichier.close()
    os.system("prettier --write out.rs")

