
DEBUG = True

def debug(c:str) -> None:
    if DEBUG:
        print("DEBUG >> " + c + "\n")

FN_LIST = ["nrem"]
OPERATOR_CORR = {"+" : "+",
                 "-" : "-",
                 "*" : "*",
                 "/" : "/",
                 "nrem" : "%",
                 "=" : "==",
                 "<" : "<"
                 }

def get_type(t):
    # Get rust type from IR type string
    if isinstance(t, str):
        t = t.strip(" \n")
        if t == "mpq":
            raise Exception("E >> Reals unsupported yet")
            return "real"
        elif t == "bool" or t == "boolean":
            return "bool"
        else:
            print("W >> unknown type :", t, ", trying Integer\n")
            return "Integer"
            raise Exception("UKNW STR TYPE : " + t)
    else:
        try:
            assert(t[0] == "subrange" or t[0] == "->" or "recordtype")
        except:
            raise Exception("E >> UKNW TYPE : ", t)
        if t[0] == "subrange":
            if t[1] == '*':
                return 'nat'
            elif int(t[1]) >= 0:
                return 'Integer' #posnat
            else:
                return 'Integer'
        elif t[0] == "->":
            argtype = get_type(t[1])
            outtype = get_type(t[2])
            return "Box<dyn Fn(" + argtype + ") -> " + outtype + ">"
        elif t[0] == "recordtype":
            #TODO
            pass


def get_var(v):
    # From parsed var return name and type
    # e.g. from ['last', ['ivar_1', ['subrange', '0', '*', 'nil', 'nil'], 'n']]
    # to [name='ivar_1', type='Integer']
    if v[0] == "last":
        return get_var(v[1])
    if isinstance(v, str):
        v = v.strip(' \n')
        if v.isdigit():
            return v, "Integer"
        else:
            raise Exception("E >> get_var error on : " + v)
    return v[0], get_type(v[1])


#### LANGUAGE ####

# env est un tableau de la forme:
# [ [names, name, type, used ] ]
# eg [ [ ["ivar_1", "ivar_5"], "ivar_1", "Integer", True ] ]

class expr: 
    # abstract class for expressions (= everything)
    # the init must parse
    def __init__(self, code, env = []) -> None:
        raise Exception("Must implement __init__ function !")
    
    def toRust(self) -> str:
        raise Exception("Must implement toRust function !")
    
def get_expr(tabl, env) -> expr:
    # From ['object', ...] to corresponding expr
    if isinstance(tabl, str):
        return Evalue(tabl, env)
    try:
        key = tabl[0]
        if not isinstance(key, str): # handles cases such as [[ thing ]]
            return get_expr(key, env)
        else:
            key = key.strip(' \n')
    except:
        raise Exception("E >> error getting expr from : " + str(tabl))

    if key == "lambda": return Efn(tabl, env)
    elif key == "let": return Elet(tabl, env)
    elif key == "if": return Eif(tabl, env)
    elif key in OPERATOR_CORR.keys(): return Eoperator(tabl, env)
    elif key[:4] == "ivar" or key == "last": return Evariable(tabl, env)
    else:
        raise Exception("E >> falling through parser with : " + str(tabl))


class Evariable(expr):
    # Representation of a variable with possibly a last before
    # Here is a representation for variables as expr ! Hence they
    # must already be in the env. For declaration see Elet and Efn
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env

        if not Evariable.isVariable(self.code):
            raise Exception("E >> can't parse variable : " + self.code)

        self.isLast = code[0].strip(' \n') == 'last'
        if self.isLast:
            self.code = self.code[1]

        self.name = self.code[0].strip(' \n')

        self.fromEnv = None
        for envVar in env:
            if self.name in envVar[0]:
                self.fromEnv = envVar 
                break
        
        if self.fromEnv == None:
            raise Exception("E >> can't find variable " + self.name + " in env " + str(self.env))
        
        self.name = self.fromEnv[1]
        self.type = self.fromEnv[2]
        self.used = self.fromEnv[3]

        debug("Evariable : Fetched var "+ self.name + " of type " + self.type + " from env.")

    def isVariable(arr) -> bool:
        try:
            if arr[0].strip(" \n") == "last":
                return Evariable.isVariable(arr[1])
            return True
        except:
            return False
    
    def toRust(self) -> str:
        if self.used:
            return self.name + ".clone()"
        return self.name

class Evalue(expr):
    # Representation of a value sur as "123"
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env

        if not Evalue.isValue(self.code):
            raise Exception("E >> can't parse value : " + self.code)
        
        debug("Evalue : retourning value " + code)

    def isValue(arr) -> bool:
        return arr.isdigit()
    
    def toRust(self) -> str:
        return self.code

class Elet(expr):
    # Representation of a let. It changes the env with the new variable
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env

        self.varName = self.code[1].strip(' \n')
        self.varType = get_type(self.code[2])
        self.env.append([[self.varName], self.varName, self.varType, False])

        debug("Elet : created let for variable " + self.varName)
    
    def toRust(self) -> str:
        output = "let " + self.varName + " : " + self.varType + " = {"
        output += get_expr(self.code[3], self.env).toRust()
        output += '};\n'
        output += get_expr(self.code[4], self.env).toRust()
        return output

class Eif(expr):
    # Representation of a if then else
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env
        debug("Eif : if stmt")
    
    def toRust(self) -> str:
        output = "if " + get_expr(self.code[1], self.env).toRust()
        output += "{" + get_expr(self.code[2], self.env).toRust() 
        output += "} else {" + get_expr(self.code[3], self.env).toRust() + "}"
        return output

class Eoperator(expr):
    # Representation of an operator, which is some functions (see OPERATOR_CORR)
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env

        if not Eoperator.isOperator(self.code):
            raise Exception("E >> can't parse operation : " + self.code)
        self.op = code[0]

        debug("Eoperator : operator " + self.op)

    def isOperator(arr) -> bool:
        try:
            assert(arr[0] in OPERATOR_CORR.keys())
            return True
        except:
            return False
    
    def toRust(self) -> str:
        return get_expr(self.code[1], self.env).toRust() + self.op + get_expr(self.code[2], self.env).toRust()

class Efn(expr):
    # Representation of a function, it updates the env and returns a 
    # boxed (std::Box) closure
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.type = ""

        self.args = [] # [[name, type]]
        self.outtype = ""
        self.body = None
        self.env = env 

        self.parse()
        for var in self.env: # mark all variables used (later we need to clone them )
            var[3] = True

        for arg in self.args:
            self.env.append([[arg[0]], arg[0], arg[1], False])
        
        debug("Efn : function " + str(self.args) + " -> " + str(self.outtype))

    def isFn(arr) -> bool:
        try:
            assert(arr[0].strip(' \n') == 'lambda')
            assert(not isinstance(arr[1], str))
            assert(arr[2].strip(' \n') == "'->")
            return True
        except:
            return False

    def parse(self):
        try:
            assert(Efn.isFn(self.code))
            for var in self.code[1]:
                v, t = get_var(var)
                self.args.append([v, t])
            self.outtype = get_type(self.code[3])
            self.body = self.code[4]

            self.type = "Box<impl Fn(" 
            for arg in self.args:
                self.type += arg[1] + ','
            self.type = self.type.strip(',') + ") -> " + self.outtype + '>'

        except:
            raise Exception("E >> can't parse fn : " + str(self.code))
        
    def toRust(self):
        output = "Box::new(move |"
        for arg in self.args:
            output += arg[0] + ": " + arg[1] + ","
        output = output.strip(',') + "| -> " + self.outtype + '{'
        output += get_expr(self.body, self.env).toRust() + '})'
        return output
