import bdb, pprint, sys
from util import *

class NameSpaceDefinition():
    DefCounter = 0
    def __init__(self, Id,
                 Name,
                 FileName="",
                 LineNumDef=-1,
                 LinesSourceFile = None
                 ):
        NameSpaceDefinition.DefCounter += 1

        self.FileName = FileName
        self.Name = Name
        self.LinesSourceFile = LinesSourceFile
        self.LinesExecutedAllInNameSpaceDef = {}
        self.LineNumDef = LineNumDef

        # in list of all Namespaces: File and Linenum
        self.Id = Id

        self.GuiElems = []
        self.LineNumRetLatest = LineNumDef  # the latest Return Linenum

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
    def __init__(self, NameSpaceDef=None,
                 Fun=True,
                 Parent=None,
                 Level = 0):

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

    def name_space_def_parent_total_counter_inc(self):
        if self.Parent:
            self.Parent.NameSpaceDef.CounterCallsTotalUnderNameSpace += 1
            self.Parent.name_space_def_parent_total_counter_inc()

    def name(self):
        if self.NameSpaceDef:
            return self.NameSpaceDef.Name
        return "NoDefName"

    def id(self):
        return self.NameSpaceDef.Id

    def __str__(self):
        Prefix = " " * self.Level
        Out = []
        Out.append(f"{Prefix} -> {self.name()}")
        for Child in self.ChildrenCalls:
            Out.append(Child.__str__())
        Out.append(f"{Prefix} <- {self.name()}: {self.RetVal}")
        return "\n".join(Out)

class ExecLine():
    FileNameLenMax = 0
    LineLenMax = 0

    def __init__(self, FileName, LineNum, Line, FrameLocals, NameSpaceOneCall):
        self.FileName = FileName
        self.LineNum = LineNum
        self.Line = Line
        self.Locals = self.filterOnlyUserVariables(FrameLocals)
        self.NameSpaceOneCallWhereExecuted = NameSpaceOneCall

        if Len := len(FileName) > ExecLine.FileNameLenMax:
            ExecLine.FileNameLenMax = Len

        if Len := len(Line) > ExecLine.LineLenMax:
            ExecLine.LineLenMax = Len

    def __str__(self):
        # return f"EXEC: {self.LineNum} {self.Line} {self.FileName}\nLOCAL " + str(self.Locals)
        return f"\n========================\nLOCAL " + pprint.pformat(self.Locals) + f"\nnext > {self.LineNum} {self.Line}..........................."

    def filterOnlyUserVariables(self, FrameLocals):
        # in this Frame we can find special vars, keys, everything that needed to execute Py program,
        # we need only simple data types in modelling/program planning system

        def copy(Obj):
            if is_simple(Obj): return Obj

            if is_list(Obj):
                Parent = []
                for Elem in Obj:
                    Parent.append(copy(Elem))
                return Parent

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
    NameSpaceDefinitions = {Root.id(): Root.NameSpaceDef}
    NameSpaceActual = Root
    SourceFiles = {}
    ExecutionAll = []

    def user_call(self, frame, args):
        Name = frame.f_code.co_name or "<unknown>"
        FileName = self.canonic(frame.f_code.co_filename)
        LineNumDef = frame.f_lineno
        if FileName not in Debugger.SourceFiles:
            Debugger.SourceFiles[FileName] = ["# hidden zero line, debugger is 1 based'"]
            Debugger.SourceFiles[FileName].extend(file_read_lines(FileName))

        print("+++ call", Name, args, LineNumDef, FileName)

        Parent = Debugger.NameSpaceActual
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
        Debugger.NameSpaceActual.ChildrenCalls.append(NameSpace)
        Debugger.NameSpaceActual = NameSpace


    def user_line(self, Frame):
        import linecache
        Name = Frame.f_code.co_name
        if not Name: Name = '???'
        Fn = self.canonic(Frame.f_code.co_filename)

        LineNo = Frame.f_lineno
        Line = linecache.getline(Fn, LineNo, Frame.f_globals)
        print('+++ USERLINE', Debugger.NameSpaceActual.name(), Fn, LineNo, Name, ':', Line.strip(), )

        LineInserted = f"{LineNo} {Line}"
        if Fn in Debugger.SourceFiles:
            LineInserted = f"{LineNo} {Debugger.SourceFiles[Fn][LineNo]}"

        print(">>>>>>>>>>> id:", id(Frame.f_locals), Frame.f_locals)
        # LineObj = ExecLine(Fn, LineNo, LineInserted, Frame.f_locals, Debugger.NameSpaceActual)
        # FileName is "<string>" at first execution so I use the namespace's default
        LineObj = ExecLine(Debugger.NameSpaceActual.NameSpaceDef.FileName, LineNo, Line, Frame.f_locals, Debugger.NameSpaceActual)
        Debugger.NameSpaceActual.ExecLines.append(LineObj)

        Debugger.ExecutionAll.append(LineObj)
        Debugger.NameSpaceDefinitions[Debugger.NameSpaceActual.id()].LinesExecutedAllInNameSpaceDef[LineNo] = LineObj

    def user_return(self, Frame, RetVal):
        Name = Frame.f_code.co_name or "<unknown>"
        LineNumRet = Frame.f_lineno
        print('+++ return', Name, RetVal, LineNumRet)

        NameSpaceActual = Debugger.NameSpaceActual
        NameSpaceActual.RetVal = RetVal

        NameSpaceDef = NameSpaceActual.NameSpaceDef
        if NameSpaceDef: # not root elem, it hasn't got name space def

            if NameSpaceDef.LineNumRetLatest is None:
                # root elem hasn't got LineNums
                NameSpaceDef.LineNumRetLatest = LineNumRet

            elif LineNumRet > NameSpaceDef.LineNumRetLatest:
                NameSpaceDef.LineNumRetLatest = LineNumRet

        if Debugger.NameSpaceActual.Parent:
            Debugger.NameSpaceActual = Debugger.NameSpaceActual.Parent

    def user_exception(self, frame, exc_stuff):
        #print('+++ exception', exc_stuff)
        self.set_continue()
