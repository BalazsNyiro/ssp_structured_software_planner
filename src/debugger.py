# credits for process handling:
# https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
# https://stackoverflow.com/questions/19880190/interactive-input-output-using-python

import subprocess
import os, fcntl

LineSep = "\n"

class Step:

    def __init__(self, Txt, ProcForPossibleQuestions):
        self.Txt = Txt
        self.Call = "--Call--"  in Txt
        self.Return = "--Return--" in Txt
        self.End = "<<PrgEnd>>" in Txt

        self.ReturnValue = None
        if self.Return:
            self.ReturnValue = eval(Txt.split(LineSep)[1].split("->")[1])

        self.FileName = ""
        self.LineNum = ""
        self.FunName = ""
        for Line in Txt.split(LineSep):
            if not self.FileName:
                if "> " == Line[0:2]:
                    FileAndLineNum, self.FunName = Line.split(")", 1)
                    self.FileName, self.LineNum = FileAndLineNum.split("(")
                    self.FileName = self.FileName[2:] # "> " removed from line head

        self.Args = dict()
        if self.Call: # Get arguments
            proc_input(ProcForPossibleQuestions, b"args") #list arguments
            ProcReplyArgs = proc_output(ProcForPossibleQuestions)
            # print("ProcReplyArgs ", ProcReplyArgs )
            if ProcReplyArgs.strip(): # if call has any arguments
                for Line in ProcReplyArgs.split(LineSep):
                    if "=" in Line:
                        Key, Val = Line.split("=")
                        Key = Key.strip()
                        Val = eval(Val)
                        self.Args[Key] = Val

def proc_step(Proc):
    proc_input(Proc, b"step")
    ProcReply = proc_output(Proc)
    StepNow = Step(ProcReply, Proc)
    # print(StepNow.Txt)
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
    return Proc

def prg_end(Proc):
    Proc.stdin.close()
    Proc.terminate()
    Proc.wait(timeout=0.2)

def proc_input(Proc, Input):
    if Input[-1] != b"\n":
        Input += b"\n"
    Proc.stdin.write(Input)
    Proc.stdin.flush()

def proc_output(Proc):
    Lines = []
    while True:
        Line = Proc.stdout.readline()
        if b"(Pdb)" in Line:
            break
        if Line != b"":
            Lines.append(Line)

    AllLines = (b"".join(Lines)).decode('utf-8')
    # print(AllLines)
    return AllLines

