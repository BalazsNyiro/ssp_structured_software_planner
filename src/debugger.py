# credits for process handling:
# https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
# https://stackoverflow.com/questions/19880190/interactive-input-output-using-python

import subprocess
import os, fcntl

class Step:

    def __init__(self, Txt):
        self.Txt = Txt
        self.Call = "--call--"  in Txt
        self.Return = "--return--" in Txt

        self.ReturnValue = ""
        if self.Return:
            self.ReturnValue = Txt.split("\n")[1].split("->")[1]

def proc_step(Proc):
    pass

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
    print(AllLines)
    return AllLines

