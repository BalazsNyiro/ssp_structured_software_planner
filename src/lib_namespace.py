NameSpaceDefinitions = {}
NameSpaceMaxNameLength = 0

HiddenCallsGeneral = {
    "__enter__",
    "__exit__",
    "_get_sep",
    "__contains__",
    "__del__",
    "_joinrealpath",
    "__getattr__",
    "__getitem__",
    "__init__",
    "join",
    "isfile",
    "isdir",
    "shell",
    "abspath",
    "walk",

}

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
        self.Calls = []
        self.Level = Level

        self.DisplayThisCall = True
        self.DisplayChildren = True

        if Name in HiddenCallsGeneral.union(Prg["Saved"]["HiddenCallsPrgSpecific"]):
            self.DisplayThisCall = False

        if Name in Prg["Saved"]["HideChildrenInTheseCalls"]:
            self.DisplayChildren = False

    def call(self, Called):
        self.Calls.append(Called)

    def __str__(self):
        if not self.DisplayThisCall:
            return ""

        ChildrenOut = []
        if self.DisplayChildren:
            for Call in self.Calls:
                if self.DisplayChildren:
                    if CallDisplayedText := str(Call):
                       ChildrenOut.append(CallDisplayedText)

        NewLineBeforeChildren = "" if not ChildrenOut else "\n"

        Indent = " " * self.Level
        return f"{Indent} {self.Name}{NewLineBeforeChildren}" + "\n".join(ChildrenOut)

def name_space_calls_create(Prg):
    NameSpaceRoot = None
    NameSpaceActual = None

    for ExecLine in Prg["Saved"]["ExecutionAll"]:
        # print("\n>>>", ExecLine.Event, type(ExecLine.Name))
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

            NameSpaceActual.Calls.append(NameSpaceNew)
            NameSpaceNew.Caller = NameSpaceActual
            NameSpaceActual = NameSpaceNew

        elif ExecLine.Event == "ret":
            NameSpaceActual = NameSpaceActual.Caller

    return NameSpaceRoot

