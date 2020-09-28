# https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
#
import subprocess

def prg_start(PathPy):
    print(PathPy)
    proc = subprocess.Popen(['python3', '-i'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    #print(proc.stdout.readline())


    # To avoid deadlocks: careful to: add \n to output, flush output, use
    # readline() rather than read()
    proc.stdin.write(b'2+3\n')
    proc.stdin.flush()
    print(proc.stdout.readline())


    proc.stdin.close()
    proc.terminate()
    proc.wait(timeout=0.2)
