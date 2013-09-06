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
import itertools

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

class Marker(object):
    def markupConstruct(self, text, construct):
        return '<' + construct.idlType + '>' + text + '</' + construct.idlType + '>'
    
    def markupType(self, text, construct):
        return '<TYPE for=' + construct.idlType + '>' + text + '</TYPE>'
    
    def markupName(self, text, construct):
        return '<NAME for=' + construct.idlType + '>' + text + '</NAME>'

class NullMarker(object):
    def markupConstruct(self, text, construct):
        return text
    
    def markupType(self, text, construct):
        return text
    
    def markupName(self, text, construct):
        return text

class ui(object):
    def warn(self, str):
        print str

def testDifference(input, output):
    if (output == input):
        print "NULLIPOTENT"
    else:
        print "DIFFERENT"
        inputLines = input.split('\n')
        outputLines = output.split('\n')
        
        for inputLine, outputLine in itertools.izip_longest(inputLines, outputLines, fillvalue = ''):
            if (inputLine != outputLine):
                print "<" + inputLine
                print ">" + outputLine
                print


if __name__ == "__main__":      # called from the command line
    sys.excepthook = debugHook
    parser = parser.Parser(ui=ui())
    idl = """ // this is a comment
interface Multi : One  ,  Two   ,   Three     {
        attribute short one;
};
typedef sequence<Foo[]>? fooType;
typedef (short or Foo) maybeFoo;
typedef sequence<(short or Foo)> maybeFoos;
interface foo {
  [one] attribute Foo one;
  [two] Foo two();
  [three] const Foo three = 3;
};
 typedef   short    shorttype  = error this is;

   const  long    long   one=   2   ;
 Window   implements     WindowInterface  ; // more comment
       
enum   foo    {"one"  ,    "two",    }     ;
enum foo { "one" };
enum bar{"one","two","three",}; // and another
enum comments {
"one", //comment one
"two", //comment two
"three"  , //coment three
};

 typedef  short shorttype;
typedef long longtype;
typedef long long longtype;
typedef [hello, my name is inigo montoya (you ] killed my father)] unsigned long long inigo;
typedef unrestricted double dubloons;
typedef short [ ] shortarray;
typedef DOMString string;
typedef DOMString[] stringarray;
typedef foo barType;
typedef foo [ ] [ ]  barTypes;
typedef sequence<DOMString[]> sequins;
typedef sequence<DOMString[]>? sequinses;
typedef object obj;
typedef Date? today;
typedef (short or double) union;
typedef (short or sequence < DOMString [ ] ? [ ] > ? or DOMString[]?[] or unsigned long long or unrestricted double) craziness;
typedef (short or (long or double)) nestedUnion;
typedef (short or (long or double) or long long) moreNested;
typedef (short or sequence<(DOMString[]?[] or short)>? or DOMString[]?[]) sequenceUnion;

[ Constructor , NamedConstructor = MyConstructor, Constructor (Foo one), NamedConstructor = MyOtherConstructor (Foo two , long long longest ) ] partial interface Foo: Bar {
    unsigned long long method(short x, unsigned long long y, optional sequence<Foo> fooArg = 123.4) raises (hell);
    [ha!] attribute short bar getraises (an, exception);
    const short fortyTwo = 42;
    long foo(long x, long y);
};
[ NoInterfaceObject ] interface LinkStyle {
    stringifier attribute DOMString mediaText;
    readonly attribute short bar;
    getter object (DOMString name);
    getter setter object bob(DOMString name);
    stringifier foo me(int x);
    stringifier foo ();
    stringifier;
    stringifier attribute short string;
    this is a syntax error, naturally
};
[foo] partial dictionary FooDict:BarDict {
    [one "]" ( tricky ] test)] short bar;
    [two] sequence<(double or Foo)> foo = "hello";
};

callback callFoo = short();
callback callFoo2 = unsigned long long(unrestricted double one, DOMString two, Fubar ... three);
callback interface callMe {
    attribute short round setraises (for the heck of it);
};

exception foo:bar {
    short round;
    const long one = 2;
    Foo foo;
    unsigned long long longest;
};
"""
#    idl = idl.replace(' ', '  ')
    print "IDL >>>\n" + idl + "\n<<<"
    parser.parse(idl)
    testDifference(idl, str(parser))

    print "MARKED UP:"
    testDifference(idl, parser.markup(NullMarker()))
    print parser.markup(Marker())

    print repr(parser)
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

