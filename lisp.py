'''
REPL for lisp (train project)
'''

def tokenize(st):
    lst = list()
    token = ''
    for i,el in enumerate(st):
        if el in ['(', ')']:
            if token:
                lst = lst + [token]
            lst = lst + [el]
            token = ''
        elif el == ' ':
            if token:
                lst = lst + [token]
            token = ''
        elif i == len(st) - 1:
            token += el
            lst = lst + [token]
        else:
            token += el
    return lst


def parser(tokens):
    stack = []
    buf = []
    for i, el in enumerate(tokens):
        if el == ')':
            while 1:
                buf = [stack.pop()] + buf
                if stack[-1] == '(':
                    stack = stack[:-1]
                    break
            stack = stack + [buf[:]]
            buf = []
        elif el.isnumeric():
            stack = stack + [int(el)]
        else:
            stack = stack + [el]
    return stack[0]


def my_eval(exp, globls, locls):
    if type(exp) == int or type(exp) == float:
        return exp
    elif exp == 't':
        return 't'
    elif exp == 'nil':
        return 'nil'
    elif isinstance(exp, str):
        obj = object()
        get_from_locls = locls.get(exp, obj)
        if get_from_locls is not obj:
            return get_from_locls
        else:
            return globls.get(exp)
    elif exp[0] == 'if':
        return (my_eval(exp[2], globls, locls) if my_eval(exp[1], globls, locls) == 't'  else my_eval(exp[3], globls, locls)) # <-
    elif exp[0] == '+':
        return my_eval(exp[1], globls, locls) + my_eval(exp[2], globls, locls) 
    elif exp[0] == '-':
        return my_eval(exp[1], globls, locls) - my_eval(exp[2], globls, locls)
    elif exp[0] == '*':
        return my_eval(exp[1], globls, locls) * my_eval(exp[2], globls, locls)
    elif exp[0] == '/':
        return my_eval(exp[1], globls, locls) / my_eval(exp[2], globls, locls)
    elif exp[0] == '=': # <-
        return 't' if my_eval(exp[1], globls, locls) == my_eval(exp[2], globls, locls) else 'nil'
    elif exp[0] == "quote":
        return exp[1]
    elif exp[0] == "car":        # (car '((+ 1 2) 3 4 6)) -> 
        return my_eval(exp[1], globls, locls)[0]
    elif exp[0] == "cdr":
        return my_eval(exp[1], globls, locls)[1:]
    elif exp[0] == "cons":
        return [my_eval(exp[1], globls, locls)] + my_eval(exp[2], globls, locls)
    elif exp[0] == "list":
        return [my_eval(i, globls, locls) for i in exp[1:]]
    # пример использования оператора let в lisp: (let ((x 42) (y (+ 1 2))) (list x y))
    elif exp[0] == "let":
        locls_copy = locls.copy()
        locls_copy.update(dict(zip([el[0] for el in exp[1]],
                            [my_eval(el[1], globls, locls) for el in exp[1]])))
        return my_eval(exp[-1], globls, locls_copy)
    elif exp[0] == "lambda":
        return exp
    elif exp[0][0] == "lambda":
        locls_copy = locls.copy()
        locls_copy.update(dict(zip(exp[0][1], [my_eval(el, globls, locls) for el in exp[1:]])))
        return my_eval(exp[0][2], globls, locls_copy)
    elif exp[0] == "define":
        globls[exp[1]] = my_eval(exp[2], globls, locls)
        return exp[1]


def convert(exp):
    if isinstance(exp, list):
        fin_exp = ''
        for i, el in enumerate(exp):
            fin_exp += ' '*bool(i) + convert(el)
        return '(' + fin_exp + ')'
    elif isinstance(exp, int):
        return str(exp)
    elif isinstance(exp, str):
        return exp
    else:
        return 'error:' + str(exp)


globls, locls = {}, {}

# print("(+ (* 23 2)   43) + 1", tokenize("(+ (* 23 2)   43) + 1"))
while True:
    print(convert(my_eval(parser(tokenize(input())), globls, locls)))


'''
Примеры конструкция в ЯП lisp с результатами их преобразования:
'(+ 1 2)'           -> ['+',1,2] -> 3
'(+ (* 23 2) 43)'   -> ['(','+','(','*','23','2',')','43',')']
'(12(13))'          -> ['(','12','(','13',')',')'] -> [12,[13]]

'(= 1 2)'           -> nil
'(= 1 1)'           -> t
'(if t 13 42)'      -> 13
'(if nil 13 42)'    -> 42
'''