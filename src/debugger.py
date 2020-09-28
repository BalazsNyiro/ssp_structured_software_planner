from subprocess import Popen, PIPE

def proc_start(Cmd):
    FileWrite = open("tmpout", "wb")
    FileRead = open("tmpout", "r")

    Process = Popen(Cmd, stdin = PIPE, stdout = FileWrite, stderr = FileWrite)
    return Process, FileWrite, FileRead

def proc_input(Input, Process, FileRead):
    # if Input[-1] != b"\n":
    #     Input += b"\n"
    Process.stdin.write(Input)
    return FileRead.read()

def proc_end(FileWrite, FileRead):
    FileWrite.close()
    FileRead.close()
