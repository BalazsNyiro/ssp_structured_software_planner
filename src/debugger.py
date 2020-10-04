# credits for process handling:
# https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
# https://stackoverflow.com/questions/19880190/interactive-input-output-using-python

import subprocess
import os, fcntl
import util

LineSep = "\n"

def find_line_with_sign(Txt, Sign, Separator="", WantedIndex=0, FirstOrLastResult="last"):
    Ret = ""
    for Line in Txt.split(LineSep):
        if Sign == Line[0:len(Sign)]: # find sign at the beginning of the line
            if Separator:
                Elems = Line.split(Separator)
                Ret = Elems[WantedIndex]
            else:
                Ret = Line
            if FirstOrLastResult == "first":
                break
                # else later we can catch another line
    return Ret



Files = {}

def get_line_from_file(DebuggerLine, Return):
    """
     
    :param DebuggerLine: '> ./ssp_structured_software_planner/try/riverbank.py(55)main()'
    :return: 
    """
    print("DebuggerLine:", DebuggerLine)
    PathLineNumFun = DebuggerLine[2:]
    Path, LineNum = PathLineNumFun.split(")", 1)[0].split("(")
    print(f"Path: {Path}  Linenum:{LineNum}")

    ReturnPrefix = "ret" if Return else "   "
    return f"{LineNum:2} {ReturnPrefix}" + util.file_read(Path)[int(LineNum)-1] # 0 based linenum vs human 1 based in debugger

class StepNext:

    def gui_id(self):
        return f"{self.FileName}{self.LineNum}"

    def __init__(self, Txt):
        self.Txt = Txt # the current step's source code
        self.Call = "--Call--" in Txt



        self.Return = "--Return--" in Txt
        self.ReturnValue = None

        if self.Return:
            # empty line can be before --Return--,
            # I can't be sure the exact num of line of return object

            # EXAMPLE RETURN STRING:
            # --Return--
            # > ./ssp_structured_software_planner/try/riverbank.py(22)change()->18.549999999999997
            # -> return AmountTo
            # (Pdb)
            self.ReturnValue = eval( find_line_with_sign(Txt, "> ", "->", 1)   ) # return with FIRST -> line!



        # the program can print his own output into the debugger's output
        # so sometime I need to catch the last result

        #   0.4 GBP -> 0.60 USD
        # > ./ssp_structured_software_planner/try/riverbank.py(22)change()
        # -> return AmountTo
        # (Pdb)
        print("\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n")
        #print(Txt)
        print("\n......................\n")
        self.SourceCodeLineInFile = get_line_from_file(find_line_with_sign(Txt, "> "), self.Return).rstrip()
        self.SourceCodeLineInDebugger = find_line_with_sign(Txt, "-> ", "-> ", 1)
        print("SourceCodeLineInDebugger", self.SourceCodeLineInDebugger)
        print("\nBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\n")

        self.SourceCodeLinesOfCurrentNameSpace = []
        self.End = "<<PrgEnd>>" in Txt

        self.FileName = ""
        self.LineNum = ""
        self.FunName = ""
        for Line in Txt.split(LineSep):
            if not self.FileName:
                if "> " == Line[0:2]:
                    FileAndLineNum, self.FunName = Line.split(")", 1)
                    self.FileName, self.LineNum = FileAndLineNum.split("(")
                    self.FileName = self.FileName[2:] # "> " removed from line head

                    # at return statements the ret value is after the fun name
                    # > ./try/riverbank.py(21)change()->0.6000000000000001
                    self.FunName = self.FunName.split("->")[0]

        self.DisplayedName = f"{self.FileName.split('/')[-1]} {self.FunName}"
        self.Args = dict()

def proc_step_next(Proc):
    proc_input(Proc, b"step")
    ProcReply = proc_output(Proc)
    StepNow = StepNext(ProcReply)
    print("StepNow.Txt", StepNow.Txt)
    print("\nCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\n\n\n")

    # we have to process prev ProcReply,
    # then we can call next debugger statement and process it's reply
    if StepNow.Call:  # Get arguments, we entered into a call
        proc_input(Proc, b"args")  # list arguments
        ProcReplyArgs = proc_output(Proc)
        if ProcReplyArgs.strip():  # if call has any arguments
            for Line in ProcReplyArgs.split(LineSep):
                if "=" in Line:
                    Key, Val = Line.split("=")
                    Key = Key.strip()
                    Val = eval(Val)
                    StepNow.Args[Key] = Val
            # print("ARGS:", StepNow.Args)

        proc_input(Proc, b"ll")  # list source code
        ProcReplyLL = proc_output(Proc)
        if ProcReplyLL.strip():  # if call has any arguments
            # last line is always (Pdb), remove it
            StepNow.SourceCodeLinesOfCurrentNameSpace.extend(ProcReplyLL.split(LineSep)[:-1])
    return StepNow


def setNonBlocking(fd):
    """
    Set the file description of the given file descriptor to non-blocking.
    """
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

def prg_start(PathPy):
    Proc = subprocess.Popen(['python3', PathPy],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            )
    setNonBlocking(Proc.stdout)
    setNonBlocking(Proc.stderr)
    setNonBlocking(Proc.stdin)
    return Proc

def prg_end(Proc):
    Proc.stdin.close()
    Proc.terminate()
    Proc.wait(timeout=0.2)

def proc_input(Proc, Input):
    if Input[-1] != b"\n":
        Input = Input + b"\n"
    # print("proc_input", Input)
    Proc.stdin.write(Input)
    Proc.stdin.flush()

def proc_output(Proc):
    # print("proc_output")
    Lines = []
    while True:
        Line = Proc.stdout.readline()
        if Line != b"":
            Lines.append(Line)
            if b"(Pdb)" == Line[0:5]:
                break

    AllLines = (b"".join(Lines)).decode('utf-8')
    # print(AllLines)
    return AllLines

