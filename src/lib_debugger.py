import bdb, pprint, sys, os
from util_ssp import *
import linecache

class ExecLine():
    NameSpaceLenMax = 0
    FileNameLenMax = 0
    LineLenMax = 0
    def __init__(self, NameSpace, FileName, LineNum, Line, FrameLocals, Event=""):
        self.NameSpace = NameSpace
        if (Max:=len(NameSpace)) > ExecLine.NameSpaceLenMax:
            ExecLine.NameSpaceLenMax = Max
        self.Event = Event
        self.FileName = FileName
        self.LineNum = LineNum
        self.Line = Line.rstrip()
        self.Locals = self.filterOnlyUserVariables(FrameLocals)

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
        LineNumDisplayed = str(self.LineNum).strip()
        if not LineNumDisplayed:
            LineNumDisplayed = "-"
        return f"{LineNumDisplayed:>3} {self.Event:>4} {self.NameSpace:>{self.NameSpaceLenMax}} {self.Line}"

    def filterOnlyUserVariables(self, FrameLocals):
        # in this Frame we can find special vars, keys, everything that needed to execute Py program,
        # we need only simple data types in modelling/program planning system
        return copy(FrameLocals)




class Debugger(bdb.Bdb):
    SourceFiles = {}
    ExecutionAll = []

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
        NameSpace, FileName, LineNumDef, Line = self.frame_info(Frame)

        if FileName not in Debugger.SourceFiles:
            Debugger.SourceFiles[FileName] = ["# hidden zero line, debugger is 1 based'"]
            Debugger.SourceFiles[FileName].extend(file_read_lines(FileName))

        print("+++ call", NameSpace, args, LineNumDef, FileName)

        LineObj = ExecLine(NameSpace, FileName, LineNumDef, Line, Frame.f_locals, Event="call")
        Debugger.ExecutionAll.append(LineObj)

    def user_line(self, Frame):
        NameSpace, FileName, LineNo, Line = self.frame_info(Frame)
        print('\n+++ USERLINE', FileName, LineNo, NameSpace, ':', Line.strip(), )
        LineInserted = f"{LineNo} {Line}"
        print(f"+++      flocals id:  {id(Frame.f_locals)}", Frame.f_locals)
        LineObj = ExecLine(NameSpace, FileName, LineNo, LineInserted, Frame.f_locals, Event="line")
        Debugger.ExecutionAll.append(LineObj)

    def user_return(self, Frame, RetVal):
        NameSpace, FileName, LineNumRet, Line = self.frame_info(Frame)
        print('+++ return', f"flocal id: {id(Frame.f_locals)}", NameSpace, RetVal, LineNumRet, Line)
        LineObj = ExecLine(NameSpace, FileName, LineNumRet, Line, Frame.f_locals, Event="ret")
        Debugger.ExecutionAll.append(LineObj)

    def user_exception(self, frame, exc_stuff):
        #print('+++ exception', exc_stuff)
        self.set_continue()
