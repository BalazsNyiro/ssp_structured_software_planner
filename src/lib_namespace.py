NameSpaceDefinitions = {}
NameSpaceMaxNameLength = 0

HiddenCallsGeneral = {
    "deepcopy",
    "__enter__",
    "__exit__",
    "_get_sep",
    "__contains__",
    "__del__",
    "__new__",
    "_joinrealpath",
    "__getattr__",
    "__getitem__",
    "__init__",
    "join",
    #"isfile",
    "isdir",
    #"shell",
    "abspath",
    "closed",
    #"walk",

}
# HiddenCallsGeneral = set()

class NameSpaceDef():

    def __init__(self, Name, FileName, LineNum):
        global NameSpaceDefinitions
        global NameSpaceMaxNameLength

        NsId = (Name, FileName, LineNum)
        if NsId not in NameSpaceDefinitions:
            NameSpaceDefinitions[NsId] = self
        if Len := len(Name) > NameSpaceMaxNameLength:
           NameSpaceMaxNameLength = Len

class NameSpaceCall():
    def __init__(self, Prg, Name, FileName, LineNum, Caller = None, Level=0):
        self.NameSpace = NameSpaceDef(Name, FileName, LineNum)
        self.Name = Name
        self.Caller = Caller
        self.Lines = []
        self.Level = Level
        self.Type = "NameSpaceCall"

        self.DisplayThisCall = True
        self.DisplayChildren = True

        if Name in HiddenCallsGeneral.union(Prg["HiddenCallsPrgSpecific"]):
            self.DisplayThisCall = False

        if Name in Prg["HideChildrenInTheseCalls"]:
            self.DisplayChildren = False

    def __str__(self):
        Indent = "  " * self.Level
        #print(f"{Indent} {self.Name}")

        ChildrenOut = []
        if self.DisplayChildren:
            for Elem in self.Lines:

                if Elem.Type == "NameSpaceCall":
                    if Elem.DisplayThisCall:
                        if CallDisplayedText := str(Elem):
                           ChildrenOut.append(CallDisplayedText)

                if Elem.Type == "ExecLine":
                    #   : means: simmple line in Call
                    ChildrenOut.append(Indent + "  :" + Elem.Line)

        NewLineBeforeChildren = "" if not ChildrenOut else "\n"
        return f"{Indent}{self.Name.upper()}{NewLineBeforeChildren}" + "\n".join(ChildrenOut)

def name_space_calls_create(Prg, PrgSaved):
    NameSpaceRoot = None
    NameSpaceActual = None

    for ExecLine in PrgSaved["ExecutionAll"]:
        print("\n>>>", ExecLine.Event, type(ExecLine.Name))
        if not NameSpaceRoot:
            NameSpaceRoot = NameSpaceCall(Prg,
                                          ExecLine.Name,
                                          ExecLine.FileName,
                                          ExecLine.LineNum)
            NameSpaceActual = NameSpaceRoot
            continue ##########################################


        if ExecLine.Event == "call":
            NameSpaceNew = NameSpaceCall(Prg,
                                         ExecLine.Name,
                                         ExecLine.FileName,
                                         ExecLine.LineNum,
                                         Level = NameSpaceActual.Level+1)

            NameSpaceActual.Lines.append(NameSpaceNew)
            NameSpaceNew.Caller = NameSpaceActual
            NameSpaceActual = NameSpaceNew

        if ExecLine.Event == "line":
            NameSpaceActual.Lines.append(ExecLine)

        elif ExecLine.Event == "ret":
            NameSpaceActual = NameSpaceActual.Caller

    return NameSpaceRoot

