#!/usr/bin/env python
# coding=utf-8
#
#  Copyright © 2013 Hewlett-Packard Development Company, L.P.
#
#  This work is distributed under the W3C® Software License [1]
#  in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  [1] http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231
#

import sys

from widlparser import parser



def debugHook(type, value, tb):
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
        # we are in interactive mode or we don't have a tty-like
        # device, so we call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback, pdb
        # we are NOT in interactive mode, print the exception...
        traceback.print_exception(type, value, tb)
        print
        # ...then start the debugger in post-mortem mode.
        pdb.pm()



if __name__ == "__main__":      # called from the command line
    sys.excepthook = debugHook
    parser = parser.Parser()
    idl = """
Window implements WindowInterface;

enum foo { "one" };
enum bar { "one", "two", "three" };

typedef short shorttype;
typedef long longtype;
typedef long long longtype;
typedef [hello, my name is inigo montoya (you ] killed my father)] unsigned long long inigo;
typedef unrestricted double dubloons;
typedef short[] shortarray;
typedef DOMString string;
typedef DOMString[] stringarray;
typedef foo barType;
typedef foo[][] barTypes;
typedef sequence<DOMString[]> sequins;
typedef sequence<DOMString[]>? sequinses;
typedef object obj;
typedef Date? today;
typedef (short or double) union;
typedef (short or sequence<DOMString[]?[]>? or DOMString[]?[] or unsigned long long or unrestricted double) craziness;
typedef (short or (long or double)) nestedUnion;
typedef (short or (long or double) or long long) moreNested;
typedef (short or sequence<(DOMString[]?[] or short)>? or DOMString[]?[]) sequenceUnion;

[Constructor, NamedConstructor=MyConstructor, Constructor(short one), NamedConstructor=MyOtherConstructor(long two, long long longest)] partial interface Foo: Bar {
    unsigned long long method(short x, unsigned long long y, optional sequence<Foo> fooArg = 123.4) raises (hell);
    [ha!] attribute short bar getraises (an, exception);
    const short fortyTwo = 42;
    long foo(long x, long y);
};
[NoInterfaceObject] interface LinkStyle {
    stringifier attribute DOMString mediaText;
    readonly attribute short bar;
    getter object (DOMString name);
    getter object bob(DOMString name);
    stringifier foo me(int x);
    stringifier foo ();
    stringifier;
    stringifier attribute short string;
};
[foo] partial dictionary FooDict:BarDict {
    [one "]" ( tricky ] test)] short bar;
    [two] sequence<(double or Foo)> foo = "hello";
};

callback callFoo = short();
callback callFoo2 = unsigned long long(unrestricted double one, DOMString two, Fubar... three);
callback interface callMe {
    attribute short round setraises (for the heck of it);
}

exception foo:bar {
    short round;
    const long one = 2;
    unsigned long long longest;
};
"""
    print "IDL >>>\n" + idl + "\n==="
    parser.parse(idl)
    print repr(parser)
    print str(parser)
    print "<<<"
    print "Complexity: " + str(parser.complexityFactor())
    
    
    for construct in parser.constructs:
        print construct.idlType + ': ' + construct.normalName
        for member in construct:
            print '    ' + member.idlType + ': ' + str(member.normalName) + ' (' + str(member.name) + ')'

    print "FIND:"
    print parser.find('round').fullName
    print parser.find('foo/round').fullName
    print parser.find('Foo/method/y').fullName
    print parser.find('Foo.method').fullName
    print parser.find('Foo(constructor)').fullName
    print parser.find('longest').fullName
    print parser.find('fooArg').fullName
    print parser.find('Window').fullName
    print parser.find('mediaText').fullName

    print "NORMALIZE:"
    print parser.normalizedMethodName('foo')
    print parser.normalizedMethodName('unknown')
    print parser.normalizedMethodName('testMethod(short one, double two)')
    print parser.normalizedMethodName('testMethod2(one, two, and a half)')

