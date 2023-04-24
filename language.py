
DEBUG = True


def debug(c: str) -> None:
    if DEBUG:
        print("DEBUG >> " + c)


OPERATOR_CORR = {"+": "+",
                 "-": "-",
                 "*": "*",
                 "/": "/",
                 "nrem": "%",
                 "=": "==",
                 "<": "<"
                 }


def get_type(t):
    # Get rust type from IR type string
    if isinstance(t, str):
        t = t.strip(" \n")
        if t == "mpq":
            debug("W >> float found, trying integer")
            return "i32"
        elif t == "bool" or t == "boolean":
            return "bool"
        else:
            print("W >> unknown type :", t, ", trying i32\n")
            return "i32"
            raise Exception("UKNW STR TYPE : " + t)
    else:
        if t[0] == "subrange":
            if t[1] == '*':
                return 'nat'
            elif int(t[1]) >= 0:
                return 'i32'  # posnat
            else:
                return 'i32'
        elif t[0] == "->":
            argtype = get_type(t[1])
            outtype = get_type(t[2])
            return "Box<dyn Fn(" + argtype + ") -> " + outtype + ">"
        elif t[0] == "recordtype":
            # TODO
            raise Exception("E >> TODO")
        elif t[0] == "array":
            arrayType = get_type(t[1])
            size, high = t[2].strip(' \n[]').split("/")
            return "Rc<[" + arrayType + "; " + size + "]>"
        elif t[1].strip(' \n') == ":":
            # custom type
            return get_type(t[2])  # we try to guess the custom type
        else:
            raise Exception("E >> UKWN TYPE : ", t)


def get_var(v):
    # From parsed var return name and type
    # e.g. from ['last', ['ivar_1', ['subrange', '0', '*', 'nil', 'nil'], 'n']]
    # to [name='ivar_1', type='i32']
    if v[0] == "last":
        return get_var(v[1])
    if isinstance(v, str):
        v = v.strip(' \n')
        if v.isdigit():
            return v, "i32"
        else:
            raise Exception("E >> get_var error on : " + v)
    return v[0], get_type(v[1])


#### LANGUAGE ####

class expr:
    # abstract class for expressions (= everything)
    # the init must parse
    def __init__(self, code, env=[]) -> None:
        raise Exception("Must implement __init__ function !")

    def toRust(self) -> str:
        raise Exception("Must implement toRust function !")


class var:
    def __init__(self, name: str, type: str, scope: expr) -> None:
        self.name: str = name
        self.names: list[str] = [name]
        self.type: str = type
        self.used: bool = False
        self.scope: expr


class env:
    def __init__(self, from_env=None):
        self.variables: list[var] = [
        ] if from_env == None else from_env.variables

    def get_var(self, s: str):
        for var in self.variables:
            if s in var.names:
                return var
        return None

    def set_used(self, s: str):
        self.get_var(s).used = True


def get_expr(tabl: list[list | str] | str, env: env) -> expr:
    # From ['object', ...] to corresponding expr
    if isinstance(tabl, str):
        return Evalue(tabl, env)
    try:
        key = tabl[0]
        if not isinstance(key, str):  # handles cases such as [[ thing ]]
            if len(tabl) < 2:
                return get_expr(key, env)
            else:
                # lambda calls : [[expr fn] [expr arg]]
                return Elambdacall(tabl, env)
        else:
            key = key.strip(' \n')  # hence str
    except:
        raise Exception("E >> error getting expr from : " + str(tabl))

    if key == "lambda":
        return Efn(tabl, env)
    elif key == "let":
        return Elet(tabl, env)
    elif key == "if":
        return Eif(tabl, env)
    elif key == "release":
        return Erelease(tabl, env)
    elif key == "lett":
        return Elett(tabl, env)
    elif key == "lookup":
        return Elookup(tabl, env)
    elif key == "update":
        return Eupdate(tabl, env)
    elif key in OPERATOR_CORR.keys():
        return Eoperator(tabl, env)
    elif key[:4] == "ivar" or key == "last":
        return Evariable(tabl, env)
    else:
        return Eappication(tabl, env)


class Evariable(expr):
    # Representation of a variable with possibly a last before
    # Here is a representation for variables as expr ! Hence they
    # must already be in the env. For declaration see Elet and Efn
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        if not Evariable.isVariable(self.code):
            raise Exception("E >> can't parse variable : " + self.code)

        self.isLast = code[0].strip(' \n') == 'last'
        if self.isLast:
            self.code = self.code[1]

        self.name = self.code[0].strip(' \n')

        self.fromEnv = self.env.get_var(self.name)

        if self.fromEnv == None:
            raise Exception("E >> can't find variable " +
                            self.name + " in env " + str(self.env.variables))

        self.name = self.fromEnv.name
        self.type = self.fromEnv.type
        self.used = self.fromEnv.used

        debug("Evariable : Fetched var " + self.name + " of type " +
              self.type + " from env, used : " + str(self.used))

    def isVariable(arr) -> bool:
        try:
            if arr[0].strip(" \n") == "last":
                return Evariable.isVariable(arr[1])
            return True
        except:
            return False

    def toRust(self) -> str:
        if self.used and not self.isLast:  # TODO : regarder si ce clone est vraiment necessaire
            return self.name + ".clone()"
        return self.name


class Evalue(expr):
    # Representation of a value sur as "123"
    def __init__(self, code: str, env: env) -> None:
        self.code = code.strip(' \n')
        self.env = env

        if not Evalue.isValue(self.code):
            raise Exception("E >> can't parse value : " + self.code)

        debug("Evalue : returning value " + code)

    def isValue(arr) -> bool:
        return arr.isdigit()

    def toRust(self) -> str:
        return self.code


class Elambdacall(expr):
    # Representation of a lambda call: the first element is a var
    # containing a fn, the following are the arguments
    # TODO :
    #   Do some more checks
    #   Handles > 1 args
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        self.fn = get_expr(self.code[0], self.env)

        self.body = get_expr(self.code[1], self.env)
        self.env = self.body.env

        debug("Elambdacall : calling lamda fn with arg: " + str(code[1]))

    def toRust(self) -> str:
        return self.fn.toRust() + "(" + self.body.toRust()+")"


class Elet(expr):
    # Representation of a let. It changes the env with the new variable
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        self.varName: str = self.code[1].strip(' \n')
        self.varType: str = get_type(self.code[2])

        # TODO : modifier le bypass en un simple rename
        if isinstance(self.code[3], str) and self.code[3].strip(' \n') == 'nil':
            self.middle = None
            debug(
                "WARN : cannot create null from nil [let " + self.varName+"]")
            self.env.variables.append(var(self.varName, self.varType, self))
            self.right = get_expr(self.code[4], self.env)
            if isinstance(self.right, Eupdate):
                debug(
                    "WARN : making exception : found update in that let. It will not be done")
                self.env.get_var(
                    self.right.array.name).names.append(self.varName)

            else:
                raise Exception("E >> found let "+self.varName+" = null")
        else:
            self.middle = get_expr(self.code[3], self.env)
            self.env = self.middle.env
            self.env.variables.append(var(self.varName, self.varType, self))
            self.right = get_expr(self.code[4], self.env)

        debug("Elet : created let for variable " + self.varName)

    def toRust(self) -> str:
        if self.middle == None:
            # so we have an update to bypass:
            output = self.right.array.name
        else:
            v = self.env.get_var(self.varName)
            output = "let "
            output += v.name + " : " + v.type
            output += " = {" + self.middle.toRust()
            output += '};\n'
            output += self.right.toRust()
        return output


class Elett(expr):
    # Representation of a lett. It adds a new name for the variable in the env
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        self.varName = self.code[1].strip(' \n')
        self.varType = get_type(self.code[2])

        self.targetVar, t = get_var(self.code[4])

        for var in self.env.variables:
            if self.targetVar in var.names:
                var.names.append(self.varName)
                break

        self.body: expr = get_expr(self.code[5], self.env)
        self.env = self.body.env

        debug("Elett : added name " + self.varName + " to var " + self.targetVar)

    def toRust(self) -> str:
        return self.body.toRust()


class Eif(expr):
    # Representation of a if then else
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        self.cond: expr = get_expr(self.code[1], self.env)
        self.env = self.cond.env
        self.true: expr = get_expr(self.code[2], self.env)
        self.env = self.true.env  # conservative
        self.false: expr = get_expr(self.code[3], self.env)
        self.env = self.false.env

        debug("Eif : if stmt")

    def toRust(self) -> str:
        output = "if " + self.cond.toRust()
        output += "{" + self.true.toRust()
        output += "} else {" + self.false.toRust() + "}"
        return output


class Erelease(expr):
    # Representation of release
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env
        debug("Erelease : ignoring")

    def toRust(self) -> str:
        return get_expr(self.code[3], self.env).toRust()


class Elookup(expr):
    # Lookup of an array
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        self.arrayName, self.arrayType = get_var(self.code[1])

        self.var: var = env.get_var(self.arrayName)

        self.index: expr = get_expr(self.code[2], self.env)
        self.env = self.index.env

        debug("Elookup")

    def toRust(self) -> str:
        # the clone is only of ref so not a big deal
        return self.arrayName + "[" + self.index.toRust() + " as usize].clone()"


class Eupdate(expr):
    # Update of an array
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        self.array: expr = get_expr(self.code[1], self.env)

        self.index: expr = get_expr(code[2], self.env)
        self.env = self.index.env
        self.value: expr = get_expr(code[3], self.env)
        self.env = self.value.env

        debug("Eupdate : array " + self.array.name)

    def toRust(self) -> str:
        output = "(*Rc::make_mut(&mut " + self.array.toRust() + "))["+ self.index.toRust() +" as usize] = "
        output += self.value.toRust() +"; " + self.array.toRust() 
        return output


class Eoperator(expr):
    # Representation of an operator, which is some functions (see OPERATOR_CORR)
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        if not self.code[0].strip(' \n') in OPERATOR_CORR.keys():
            raise Exception("E >> can't parse operation : " + self.code)
        self.op = OPERATOR_CORR[code[0]]

        self.leftOp = get_expr(self.code[1], self.env)
        self.env = self.leftOp.env
        self.rightOp = get_expr(self.code[2], self.env)
        self.env = self.rightOp.env

        debug("Eoperator : operator " + self.op)

    def toRust(self) -> str:
        return self.leftOp.toRust() + self.op + self.rightOp.toRust()


class Eappication(expr):
    # Representation of an expression, fn name must be is FN_NAMES
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        try:
            self.name = code[0].strip(' \n')
        except:
            raise Exception("E >> error while parsing function: " + code)

        self.args: list[expr] = []
        for argCode in self.code[1:]:
            if not isinstance(argCode, str) or argCode.strip(' \n') != 'nil':
                self.args.append(get_expr(argCode, self.env))
                self.env = self.args[-1].env

        debug("Eapplication : application " + self.name)

    def toRust(self) -> str:
        output = self.name + "("
        for arg in self.args:
            output += arg.toRust() + ','
        output = output.strip(',') + ")"
        return output


class Efn(expr):
    # Representation of a function, it updates the env and returns a
    # boxed (std::Box) closure, except on first level
    def __init__(self, code: str, env: env, name="") -> None:
        self.code = code
        self.name = name
        self.type = ""
        self.firstLevel = name != ""

        self.args = []  # [[name, type]]
        self.outtype = ""
        self.body = None
        self.env = env

        self.parse()
        # mark all variables used (later we need to clone them )
        for vari in self.env.variables:
            vari.used = True

        for arg in self.args:
            self.env.variables.append(var(arg[0], arg[1], self))

        self.body: expr = get_expr(self.body, self.env)
        self.env = self.body.env

        debug("Efn : function " + str(self.args) + " -> " + str(self.outtype))

    def isFn(arr) -> bool:
        try:
            assert (arr[0].strip(' \n') == 'lambda')
            assert (not isinstance(arr[1], str))
            assert (arr[2].strip(' \n') == "'->")
            return True
        except:
            return False

    def parse(self):
        try:
            assert (Efn.isFn(self.code))
            for var in self.code[1]:
                v, t = get_var(var)
                self.args.append([v.strip(' \n'), t.strip(' \n')])
            self.outtype = get_type(self.code[3])
            self.body = self.code[4]

            self.type = "Box<impl Fn("
            for arg in self.args:
                self.type += arg[1] + ','
            self.type = self.type.strip(',') + ") -> " + self.outtype + '>'
        except:
            raise Exception("E >> can't parse fn : " + str(self.code))

    def toRust(self):
        if self.firstLevel:  # we are at the base level
            output = "fn " + self.name + "("
            for arg in self.args:
                output += arg[0] + ": " + arg[1] + ","
            output = output.strip(',') + ") -> " + self.outtype + '{'
            output += self.body.toRust() + '}'
        else:
            output = "Box::new(move |"
            for arg in self.args:
                output += arg[0] + ": " + arg[1] + ","
            output = output.strip(',') + "| -> " + self.outtype + '{'
            output += self.body.toRust() + '})'
        return output
