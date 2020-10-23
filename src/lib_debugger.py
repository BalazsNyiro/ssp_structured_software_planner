import bdb, pprint, sys, os
from util_ssp import *
import linecache

class ExecLine():
    NameSpaceLenMax = 0
    FileNameLenMax = 0
    LineLenMax = 0
    def __init__(self, Name, FileName, LineNum, Line, FrameLocals, Event=""):
        self.Name = Name
        if (Max:=len(Name)) > ExecLine.NameSpaceLenMax:
            ExecLine.NameSpaceLenMax = Max
        self.Event = Event
        self.FileName = FileName
        self.LineNum = LineNum
        self.Line = Line.rstrip()
        self.Locals = self.filterOnlyUserVariables(FrameLocals)

        self.Type = "ExecLine"

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
        # if "/usr/lib" in self.FileName:
        #     return ""
        LineNumDisplayed = str(self.LineNum).strip()
        if not LineNumDisplayed:
            LineNumDisplayed = "-"
        return f"{LineNumDisplayed:>3} {self.Event:>4} {self.Name:>{self.NameSpaceLenMax}} {self.Line}"

    def filterOnlyUserVariables(self, FrameLocals):
        # in this Frame we can find special vars, keys, everything that needed to execute Py program,
        # we need only simple data types in modelling/program planning system
        return copy(FrameLocals)

class Debugger(bdb.Bdb):
    SourceFiles = {}
    ExecutionAll = []
    Verbose = True

    def frame_info(self, Frame):
        NameSpace = Frame.f_code.co_name or "<unknown>"
        if not NameSpace: NameSpace = '???'

        # FileName is "<string>" at first execution so I use the namespace's default
        FileName = str(self.canonic(Frame.f_code.co_filename))

        LineNum = Frame.f_lineno
        Line = linecache.getline(FileName, LineNum, Frame.f_globals)

        if FileName in Debugger.SourceFiles: # use original code if you can
            Line = Debugger.SourceFiles[FileName][LineNum]

        return NameSpace, FileName, LineNum, Line

    def user_call(self, Frame, args):

        Name, FileName, LineNumDef, Line = self.frame_info(Frame)

        if Debugger.Verbose:
            print("+++ call", Name, LineNumDef, args)

        # for loop over list:
        # if Name[0] =="<":
        #     return # list comprehension or other inner call, not real user called fun

        # if FileName not in Debugger.SourceFiles:
        #     Debugger.SourceFiles[FileName] = ["# hidden zero line, debugger is 1 based'"]
        #     Debugger.SourceFiles[FileName].extend(file_read_lines(FileName))

        LineObj = ExecLine(Name, FileName, LineNumDef, Line, Frame.f_locals, Event="call")
        Debugger.ExecutionAll.append(LineObj)

    def user_line(self, Frame):
        Name, FileName, LineNo, Line = self.frame_info(Frame)
        if Debugger.Verbose:
            print('+++ line  ', Name, LineNo, ':', Line.strip(), )
            #print(f"+++      flocals id:  {id(Frame.f_locals)}", Frame.f_locals)
        LineInserted = f"{LineNo} {Line}"
        LineObj = ExecLine(Name, FileName, LineNo, LineInserted, Frame.f_locals, Event="line")
        Debugger.ExecutionAll.append(LineObj)

    def user_return(self, Frame, RetVal):
        Name, FileName, LineNumRet, Line = self.frame_info(Frame)
        if Debugger.Verbose:
            print('+++ return', Name, LineNumRet, f"flocal id: {id(Frame.f_locals)}", RetVal, Line)
        LineObj = ExecLine(Name, FileName, LineNumRet, Line, Frame.f_locals, Event="ret")
        Debugger.ExecutionAll.append(LineObj)

    def user_exception(self, frame, exc_stuff):
        if Debugger.Verbose:
            print('+++ except', exc_stuff)
