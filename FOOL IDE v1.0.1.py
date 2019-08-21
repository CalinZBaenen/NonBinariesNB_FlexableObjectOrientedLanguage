import sys as outerSystem
import datetime
import os

os.system("title FOOL IDE v1.0.1")
inputInterface = ""
indentationNumber = 0

print("Welcome to the FOOL programming interface. Do '[]help' for help.\n")

def programming():
    global inputInterface
    Lang.parse("run Modules/System/help.fool ")
    while True:
        script = input("")
        script += " "
        Lang.parse(script)
class Lang:
    globalClasses = {}
    codeBlocks = {"if": [], "elif": [] ,"else": [],"while": [],"for": [], "try": [], "catch": []}
    globalVariables = {}
    codeNum = -1
    showDebugInfo = False
    lastLoadedClass = ""
    currentLoadedClass = ""
    dataTypes = ["string","boolean","list","number","class","dynamic","none","any","None"]
    variableScopes = ["global"]
    sysElements = ["INTERFACE","TITLE"]
    sysColors = ["WHITE","GRAY","GREY","LIGHT_GRAY","LIGHT_GREY","LAPIS","BLUE","CYAN","AQUA","VIOLET","PURPLE","MAGENTA","PINK","RED","CRIMSON","LIME","GREEN","DARK_GREEN","CACTI_GREEN","BLACK"]
    stringOperators = ["+","*"]
    numberOperators = ["+","-","*","/","%"]
    indentationFormat = 0
    fileNameSpace = "Main"
    classesVisited = [fileNameSpace]
    globalClasses[fileNameSpace] = []
    globalCommandList = []
    currentLoadedClass = fileNameSpace
    thisReturnVariable = None
    BCC = ["if","elif","else","while","for","try","catch"]
    def parse(src):
        this = Lang
        global inputInterface
        global indentationNumber
        tok = ""
        command = ""
        operation = ""
        modifier = ""
        classReturnValue = None
        lastValue = None
        currentValue = None
        expectedValue = ""
        string =""
        expectedDataType = "none"
        givenDataType = "none"
        fileToRun = None
        sysInput = ""
        heap = []
        strings = []
        numbers = []
        bools = []
        lists = []
        finalList = []
        reservedLists = [None]
        state = 0
        parametersForClass = None
        programStatus = None
        isDataType = False
        blockRun = False
        lookingForParams = False
        extraString = False
        leftOverInt = False
        stringStarter = ""
        charNumber = 0
        if this.thisReturnVariable is not None and this.currentLoadedClass == this.fileNameSpace:
            src += (str(this.thisReturnVariable) + " ")
            this.thisReturnVariable = None
        else:
            pass
        if (this.currentLoadedClass in this.globalClasses):
            this.globalClasses[this.currentLoadedClass].append(src)
        elif len(this.globalCommandList) > 0:
            this.codeBlocks[this.globalCommandList[-1]].append(src)
        else:
            outerSystem.exit()
        for char in src:
            heap = list(filter(lambda a: a != "", heap))
            heap = list(filter(lambda a: a != "=", heap))
            heap = list(filter(lambda a: a != "True", heap))
            heap = list(filter(lambda a: a != "False", heap))
            if programStatus == 0 or programStatus == False or tok == "close":
                os.system("exit")
                outerSystem.exit(0)
            for scope in this.variableScopes:
                heap = list(filter(lambda a: a != scope, heap))
            if state == 1:
                string += char
            tok += char
            if tok == " " or tok == "\t":
                tok = ""
            elif tok == "namespace":
                command = "fileID"
                tok = ""
            elif (tok in this.globalClasses) and state == 0 and indentationNumber == 0:
                try:
                    if type(reservedLists[-1]) is not list:
                        pass
                    else:
                        parameterNumber = 1
                        del lists[-1]
                        for block in this.globalClasses[tok]:
                            for parameterVariable in reservedLists[-1]:
                                this.parse("parameter"+str(parameterNumber)+" = \""+str(parameterVariable)+"\"")
                                parameterNumber += 1
                            this.parse(block)
                        while parameterNumber > 1:
                            this.globalVariables.pop("parameter"+str(parameterNumber))
                            parameterNumber -= 1
                except Exception:
                    pass
                tok = ""
            elif tok in this.globalVariables and indentationNumber == 0 and state == 0:
                if type(this.globalVariables[tok][1] == str):
                    strings.append(this.globalVariables[tok][1])
                    lastValue = currentValue
                    currentValue = this.globalVariables[tok][1]
                    givenDataType = this.globalVariables[tok][0]
                    try:
                        if lookingForParams == True:
                            parametersForClass.append(currentValue)
                    except Exception:
                        pass
                elif type(this.globalVariables[tok][1] == bool):
                    bools.append(this.globalVariables[tok][1])
                    lastValue = currentValue
                    currentValue = this.globalVariables[tok][1]
                    givenDataType = this.globalVariables[tok][0]
                    try:
                        if lookingForParams == True:
                            parametersForClass.append(currentValue)
                    except Exception:
                        pass
                elif type(this.globalVariables[tok][1] == float):
                    numbers.append(this.globalVariables[tok][1])
                    lastValue = currentValue
                    currentValue = this.globalVariables[tok][1]
                    givenDataType = this.globalVariables[tok][0]
                    try:
                        if lookingForParams == True:
                            parametersForClass.append(currentValue)
                    except Exception:
                        pass
                if command == "assign" or command == "compare":
                    tok = ""
            elif char == "[" and state == 0 and indentationNumber == 0:
                if parametersForClass is None:
                    parametersForClass = []
                    lookingForParams = True
                tok = ""
            elif char == "]" and state == 0 and indentationNumber == 0:
                if type(parametersForClass) is list:
                    lookingForParams = False
                    finalList = parametersForClass
                    givenDataType = "list"
                    lastValue = currentValue
                    currentValue = finalList
                    lists.append(currentValue)
                    parametersForClass = []
                    finalList = []
                    reservedLists.append(currentValue)
                tok = ""
            elif char == "{" and state == 0:
                if this.currentLoadedClass == this.fileNameSpace:
                    if command == "":
                        try:
                            this.globalClasses[heap[len(heap)-1]] = []
                            this.lastLoadedClass = this.currentLoadedClass
                            this.currentLoadedClass = heap[len(heap)-1]
                            this.classesVisited.append(heap[len(heap)-1])
                            indentationNumber += 1
                        except IndexError:
                            print("Unexpected token '{'")
                    elif command in this.BCC:
                        if this.indentationFormat == 0:
                            this.codeNum += 1
                            this.globalCommandList.append(command)
                            command = ""
                            indentationNumber += 1
                        this.indentationFormat += 1
                tok = ""
            elif char == "}" and state == 0:
                if this.indentationFormat >= 1:
                    this.indentationFormat -= 1
                if indentationNumber >= 1:
                    indentationNumber -= 1
                if this.classesVisited[-1] != this.fileNameSpace:
                    del this.classesVisited[-1]
                    this.lastLoadedClass = this.currentLoadedClass
                    this.currentLoadedClass = this.classesVisited[-1]
                tok = ""
            elif tok in this.dataTypes and state == 0 and indentationNumber == 0:
                expectedDataType = tok
                tok = ""
            elif tok in this.variableScopes and state == 0 and indentationNumber == 0:
                modifier = tok
                tok = ""
            elif tok == "$sysConsoleClr" or tok == "$sysConsoleClear":
                os.system("cls")
                tok = ""
            elif tok == "$sysDebugInfo" and state == 0 and indentationNumber == 0:
                if this.showDebugInfo == False:
                    this.showDebugInfo = True
                elif this.showDebugInfo == True:
                    this.showDebugInfo = False
                tok = ""
            elif tok == "$sysInnerCode" and state == 0 and indentationNumber == 0:
                print(this.globalClasses["Main"])
                tok = ""
            elif tok == "out" and state == 0 and indentationNumber == 0:
                command = "out"
                tok = ""
            elif tok == "run" and state == 0 and indentationNumber == 0:
                command = "scan"
                tok = ""
            elif tok == "read" and state == 0 and indentationNumber == 0:
                command = "read"
                tok = ""
            elif tok == "return" and state == 0 and indentationNumber == 0:
                command = "give"
                tok = ""
            elif givenDataType == "string" and char in this.stringOperators:
                innerStringValue = strings[-1]
                del strings[-1]
                if char == "+":
                    innerToken = ""
                    try:
                        newNextString = this.parse(src[charNumber+1:])
                        innerStringValue += newNextString
                        lastValue = currentValue
                        currentValue = innerStringValue
                        strings.append(innerStringValue)
                        extraString = True
                    except:
                        print("(TrailingOperationError) EOF Error: Found string operation '+' with no end...")
                elif char == "*":
                    try:
                        multiplyStringBy = this.parse(src[charNumber+1:])
                        mockUp = innerStringValue
                        innerStringValue = innerStringValue * int(multiplyStringBy)
                        lastValue = currentValue
                        currentValue = innerStringValue
                        strings.append(innerStringValue)
                        leftOverInt = True
                    except Exception as e:
                        print("(TrailingOperationError) EOF Error: found string operation '*' with no number to multiply by...")
                tok = ""
            elif (char == "\"" or char == "'") and (state == 0 or state == 1) and indentationNumber == 0:
                if state == 0:
                    state = 1
                    stringStarter = char
                elif state == 1 and char == stringStarter:
                    state = 0
                    string = string[:-1]
                    strings.append(string)
                    lastValue = currentValue
                    currentValue = string
                    givenDataType = "string"
                    stringStarter = ""
                    string = ""
                    try:
                        if lookingForParams == True:
                            del strings[-1]
                            parametersForClass.append(currentValue)
                    except Exception:
                        pass
                tok = ""
            elif tok == "input" and state == 0 and indentationNumber == 0:
                sysInput = input(">")
                strings.append(sysInput)
                lastValue = currentValue
                currentValue = sysInput
                try:
                    if lookingForParams == True:
                        del strings[-1]
                        parametersForClass.append(currentValue)
                except Exception:
                    pass
                tok = ""
            if (tok.title() == "True" or tok.title() == "Yes") and state == 0 and indentationNumber == 0:
                bools.append(True)
                lastValue = currentValue
                currentValue = True
                givenDataType = "boolean"
                isDataType = True
                try:
                    if lookingForParams == True:
                        del bools[-1]
                        parametersForClass.append(currentValue)
                except Exception:
                    pass
                tok = ""
            elif (tok.title() == "False" or tok.title() == "No") and state == 0 and indentationNumber == 0:
                bools.append(False)
                lastValue = currentValue
                currentValue = False
                givenDataType = "boolean"
                isDataType = True
                try:
                    if lookingForParams == True:
                        del bools[-1]
                        parametersForClass.append(currentValue)
                except Exception:
                     pass
                tok = ""
            elif (char == "=" and tok != "") and state == 0 and indentationNumber == 0:
                heap.append(tok[:-1])
                command = "assign"
                tok = ""
            elif (char == "=" and tok == "") and state == 0 and indentationNumber == 0:
                command = "assign"
                tok = ""
            elif tok == "is" and state == 0 and indentationNumber == 0:
                operation = "compare"
                tok = ""
            elif tok == "not" and state == 0 and indentationNumber == 0:
                operation = "unite"
                tok = ""
            elif tok == "if" and state == 0 and indentationNumber == 0:
                command = "if"
                tok = ""
            elif (char == " " and (tok != "" or tok != " " or tok != "\t")) and state == 0 and indentationNumber == 0:
                try:
                    numbers.append(float(tok))
                    lastValue = currentValue
                    currentValue = float(tok)
                    givenDataType = "number"
                    isDataType = True
                except Exception:
                    pass
                # try:
                #     pass
                # except Exception:
                #     pass
                if isDataType == False:
                    heap.append(tok[0:-1])
                isDataType = False
                tok = ""
            heap = list(filter(lambda a: a != "", heap))
            heap = list(filter(lambda a: a != "=", heap))
            heap = list(filter(lambda a: a != "True", heap))
            heap = list(filter(lambda a: a != "False", heap))
            for scope in this.variableScopes:
                heap = list(filter(lambda a: a != scope, heap))
            charNumber += 1
        if extraString == True:
            del strings[-1]
            currentValue = strings[-1]
            extraString = False
        if leftOverInt == True:
            del numbers[-1]
            middleman = currentValue
            currentValue = lastValue
            lastValue = middleman
            leftOverInt = False
        if operation == "compare":
            if lastValue == currentValue:
                bools.append(True)
                lastValue = currentValue
                currentValue = True
            else:
                bools.append(False)
                lastValue = currentValue
                currentValue = False
            operation = ""
        if operation == "unite":
            if lastValue != currentValue:
                bools.append(True)
                lastValue = currentValue
                currentValue = True
            else:
                bools.append(False)
                lastValue = currentValue
                currentValue = False
            operation = ""
        if command == "assign":
            if expectedDataType == "string" and givenDataType != "string":
                givenDataType = "string"
                currentValue = str(currentValue)
            elif expectedDataType == "boolean" and givenDataType == "number":
                givenDataType = "boolean"
                if currentValue > 0:
                    currentValue = True
                else:
                    currentValue = False
            elif expectedDataType == "number" and givenDataType == "string":
                try:
                    currentValue = float(currentValue)
                    givenDataType = "number"
                except ValueError:
                    print("The string given could not be parsed as a number.")
            if (givenDataType == expectedDataType) or (expectedDataType == "none" or expectedDataType == "any" or expectedDataType == "dynamic"):
                displayedType = "dynamic"
                try:
                    if (expectedDataType == "" or expectedDataType == "none" or expectedDataType == "dynamic" or (expectedDataType not in this.dataTypes)):
                        expectedDataType = "any"
                    if expectedDataType == "any":
                        displayedType = givenDataType
                    else:
                        displayedType = expectedDataType
                    if modifier == "global" or modifier == "":
                        this.globalVariables[heap[len(heap)-1]] = [displayedType,currentValue]
                except IndexError:
                    pass
            else:
                print("Error: the given datatype '"+givenDataType+"' could not be converted to type '"+expectedDataType+"'.")
            command = ""
        elif command == "if":
            if currentValue == True:
                if blockRun == False:
                    blockRun = True
                    try:
                        for code in this.loadedBlock[0]:
                            this.parse(code)
                        this.codeNum = -1
                    except RecursionError:
                        pass
                    except IndexError:
                        print("No code given for statement 'if' or statement 'while'.")
                this.loadedBlock = []
        elif command == "scan":
            try:
                fileToRun = heap[-1]
                f = open(fileToRun,"r")
                for item in f.readlines():
                    Lang.parse(item)
            except IndexError:
                print("No arguement was given for the file name.")
            except FileNotFoundError:
                print("The file specified does not exist, or is not readable from the current path.")
            except Exception:
                pass
        elif command == "read":
            try:
                fileToRun = heap[-1]
                f = open(fileToRun,"r")
                for item in f.readlines():
                    print(item)
            except IndexError:
                print("No arguement was given for the file name.")
            except FileNotFoundError:
                print("The file specified does not exist, or is not readable from the current path.")
            except Exception:
                pass
        elif command == "fileID":
            try:
                oldName = this.fileNameSpace
                this.fileNameSpace = heap[-1]
                this.classesVisited[0] = this.fileNameSpace
                this.lastLoadedClass = this.currentLoadedClass
                this.currentLoadedClass = this.fileNameSpace
                this.globalClasses[this.fileNameSpace] = this.globalClasses[oldName]
                this.globalClasses.pop(oldName)
            except IndexError:
                print("No name given -> the namespace could not be changed.")
        elif command == "give":
            retVl = ""
            if type(currentValue) is str:
                retVl = "\""+str(currentValue)+"\""
            else:
                retVl = str(currentValue)
            this.thisReturnVariable = retVl
        if this.showDebugInfo == True:
            print("EXPECTED DATA TYPE: "+expectedDataType)
            print("GIVEN DATA TYPE: "+givenDataType)
            print("GLOBAL VARIABLES: "+str(this.globalVariables))
            print("EXE: "+str(this.globalClasses[this.fileNameSpace][2:]))
            print("EXE_NAME: "+str(this.fileNameSpace))
            print("(THIS) CLASS: "+this.currentLoadedClass)
            print("COMMAND: "+command)
            print("OPERATION: "+operation)
            print("MODIFIER: "+modifier)
            print("HEAP: "+str(heap))
            print("STRINGS: "+str(strings))
            print("NUMBERS: "+str(numbers))
            print("BOOLEANS: "+str(bools))
            print("LISTS: "+str(lists))
        lex(command,strings,numbers,bools,lists)
        return currentValue
def lex(code,strs,nums,bols,lsts):
    if code == "out":
        for stri in strs:
            print(stri)
        for numbs in nums:
            print(numbs)
        for booln in bols:
            print(booln)
        for listt in lsts:
            print(str(listt))
programming()