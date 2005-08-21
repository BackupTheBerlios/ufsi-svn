"""
Uses docutils to produce formatted html documentation for a module.
"""

#import types
import inspect
import docutils.core


def docFunctionName(f):
    (args,varargs,varkw,defaults)=inspect.getargspec(f)
    return '%s%s'%(f.__name__,
                   inspect.formatargspec(args,varargs,varkw,defaults))

def docFunction(f):
    s='%s:\n%s\n'%(docFunctionName(f),str(f.__doc__))

    return s


def docClass(c):
    return '%s: %s\n'%(c.__name__,c.__doc__)


def docModule(module):
    classes=[]
    functions=[]

    if not inspect.ismodule(module):
        raise TypeError('docModule requires a Module object.'\
                        'Received: %r'%module)
    
    for k in module.__dict__.keys():
        i=module.__dict__[k]
        if inspect.isclass(i):
            classes.append(i)
        if inspect.isfunction(i):
            functions.append(i)

    s=''
    
    if classes:
        s+='Classes: \n'
        s+=''.join(map(docClass,classes))

    if functions:
        s+='Functions: \n'
        s+=''.join(map(docFunction,functions))

    return s


if __name__=='__main__':
    import ufsi

    print docModule(ufsi)
