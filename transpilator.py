# PVS 2 Rust PoC
# Translates the code from IR.lisp to out.rs
# Nathan Gasc - SRI International 

# dependencies : Python3, prettier with rust plugin
 
import os
from IRparser import *

FN_NAME = "is_prime__fibo"
FN_LIST = {"is_prime__fibo":1,
           "nrem":2,
           }

def get_type(t):
    # Get rust type from IR type string
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
            raise Exception("UKNW TYPE : " + t)
        if t[1] == '*':
            return 'nat'
        elif int(t[1]) >= 0:
            return 'Integer' #posnat
        else:
            return 'Integer'

def get_var(v):
    # From parsed var return name and type
    # e.g. from ['last', ['ivar_1', ['subrange', '0', '*', 'nil', 'nil'], 'n']]
    # to [name='ivar_1', type='Integer']
    if v[0] == "last":
        return get_var(v[1])
    return v[0], get_type(v[1])


def interp(parsed_IR) -> str:
    # Recursive function to translate a subset of IR to rust
    # It takes advantage of the functionnal aspects of rust
    command = parsed_IR[0]

    # to bypass things like [[command]]
    if not isinstance(command, str):
        return interp(parsed_IR[0])
    output = ""

    # literal translation
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

        case _: #else
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

    #uses parser to go from lisp with parenthesis, to the same but in an array structure
    parsed = get_els_from_str(src) 

    #actual translation
    header = "use rug::Integer;\n"
    rust = header + interp(parsed)

    fichier = open("out.rs", "w")
    fichier.write(rust)
    fichier.close()

    os.system("prettier --write out.rs") # requires prettier

