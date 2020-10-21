import bdb, pprint, sys, os
from util_ssp import *
import linecache

class NameSpaceDefinition():
    NameLengthMax = 0
    DefCounter = 0
    def __init__(self, Id,
                 Name,
                 FileName="",
                 LineNumDef=-1,
                 LinesSourceFile = None
                 ):
        NameSpaceDefinition.DefCounter += 1

        self.FileName = FileName
        if (Len:=len(Name)) > NameSpaceDefinition.NameLengthMax:
            NameSpaceDefinition.NameLengthMax = Len

        self.Name = Name
        self.LinesSourceFile = LinesSourceFile
        self.LinesExecutedAllInNameSpaceDef = {}
        self.LineNumDef = LineNumDef

        # in list of all Namespaces: File and Linenum
        self.Id = Id

        self.GuiElems = []

        self.CounterCalled = 0
        self.CounterCallsOut = 0
        self.CounterCallsTotalUnderNameSpace = 0

    def counter_called_inc(self):
        self.CounterCalled += 1

    def counter_calls_out(self):
        self.CounterCallsOut += 1

    def def_line(self):
        if self.LineNumDef == -1:
            return "-- no def line --"
        return self.LinesSourceFile[self.LineNumDef]

    def __str__(self):
        return f"total Calls under: {self.CounterCallsTotalUnderNameSpace:>3}    in: {self.CounterCalled:>3}  out: {self.CounterCallsOut:>3}  {self.Name}    "

class NameSpaceOneCall():
    OneCallCounter = 0

    def __init__(self, NameSpaceDef=None,
                 Fun=True,
                 Parent=None,
                 Level = 0):

        NameSpaceOneCall.OneCallCounter += 1
        self.Id = NameSpaceOneCall.OneCallCounter

        self.ChildrenCalls = []
        self.Parent = Parent
        self.Fun = Fun
        self.RetVal = None
        self.Level = Level
        self.ExecLines = []

        if NameSpaceDef == None:

            NameSpaceDefCounter = NameSpaceDefinition.DefCounter
            NameSpaceDef = NameSpaceDefinition((f"NoDefFile_{NameSpaceDefCounter}",
                                                f"NoDefLineNo_{NameSpaceDefCounter}"),
                                               f"NoDefName_{NameSpaceDefCounter}" )

        self.NameSpaceDef = NameSpaceDef

        if self.Parent:
            self.Parent.NameSpaceDef.counter_calls_out()

        self.name_space_def_parent_total_counter_inc()

    def namespace_def_id(self):
        return self.NameSpaceDef.Id

    def name_space_def_parent_total_counter_inc(self):
        if self.Parent:
            self.Parent.NameSpaceDef.CounterCallsTotalUnderNameSpace += 1
            self.Parent.name_space_def_parent_total_counter_inc()

    def name(self):
        if self.NameSpaceDef:
            return self.NameSpaceDef.Name
        return "NoDefName"

    def __str__(self):
        self.to_str({"hidden_calls_in_analyser":[]})

    def to_str(self, Prg):
        if self.name() in Prg["hidden_calls_in_analyser"]:
            return ""
        Prefix = " " * self.Level
        Out = []
        Out.append(f"{Prefix} -> {self.name()}")
        for Child in self.ChildrenCalls:
            OutChild = Child.to_str(Prg)
            if OutChild: # if OutChild == "" then skip, no empty line in debug output
                Out.append(OutChild)

        RetVal = self.RetVal
        Limit = 100
        if len(str(RetVal)) > Limit:
            RetVal = str(RetVal)[:Limit]
        Out.append(f"{Prefix} <- {self.name()}: {RetVal}")

        return "\n".join(Out)

    def html_create(self, Prg, Dir="./html", FirstCall=True):
        # undisplayed function calls, example: __init__
        if self.name() in Prg["hidden_calls_in_analyser"]:
            return ""

        Prefix = " " * self.Level

        FileLocalsBegin = f"local_{self.Id}_begin.html"
        FileLocalsDiff = f"local_{self.Id}_diff.html"

        LinkOpenBegin = f"<a href='{FileLocalsBegin}' target='right'>"
        LinkOpenDiff = f"<a href='{FileLocalsDiff}' target='right'>"
        LinkClose = "</a>"


        # help files writing out
        LocalsBegin = self.ExecLines[0].Locals
        LocalsEnd = self.ExecLines[-1].Locals
        # print("\nLocalsBegin", LocalsBegin)
        # print("\nLocalsEnd", LocalsEnd)

        file_write_simple(os.path.join(Dir, FileLocalsBegin), "<pre>begin:" + pprint.pformat(LocalsBegin)+"</pre>")
        #file_write_simple(os.path.join(Dir, FileLocalsDiff),  "<pre> diff: " + pprint.pformat( diff_objects(LocalsBegin, LocalsEnd))+"</pre>")
        file_write_simple(os.path.join(Dir, FileLocalsDiff),  "<pre> diff: " + pprint.pformat( LocalsEnd)+"</pre>")


        Out = []
        if FirstCall:
            Out.append("<pre>")

        Out.append(f"{Prefix} -> {LinkOpenBegin}{self.name()}{LinkClose}")

        for Child in self.ChildrenCalls:
            OutChild = Child.html_create(Prg, FirstCall=False)
            if OutChild: # if OutChild == "" then skip, no empty line in debug output
                Out.append(OutChild)

        RetVal = self.RetVal
        Limit = 100
        if len(str(RetVal)) > Limit:
            RetVal = str(RetVal)[:Limit]
        Out.append(f"{Prefix} <- {LinkOpenDiff}{self.name()}{LinkClose}: {self.RetVal}")

        if FirstCall:
            FileCalls = os.path.join(Dir, "calls.html")
            file_write_simple(FileCalls, "\n".join(Out) + "\n</pre>", Mode="w")
        else:
            return "\n".join(Out)


class ExecLine():
    FileNameLenMax = 0
    LineLenMax = 0
    def __init__(self, FileName, LineNum, Line, FrameLocals, NameSpaceOneCall):
        self.FileName = FileName
        self.LineNum = LineNum
        self.Line = Line.rstrip()
        self.Locals = self.filterOnlyUserVariables(FrameLocals)
        self.NameSpaceOneCallWhereExecuted = NameSpaceOneCall

        if Len := len(FileName) > ExecLine.FileNameLenMax:
            ExecLine.FileNameLenMax = Len

        if Len := len(Line) > ExecLine.LineLenMax:
            ExecLine.LineLenMax = Len

    def __str__(self):
        return f"\n========================\nLOCAL " + pprint.pformat(self.Locals) + f"\nnext > {self.LineNum} {self.Line}..........................."

    def to_file(self):
        # FilesSkipped = ("posixpath.py", "os.py")
        #
        # if self.FileName.split(os.path.sep)[-1] in FilesSkipped:
        #     return ""
        # FIXME: linux specific solution
        if "/usr/lib" in self.FileName:
            return ""
        #return f"{self.LineNum:>3} {self.FileName.split(os.path.sep)[-1]} {self.Line}"
        NameLengthMax = self.NameSpaceOneCallWhereExecuted.NameSpaceDef.NameLengthMax
        return f"{self.LineNum:>3} {self.NameSpaceOneCallWhereExecuted.NameSpaceDef.Name:>{NameLengthMax}} {self.Line}"

    def filterOnlyUserVariables(self, FrameLocals):
        # in this Frame we can find special vars, keys, everything that needed to execute Py program,
        # we need only simple data types in modelling/program planning system

        def copy(Obj):
            if is_simple(Obj): return Obj

            if is_tuple(Obj):
                New = []
                for Elem in Obj:
                    New.append(copy(Elem))
                return tuple(New)

            if is_list(Obj):
                New = []
                for Elem in Obj:
                    New.append(copy(Elem))
                return New

            if is_dict(Obj):
                Parent = dict()
                for Key, Val in Obj.items():
                    if is_simple(Key):
                        Parent[Key] = copy(Val)
                return Parent

            # print("too:", type(Obj))
            return "too complicated elem to duplicate"

        return copy(FrameLocals)

class Debugger(bdb.Bdb):
    Root = NameSpaceOneCall()
    NameSpaceDefinitions = {Root.namespace_def_id(): Root.NameSpaceDef}
    NameSpaceActualCall = Root
    SourceFiles = {}
    ExecutionAll = []

    def user_call(self, Frame, args):
        Name = Frame.f_code.co_name or "<unknown>"
        FileName = self.canonic(Frame.f_code.co_filename)
        LineNumDef = Frame.f_lineno
        if FileName not in Debugger.SourceFiles:
            Debugger.SourceFiles[FileName] = ["# hidden zero line, debugger is 1 based'"]
            Debugger.SourceFiles[FileName].extend(file_read_lines(FileName))

        print("+++ call", Name, args, LineNumDef, FileName)

        Parent = Debugger.NameSpaceActualCall
        ##############################################################################
        NameSpaceDefId = (FileName, LineNumDef)
        # Save all namespaces Once
        if NameSpaceDefId not in Debugger.NameSpaceDefinitions:

            Debugger.NameSpaceDefinitions[NameSpaceDefId] = \
                NameSpaceDefinition(NameSpaceDefId,
                                    Name,
                                    FileName=FileName,
                                    LineNumDef=LineNumDef,
                                    LinesSourceFile = Debugger.SourceFiles[FileName])

        ##############################################################################
        NameSpace = NameSpaceOneCall(Debugger.NameSpaceDefinitions[NameSpaceDefId],
                                     Parent = Parent,
                                     Level = Parent.Level+1)

        ##############################################################################
        Debugger.NameSpaceActualCall.ChildrenCalls.append(NameSpace)
        Debugger.NameSpaceActualCall = NameSpace


    def user_line(self, Frame):
        Name = Frame.f_code.co_name
        if not Name: Name = '???'
        Fn = self.canonic(Frame.f_code.co_filename)

        LineNo = Frame.f_lineno
        Line = linecache.getline(Fn, LineNo, Frame.f_globals)
        print('\n+++ USERLINE', Debugger.NameSpaceActualCall.name(), Fn, LineNo, Name, ':', Line.strip(), )

        LineInserted = f"{LineNo} {Line}"
        if Fn in Debugger.SourceFiles:
            LineInserted = f"{LineNo} {Debugger.SourceFiles[Fn][LineNo]}"

        print(f"+++      flocals id:  {id(Frame.f_locals)}", Frame.f_locals)
        # LineObj = ExecLine(Fn, LineNo, LineInserted, Frame.f_locals, Debugger.NameSpaceActualCall)
        # FileName is "<string>" at first execution so I use the namespace's default
        LineObj = ExecLine(Debugger.NameSpaceActualCall.NameSpaceDef.FileName, LineNo, Line, Frame.f_locals, Debugger.NameSpaceActualCall)
        Debugger.NameSpaceActualCall.ExecLines.append(LineObj)

        Debugger.ExecutionAll.append(LineObj)
        Debugger.NameSpaceDefinitions[Debugger.NameSpaceActualCall.NameSpaceDef.Id].LinesExecutedAllInNameSpaceDef[LineNo] = LineObj

    def user_return(self, Frame, RetVal):
        Name = Frame.f_code.co_name or "<unknown>"
        LineNumRet = Frame.f_lineno
        FileName = self.canonic(Frame.f_code.co_filename)
        Line = linecache.getline(FileName, LineNumRet, Frame.f_globals)
        print('+++ return', f"flocal id: {id(Frame.f_locals)}", Name, RetVal, LineNumRet, Line)

        Debugger.NameSpaceActualCall.RetVal = RetVal

        #
        # LineObj = ExecLine(FileName, LineNumRet, Line, Frame.f_locals, Debugger.NameSpaceActualCall)
        # Debugger.NameSpaceActualCall.ExecLines.append(LineObj)

        if Debugger.NameSpaceActualCall.Parent:
            Debugger.NameSpaceActualCall = Debugger.NameSpaceActualCall.Parent

    def user_exception(self, frame, exc_stuff):
        #print('+++ exception', exc_stuff)
        self.set_continue()
