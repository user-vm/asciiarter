# -*- coding: utf-8 -*-
import Tkinter
import ttk
import tkMessageBox
import tkFileDialog
import pickle
import copy
import os
import random
import sys
from PIL import Image, ImageTk

root=Tkinter.Tk()

# color dictionaries

fgColorDict={"black":["#000000",0],
           "blue":["#0000aa",1],
           "green":["#00aa00",2],
            "cyan":["#00aaaa",3],
            "red":["#aa0000",4],
            "magenta":["#aa00aa",5],
            "brown":["#aa5500",6],
            "lightgray":["#aaaaaa",7],
            "darkgray":["#555555",8],
            "lightblue":["#5555ff",9],
            "lightgreen":["#55ff55",10],
            "lightcyan":["#55ffff",11],
            "lightred":["#ff5555",12],
            "lightmagenta":["#ff55ff",13],
            "yellow":["#ffff55",14],
            "white":["#ffffff",15]}

bgColorDict={"black":["#000000",0],
           "blue":["#0000aa",1],
           "green":["#00aa00",2],
            "cyan":["#00aaaa",3],
            "red":["#aa0000",4],
            "magenta":["#aa00aa",5],
            "brown":["#aa5500",6],
            "lightgray":["#aaaaaa",7]}

# classes

class gridPointClass:
    
    def __init__(self):
        self.x=0
        self.y=0

class pBrushClass:

    def __init__(self,letter=-1,fgColor=fgColorDict["white"],bgColor=bgColorDict["black"]):
        #if letter in [0,7,8,9,10,13,26,27,255]:
            #letter=32
        self.letter=letter
        self.fgColor=fgColor
        self.bgColor=bgColor

class undoInfoNormal:

    __name__ = "undoInfoNormal"

    def __init__(self,x,y,letter1,fgColor1,bgColor1,letter2,fgColor2,bgColor2):
        self.x=x
        self.y=y
        self.letter1=letter1
        self.fgColor1=fgColor1
        self.bgColor1=bgColor1
        self.letter2=letter2
        self.fgColor2=fgColor2
        self.bgColor2=bgColor2

    def getAll(self):
        print self.x, self.y, self.letter1, self.fgColor1, self.bgColor1, self.letter2, self.fgColor2, self.bgColor2

class undoInfoDelete:

    def __init__(self,frameMatrix):
        self.frameMatrix = frameMatrix

class undoInfoCut:

    def __init__(self,x,y,letter1,fgColor1,bgColor1,letter2,fgColor2,bgColor2):
        self.x=x
        self.y=y
        self.letter1=letter1
        self.fgColor1=fgColor1
        self.bgColor1=bgColor1
        self.letter2=letter2
        self.fgColor2=fgColor2
        self.bgColor2=bgColor2

    def getAll(self):
        print self.x, self.y, self.letter1, self.fgColor1, self.bgColor1, self.letter2, self.fgColor2, self.bgColor2

class undoInfoCopy:

    def __init__(self, x, y):

        self.x = x
        self.y = y

    def getAll(self):
        print self.x, self.y

class undoInfoAnchor:

    def __init__(self,x,y,letter1,fgColor1,bgColor1,letter2,fgColor2,bgColor2):
        self.x=x
        self.y=y
        self.letter1=letter1
        self.fgColor1=fgColor1
        self.bgColor1=bgColor1
        self.letter2=letter2
        self.fgColor2=fgColor2
        self.bgColor2=bgColor2

    def getAll(self):
        print self.x, self.y, self.letter1, self.fgColor1, self.bgColor1, self.letter2, self.fgColor2, self.bgColor2

class undoInfoPaste:

    def __init__(self):
        self = self

class undoInfoDragSelection:

    def __init__(self, x1, y1, x2, y2):

        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

class undoInfoInsertImage:

    def __init__(self, filename):

        self.filename = filename

class undoInfoInsertImageSequence:

    def __init__(self, imageList, firstFrame):

        self.imageList = imageList
        self.firstFrame = firstFrame

class FloatMatrix:

    def __init__(self):
        self.data = []
        self.x = 0
        self.y = 0
        self.visible = False
        self.beingDragged = False
        self.isPasted = True

# variables and lists

currentFrame = 0
undo_step = []
texts=[]
rects=[]
letters=[]
images=[]
rectsPalette=[]
rectsBg=[]
rectsFg=[]
i_offset=5
j_offset=5
i_offset_p=2
j_offset_p=2
data_matrix=[[]]
frameRects = []

picDict = {}
showImages = False
imagesFront = True

select_matrix = []
subSelection = []
selectedNumber = 0
subSelectedNumber =  0
isDraggingSelection = False

undo_sequence=[]
undoOperations = 100
undo_pos = 0
dragWait = False
enableFrameChange = True

timelineSelectedFrame = -1

isSaved = True

float_matrix = FloatMatrix()

frameNumber = Tkinter.StringVar()
useCurrentFrame = Tkinter.IntVar()

origSelGridPoint = gridPointClass()

fileList = []

askWindow = None
traceType = None
enterChars = None
traceChars = None
askTraceWindow = None
askFindReplaceWindow = None

exportAllFrames = None
lfString = None
ffString = None
lfEntry = None
ffEntry = None
offsetString = None
offsetEntry = None
lastExportDirectory = None
lastOffset = 0
exportDirectoryString = None

exportFileString = None

traceColors = None
bgColorType = None
fgColorType = None
bgColorEntry = None
fgColorEntry = None
traceFGColors = None
traceBGColors = None

firstEntry = None
lastEntry = None
firstFrame = None
lastFrame = None
traceFrames = None

blockMain = False

askMergeWindow = None
mergeType = None
firstFileEntry = None
firstFileFramesType = None
firstFileFirstFrame = None
firstFileLastFrame = None
firstFileFirstFrameEntry = None
firstFileLastFrameEntry = None
firstFile = None
secondFileFramesType = None
secondFileFirstFrame = None
secondFileLastFrame = None
secondFileFirstFrameEntry = None
secondFileLastFrameEntry = None
secondFile = None
secondFileOffsetEntry = None
secondFileOffset = None
outputFile = None

unprintable = [0,7,8,9,10,13,26,27,255]

#find and replace
anyChar = Tkinter.IntVar()
anyFg = Tkinter.IntVar()
anyBg = Tkinter.IntVar()
findScope = Tkinter.StringVar()
doReplace = Tkinter.IntVar()

anyChar.set(0)
anyFg.set(0)
anyBg.set(0)
findScope.set("SELECTION")
doReplace.set(1);



# miscellanous functions

def colorInvert(colorString):
    invColorString="#"+(hex(0xFFFFFF-int(colorString[1:],16)))[2:]
    return invColorString

gridPoint = gridPointClass()
pBrush = pBrushClass()

# functions for canvas drawing

# BOTH CLICK AND DRAG ACTIVATE ONE AFTER EACH OTHER BEFORE RELEASE

def onClick(click):

    if blockMain:

        return
    
    global float_matrix, gridPoint, pBrush, undo_sequence, data_matrix, undo_step, undo_pos, isSaved, dragWait, currentFrame
    global mainCanvas, i_offset, j_offset
    global selectedNumber, select_matrix, mainCanvas

    #print "Click"

    x=(click.x-i_offset)/8
    y=(click.y-j_offset)/8

    if x < 0 or y < 0 or x >= 80 or y >= 50:

        return

    gridPoint.x = x
    gridPoint.y = y

    if selectedNumber > 0:
            
        if select_matrix[y][x] == None:

            toggleFrameChange(True)

            if float_matrix.isPasted:

                anchorFloat()
                float_matrix.visible = False
                float_matrix.isPasted = False
            
            selectedNumber = 0
            for i in range(50):
                for j in range(80):
                    mainCanvas.delete(select_matrix[i][j])
                    select_matrix[i][j] = None
            dragWait = True

        else:

            #FIX THIS
            
            if len(float_matrix.data):
                float_matrix.beingDragged = True
                undo_step = [undoInfoDragSelection(float_matrix.x, float_matrix.y, float_matrix.x, float_matrix.y)]
                #print "LOLZORZ"
            
        return

    if pBrush.letter == -1:
        return

    if pBrush.letter in [0,7,8,9,10,13,26,27,255]:
        letter=32
    else:
        letter=pBrush.letter
    
    if data_matrix[currentFrame][gridPoint.y][gridPoint.x]!=(letter,pBrush.fgColor[1],pBrush.bgColor[1]):
        isSaved = False
        if undo_pos!=len(undo_sequence):
            del undo_sequence[undo_pos:]
        undo_step = [undoInfoNormal(gridPoint.x, gridPoint.y, data_matrix[currentFrame][gridPoint.y][gridPoint.x][0], data_matrix[currentFrame][gridPoint.y][gridPoint.x][1], data_matrix[currentFrame][gridPoint.y][gridPoint.x][2], letter, pBrush.fgColor[1], pBrush.bgColor[1])]
        #print vars(undo_step[len(undo_step)-1])
        data_matrix[currentFrame][gridPoint.y][gridPoint.x]=(letter,pBrush.fgColor[1],pBrush.bgColor[1])
        mainCanvas.itemconfig(texts[gridPoint.x+(gridPoint.y)*80],image=letters[256*pBrush.fgColor[1]+letter])
        mainCanvas.itemconfig(rects[gridPoint.x+(gridPoint.y)*80],fill=pBrush.bgColor[0])
    
def onDrag(click):

    if blockMain:

        return
    
    global float_matrix, gridPoint, pBrush, undo_step, undo_sequence, data_matrix, undo_pos, isSaved, dragWait
    global mainCanvas, i_offset, j_offset

    #print "Drag"

    if selectedNumber > 0 and float_matrix.beingDragged == False:
        return

    if dragWait:
        return
    
    if pBrush.letter in [0,7,8,9,10,13,26,27,255]:
        letter=32
    else:
        letter=pBrush.letter
    
    if(click.x/8!=gridPoint.x or click.y/8!=gridPoint.y):

        x = gridPoint.x
        y = gridPoint.y

        if x < 0 or y < 0 or x >= 80 or y >= 50:

            return

        gridPoint.x=(click.x-i_offset)/8
        gridPoint.y=(click.y-j_offset)/8

        #print float_matrix.beingDragged

        if float_matrix.beingDragged == True:

            #print "LOLZ"

            if(gridPoint.x == x and gridPoint.y == y):

                return

            float_matrix.x += gridPoint.x - x
            float_matrix.y += gridPoint.y - y

            clearSelection()
            
            selectionToFloat()

            repaint()

            #print "LOLZ"

            return

        if pBrush.letter == -1:

            return
        
        if data_matrix[currentFrame][gridPoint.y][gridPoint.x]!=(letter,pBrush.fgColor[1],pBrush.bgColor[1]):
            isSaved = False
            if undo_pos!=len(undo_sequence):
                del undo_sequence[undo_pos:]
            undo_step += [undoInfoNormal(gridPoint.x, gridPoint.y, data_matrix[currentFrame][gridPoint.y][gridPoint.x][0], data_matrix[currentFrame][gridPoint.y][gridPoint.x][1], data_matrix[currentFrame][gridPoint.y][gridPoint.x][2], letter, pBrush.fgColor[1], pBrush.bgColor[1])]
            data_matrix[currentFrame][gridPoint.y][gridPoint.x]=(letter,pBrush.fgColor[1],pBrush.bgColor[1])
            mainCanvas.itemconfig(texts[gridPoint.x+(gridPoint.y)*80],image=letters[256*pBrush.fgColor[1]+letter])    
            mainCanvas.itemconfig(rects[gridPoint.x+(gridPoint.y)*80],fill=pBrush.bgColor[0])

def onRelease(click):

    if blockMain:

        return

    global undo_sequence, undo_step, currentFrame, undo_pos, undoOperations, dragWait
    #print "release"

    if(float_matrix.beingDragged):

        float_matrix.beingDragged = False

        if (len(undo_step) and (undo_step[0].x1 != undo_step[0].x2 or undo_step[0].y1 != undo_step[0].y2)):

            undo_sequence += [[currentFrame, undo_step]]
            if len(undo_sequence)>undoOperations:
                del undo_sequence[:undoOperations-len(undo_sequence)]
            else:
                undo_pos += 1
            undo_step = []

    if len(undo_step):
        undo_sequence += [[currentFrame, undo_step]]
        if len(undo_sequence)>undoOperations:
            del undo_sequence[:undoOperations-len(undo_sequence)]
        else:
            undo_pos += 1
        undo_step = []

    dragWait = False

def onEnter(event):

    global nextFrameButton, data_matrix
    global currentFrameString, currentFrame

    if (not blockMain) and currentFrameString.get().isdigit() and int(currentFrameString.get()) < len(data_matrix):

        currentFrame = int(currentFrameString.get())
        repaint()

    else:

        currentFrameString.set(str(currentFrame))

    nextFrameButton.focus_set()
        
def onSelect(click):

    if blockMain:

        return
    
    global float_matrix, gridPoint, pBrush, undo_sequence, data_matrix, undo_step, undo_pos, isSaved, enableFrameChange
    global mainCanvas, i_offset, j_offset
    global selectedNumber

    if not(enableFrameChange):
        return

    gridPoint.x=(click.x-i_offset)/8
    gridPoint.y=(click.y-j_offset)/8

    if gridPoint.x < 0 or gridPoint.x >= 80 or gridPoint.y < 0 or gridPoint.y >= 50:

        return
    
    if select_matrix[gridPoint.y][gridPoint.x]!=None:
        mainCanvas.delete(select_matrix[gridPoint.y][gridPoint.x])
        select_matrix[gridPoint.y][gridPoint.x] = None
        selectedNumber -= 1
    else:
        select_matrix[gridPoint.y][gridPoint.x]=mainCanvas.create_rectangle(gridPoint.x*8+j_offset_p+2,gridPoint.y*8+i_offset_p+2,gridPoint.x*8+j_offset_p+10,gridPoint.y*8+i_offset_p+10,width=1,outline="red")
        selectedNumber += 1

def onSelectDrag(click):

    if blockMain:

        return
    
    global float_matrix, gridPoint, pBrush, undo_sequence, data_matrix, undo_step, undo_pos, isSaved, enableFrameChange
    global mainCanvas, i_offset, j_offset, subSelection, i_offset_p, j_offset_p
    global subSelectedNumber, isDraggingSelection

    if not(enableFrameChange):
        return

    if gridPoint.x==(click.x-i_offset)/8 and gridPoint.y==(click.y-j_offset)/8:
        return

    x = (click.x-i_offset)/8
    y = (click.y-j_offset)/8

    if x < 0 or y < 0 or x >= 80 or y >= 50:
        return

    if isDraggingSelection == False:

        isDraggingSelection = True
        for i in range(50):
            subSelection += [[]]
            for j in range(80):
                subSelection[i] += [None]
        subSelectedNumber = 0
        origSelGridPoint.x = gridPoint.x
        origSelGridPoint.y = gridPoint.y

    gridPoint.x = x
    gridPoint.y = y

    clearSubSelection()

    if gridPoint.x > origSelGridPoint.x:

        xDir = 1

    else:

        xDir = -1

    if gridPoint.y > origSelGridPoint.y:

        yDir = 1

    else:

        yDir = -1

    for i in range(abs(gridPoint.x-origSelGridPoint.x)+1):
        for j in range(abs(gridPoint.y-origSelGridPoint.y)+1):

            subSelection[origSelGridPoint.y+yDir*j][origSelGridPoint.x+xDir*i]=mainCanvas.create_rectangle((origSelGridPoint.x+xDir*i)*8+j_offset_p+2,(origSelGridPoint.y+yDir*j)*8+i_offset_p+2,(origSelGridPoint.x+xDir*i)*8+j_offset_p+10,(origSelGridPoint.y+yDir*j)*8+i_offset_p+10,width=1,outline="red")
            subSelectedNumber += 1
            #print i,j,

    #print "end"

def onSelectRelease(click):

    if blockMain:

        return

    global subSelectedNumber, subSelection, select_matrix, selectedNumber, isDraggingSelection, j_offset_p, i_offset_p, mainCanvas

    isDraggingSelection = False

    if subSelectedNumber == 0:
        return

    for i in range(50):
        for j in range(80):

            if subSelection[i][j] != None:
                if select_matrix[i][j] == None:
                    select_matrix[i][j] = subSelection[i][j]
                    selectedNumber += 1
                else:
                    mainCanvas.delete(subSelection[i][j])
                    
                subSelection[i][j] = None

def clearSelection():

    global select_matrix, selectedNumber, mainCanvas

    for i in range(50):
        for j in range(80):

            if selectedNumber == 0:
                break
            
            if select_matrix[i][j] != None:

                mainCanvas.delete(select_matrix[i][j])
                select_matrix[i][j] = None
                selectedNumber -= 1

        if selectedNumber == 0:
            break

def clearSubSelection():

    global subSelection, subSelectedNumber, mainCanvas

    for i in range(50):
        for j in range(80):

            if subSelectedNumber == 0:
                break
            
            if subSelection[i][j] != None:

                mainCanvas.delete(subSelection[i][j])
                subSelection[i][j] = None
                subSelectedNumber -= 1

        if subSelectedNumber == 0:
            break

def onClickLetter(click):  #letter select
    global gridPoint,pBrush
    global paletteCanvas,i_offset_p,j_offset_p,palette_select_bg
    global data_matrix, mainCanvas, rects, texts, letters, currentFrame, bgColorDict, select_matrix, selectedNumber
    gridPoint.x=(click.x-i_offset_p)/10
    gridPoint.y=(click.y-j_offset_p)/10
    pBrush.letter = gridPoint.x + 8*gridPoint.y
    if pBrush.letter in [0,7,8,9,10,13,26,27,255]:
        pBrush.letter=32
    if selectedNumber > 0:
        for i in range(50):
            for j in range(80):
                if select_matrix[i][j]!=None:
                    data_matrix[currentFrame][i][j] = (pBrush.letter,pBrush.fgColor[1],data_matrix[currentFrame][i][j][2])
                    mainCanvas.itemconfig(texts[j+i*80],image=letters[256*pBrush.fgColor[1]+pBrush.letter])
    #print pBrush.letter
    paletteCanvas.coords(palette_select_bg, pBrush.letter%8*10+i_offset_p+1, pBrush.letter/8*10+j_offset_p+1, pBrush.letter%8*10+10+i_offset_p+1,pBrush.letter/8*10+10+j_offset_p+1)

def onClickBg(click): #background color select
    global gridPoint,pBrush
    global bgCanvas,bgColor_select_bg,bgcolors
    global data_matrix, mainCanvas, rects, texts, letters, currentFrame, bgColorDict, select_matrix, selectedNumber
    gridPoint.x=(click.x)/10
    pBrush.bgColor = bgColorDict[bgcolors[gridPoint.x]]
    if selectedNumber > 0:
        for i in range(50):
            for j in range(80):
                if select_matrix[i][j]!=None:
                    data_matrix[currentFrame][i][j] = (data_matrix[currentFrame][i][j][0],data_matrix[currentFrame][i][j][1],pBrush.bgColor[1])
                    mainCanvas.itemconfig(rects[j+i*80],fill=bgColorDict[bgcolors[data_matrix[currentFrame][i][j][2]]][0],width=0)
    bgCanvas.coords(bgColor_select_bg, gridPoint.x*10+3, 3, gridPoint.x*10+12, 12)

def onClickFg(click): #foreground color select
    global gridPoint,pBrush
    global fgCanvas,fgColor_select_bg,fgcolors
    global data_matrix, mainCanvas, rects, texts, letters, currentFrame, fgColorDict, select_matrix, selectedNumber
    gridPoint.x = (click.x)/10
    gridPoint.y = (click.y)/10
    pBrush.fgColor = fgColorDict[fgcolors[gridPoint.y*8+gridPoint.x]]
    if selectedNumber > 0:
        for i in range(50):
            for j in range(80):
                if select_matrix[i][j]!=None:
                    data_matrix[currentFrame][i][j] = (data_matrix[currentFrame][i][j][0],pBrush.fgColor[1],data_matrix[currentFrame][i][j][2])
                    mainCanvas.itemconfig(texts[j+i*80],image=letters[256*pBrush.fgColor[1]+data_matrix[currentFrame][i][j][0]])
    fgCanvas.coords(fgColor_select_bg, gridPoint.x*10+3, gridPoint.y*10+3, gridPoint.x*10+12, gridPoint.y*10+12)

# button and menu functions

def undo():
    global undo_sequence, undo_pos, data_matrix, currentFrame, bgcolors, bgColorDict, texts, rects, isSaved, currentFrameString, float_matrix
    global mainCanvas
    if undo_pos>0:
        isSaved = False
        undo_pos-=1
        thisFrame = currentFrame

        try:
            currentFrame = undo_sequence[undo_pos][0]

        except:

            print undo_pos, len(undo_sequence)
            return
        
        toggleFrameChange(True)
        
        if isinstance(undo_sequence[undo_pos][1][0], undoInfoNormal):

            if thisFrame == currentFrame:
            
                for undoOperationPart in undo_sequence[undo_pos][1]:
                
                    data_matrix[currentFrame][undoOperationPart.y][undoOperationPart.x] = (undoOperationPart.letter1,undoOperationPart.fgColor1,undoOperationPart.bgColor1)
                    mainCanvas.itemconfig(texts[undoOperationPart.x+(undoOperationPart.y)*80],image=letters[256*undoOperationPart.fgColor1+undoOperationPart.letter1])    
                    mainCanvas.itemconfig(rects[undoOperationPart.x+(undoOperationPart.y)*80],fill=bgColorDict[bgcolors[undoOperationPart.bgColor1]][0])
                
            else:

                for undoOperationPart in undo_sequence[undo_pos][1]:
                
                    data_matrix[currentFrame][undoOperationPart.y][undoOperationPart.x] = (undoOperationPart.letter1,undoOperationPart.fgColor1,undoOperationPart.bgColor1)
                
                repaint()
        
        else:

            # CUT

            if isinstance(undo_sequence[undo_pos][1][0], undoInfoCut):

                clearSelection()

                selectionToFloat()
                
                anchorFloatNoUndo()

                if thisFrame != currentFrame:

                    repaint()

            else:

                # COPY

                if isinstance(undo_sequence[undo_pos][1][0], undoInfoCopy):

                    clearSelection()

                    selectionToFloat()

                    if thisFrame != currentFrame:

                        repaint()

                else:

                    # ANCHOR

                    if isinstance(undo_sequence[undo_pos][1][0], undoInfoAnchor):

                        toggleFrameChange(False)

                        float_matrix.x = undo_sequence[undo_pos][2]
                        float_matrix.y = undo_sequence[undo_pos][3]
                        del float_matrix.data[:]

                        if thisFrame == currentFrame:
            
                            for undoOperationPart in undo_sequence[undo_pos][1]:

                                float_matrix.data += [(undoOperationPart.x, undoOperationPart.y) + data_matrix[currentFrame][undoOperationPart.y + float_matrix.y][undoOperationPart.x + float_matrix.x]]
                                data_matrix[currentFrame][undoOperationPart.y + float_matrix.y][undoOperationPart.x + float_matrix.x] = (undoOperationPart.letter1,undoOperationPart.fgColor1,undoOperationPart.bgColor1)
                                #print undoOperationPart.x, undoOperationPart.y
                                #mainCanvas.itemconfig(rects[undoOperationPart.x+(undoOperationPart.y)*80],fill=bgColorDict[bgcolors[float_matrix.data[-1][4]]][0])
                                #mainCanvas.itemconfig(texts[undoOperationPart.x+(undoOperationPart.y)*80],image=letters[256*float_matrix.data[-1][3]+float_matrix.data[-1][2]])    
                                

                            #print float_matrix.data
                            #print float_matrix.x
                            #print float_matrix.y
                        else:

                            for undoOperationPart in undo_sequence[undo_pos][1]:

                                float_matrix.data += [(undoOperationPart.x, undoOperationPart.y) + data_matrix[currentFrame][undoOperationPart.y][undoOperationPart.x]]
                                data_matrix[currentFrame][undoOperationPart.y][undoOperationPart.x] = (undoOperationPart.letter1,undoOperationPart.fgColor1,undoOperationPart.bgColor1)
                
                            repaint()

                        clearSelection()

                        selectionToFloat()

                        float_matrix.visible = True

                        repaint()
            
                    else:

                        if isinstance(undo_sequence[undo_pos][1][0], undoInfoPaste):

                            #print "something"

                            toggleFrameChange(True)

                            float_matrix.visible = False
                            float_matrix.isPasted = False

                            clearSelection()

                            repaint()

                        else:

                            if isinstance(undo_sequence[undo_pos][1][0], undoInfoDragSelection):

                                toggleFrameChange(False)

                                float_matrix.x = undo_sequence[undo_pos][1][0].x1
                                float_matrix.y = undo_sequence[undo_pos][1][0].y1

                                clearSelection()

                                selectionToFloat()

                                repaint()

                            else:
                            
                                undoOperationPart = undo_sequence[undo_pos][1][0]
                                if isinstance(undoOperationPart, list):
                    
                                    data_matrix.pop(currentFrame)
                                    currentFrame-=1
                                    currentFrameString.set(str(currentFrame))
                    
                                else:

                                    data_matrix.insert(currentFrame,undoOperationPart.frameMatrix)
                                    currentFrame = undo_sequence[undo_pos][0]

                                repaint()

    currentFrameString.set(str(currentFrame))
            
def redo():
    global undo_sequence, undo_pos, data_matrix, currentFrame, bgcolors, bgColorDict, texts, rects, isSaved, currentFrameString, selectedNumber, select_matrix
    global mainCanvas
    if undo_pos<len(undo_sequence):
        isSaved = False
        #print undo_sequence[undo_pos][1]
        thisFrame = currentFrame
        currentFrame = undo_sequence[undo_pos][0]
        if isinstance(undo_sequence[undo_pos][1][0], undoInfoNormal):
            if thisFrame == currentFrame:
                for undoOperationPart in undo_sequence[undo_pos][1]:

                    data_matrix[currentFrame][undoOperationPart.y][undoOperationPart.x] = (undoOperationPart.letter2,undoOperationPart.fgColor2,undoOperationPart.bgColor2)
                    mainCanvas.itemconfig(texts[undoOperationPart.x+(undoOperationPart.y)*80],image=letters[256*undoOperationPart.fgColor2+undoOperationPart.letter2])
                    mainCanvas.itemconfig(rects[undoOperationPart.x+(undoOperationPart.y)*80],fill=bgColorDict[bgcolors[undoOperationPart.bgColor1]][0])

            else:

                for undoOperationPart in undo_sequence[undo_pos][1]:

                    data_matrix[currentFrame][undoOperationPart.y][undoOperationPart.x] = (undoOperationPart.letter2,undoOperationPart.fgColor2,undoOperationPart.bgColor2)

                repaint()
        else:

            if isinstance(undo_sequence[undo_pos][1][0], undoInfoCut):

                clearSelection()

                selectedNumber = 0

                #print undo_sequence[undo_pos][1]

                for undoOperationPart in undo_sequence[undo_pos][1]:

                    select_matrix[undoOperationPart.y][undoOperationPart.x]=mainCanvas.create_rectangle(undoOperationPart.x*8+j_offset_p+2,undoOperationPart.y*8+i_offset_p+2,undoOperationPart.x*8+j_offset_p+10,undoOperationPart.y*8+i_offset_p+10,width=1,outline="red")
                    selectedNumber += 1

                #print "redoCut"

                onCutNoUndo()

            else:

                if isinstance(undo_sequence[undo_pos][1][0], undoInfoCopy):

                    clearSelection()

                    selectedNumber = 0

                    for undoOperationPart in undo_sequence[undo_pos][1]:

                        select_matrix[undoOperationPart.y][undoOperationPart.x]=mainCanvas.create_rectangle(undoOperationPart.x*8+j_offset_p+2,undoOperationPart.y*8+i_offset_p+2,undoOperationPart.x*8+j_offset_p+10,undoOperationPart.y*8+i_offset_p+10,width=1,outline="red")
                        selectedNumber += 1

                    onCopyNoUndo()

                else:

                    if isinstance(undo_sequence[undo_pos][1][0], undoInfoAnchor):
                        
                        anchorFloatNoUndo()

                        clearSelection()

                    else:

                        if isinstance(undo_sequence[undo_pos][1][0], undoInfoPaste):

                            onPasteNoUndo()

                        else:
                    
                            undoOperationPart = undo_sequence[undo_pos][1][0]
                    
                            if isinstance(undoOperationPart, list):
                                newFrameMatrix = []
                                for j in range(50):
                                    newFrameMatrix += [[]]
                                    for i in range(80):
                                        newFrameMatrix[j] += [(32, fgColorDict["white"][1], bgColorDict["black"][1])]
                                data_matrix.insert(currentFrame, newFrameMatrix)

                            else:
                
                                data_matrix.pop(currentFrame)
                                if currentFrame >= len(data_matrix):
                                    currentFrame = len(data_matrix) - 1;

                            repaint()
            
        undo_pos+=1
        currentFrameString.set(currentFrame)

def newFile():
    
    global isSaved, data_matrix, currentFrame, undo_pos, undo_step, undo_sequence, rects, texts, spacecopy, currentFrameString
    global pBrush, mainCanvas, fgColorDict, bgColorDict, paletteCanvas, fgCanvas, bgCanvas
    
    if not(isSaved):
        doSave = tkMessageBox.askquestion("File not saved", "Save?", type = tkMessageBox.YESNOCANCEL, parent = root)
        if doSave == "cancel":
            return
        if doSave == "yes":
            saveFile()

    currentFrame = 0

    currentFrameString.set("0")
    
    undo_pos = 0
    undo_step = []
    undo_sequence = []

    pBrush.fgColor = fgColorDict["white"]
    pBrush.bgColor = bgColorDict["black"]
    pBrush.letter = -1;

    clearSelection()

    del data_matrix[1:]
    
    for j in range(50):
        for i in range(80):
    
            mainCanvas.itemconfig(rects[i+j*80],fill="#000000",width=0)
            mainCanvas.itemconfig(texts[i+j*80],image=spacecopy)
            data_matrix[0][j][i] = (32, pBrush.fgColor[1], pBrush.bgColor[1])

    paletteCanvas.coords(palette_select_bg, -10,-10,-5,-5)
    fgCanvas.coords(fgColor_select_bg, 3, 3, 12, 12)
    bgCanvas.coords(bgColor_select_bg, 3, 3, 12, 12)

def openFile():
    global isSaved, data_matrix, currentFrame, undo_pos, undo_step, undo_sequence, rects, texts, picDict, currentFrameString
    global fgColorDict, bgColorDict, pBrush, mainCanvas, paletteCanvas, fgCanvas, bgCanvas
    
    if not(isSaved):
        doSave = tkMessageBox.askquestion("File not saved", "Save?", type = tkMessageBox.YESNOCANCEL, parent = root)
        if doSave == "cancel":
            return
        if doSave == "yes":
            saveFile()
    openOptions = {}
    openOptions["parent"] = root
    openOptions["filetypes"] = [("Ascii data", ".asc")]
    openFileName = tkFileDialog.askopenfilename(**openOptions)
    if openFileName == "":
        return
    if openFileName[-4:].lower()!=".asc":
        return

    clearSelection()
    
    inFile = open(openFileName, "rb")
    data_matrix = [[]]
    numFrames = 0
    thisFrame = inFile.read(8000)
    while len(thisFrame)==8000:
            
        for j in range(50):
            data_matrix[numFrames] += [[]]
            for i in range(80):
                data_matrix[numFrames][j] += [((ord)(thisFrame[2*(j*80+i)+1]), (ord)(thisFrame[2*(j*80+i)])/8, (ord)(thisFrame[2*(j*80+i)])%8)]
        thisFrame = inFile.read(8000)
        if len(thisFrame)==8000:
            data_matrix += [[]]
            numFrames += 1

    inFile.close()
    currentFrame = 0
    currentFrameString.set("0")
    undo_pos = 0
    undo_step = []
    undo_sequence = []

    pBrush.fgColor = fgColorDict["white"]
    pBrush.bgColor = bgColorDict["black"]
    pBrush.letter = -1;
    
    for j in range(50):
        for i in range(80):
            
            mainCanvas.itemconfig(rects[i+j*80],fill=bgColorDict[bgcolors[data_matrix[0][j][i][2]]][0],width=0)
            mainCanvas.itemconfig(texts[i+j*80],image=letters[256*data_matrix[0][j][i][1]+data_matrix[0][j][i][0]])

    paletteCanvas.coords(palette_select_bg, -10,-10,-5,-5)
    fgCanvas.coords(fgColor_select_bg, 3, 3, 12, 12)
    bgCanvas.coords(bgColor_select_bg, 3, 3, 12, 12)

    clearPicDict()

def saveFile():
    global root, data_matrix, isSaved
    fileOptions = {}
    fileOptions["parent"] = root
    fileOptions["filetypes"] = [("Ascii data", ".asc")]
    filename = tkFileDialog.asksaveasfilename(**fileOptions)
    if filename=="":
        return
    
    if filename[-4:]!=".asc":
        filename+=".asc"
    
    outFile = open(filename, "wb")
    letterList = []
    #print data_matrix
    for frame in range(len(data_matrix)):
        for j in range(50):
            for i in range(80):
                if data_matrix[frame][j][i][0] in [0,7,8,9,10,13,26,27,255]:
                    data_matrix[frame][j][i] = (32,data_matrix[frame][j][i][1],data_matrix[frame][j][i][2])
                letterList += [data_matrix[frame][j][i][1]*8 + data_matrix[frame][j][i][2], data_matrix[frame][j][i][0]]
    #print letterList
    outFile.write(bytearray(letterList))
    outFile.close()

    isSaved = True

def repaint():
    global float_matrix, currentFrame, data_matrix, rects, texts, bgColorDict, bgcolors, letters, picDict, showImages, mainCanvas, imagesFront, currentFrameString
    #print currentFrame
    #print len(data_matrix)

    for j in range(50):
        for i in range(80):
            mainCanvas.itemconfig(rects[i+j*80],fill=bgColorDict[bgcolors[data_matrix[currentFrame][j][i][2]]][0],width=0)
            mainCanvas.itemconfig(texts[i+j*80],image=letters[256*data_matrix[currentFrame][j][i][1]+data_matrix[currentFrame][j][i][0]])

    for i in picDict.values():

        mainCanvas.itemconfig(i[1], state = Tkinter.HIDDEN)

    if showImages and (str(currentFrame) in picDict.keys()):

        mainCanvas.itemconfig(picDict[str(currentFrame)][1], state = Tkinter.NORMAL)

        if imagesFront:

            mainCanvas.tag_raise(picDict[str(currentFrame)][1])

        else:

            for j in range(50):
                for i in range(80):

                    mainCanvas.tag_raise(texts[i+j*80])
        
    if float_matrix.visible == True:
        
        for i in float_matrix.data:

            x = i[0] + float_matrix.x
            y = i[1] + float_matrix.y

            if x < 0 or y < 0 or x >= 80 or y >= 50:

                continue
            
            v1 = i[2]
            v2 = i[3]
            v3 = i[4]

            mainCanvas.itemconfig(rects[x+y*80],fill=bgColorDict[bgcolors[v3]][0],width=0)
            mainCanvas.itemconfig(texts[x+y*80],image=letters[256*v2+v1])

    currentFrameString.set(str(currentFrame))

    #print float_matrix.data
    #print float_matrix.x, float_matrix.y
    #print "repaint"
    
def gotoFirstFrame():
    global currentFrameString, currentFrame
    if currentFrame!=0:
        currentFrameString.set("0")
        currentFrame = 0
        repaint()

def gotoPrevFrame():
    global currentFrameString, currentFrame
    if currentFrame!=0:
        currentFrame -= 1
        currentFrameString.set(str(currentFrame))
        repaint()

def gotoNextFrame():
    global currentFrameString, data_matrix, currentFrame
    if currentFrame!=len(data_matrix)-1:
        currentFrameString.set(str(currentFrame+1))
        currentFrame += 1
        repaint()

def insertFrame():
    global currentFrame, data_matrix, undo_sequence, undo_step, currentFrameString, undo_pos
    undo_step = [[]]
    undo_sequence += [[currentFrame+1, undo_step]]
    undo_pos += 1
    newFrameMatrix = []
    for j in range(50):
        newFrameMatrix += [[]]
        for i in range(80):
            newFrameMatrix[j] += [(32, fgColorDict["white"][1], bgColorDict["black"][1])]
    data_matrix.insert(currentFrame+1, newFrameMatrix)
    currentFrame+=1
    currentFrameString.set(str(currentFrame))
    repaint()

def deleteFrame():
    global currentFrame, data_matrix, undo_sequence, undo_step, currentFrameString, undo_pos

    if len(data_matrix) == 1:

        return

    undo_step = [undoInfoDelete(data_matrix.pop(currentFrame))]
    undo_sequence += [[currentFrame, undo_step]]
    undo_pos += 1

    if currentFrame >= len(data_matrix):
        currentFrame = len(data_matrix) - 1;
        currentFrameString.set(str(currentFrame))
 
    repaint()

def gotoLastFrame():
    global currentFrameString, currentFrame
    if currentFrame!=len(data_matrix)-1:
        currentFrameString.set(str(len(data_matrix)-1))
        currentFrame = len(data_matrix)-1
        repaint()

def showFramePopup(event):
    global framePopup, frameSelectRect
    framePopup.post(event.x_root, event.y_root)

def toggleFrameChange(flag):

    enableFrameChange = flag

    if flag:

        insertFrameButton.config(state="normal")
        deleteFrameButton.config(state="normal")
        nextFrameButton.config(state="normal")
        prevFrameButton.config(state="normal")
        firstFrameButton.config(state="normal")
        lastFrameButton.config(state="normal")

    else:
    
        insertFrameButton.config(state="disabled")
        deleteFrameButton.config(state="disabled")
        nextFrameButton.config(state="disabled")
        prevFrameButton.config(state="disabled")
        firstFrameButton.config(state="disabled")
        lastFrameButton.config(state="disabled")

def onCopy(a):

    if blockMain:

        return
    
    global float_matrix, select_matrix, selectedNumber, data_matrix, currentFrame, undo_sequence, undo_step, undoOperations, undo_pos

    if float_matrix.visible == True:

        return
    
    undo_step = []
    
    if selectedNumber == 0:
        return

    del float_matrix.data[:]
    float_matrix.data = []
    float_matrix.x = 0
    float_matrix.y = 0
    
    for i in range(50):
        for j in range(80):
            
            if select_matrix[i][j] != None:
                
                float_matrix.data += [(j,i,data_matrix[currentFrame][i][j][0],data_matrix[currentFrame][i][j][1],data_matrix[currentFrame][i][j][2])]
                undo_step += [undoInfoCopy(j, i)]

    undo_sequence += [[currentFrame, undo_step]]

    if len(undo_sequence)>undoOperations:
        del undo_sequence[:undoOperations-len(undo_sequence)]

    else:

        undo_pos += 1

    undo_step = []

    clearSelection()
    float_matrix.visible = False
    float_matrix.isPasted = False

def onCopyNoUndo():
    global float_matrix, select_matrix, selectedNumber, data_matrix, currentFrame
    
    if selectedNumber == 0:
        return

    del float_matrix.data[:]
    float_matrix.data = []
    float_matrix.x = 0
    float_matrix.y = 0
    
    for i in range(50):
        for j in range(80):
            
            if select_matrix[i][j] != None:
                
                float_matrix.data += [(j,i,data_matrix[currentFrame][i][j][0],data_matrix[currentFrame][i][j][1],data_matrix[currentFrame][i][j][2])]

    clearSelection()
    float_matrix.visible = False
    float_matrix.isPasted = False

def onCut(a):

    if blockMain:

        return
    
    global enableFrameChange, float_matrix, select_matrix, selectedNumber, data_matrix, currentFrame, undo_sequence, undo_step, undoOperations, undo_pos

    enableFrameChange = True

    if float_matrix.visible == True:

        float_matrix.visible = False
        undo_pos -= 1
        del undo_sequence[-1]

        return

    undo_step = []
    
    if selectedNumber == 0:
        return

    del float_matrix.data[:]
    float_matrix.data = []
    float_matrix.x = 0
    float_matrix.y = 0
    
    for i in range(50):
        for j in range(80):
            
            if select_matrix[i][j] != None:
                
                float_matrix.data += [(j,i,data_matrix[currentFrame][i][j][0],data_matrix[currentFrame][i][j][1],data_matrix[currentFrame][i][j][2])]
                undo_step += [undoInfoCut(j, i, data_matrix[currentFrame][i][j][0], data_matrix[currentFrame][i][j][1], data_matrix[currentFrame][i][j][2], 32, fgColorDict["white"][1], bgColorDict["black"][1])]
                data_matrix[currentFrame][i][j] = (32, fgColorDict["white"][1], bgColorDict["black"][1])

    undo_sequence += [[currentFrame, undo_step]]

    if len(undo_sequence)>undoOperations:
        del undo_sequence[:undoOperations-len(undo_sequence)]

    else:

        undo_pos += 1

    undo_step = []

    clearSelection()
    float_matrix.visible = False
    float_matrix.isPasted = False

    repaint()

def onCutNoUndo():

    global float_matrix, select_matrix, selectedNumber, data_matrix, currentFrame
    
    if selectedNumber == 0:
        return

    del float_matrix.data[:]
    float_matrix.data = []
    float_matrix.x = 0
    float_matrix.y = 0
    
    for i in range(50):
        for j in range(80):
            
            if select_matrix[i][j] != None:
                
                float_matrix.data += [(j,i,data_matrix[currentFrame][i][j][0],data_matrix[currentFrame][i][j][1],data_matrix[currentFrame][i][j][2])]
                data_matrix[currentFrame][i][j] = (32, fgColorDict["white"][1], bgColorDict["black"][1])

    clearSelection()

    #print float_matrix.data
    
    float_matrix.visible = False
    float_matrix.isPasted = False

    repaint()

def selectionToFloat():

    global float_matrix, mainCanvas, select_matrix, selectedNumber

    selectedNumber = 0

    #print float_matrix.data
    #print float_matrix.x, float_matrix.y

    #print "selectionToFloat"

    for i in float_matrix.data:

        x = i[0] + float_matrix.x
        y = i[1] + float_matrix.y
        #print x, y
        if y>=0 and x>=0 and y<50 and x<80:
            select_matrix[y][x] = mainCanvas.create_rectangle(x*8+j_offset_p+2,y*8+i_offset_p+2,x*8+j_offset_p+10,y*8+i_offset_p+10,width=1,outline="red")
            selectedNumber += 1

def anchorFloatNoUndo():

    global float_matrix, data_matrix, currentFrame

    toggleFrameChange(True)

    x = float_matrix.x
    y = float_matrix.y
    
    for i in float_matrix.data:

        if (y + i[1] < 50 and y + i[1] >= 0) and (x + i[0] < 80 and x + i[0] >= 0):
            
            data_matrix[currentFrame][y + i[1]][x + i[0]] = (i[2], i[3], i[4])
            mainCanvas.itemconfig(texts[x + i[0] + (y + i[1])*80],image=letters[256*i[3]+i[2]])
            mainCanvas.itemconfig(rects[x + i[0] + (y + i[1])*80],fill=bgColorDict[bgcolors[i[4]]][0],width=0)

    float_matrix.visible = False
        

def anchorFloat():

    global float_matrix, data_matrix, undo_step, undo_sequence, undoOperations, currentFrame, undo_pos

    toggleFrameChange(True)

    x = float_matrix.x
    y = float_matrix.y
    undo_step = []
    
    for i in float_matrix.data:

        if x + i[0] < 80 and x + i[0] >= 0 and y + i[1] < 50 and y + i[1] >= 0:
            
            data_matrix[currentFrame][y + i[1]][x + i[0]] = (i[2], i[3], i[4])
            undo_step += [undoInfoAnchor(i[0], i[1], data_matrix[currentFrame][y + i[1]][x + i[0]][0], data_matrix[currentFrame][y + i[1]][x + i[0]][1], data_matrix[currentFrame][y + i[1]][x + i[0]][2], i[2], i[3], i[4])]

        else:

            undo_step += [undoInfoAnchor(i[0], i[1], None, None, None, i[2], i[3], i[4])]
            
    undo_sequence += [[currentFrame, undo_step, x, y]]

    if len(undo_sequence)>undoOperations:
        del undo_sequence[:undoOperations-len(undo_sequence)]

    else:

        undo_pos += 1

    undo_step = []

    float_matrix.visible = False

def onPaste(a):

    if blockMain:

        return

    global float_matrix, select_matrix, selectedNumber, data_matrix, currentFrame, undo_sequence, undo_step, undoOperations, mainCanvas, undo_pos

    float_matrix.visible = True
    float_matrix.isPasted = True

    undo_step = [undoInfoPaste()]

    undo_sequence += [[currentFrame, undo_step]]

    toggleFrameChange(False)

    clearSelection()

    selectionToFloat()

    repaint()

    if len(undo_sequence)>undoOperations:
        del undo_sequence[:undoOperations-len(undo_sequence)]

    else:

        undo_pos += 1

    undo_step = []

def onPasteNoUndo():

    global float_matrix, select_matrix, selectedNumber, data_matrix, currentFrame, mainCanvas

    float_matrix.visible = True
    float_matrix.isPasted = True

    toggleFrameChange(False)

    clearSelection()

    selectionToFloat()

    repaint()

def onUndo(a):

    undo()

def onRedo(a):

    redo()

def insertImage():

    global isSaved, data_matrix, currentFrame, undo_pos, undo_step, undo_sequence, rects, texts, i_offset, j_offset
    global fgColorDict, bgColorDict, pBrush, mainCanvas, paletteCanvas, fgCanvas, bgCanvas, root, picDict, showImages
    openOptions = {}
    openOptions["parent"] = root
    openOptions["filetypes"] = [("Supported formats", (".png", ".gif")),("Portable Network Graphics", ".png"),("Graphics Interchange Format", ".gif")]
    openFileName = tkFileDialog.askopenfilename(**openOptions)
    if openFileName == "":
        return
    if openFileName[-4:].lower()!=".png" and openFileName[-4:].lower()!=".gif":
        return

    try:
        p = Image.open(openFileName)
        pi = ImageTk.PhotoImage(p)
        picDict[str(currentFrame)] = [pi, mainCanvas.create_image(j_offset, i_offset, anchor = Tkinter.NW, image = pi, state = Tkinter.HIDDEN), openFileName]

    except:

        tkMessageBox.showerror("Error", "Cannot open image file")
        return

    #mainCanvas.tag_lower(picDict[str(currentFrame)][1])
        
    undo_sequence += [[currentFrame,[undoInfoInsertImage(openFileName)]]]

    if len(undo_sequence)>undoOperations:
        del undo_sequence[:undoOperations-len(undo_sequence)]

    else:

        undo_pos += 1

    showImages = True

    repaint()

def insertImageSequence():

    global root, frameNumber, undo_sequence, currentFrame, askWindow, fileList, blockMain

    openOptions = {}
    openOptions["parent"] = root
    openOptions["filetypes"] = [("Supported formats", (".png", ".gif")),("Portable Network Graphics", ".png"),("Graphics Interchange Format", ".gif")]
    fileString = tkFileDialog.askopenfilenames(**openOptions)

    if fileString == "":

        return

    fileList = fileString.split()

    askWindow = Tkinter.Toplevel()

    askWindow.protocol("WM_DELETE_WINDOW", cancelFrameNumber)

    askWindow.grab_set()

    blockMain = True

    msg = Tkinter.Message(askWindow, text = "Enter starting frame:")
    msg.grid(row=0, column=0)
    
    enterFrame = Tkinter.Entry(askWindow, textvariable = frameNumber, validatecommand = validateFrameNumber, validate = "key")
    enterFrame.grid(row=1, column=0)

    useCurrentFrameCheck = Tkinter.Checkbutton(askWindow, text = "Use current frame", var = useCurrentFrame)
    useCurrentFrameCheck.grid(row=2, column=0)

    OKButton = Tkinter.Button(askWindow, text = "OK", command = okFrameNumber)
    OKButton.grid(row=3, column=0)

    CancelButton = Tkinter.Button(askWindow, text = "Cancel", command = cancelFrameNumber)
    OKButton.grid(row=4, column=0)

def validateFrameNumber():

    global frameNumber

    s = ""

    foundNonZero = False

    for i in range(len(frameNumber.get())):

        if foundNonZero == False and (frameNumber.get())[i] == "0":

            continue

        else:

            foundNonZero = True

        if (frameNumber.get())[i].isdigit():

            s += (frameNumber.get())[i]

    frameNumber.set(s)

    return True

def validateCurrentFrameNumber():

    global currentFrameString

    s = ""

    foundNonZero = False

    for i in range(len(currentFrameString.get())):

        if foundNonZero == False and (currentFrameString.get())[i] == "0":

            continue

        else:

            foundNonZero = True

        if (currentFrameString.get())[i].isdigit():

            s += (currentFrameString.get())[i]

    currentFrameString.set(s)

    return True

def okFrameNumber():

    global frameNumber, askWindow, undo_sequence, currentFrame, fileList, root, picDict
    global showImages, undo_pos, undoOperations, useCurrentFrame, i_offset, j_offset, blockMain

    #print useCurrentFrame.get(), frameNumber.get().isdigit()

    if useCurrentFrame.get():

        frameNumber.set(str(currentFrame))

    if not(frameNumber.get().isdigit()):

        return

    blockMain = False

    undo_sequence += [[currentFrame,[undoInfoInsertImageSequence(fileList, int(frameNumber.get()))]]]

    if len(undo_sequence)>undoOperations:
        del undo_sequence[:undoOperations-len(undo_sequence)]
    else:
        undo_pos += 1
        
    askWindow.grab_release()

    askWindow.destroy()

    fileList.sort()

    for i in range(len(fileList)):

        p = Image.open(fileList[i])
        pi = ImageTk.PhotoImage(p)
        picDict[str(i + int(frameNumber.get()))] = [pi, mainCanvas.create_image(j_offset, i_offset, anchor = Tkinter.NW, image = pi, state = Tkinter.HIDDEN), fileList[i]]

    if str(currentFrame) in picDict.keys():

        mainCanvas.itemconfig(picDict[str(currentFrame)][1], state = Tkinter.NORMAL)

    showImages = True

    repaint()

def cancelFrameNumber():

    global askWindow, fileList, blockMain

    blockMain = False

    fileList = []

    askWindow.grab_release()

    askWindow.destroy()

def clearPicDict():

    global root, mainCanvas, picDict

    for i in picDict.values():

        mainCanvas.delete(i[1])

    picDict.clear()

def clearThisImage():

    global mainCanvas, picDict, currentFrame

    mainCanvas.delete(picDict[str(currentFrame)][1])

    del picDict[str(currentFrame)]

def resetFloatAndSelection():

    global float_matrix, enableFrameChange

    float_matrix.data = []
    float_matrix.visible = False
    clearSelection()
    toggleFrameChange(True)
    blockMain = False

    repaint()

def duplicateFrame():

    global data_matrix, currentFrame, undo_sequence, undo_pos

    del undo_sequence[:]

    undo_pos = 0

    insertFrame()

    for i in range(50):
        for j in range(80):

            data_matrix[currentFrame][i][j] = data_matrix[currentFrame - 1][i][j]

    repaint()

def cancelExport():

    global askExportWindow, blockMain

    askExportWindow.grab_release()
    askExportWindow.destroy()
    blockMain = False

def OKExport():

    global askExportWindow, blockMain, exportAllFrames, ffString, lfString, data_matrix, exportDirectoryString, offsetString

    if (not ffString.get().isdigit()) or (not lfString.get().isdigit()) or int(lfString.get()) >= len(data_matrix) or int(lfString.get()) < int(ffString.get()):

        tkMessageBox.showerror("Error", "Invalid first and/or last frame number", parent = askExportWindow)
        return

    if (not offsetString.get().isdigit()):

        tkMessageBox.showerror("Error", "Invalid offset", parent = askExportWindow)
        return

    if not os.path.isdir(exportDirectoryString.get()):

        tkMessageBox.showerror("Error", "Invalid export directory", parent = askExportWindow)
        return

    askExportWindow.grab_release()
    askExportWindow.destroy()
    blockMain = False

    if not exportAllFrames.get():

        exportImageSequence(int(ffString.get()), int(lfString.get()))

    else:

        exportImageSequence(0, len(data_matrix)-1)

def toggleExportAllFrames():

    global exportAllFrames, ffString, lfString, ffEntry, lfEntry, data_matrix

    if exportAllFrames.get():

        ffString.set("0")
        ffEntry.config(state = Tkinter.DISABLED)

        lfString.set(str(len(data_matrix)-1))
        lfEntry.config(state = Tkinter.DISABLED)

    else:

        ffString.set("")
        ffEntry.config(state = Tkinter.NORMAL)

        lfString.set("")
        lfEntry.config(state = Tkinter.NORMAL)

def offsetEh():

    global askExportWindow
    
    tkMessageBox.showinfo("Offset", "Frame x will have filename \"[x+offset].png\"", parent = askExportWindow)

def browseExportDirectory():

    global askExportWindow, exportDirectoryString

    dirString = exportDirectoryString.get()

    if exportDirectoryString != None:

        exportDirectoryString.set(tkFileDialog.askdirectory(initialdir = exportDirectoryString.get(), parent = askExportWindow, title = "Choose export directory", mustexist = True))

    else:

        exportDirectoryString.set(tkFileDialog.askdirectory(parent = askExportWindow, title = "Choose export directory", mustexist = True))

    if not(os.path.isdir(exportDirectoryString.get())):

        exportDirectoryString.set(dirString)

def exportImageSequenceDialog():

    global askExportWindow, ffString, lfString, blockMain, exportAllFrames, ffEntry, lfEntry, offsetString, offsetEntry
    global exportDirectoryString, lastExportDirectory, lastOffset

    askExportWindow = Tkinter.Toplevel()
    askExportWindow.grab_set()
    askExportWindow.title("Export image sequence")
    askExportWindow.protocol("WM_DELETE_WINDOW", cancelExport)

    blockMain = True

    ffString = Tkinter.StringVar()
    ffString.set("")

    lfString = Tkinter.StringVar()
    lfString.set("")

    offsetString = Tkinter.StringVar()
    offsetString.set(str(lastOffset))

    exportDirectoryString = Tkinter.StringVar()

    if lastExportDirectory != None:

        exportDirectoryString.set(lastExportDirectory)

    else:

        exportDirectoryString.set("")

    exportAllFrames = Tkinter.IntVar()
    exportAllFrames.set(0)

    ffMsg = Tkinter.Message(askExportWindow, text = "First frame:")
    ffMsg.grid(row = 0, column = 0, columnspan = 2)

    ffEntry = Tkinter.Entry(askExportWindow, textvariable = ffString)
    ffEntry.grid(row = 1, column = 0, columnspan = 2)

    lfMsg = Tkinter.Message(askExportWindow, text = "Last frame:")
    lfMsg.grid(row = 2, column = 0, columnspan = 2)

    lfEntry = Tkinter.Entry(askExportWindow, textvariable = lfString)
    lfEntry.grid(row = 3, column = 0, columnspan = 2)

    exportAllFramesChkBtn = Tkinter.Checkbutton(askExportWindow, text = "Export all frames", variable = exportAllFrames, command = toggleExportAllFrames)
    exportAllFramesChkBtn.grid(row = 4, column = 0, columnspan = 2)

    offsetMessage = Tkinter.Message(askExportWindow, text = "Offset:")
    offsetMessage.grid(row = 5, column = 0)

    offsetEhButton = Tkinter.Button(askExportWindow, text = "Eh?", command = offsetEh)
    offsetEhButton.grid(row = 5, column = 1)

    offsetEntry = Tkinter.Entry(askExportWindow, textvariable = offsetString)
    offsetEntry.grid(row = 6, column = 0, columnspan = 2)

    exportDirectoryMessage = Tkinter.Message(askExportWindow, text = "Output directory:")
    exportDirectoryMessage.grid(row = 7, column = 0, columnspan = 2)

    exportDirectoryEntry = Tkinter.Entry(askExportWindow, textvariable = exportDirectoryString)
    exportDirectoryEntry.grid(row = 8, column = 0)

    exportDirectoryBrowseButton = Tkinter.Button(askExportWindow, text = "Browse...", command = browseExportDirectory)
    exportDirectoryBrowseButton.grid(row = 8, column = 1)

    OKButton = Tkinter.Button(askExportWindow, text = "OK", command = OKExport)
    OKButton.grid(row = 9, column = 0)

    CancelButton = Tkinter.Button(askExportWindow, text = "Cancel", command = cancelExport)
    CancelButton.grid(row = 9, column = 1)

def exportImageSequence(first, last):

    global data_matrix, currentFrame, images, exportDirectoryString, lastExportDirectory, offsetString, lastOffset

    lastExportDirectory = exportDirectoryString.get()
    lastOffset = int(offsetString.get())

    for i in range(first, last+1):

        frameImage = Image.new("RGB", (640, 400), None)

        for j in range(50):
            for k in range(80):
                frameImage.paste(images[256*data_matrix[i][j][k][2]+219],(8*k,8*j))
                frameImage.paste(images[256*data_matrix[i][j][k][1]+data_matrix[i][j][k][0]],(8*k,8*j), images[256*data_matrix[i][j][k][1]+data_matrix[i][j][k][0]])

        frameImage.save(lastExportDirectory + "\\" + str(i+lastOffset)+".png","PNG")

def exportCurrentFrameDialog():

    global exportFileString, lastExportDirectory, exportDirectoryString

    if exportDirectoryString != None:

        exportFileString = tkFileDialog.asksaveasfilename(initialdir = exportDirectoryString.get(), parent = root,
                                                                 title = "Choose export filename", filetypes = [("Portable Network Graphics", ".png")])

    else:

        exportFileString = tkFileDialog.asksaveasfilename(parent = root, title = "Choose export filename", filetypes = [("Portable Network Graphics", ".png")])

    if exportFileString == None or exportFileString == "":

        return

    if (exportFileString[-4:]).lower() != ".png":

        exportFileString += ".png" 

    exportCurrentFrame()
    
def exportCurrentFrame():

    global data_matrix, currentFrame, images, exportFileString

    for i in range(currentFrame,currentFrame+1):

        frameImage = Image.new("RGB", (640, 400), None)

        for j in range(50):
            for k in range(80):
                frameImage.paste(images[256*data_matrix[currentFrame][j][k][2]+219],(8*k,8*j))
                frameImage.paste(images[256*data_matrix[currentFrame][j][k][1]+data_matrix[i][j][k][0]],(8*k,8*j), images[256*data_matrix[currentFrame][j][k][1]+data_matrix[i][j][k][0]])
                
        frameImage.save(exportFileString,"PNG")        

def hideShowImages():

    global showImages

    showImages = not(showImages)

    repaint()

def imagesFrontBack():

    global imagesFront

    imagesFront = not(imagesFront)

    repaint()

def resetUndo():

    global undo_sequence, undo_pos

    del undo_sequence[:]

    undo_pos = 0

def flipSelectionHoriz():

    global i_offset_p, j_offset_p, undo_sequence, undo_pos, data_matrix, currentFrame, flipListHoriz, undo_step, select_matrix

    undo_step = []
    selectSequence = []
    currentFrameMatrix = []
    currentFrameMatrix2 = []

    min = 100
    max = 0
    
    for i in range(50):

        currentFrameMatrix += [[]]
        currentFrameMatrix2 += [[]]
        
        for j in range(80):

            currentFrameMatrix[i] += [data_matrix[currentFrame][i][j]]
            currentFrameMatrix2[i] += [data_matrix[currentFrame][i][j]]

            if select_matrix[i][j] != None:

                if j < min:

                    min = j

                if j > max:

                    max = j

                selectSequence += [[j, i]]
    
    for x in selectSequence:

        #print 1

        i = x[1]
        j = x[0]

        currentFrameMatrix2[i][max-j+min] = (flipListHoriz[data_matrix[currentFrame][i][j][0]], data_matrix[currentFrame][i][j][1], data_matrix[currentFrame][i][j][2])
        currentFrameMatrix2[i][j] = (flipListHoriz[data_matrix[currentFrame][i][max-j+min][0]], data_matrix[currentFrame][i][max-j+min][1], data_matrix[currentFrame][i][max-j+min][2])

        if select_matrix[i][max-j+min] == None:

            mainCanvas.delete(select_matrix[i][j])
            select_matrix[i][j] = None
            select_matrix[i][max-j+min] = mainCanvas.create_rectangle((max-j+min)*8+j_offset_p+2,i*8+i_offset_p+2,(max-j+min)*8+j_offset_p+10,i*8+i_offset_p+10,width=1,outline="red")
        
    data_matrix[currentFrame] = currentFrameMatrix2
    
    for x in selectSequence:

        j = x[0]
        i = x[1]
        
        undo_step += [undoInfoNormal(j, i, data_matrix[currentFrame][i][j][0], data_matrix[currentFrame][i][j][1], data_matrix[currentFrame][i][j][2], currentFrameMatrix[i][max-j+min][0], currentFrameMatrix[i][max-j+min][1], currentFrameMatrix[i][max-j+min][2])]
        undo_step += [undoInfoNormal(max-j+min, i, data_matrix[currentFrame][i][max-j+min][0], data_matrix[currentFrame][i][max-j+min][1], data_matrix[currentFrame][i][max-j+min][2], currentFrameMatrix[i][j][0], currentFrameMatrix[i][j][1], currentFrameMatrix[i][j][2])]

    undo_sequence += [[currentFrame, undo_step]]
    
    repaint()

def flipSelectionVert():

    global i_offset_p, j_offset_p, undo_sequence, undo_pos, data_matrix, currentFrame, flipListVert, undo_step, select_matrix

    undo_step = []
    selectSequence = []
    currentFrameMatrix = []
    currentFrameMatrix2 = []

    min = 100
    max = 0
    
    for i in range(50):

        currentFrameMatrix += [[]]
        currentFrameMatrix2 += [[]]
        
        for j in range(80):

            currentFrameMatrix[i] += [data_matrix[currentFrame][i][j]]
            currentFrameMatrix2[i] += [data_matrix[currentFrame][i][j]]

            if select_matrix[i][j] != None:

                if i < min:

                    min = i

                if i > max:

                    max = i

                selectSequence += [[j, i]]
    
    for x in selectSequence:

        #print 1

        i = x[1]
        j = x[0]

        currentFrameMatrix2[max-i+min][j] = (flipListVert[data_matrix[currentFrame][i][j][0]], data_matrix[currentFrame][i][j][1], data_matrix[currentFrame][i][j][2])
        currentFrameMatrix2[i][j] = (flipListVert[data_matrix[currentFrame][max-i+min][j][0]], data_matrix[currentFrame][max-i+min][j][1], data_matrix[currentFrame][max-i+min][j][2])

        if select_matrix[max-i+min][j] == None:

            mainCanvas.delete(select_matrix[i][j])
            select_matrix[i][j] = None
            select_matrix[max-i+min][j] = mainCanvas.create_rectangle(j*8+j_offset_p+2,(max-i+min)*8+i_offset_p+2,j*8+j_offset_p+10,(max-i+min)*8+i_offset_p+10,width=1,outline="red")
        
    data_matrix[currentFrame] = currentFrameMatrix2
    
    for x in selectSequence:

        j = x[0]
        i = x[1]
        
        undo_step += [undoInfoNormal(j, i, data_matrix[currentFrame][i][j][0], data_matrix[currentFrame][i][j][1], data_matrix[currentFrame][i][j][2], currentFrameMatrix[max-i+min][j][0], currentFrameMatrix[max-i+min][j][1], currentFrameMatrix[max-i+min][j][2])]
        undo_step += [undoInfoNormal(max-j+min, i, data_matrix[currentFrame][max-i+min][j][0], data_matrix[currentFrame][max-i+min][j][1], data_matrix[currentFrame][max-i+min][j][2], currentFrameMatrix[i][j][0], currentFrameMatrix[i][j][1], currentFrameMatrix[i][j][2])]

    undo_sequence += [[currentFrame, undo_step]]
    
    repaint()

def removeSpacesFromSelection():

    global select_matrix, selectedNumber, mainCanvas, data_matrix

    formerSelectedNumber = selectedNumber

    for i in range(50):
        for j in range(80):

            if select_matrix[i][j] != None:

                formerSelectedNumber -= 1
                
                if data_matrix[currentFrame][i][j][0] == 32:

                    mainCanvas.delete(select_matrix[i][j])
                    select_matrix[i][j] = None
                    selectedNumber -= 1

                if formerSelectedNumber == 0:

                    break

        if formerSelectedNumber == 0:

            break

def selectSpacesInSelection():

    global select_matrix, selectedNumber, mainCanvas, data_matrix

    formerSelectedNumber = selectedNumber

    for i in range(50):
        for j in range(80):

            if select_matrix[i][j] != None:

                formerSelectedNumber -= 1
                
                if data_matrix[currentFrame][i][j][0] != 32:

                    mainCanvas.delete(select_matrix[i][j])
                    select_matrix[i][j] = None
                    selectedNumber -= 1

                if formerSelectedNumber == 0:

                    break

        if formerSelectedNumber == 0:

            break

def selectTraceType():

    global traceType, enterChars

    if traceType.get() == "ALL":

        enterChars.config(state = Tkinter.DISABLED)

    else:

        enterChars.config(state = Tkinter.NORMAL)

def cancelTrace():

    global askTraceWindow, blockMain

    askTraceWindow.grab_release()
    askTraceWindow.destroy()

    blockMain = False

def cancelFindReplace():

    global askFindReplaceWindow, blockMain, currentFound, currentFoundRect, mainCanvas

    mainCanvas.delete(currentFoundRect)
    currentFound = None
    currentFoundRect = None
    askFindReplaceWindow.grab_release()
    askFindReplaceWindow.destroy()

    blockMain = False

def checkTraceEntry(tracePalette):

    global askTraceWindow, enterChars, traceType, traceChars

    s = traceChars.get()

    tracePalette = s.split()

    for i in range(len(tracePalette)):

        try:

            if tracePalette == "":

                continue
            
            tracePalette[i] = int(tracePalette[i])

        except:

            tkMessageBox.showerror("Invalid input string", "Enter the decimal ascii codes of the desired characters of the palette, separated by spaces.",
                                   parent = askTraceWindow)
            return

        if tracePalette[i] > 255 or tracePalette[i] < 0:

            tkMessageBox.showerror("Invalid input string", "Enter the decimal ascii codes of the desired characters of the palette, separated by spaces.",
                                   parent = askTraceWindow)
            return

    return tracePalette

def okTraceLQ():

    global askTraceWindow, unprintable, images, blockMain, traceType, traceBGColors, traceFGColors

    if traceType.get() == "ALL":

        tracePalette = range(256)

    else:

        tracePalette = []

        tracePalette = checkTraceEntry(tracePalette)

        if tracePalette == None:

            return

    traceFGColorList = traceFGColors.get().split()

    if len(traceFGColorList) == 0:

        tkMessageBox.showerror("Error", "Invalid FG colors string", parent = askTraceWindow)
        return

    for i in range(len(traceFGColorList)):

        if traceFGColorList[i].isdigit() and not (int(traceFGColorList[i]) > 15):

            traceFGColorList[i] = int(traceFGColorList[i])

        else:

            tkMessageBox.showerror("Error", "Invalid FG colors string", parent = askTraceWindow)
            return

    traceBGColorList = traceBGColors.get().split()

    if len(traceFGColorList) == 0:

        tkMessageBox.showerror("Error", "Invalid BG colors string", parent = askTraceWindow)
        return

    for i in range(len(traceBGColorList)):

        if traceBGColorList[i].isdigit() and not (int(traceBGColorList[i]) > 7):

            traceBGColorList[i] = int(traceBGColorList[i])

        else:

            tkMessageBox.showerror("Error", "Invalid BG colors string", parent = askTraceWindow)
            return

    if not checkFirstLastFrame():

        return

    askTraceWindow.grab_release()

    askTraceWindow.destroy()

    blockMain = False

    if len(traceFGColorList) == 1 and len(traceBGColorList) == 1 and traceFGColorList[0] == traceBGColorList[0]:

        for i in range(50):
            for j in range(80):

                if select[i][j] != None:

                    data_matrix[i][j] = (219,traceFGColorList[0], traceBGColorList[0])

        repaint()
        
        return

    pixValueLetter = []

    for fg in range(len(traceFGColorList)):

        pixValueLetter += [[]]
        
        for bg in range(len(traceBGColorList)):

            pixValueLetter[fg] += [[]]
            
            for k in range(len(tracePalette)):

                pixValueLetter[fg][bg] += [[0.0, 0.0, 0.0]]

                letterInfo = list(images[traceFGColorList[fg]*256+tracePalette[k]].getdata())

                bgInfo = list(images[traceBGColorList[bg]*256+219].getdata())

                if tracePalette[k] in unprintable:

                    continue

                for i1 in range(8):
                    for j1 in range(8):

                        if letterInfo[i1*8+j1][3]:
                    
                            pixValueLetter[fg][bg][k][0] += letterInfo[i1*8+j1][0]
                            pixValueLetter[fg][bg][k][1] += letterInfo[i1*8+j1][1]
                            pixValueLetter[fg][bg][k][2] += letterInfo[i1*8+j1][2]

                        else:

                            pixValueLetter[fg][bg][k][0] += bgInfo[i1*8+j1][0]
                            pixValueLetter[fg][bg][k][1] += bgInfo[i1*8+j1][1]
                            pixValueLetter[fg][bg][k][2] += bgInfo[i1*8+j1][2]

    for frame in range(int(firstFrame.get()), int(lastFrame.get()) + 1):

        print str(frame - int(firstFrame.get()) + 1) + "/" + str(int(lastFrame.get()) - int(firstFrame.get()) + 1)
        
        theImage = Image.open(picDict[str(frame)][2])
        imageInfo = list(theImage.getdata())
        
        for i in range(50):
            for j in range(80):

                if select_matrix[i][j] != None:

                    pixValuePic = [0.0, 0.0, 0.0]

                    for i1 in range(8):
                        for j1 in range(8):

                            pixValuePic[0] += (imageInfo[(i*8 + i1) * 640 + j*8 + j1][0]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0)
                            pixValuePic[1] += (imageInfo[(i*8 + i1) * 640 + j*8 + j1][1]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0)
                            pixValuePic[2] += (imageInfo[(i*8 + i1) * 640 + j*8 + j1][2]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0)

                    minDifference = 1000000000.0
                    minDifPos = tracePalette[0]
                    minDifFG = traceFGColorList[0]
                    minDifBG = traceBGColorList[0]

                    for fg in range(len(traceFGColorList)):

                        if minDifference == 0:

                            break
                        
                        for bg in range(len(traceBGColorList)):
                            
                            for k in range(len(tracePalette)):

                                if tracePalette[k] in unprintable:

                                    continue

                                difference = 0.0

                                for t in range(3):
                                    difference += abs(pixValueLetter[fg][bg][k][t] - pixValuePic[t])
                                #print difference

                                if difference < minDifference:

                                    minDifference = difference
                                    minDifPos = tracePalette[k]
                                    minDifFG = traceFGColorList[fg]
                                    minDifBG = traceBGColorList[bg]
                                    if minDifference == 0:
                                        break
                                    #print
                                    #print minDifference, minDifPos

                    data_matrix[frame][i][j] = (minDifPos,minDifFG,minDifBG)

    repaint()

def okTraceHQ():

    global askTraceWindow, unprintable, images, blockMain, traceType, isSaved, traceFGColors, traceBGColors, data_matrix, firstFrame, lastFrame

    if traceType.get() == "ALL":

        tracePalette = range(256)

    else:

        tracePalette = []

        tracePalette = checkTraceEntry(tracePalette)

        if tracePalette == None:

            return

    traceFGColorList = traceFGColors.get().split()

    if len(traceFGColorList) == 0:

        tkMessageBox.showerror("Error", "Invalid FG colors string", parent = askTraceWindow)
        return

    for i in range(len(traceFGColorList)):

        if traceFGColorList[i].isdigit() and not (int(traceFGColorList[i]) > 15):

            traceFGColorList[i] = int(traceFGColorList[i])

        else:

            tkMessageBox.showerror("Error", "Invalid FG colors string", parent = askTraceWindow)
            return

    traceBGColorList = traceBGColors.get().split()

    if len(traceBGColorList) == 0:

        tkMessageBox.showerror("Error", "Invalid BG colors string", parent = askTraceWindow)
        return

    for i in range(len(traceBGColorList)):

        if traceBGColorList[i].isdigit() and not (int(traceBGColorList[i]) > 7):

            traceBGColorList[i] = int(traceBGColorList[i])

        else:

            tkMessageBox.showerror("Error", "Invalid BG colors string", parent = askTraceWindow)
            return

    if not checkFirstLastFrame():

        return

    askTraceWindow.grab_release()

    askTraceWindow.destroy()

    blockMain = False

    isSaved = False

    if len(traceFGColorList) == 1 and len(traceBGColorList) == 1 and traceFGColorList[0] == traceBGColorList[0]:

        for frame in range(int(firstFrame.get()), int(lastFrame.get()) + 1):
            for i in range(50):
                for j in range(80):

                    if select[i][j] != None:

                        data_matrix[frame][i][j] = (219,traceFGColorList[0], traceBGColorList[0])

        repaint()
        
        return

    endColors = []

    for frame in range(int(firstFrame.get()), int(lastFrame.get()) + 1):

        print str(frame - int(firstFrame.get()) + 1) + "/" + str(int(lastFrame.get()) - int(firstFrame.get()))

        theImage = Image.open(picDict[str(frame)][2])
        imageInfo = list(theImage.getdata())
    
        for i in range(50):
            for j in range(80):

                if select_matrix[i][j] != None:

                    minDifference = 10000000
                    minDifPos = tracePalette[0]
                    minDifBG = traceBGColorList[0]
                    minDifFG = traceFGColorList[0]

                    for fg in traceFGColorList:
                        #print 1
                        for bg in traceBGColorList:

                            if fg == bg:

                                endColors += [fg]
                                continue

                            # 219 is ASCII code for solid rectangle box-drawing block (having all pixels with 100% alpha)
                            bgInfo = list(images[bg*256+219].getdata())
                
                            for k in range(len(tracePalette)):

                                if tracePalette[k] in unprintable:

                                    continue

                                letterInfo = list(images[fg*256+tracePalette[k]].getdata())
                            
                                #print letterInfo
                                difference = 0.0

                                for i1 in range(8):
                                    for j1 in range(8):

                                        if letterInfo[i1*8+j1][3]:

                                            difference += abs(letterInfo[i1*8+j1][0] - (imageInfo[(i*8 + i1) * 640 + j*8 + j1][0]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0))
                                            difference += abs(letterInfo[i1*8+j1][1] - (imageInfo[(i*8 + i1) * 640 + j*8 + j1][1]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0))                  
                                            difference += abs(letterInfo[i1*8+j1][2] - (imageInfo[(i*8 + i1) * 640 + j*8 + j1][2]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0))

                                        else:

                                            difference += abs(bgInfo[i1*8+j1][0] - (imageInfo[(i*8 + i1) * 640 + j*8 + j1][0]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0))
                                            difference += abs(bgInfo[i1*8+j1][1] - (imageInfo[(i*8 + i1) * 640 + j*8 + j1][1]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0))                  
                                            difference += abs(bgInfo[i1*8+j1][2] - (imageInfo[(i*8 + i1) * 640 + j*8 + j1][2]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0))
                                        
                                            #pixValueLetter = (letterInfo[i1*8+j1][0] + letterInfo[i1*8+j1][1] + letterInfo[i1*8+j1][2]) * (letterInfo[i1*8+j1][3] / 255.0)
                                            #pixValuePic = (imageInfo[(i*8 + i1) * 640 + j*8 + j1][0] + imageInfo[(i*8 + i1) * 640 + j*8 + j1][1] + imageInfo[(i*8 + i1) * 640 + j*8 + j1][2]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0)
                                        #print pixValueLetter, pixValuePic
                                        #if pixValuePic!=0:
                                            #print pixValueLetter, pixValuePic
                                        #difference += abs(pixValueLetter - pixValuePic)

                                    #print difference

                                if difference < minDifference:

                                    minDifference = difference
                                    minDifPos = tracePalette[k]
                                    minDifFG = fg
                                    minDifBG = bg
                                    if minDifference == 0:
                                        break
                                    #print
                                    #print minDifference, minDifPos

                    

                    for eh in endColors:

                        difference = 0
                        
                        for i1 in range(8):
                            for j1 in range(8):

                                difference += abs(bgInfo[i1*8+j1][0] - (imageInfo[(i*8 + i1) * 640 + j*8 + j1][0]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0))
                                difference += abs(bgInfo[i1*8+j1][1] - (imageInfo[(i*8 + i1) * 640 + j*8 + j1][1]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0))                  
                                difference += abs(bgInfo[i1*8+j1][2] - (imageInfo[(i*8 + i1) * 640 + j*8 + j1][2]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0))

                        if difference < minDifference:

                            minDifference = difference
                            minDifPos = 32
                            minDifFG = eh
                            minDifBG = eh
                            if minDifference == 0:
                                break
                                
                    data_matrix[frame][i][j] = (minDifPos,minDifFG,minDifBG)
   
    repaint()

def selectColorType():

    global colorType, traceFGColors, fgColorEntry, traceBGColors, bgColorEntry

    if colorType.get() == "BW":

        fgColorEntry.config(state = Tkinter.DISABLED)
        bgColorEntry.config(state = Tkinter.DISABLED)
        traceFGColors.set("15")
        traceBGColors.set("0")

    else:

        fgColorEntry.config(state = Tkinter.NORMAL)
        bgColorEntry.config(state = Tkinter.NORMAL)
        traceFGColors.set("")
        traceBGColors.set("")

def selectTraceFrames():

    global firstEntry, lastEntry, firstFrame, lastFrame, traceFrames, currentFrame

    if traceFrames.get() == "1":

        firstFrame.set(str(currentFrame))
        firstEntry.config(state = Tkinter.DISABLED)

        lastFrame.set(str(currentFrame))
        lastEntry.config(state = Tkinter.DISABLED)

    else:

        firstFrame.set("")
        firstEntry.config(state = Tkinter.NORMAL)

        lastFrame.set("")
        lastEntry.config(state = Tkinter.NORMAL)

def checkFirstLastFrame():

    global firstFrame, lastFrame, traceFrames, askTraceWindow

    if traceFrames.get() == "1":

        return True

    if not firstFrame.get().isdigit() or int(firstFrame.get()) >= len(data_matrix):

        tkMessageBox.showerror("Error", "Invalid first frame", parent = askTraceWindow)
        return False

    if not lastFrame.get().isdigit() or int(lastFrame.get()) >= len(data_matrix):

        tkMessageBox.showerror("Error", "Invalid last frame", parent = askTraceWindow)
        return False

    if int(lastFrame.get()) < int(firstFrame.get()):

        tkMessageBox.showerror("Error", "First frame number must be smaller than last frame number", parent = askTraceWindow)
        return False

    return True

#find and replace functions

askFindReplaceWindow = None

charTextField = None
allCharsString = Tkinter.StringVar()
aCharString = ""
charsToFindString = Tkinter.StringVar()
charsToFindString.set("")
charsToFind = []
anyChar = Tkinter.IntVar()
anyChar.set(0)

fgcolorTextField = None
allFgcolorsString = Tkinter.StringVar()
aFgString = ""
fgcolorsToFindString = Tkinter.StringVar()
fgcolorsToFindString.set("")
fgcolorsToFind = []
anyFg = Tkinter.IntVar()
anyFg.set(0)

bgcolorTextField = None
aBgString = ""
allBgcolorsString = Tkinter.StringVar()
bgcolorsToFindString = Tkinter.StringVar()
bgcolorsToFindString.set("")
bgcolorsToFind = []
anyBg = Tkinter.IntVar()
anyBg.set(0)

allCharsList = []

for i in range(0, 254):
    if(i not in unprintable):
        aCharString += str(i)
        aCharString += " "
        allCharsList += [i]

aCharString += "254"
allCharsString.set(aCharString)
del aCharString

for i in range(0, 7):
    aBgString += str(i)
    aBgString += " "

aBgString += "7"
allBgcolorsString.set(aBgString)
del aBgString
allBgcolorsList = range(0,8)

for i in range(0, 15):
    aFgString += str(i)
    aFgString += " "

aFgString += "15"
allFgcolorsString.set(aFgString)
del aFgString
allFgcolorsList = range(0,16)

doReplace = Tkinter.IntVar()
doReplace.set(1)

replaceBtn = None
replaceAllBtn = None
replaceCharLabel = None
replaceCharEntry = None
replaceFgcolorLabel = None
replaceFgcolorEntry = None
replaceBgcolorLabel = None
replaceBgcolorEntry = None

replaceBgString = Tkinter.StringVar()
replaceBgString.set("")

replaceFgString = Tkinter.StringVar()
replaceFgString.set("")

replaceCharString = Tkinter.StringVar()
replaceCharString.set("")

lastFrameString = Tkinter.StringVar()
lastFrameString.set("")

firstFrameString = Tkinter.StringVar()
firstFrameString.set("")

firstFrameAllString = Tkinter.StringVar()
firstFrameAllString.set("0")

lastFrameAllString = Tkinter.StringVar()
currentFrameString = Tkinter.StringVar()

allFrames = Tkinter.IntVar()
allFrames.set(0)
thisFrameOnly = Tkinter.IntVar()
thisFrameOnly.set(0)

currentFound = None
currentFoundRect = None

firstFrameEntry = None
lastFrameEntry = None

findScopeFirstFrame = 0
findScopeLastFrame = 0

def toggleThisFrameOnly():

    global lastFrameEntry, currentFrameString, currentFrame, firstFrameEntry, firstFrameString, lastFrameString, thisFrameOnly, allFrames
    if(thisFrameOnly.get() == 1):
        currentFrameString.set(currentFrame)
        firstFrameEntry.config(textvariable = currentFrameString, state = "readonly")
        lastFrameEntry.config(textvariable = currentFrameString, state = "readonly")
        allFrames.set(0)
    else:
        firstFrameEntry.config(textvariable = firstFrameString, state = Tkinter.NORMAL)
        lastFrameEntry.config(textvariable = lastFrameString, state = Tkinter.NORMAL)

def toggleAllFrames():

    global lastFrameEntry, firstFrameEntry, firstFrameString, lastFrameString, firstFrameAllString, lastFrameAllString, allFrames, data_matrix, thisFrameOnly
    
    if(allFrames.get() == 1):
        lastFrameAllString.set(len(data_matrix)-1)
        firstFrameEntry.config(textvariable = firstFrameAllString, state = "readonly")
        lastFrameEntry.config(textvariable = lastFrameAllString, state = "readonly")
        thisFrameOnly.set(0)
    else:
        firstFrameEntry.config(textvariable = firstFrameString, state = Tkinter.NORMAL)
        lastFrameEntry.config(textvariable = lastFrameString, state = Tkinter.NORMAL)

def charChkChange():

    global charTextField, allCharsString, charsToFindString, anyChar
    
    if(anyChar.get()==1):
        charTextField.config(textvariable = allFgcolorsString, state = "readonly")
    else:
        charTextField.config(textvariable = charsToFindString, state = Tkinter.NORMAL)

def fgChkChange():

    global fgcolorTextField, allFgcolorsString, fgcolorsToFindString, anyFg
    
    if(anyFg.get()==1):
        fgcolorTextField.config(textvariable = allFgcolorsString, state = "readonly")
    else:
        fgcolorTextField.config(textvariable = fgcolorsToFindString, state = Tkinter.NORMAL)

def bgChkChange():

    global bgcolorTextField, allBgcolorsString, bgcolorsToFindString, anyBg
    
    if(anyBg.get()==1):
        bgcolorTextField.config(textvariable = allBgcolorsString, state = "readonly")
    else:
        bgcolorTextField.config(textvariable = bgcolorsToFindString, state = Tkinter.NORMAL)

def findNextFunc():

    gFS = getFindStrings()

    if(gFS == None):
        return
    
    if(not(gFS)):
        currentFound = None

    findNext()
    repaint()

def findFirstFunc():
    
    if(getFindStrings() == None):
        return
    findFirst()
    repaint()
    
def findNext():

    global currentFrame, currentFound, data_matrix, findScopeFirstFrame, findScopeLastFrame, findScope, mainCanvas, currentFoundRect, currentFound
    global charsToFind, fgcolorsToFind, bgcolorsToFind, firstSearchedFrame, firstSearchedFrameSearched, anyChar, anyFg, anyBg, select_matrix

    #print currentFrame, findScopeFirstFrame

    if(currentFound == None):
        if(currentFrame < findScopeFirstFrame or currentFrame > findScopeLastFrame):
            currentFrame = findScopeFirstFrame
        repaint()
        firstSearchedFrame = currentFrame
        firstSearchedFrameSearched = False
        currentFound = gridPointClass()
        currentFound.x = 0
        currentFound.y = 0
        currentFoundx = 0
        currentFoundy = 0
    else:
        currentFoundx = (currentFound.x + 1) % 80
        currentFoundy = currentFound.y + (currentFound.x + 1) / 80
        currentFound.x = currentFoundx
        currentFound.y = currentFoundy
    
    for x in (range(currentFrame, findScopeLastFrame + 1) + range(findScopeFirstFrame, currentFrame)):

        #print "for"
        if(x!=currentFrame):
            repaint()
            currentFrame = x
        
        if(x == firstSearchedFrame):
            if(firstSearchedFrameSearched):
                if(currentFoundRect == None):
                    tkMessageBox.showinfo("", "Search target not found", parent = askFindReplaceWindow)
                else:
                    tkMessageBox.showinfo("Search wrapped", "No further search targets found", parent = askFindReplaceWindow)
                    
                mainCanvas.delete(currentFoundRect)
                currentFoundRect = None
                firstSearchedFrameSearched = False
                currentFound = None
                return None

                #print "s"
        else:
            firstSearchedFrameSearched = True

        #print findScope.get(), charsToFind, fgcolorsToFind, bgcolorsToFind, anyChar.get(), anyFg.get(), anyBg.get()
        for i in range(currentFoundy,50):
            #print currentFoundx, currentFoundy
            for j in range(currentFoundx,80):
                #print i,j,data_matrix[currentFrame][i][j]
                if((findScope.get() == "FRAME" or select_matrix[i][j] != None)
                   and (anyChar.get() == 1 or (data_matrix[currentFrame][i][j][0] in charsToFind))
                   and (anyFg.get() == 1 or (data_matrix[currentFrame][i][j][1] in fgcolorsToFind))
                   and (anyBg.get() == 1 or (data_matrix[currentFrame][i][j][2] in bgcolorsToFind))):

                    #print "y"
                    
                    if(currentFoundRect!=None):
                        mainCanvas.delete(currentFoundRect)
                    else:
                        currentFound = gridPointClass()
                    
                    currentFoundRect = mainCanvas.create_rectangle(j*8+j_offset_p+2,i*8+i_offset_p+2,j*8+j_offset_p+10,i*8+i_offset_p+10,width=2,outline="blue")
                    currentFound.x = j
                    currentFound.y = i
                    return currentFound
            currentFoundx = 0
        currentFoundy = 0
        #print x, currentFrame

    #print "x"

    if(currentFoundRect == None):
        tkMessageBox.showinfo("", "Search target not found", parent = askFindReplaceWindow)
        
    else:
        tkMessageBox.showinfo("Search wrapped", "No further search targets found", parent = askFindReplaceWindow)
        #print "d"

    mainCanvas.delete(currentFoundRect)
    currentFoundRect = None
    currentFound = None
    firstSearchedFrameSearched = False
    return None

def findFirst():

    global currentFound, findScopeFirstFrame, currentFrame
    
    currentFrame = findScopeFirstFrame
    currentFound = None
    findNext()

def replaceCurrent():

    global currentFound, data_matrix, charReplacement, currentFrame, currentFoundRect

    gFS = getFindStrings()

    if(gFS == None):
        return

    gRS = getReplaceStrings()

    if(gRS == None):
        return

    if(gFS == False or currentFoundRect == None):
        currentFound = None
        findNext()
        return

    #print currentFoundRect, currentFound
    replaceChar1, replaceFg1, replaceBg1 = charReplacement
    if(replaceChar1 == None):
        replaceChar1 = data_matrix[currentFrame][currentFound.y][currentFound.x][0]
    if(replaceFg1 == None):
        replaceFg1 = data_matrix[currentFrame][currentFound.y][currentFound.x][1]
    if(replaceBg1 == None):
        replaceBg1 = data_matrix[currentFrame][currentFound.y][currentFound.x][2]
            
    data_matrix[currentFrame][currentFound.y][currentFound.x] = (replaceChar1, replaceFg1, replaceBg1)

    repaint()

    findNext()

def replaceAll():

    global currentFrame, charReplacement, data_matrix, findScopeFirstFrame, findScopeLastFrame
    global anyChar, anyFg, anyBg, data_matrix, charsToFind, fgcolorsToFind, bgcolorsToFind, charReplacement, findScope, select_matrix

    if(getFindStrings() == None or getReplaceStrings() == None):
        return

    targetsFound = 0

    for x in range(findScopeFirstFrame, findScopeLastFrame+1):
        print x - findScopeFirstFrame + 1, "/", findScopeLastFrame - findScopeFirstFrame + 1
        for i in range(0,50):
            for j in range(0,80):
                if((findScope.get() == "FRAME" or select_matrix[i][j] != None)
                   and (anyChar.get() == 1 or (data_matrix[x][i][j][0] in charsToFind))
                   and (anyFg.get() == 1 or (data_matrix[x][i][j][1] in fgcolorsToFind))
                   and (anyBg.get() == 1 or (data_matrix[x][i][j][2] in bgcolorsToFind))):

                    targetsFound += 1

                    replaceChar1, replaceFg1, replaceBg1 = charReplacement
                    if(replaceChar1 == None):
                        replaceChar1 = data_matrix[x][i][j][0]
                    if(replaceFg1 == None):
                        replaceFg1 = data_matrix[x][i][j][1]
                    if(replaceBg1 == None):
                        replaceBg1 = data_matrix[x][i][j][2]
        
                    data_matrix[x][i][j] = (replaceChar1, replaceFg1, replaceBg1)
                    currentFrame = x

    if(targetsFound == 0):
        tkMessageBox.showinfo("", "Search target not found", parent = askFindReplaceWindow)
    else:
        tkMessageBox.showinfo("Search wrapped", str(targetsFound) + " search targets replaced", parent = askFindReplaceWindow)
    repaint()

def getReplaceStrings():

    global replaceBgString, replaceFgString, replaceCharString, charReplacement, askFindReplaceWindow

    atLeastOne = False

    if(replaceCharString.get().strip().isdigit() and int(replaceCharString.get().strip())>=0 and int(replaceCharString.get().strip())<=255):
        replaceChar = int(replaceCharString.get().strip())
        atLeastOne = True
    else:
        if(len(replaceCharString.get().strip()) == 0):
            replaceChar = None
        else:
            tkMessageBox.showerror("Error", "Invalid replacement character", parent = askFindReplaceWindow)
            return None

    if(replaceFgString.get().strip().isdigit() and int(replaceFgString.get().strip())>=0 and int(replaceFgString.get().strip())<=15):
        replaceFg = int(replaceFgString.get().strip())
        atLeastOne = True
    else:
        if(len(replaceFgString.get().strip()) == 0):
            replaceFg = None
        else:
            tkMessageBox.showerror("Error", "Invalid replacement foreground color", parent = askFindReplaceWindow)
            return None

    if(replaceBgString.get().strip().isdigit() and int(replaceBgString.get().strip())>=0 and int(replaceBgString.get().strip())<=7):
        replaceBg = int(replaceBgString.get().strip())
        atLeastOne = True
    else:
        if(len(replaceBgString.get().strip()) == 0):
            replaceBg = None
        else:
            tkMessageBox.showerror("Error", "Invalid replacement background color", parent = askFindReplaceWindow)
            return None

    if(not atLeastOne):
        tkMessageBox.showerror("Error", "At least one replacement entry must be filled", parent = askFindReplaceWindow)
        return None

    charReplacement = (replaceChar, replaceFg, replaceBg)

    return True

def getFindStrings():

    global fgcolorsToFindString, bgcolorsToFindString, charsToFindString, charsToFind, bgcolorsToFind, fgcolorsToFind, anyBg, anyFg, anyChar
    global firstFrameEntry, lastFrameEntry, findScopeFirstFrame, findScopeLastFrame, allFgcolorsList, allBgcolorsList, allCharsList, askFindReplaceWindow

    if(anyFg.get() == 0):
        newFgcolorsToFind = fgcolorsToFindString.get().split()
        newFgcolorsToFind.sort()
        if((len(newFgcolorsToFind) == 0) or (not listToDigit(newFgcolorsToFind)) or (newFgcolorsToFind[0] < 0) or (newFgcolorsToFind[-1] > 15)):
            tkMessageBox.showerror("Error", "Invalid foreground color list", parent = askFindReplaceWindow)
            return None
        removeDoubles(newFgcolorsToFind)
    else:
        newFgcolorsToFind = allFgcolorsList

    if(anyBg.get() == 0):
        newBgcolorsToFind = bgcolorsToFindString.get().split()
        newBgcolorsToFind.sort()
        if((len(newBgcolorsToFind) == 0) or (not listToDigit(newBgcolorsToFind)) or (newBgcolorsToFind[0] < 0) or (newBgcolorsToFind[-1] > 7)):
            tkMessageBox.showerror("Error", "Invalid background color list", parent = askFindReplaceWindow)
            return None
        removeDoubles(newBgcolorsToFind)
    else:
        newBgcolorsToFind = allBgcolorsList

    if(anyChar.get() == 0):
        newCharsToFind = charsToFindString.get().split()
        newCharsToFind.sort()
        if((len(newCharsToFind) == 0) or (not listToDigit(newCharsToFind)) or (newCharsToFind[0] < 0) or (newCharsToFind[-1] > 255)):
            tkMessageBox.showerror("Error", "Invalid character list", parent = askFindReplaceWindow)
            return None
        removeDoubles(newCharsToFind)
    else:
        newCharsToFind = allCharsList
    
    try:
        findScopeFirstFrame = int(firstFrameEntry.get().strip())
    except:
        tkMessageBox.showerror("Error", "Invalid first frame number", parent = askFindReplaceWindow)
        return None

    try:
        findScopeLastFrame = int(lastFrameEntry.get().strip())
    except:
        tkMessageBox.showerror("Error", "Invalid last frame number", parent = askFindReplaceWindow)
        return None

    if(newFgcolorsToFind == fgcolorsToFind and newBgcolorsToFind == bgcolorsToFind and newCharsToFind == charsToFind):
        return True
    else:
        fgcolorsToFind = newFgcolorsToFind
        bgcolorsToFind = newBgcolorsToFind
        charsToFind = newCharsToFind
        return False

def removeDoubles(aList):

    listLength = len(aList)
    i = 0
    
    while i<listLength-1:
        if(aList[i]==aList[i+1]):
            del alist[i]
            listLength-=1
        else:
            i+=1

def listToDigit(aList):

    for i in range(len(aList)):
        if(aList[i].isdigit()):
            aList[i] = int(aList[i])
        else:
            return False

    return True

def findAndReplace():

    global currentFrame, select_matrix, selectedNumber, mainCanvas, data_matrix
    global askFindReplaceWindow, anyFg, anyBg, anyChar, findScope, charsToFindString
    global blockMain, allBgcolorsString, bgcolorsToFindString, fgcolorsToFindString
    global charTextField, fgcolorTextField, bgcolorTextField, allFgcolorsString
    global replaceBtn, replaceAllBtn, replaceFgcolorLabel, replaceFgcolorEntry
    global replaceBgcolorLabel, replaceBgcolorEntry, doReplace, replaceFgString
    global replaceCharLabel, replaceCharEntry, replaceCharString, replaceBgString
    global lastFrameString, firstFrameString, allFrames, thisFrameOnly, firstFrameEntry, lastFrameEntry

    blockMain = True

    askFindReplaceWindow = Tkinter.Toplevel()

    askFindReplaceWindow.protocol("WM_DELETE_WINDOW", cancelFindReplace)

    askFindReplaceWindow.grab_set()
    askFindReplaceWindow.title("Find and Replace")

    findFrame = Tkinter.Frame(askFindReplaceWindow);
    findFrame.grid(row = 0, column = 0, ipadx = 5, rowspan = 2);

    replaceFrame = Tkinter.Frame(askFindReplaceWindow);
    replaceFrame.grid(row = 0, column = 1, ipadx = 5, sticky = "n");

    findLabel = Tkinter.Label(findFrame, text = "Find", justify = Tkinter.LEFT)
    findLabel.grid(row = 0, column = 0, columnspan = 2);

    findSeparator1 = ttk.Separator(findFrame, orient = Tkinter.HORIZONTAL);
    findSeparator1.grid(row = 1, column = 0, columnspan = 2, sticky="sew", ipady = 5)

    findCharLabel = Tkinter.Label(findFrame, text = "Character", justify = Tkinter.LEFT)
    findCharLabel.grid(row = 2, column = 0, sticky = "w")

    charTextField = Tkinter.Entry(findFrame, textvariable = charsToFindString)
    charTextField.grid(row = 3, column = 0, columnspan = 2)

    charChkChange()

    anyCharChk = Tkinter.Checkbutton(findFrame, text = "Any", justify = Tkinter.RIGHT, variable = anyChar, command = charChkChange)
    anyCharChk.grid(row = 2, column = 1, sticky = "e")

    findSeparator2 = ttk.Separator(findFrame, orient = Tkinter.HORIZONTAL);
    findSeparator2.grid(row = 4, column = 0, columnspan = 2, sticky="sew", ipady = 5)

    findFgcolorLabel = Tkinter.Label(findFrame, text = "Fg. color", justify = Tkinter.LEFT)
    findFgcolorLabel.grid(row = 5, column = 0, sticky = "w")

    anyFgcolorChk = Tkinter.Checkbutton(findFrame, text = "Any", justify = Tkinter.RIGHT, variable = anyFg, command = fgChkChange)
    anyFgcolorChk.grid(row = 5, column = 1, sticky = "e")

    fgcolorTextField = Tkinter.Entry(findFrame, textvariable = fgcolorsToFindString)
    fgcolorTextField.grid(row = 6, column = 0, columnspan = 2)

    fgChkChange()

    findSeparator3 = ttk.Separator(findFrame, orient = Tkinter.HORIZONTAL);
    findSeparator3.grid(row = 7, column = 0, columnspan = 2, sticky="sew", ipady = 5)

    findBgcolorLabel = Tkinter.Label(findFrame, text = "Bg. color", justify = Tkinter.LEFT)
    findBgcolorLabel.grid(row = 8, column = 0, sticky = "w")

    anyBgcolorChk = Tkinter.Checkbutton(findFrame, text = "Any", justify = Tkinter.RIGHT, variable = anyBg, command = bgChkChange)
    anyBgcolorChk.grid(row = 8, column = 1, sticky = "e")

    bgcolorTextField = Tkinter.Entry(findFrame, textvariable = allBgcolorsString)
    #print allBgcolorsString
    bgcolorTextField.grid(row = 9, column = 0, columnspan = 2)

    bgChkChange()

    findSeparator4 = ttk.Separator(findFrame, orient = Tkinter.HORIZONTAL);
    findSeparator4.grid(row = 10, column = 0, columnspan = 2, sticky="sew", ipady = 5)

    if(firstFrameString.get() == ""):
        firstFrameString.set(str(currentFrame))

    if(lastFrameString.get() == ""):
        lastFrameString.set(str(currentFrame))

    firstFrameLabel = Tkinter.Label(findFrame, text = "First frame", justify = Tkinter.LEFT)
    firstFrameLabel.grid(row = 11, column = 0)

    firstFrameEntry = Tkinter.Entry(findFrame, width = 10, textvariable = firstFrameString)
    firstFrameEntry.grid(row = 11, column = 1)

    lastFrameLabel = Tkinter.Label(findFrame, text = "Last frame", justify = Tkinter.LEFT)
    lastFrameLabel.grid(row = 12, column = 0)

    lastFrameEntry = Tkinter.Entry(findFrame, width = 10, textvariable = lastFrameString)
    lastFrameEntry.grid(row = 12, column = 1)

    useThisFrameChkBtn = Tkinter.Checkbutton(findFrame, text = "Current frame only", justify = Tkinter.LEFT, variable = thisFrameOnly, command = toggleThisFrameOnly)
    useThisFrameChkBtn.grid(row = 13, column = 0, columnspan = 2, sticky = "w")

    useAllFramesChkbtn = Tkinter.Checkbutton(findFrame, text = "All frames", justify = Tkinter.LEFT, variable = allFrames, command = toggleAllFrames)
    useAllFramesChkbtn.grid(row = 14, column = 0, columnspan = 2, sticky = "w")
    
    replaceLabel = Tkinter.Label(replaceFrame, text = "Replace", justify = Tkinter.LEFT)
    replaceLabel.grid(row = 0, column = 0, columnspan = 2, sticky = "w")

    replaceSeparator1 = ttk.Separator(replaceFrame, orient = Tkinter.HORIZONTAL);
    replaceSeparator1.grid(row = 1, column = 0, columnspan = 2, sticky="sew")

    replaceCharLabel = Tkinter.Label(replaceFrame, text = "Character", justify = Tkinter.LEFT)
    replaceCharLabel.grid(row = 2, column = 0)

    replaceCharEntry = Tkinter.Entry(replaceFrame, width = 10, textvariable = replaceCharString)
    replaceCharEntry.grid(row = 2, column = 1, sticky="e", pady = 5)

    replaceFgcolorLabel = Tkinter.Label(replaceFrame, text = "Fg. color", justify = Tkinter.LEFT)
    replaceFgcolorLabel.grid(row = 3, column = 0)

    replaceFgcolorEntry = Tkinter.Entry(replaceFrame, width = 10, textvariable = replaceFgString)
    replaceFgcolorEntry.grid(row = 3, column = 1, sticky="e", pady = 5)

    replaceBgcolorLabel = Tkinter.Label(replaceFrame, text = "Bg. color", justify = Tkinter.LEFT)
    replaceBgcolorLabel.grid(row = 4, column = 0)

    replaceBgcolorEntry = Tkinter.Entry(replaceFrame, width = 10, textvariable = replaceBgString)
    replaceBgcolorEntry.grid(row = 4, column = 1, sticky="e", pady = 5)

    buttonFrame = Tkinter.Frame(askFindReplaceWindow)
    buttonFrame.grid(row = 1, column = 1, sticky = "s", pady = 5)

    findInSelectionRBtn = Tkinter.Radiobutton(buttonFrame, text = "Find in selection", justify = Tkinter.LEFT, variable = findScope, value = "SELECTION")
    findInSelectionRBtn.grid(row = 0, column = 0, sticky = "w", columnspan = 2)

    findInFrameRBtn = Tkinter.Radiobutton(buttonFrame, text = "Find in whole frame", justify = Tkinter.LEFT, variable = findScope, value = "FRAME")
    findInFrameRBtn.grid(row = 1, column = 0, sticky = "w", columnspan = 2)

    if(selectedNumber == 0):
        findInSelectionRBtn.config(state = Tkinter.DISABLED)
        findScope.set("FRAME")

    replaceSeparator = ttk.Separator(buttonFrame, orient = Tkinter.HORIZONTAL)
    replaceSeparator.grid(row = 1, column = 0, sticky = "s", columnspan = 2)

    findBtn = Tkinter.Button(buttonFrame, text = "Find first", command = findFirstFunc)
    findBtn.grid(row = 2, column = 0, sticky = "ew")

    findNextBtn = Tkinter.Button(buttonFrame, text = "Find next", command = findNextFunc)
    findNextBtn.grid(row = 2, column = 1, sticky = "ew")

    replaceBtn = Tkinter.Button(buttonFrame, text = "Replace", command = replaceCurrent)
    replaceBtn.grid(row = 3, column = 0, sticky = "ew")

    replaceAllBtn = Tkinter.Button(buttonFrame, text = "Replace all", command = replaceAll)
    replaceAllBtn.grid(row = 3, column = 1, sticky = "ew")

    toggleThisFrameOnly()
    toggleAllFrames()

#generate random

askGenerateRandomWindow = None

genRandCharsString = Tkinter.StringVar()
genRandCharsString.set("")

genRandFgcolorsString = Tkinter.StringVar()
genRandFgcolorsString.set("")

genRandBgcolorsString = Tkinter.StringVar()
genRandBgcolorsString.set("")

genRandAnyChar = Tkinter.IntVar()
genRandAnyChar.set(0)

genRandAnyFg = Tkinter.IntVar()
genRandAnyFg.set(0)

genRandAnyBg = Tkinter.IntVar()
genRandAnyFg.set(0)

genRandCharTextField = None
genRandFgcolorTextField = None
genRandBgcolorTextField = None

genRandFirstFrameString = Tkinter.StringVar()
genRandFirstFrameString.set("")

genRandLastFrameString = Tkinter.StringVar()
genRandLastFrameString.set("")

genRandFirstFrameEntry = None
genRandLastFrameEntry = None

genRandThisFrameOnly = Tkinter.IntVar()
genRandThisFrameOnly.set(0)

genRandAllFrames = Tkinter.IntVar()
genRandThisFrameOnly.set(0)

genRandScope = Tkinter.StringVar()
genRandScope.set("SELECTION")

genRandInSelectionRBtn = None

genRandStepType = Tkinter.StringVar()
genRandStepType.set("CONST")

genRandStepSizeString = Tkinter.StringVar()
genRandStepSizeString.set("2")

genRandMultiFrameEntry = None

genRandOffsetString = Tkinter.StringVar()
genRandOffsetString.set("0")

genRandOffsetEntry = None
genRandOffsetLabel = None

genRandSeedString = Tkinter.StringVar()
genRandSeedString.set("")

genRandOffset = 0
genRandLength = 0

def genRandToggleThisFrameOnly():

    global genRandLastFrameEntry, currentFrameString, currentFrame, genRandFirstFrameEntry, genRandFirstFrameString, genRandLastFrameString
    global genRandThisFrameOnly, genRandAllFrames
    
    if(genRandThisFrameOnly.get() == 1):
        currentFrameString.set(currentFrame)
        genRandFirstFrameEntry.config(textvariable = currentFrameString, state = "readonly")
        genRandLastFrameEntry.config(textvariable = currentFrameString, state = "readonly")
        genRandAllFrames.set(0)
    else:
        genRandFirstFrameEntry.config(textvariable = genRandFirstFrameString, state = Tkinter.NORMAL)
        genRandLastFrameEntry.config(textvariable = genRandLastFrameString, state = Tkinter.NORMAL)

def genRandToggleAllFrames():

    global genRandLastFrameEntry, genRandFirstFrameEntry, genRandFirstFrameString, genRandLastFrameString, firstFrameAllString, lastFrameAllString
    global genRandAllFrames, data_matrix, genRandThisFrameOnly, genRandLastFrameString
    
    if(genRandAllFrames.get() == 1):
        lastFrameAllString.set(len(data_matrix)-1)
        genRandFirstFrameEntry.config(textvariable = firstFrameAllString, state = "readonly")
        genRandLastFrameEntry.config(textvariable = lastFrameAllString, state = "readonly")
        genRandThisFrameOnly.set(0)
    else:
        genRandFirstFrameEntry.config(textvariable = genRandFirstFrameString, state = Tkinter.NORMAL)
        genRandLastFrameEntry.config(textvariable = genRandLastFrameString, state = Tkinter.NORMAL)

def genRandCharChkChange():

    global genRandCharTextField, allCharsString, genRandCharsString, genRandAnyChar
    
    if(genRandAnyChar.get()==1):
        genRandCharTextField.config(textvariable = allCharsString, state = "readonly")
    else:
        genRandCharTextField.config(textvariable = genRandCharsString, state = Tkinter.NORMAL)

def genRandFgChkChange():

    global genRandFgcolorTextField, allFgcolorsString, genRandFgcolorsString, genRandAnyFg
    
    if(genRandAnyFg.get()==1):
        genRandFgcolorTextField.config(textvariable = allFgcolorsString, state = "readonly")
    else:
        genRandFgcolorTextField.config(textvariable = genRandFgcolorsString, state = Tkinter.NORMAL)

def genRandBgChkChange():

    global genRandBgcolorTextField, allBgcolorsString, genRandBgcolorsToFindString, genRandAnyBg
    
    if(genRandAnyBg.get()==1):
        genRandBgcolorTextField.config(textvariable = allBgcolorsString, state = "readonly")
    else:
        genRandBgcolorTextField.config(textvariable = genRandBgcolorsString, state = Tkinter.NORMAL)

def generateRandomFunc():

    global genRandScopeFirstFrame, genRandScopeLastFrame, genRandSeed, genRandScope, data_matrix, select_matrix, genRandLength, genRandOffset
    global charsToGenRand, fgcolorsToGenRand, bgcolorsToGenRand

    if(getGenRandStrings() == False):
        return
    
    random.seed(genRandSeed)

    print genRandScopeFirstFrame, genRandScopeLastFrame

    x = genRandScopeFirstFrame
    offsetFinished = False
    
    while(x <= genRandScopeLastFrame):
        for i in range(0,50):
            for j in range(0,80):
                if(genRandScope.get() == "FRAME" or select_matrix[i][j] != None):
                    theRandomChar = (random.choice(charsToGenRand),random.choice(fgcolorsToGenRand),random.choice(bgcolorsToGenRand))
                    if(offsetFinished):
                        for x1 in range(x, min([x+genRandLength, genRandScopeLastFrame+1])):
                            data_matrix[x1][i][j] = theRandomChar
                    else:
                        for x1 in range(x, min([x+genRandOffset, genRandScopeLastFrame+1])):
                            data_matrix[x1][i][j] = theRandomChar
                            
        if(offsetFinished):
            x += genRandLength
        else:
            x += genRandOffset

        offsetFinished = True

    cancelGenerateRandom()
    repaint()

def getGenRandStrings():

    global askGenerateRandomWindow, fgcolorsToGenRand, genRandFgcolorsString, bgcolorsToGenRand, charsToGenRand, genRandAnyFg, genRandAnyBg, genRandAnyChar
    global allCharsList, allBgcolorsList, allFgcolorsList, genRandStepSizeString, genRandSeed, genRandSeedString, genRandScopeLastFrame, genRandScopeFirstFrame
    global genRandFirstFrameString, genRandLastFrameString, genRandOffset, genRandLength, data_matrix

    if(genRandAnyChar.get() == 0):
        charsToGenRand = genRandCharsString.get().strip().split()
        charsToGenRand.sort()
        if((len(charsToGenRand) == 0) or (not listToDigit(charsToGenRand)) or (charsToGenRand[0] < 0) or (charsToGenRand[-1] > 255)):
            tkMessageBox.showerror("Error", "Invalid character list", parent = askGenerateRandomWindow)
            return False
        for i in charsToGenRand:
            if i in unprintable:
                del i
    else:
        charsToGenRand = allCharsList

    if(genRandAnyFg.get() == 0):
        fgcolorsToGenRand = genRandFgcolorsString.get().strip().split()
        fgcolorsToGenRand.sort()
        if((len(fgcolorsToGenRand) == 0) or (not listToDigit(fgcolorsToGenRand)) or (fgcolorsToGenRand[0] < 0) or (fgcolorsToGenRand[-1] > 15)):
            tkMessageBox.showerror("Error", "Invalid foreground color list", parent = askGenerateRandomWindow)
            return False
    else:
        fgcolorsToGenRand = allFgcolorsList

    if(genRandAnyBg.get() == 0):
        bgcolorsToGenRand = genRandBgcolorsString.get().strip().split()
        bgcolorsToGenRand.sort()
        if((len(bgcolorsToGenRand) == 0) or (not listToDigit(bgcolorsToGenRand)) or (bgcolorsToGenRand[0] < 0) or (bgcolorsToGenRand[-1] > 7)):
            tkMessageBox.showerror("Error", "Invalid background color list", parent = askGenerateRandomWindow)
            return False
    else:
        bgcolorsToGenRand = allBgcolorsList

    if(genRandStepType.get() == "CONST"):
        genRandLength = sys.maxint
    else:
        if(genRandStepType.get() == "ONE"):
            genRandLength = 1
        else:
            try:
                genRandLength = int(genRandStepSizeString.get())
            except:
                tkMessageBox.showerror("Error", "Invalid step size duration", parent = askGenerateRandomWindow)
                return False

            try:
                if(genRandOffsetString.get() == ""):
                    genRandOffsetString.set("0")
                genRandOffset = int(genRandOffsetString.get()) % genRandLength
            except:
                tkMessageBox.showerror("Error", "Invalid step offset", parent = askGenerateRandomWindow)
                return False

    try:
        if(genRandSeedString.get() == ""):
            genRandSeed = None
        else:
            genRandSeed = int(genRandSeedString.get())
    except:
        tkMessageBox.showerror("Error", "Invalid seed, must be an integer or omitted", parent = askGenerateRandomWindow)
        return False

    try:
        if(genRandThisFrameOnly.get() == 1):
            genRandScopeFirstFrame = currentFrame
        else:
            if(genRandAllFrames.get() == 1):
                genRandScopeFirstFrame = 0
            else:
                genRandScopeFirstFrame = int(genRandFirstFrameString.get())
    except:
        tkMessageBox.showerror("Error", "Invalid first frame", parent = askGenerateRandomWindow)
        return False

    try:
        if(genRandThisFrameOnly.get() == 1):
            genRandScopeLastFrame = currentFrame
        else:
            if(genRandAllFrames.get() == 1):
                genRandScopeLastFrame = len(data_matrix)-1
            else:
                genRandScopeLastFrame = int(genRandLastFrameString.get())
                if(genRandScopeLastFrame >= len(data_matrix)):
                    tkMessageBox.showerror("Error", "Invalid last frame; must be below " + str(len(data_matrix)), parent = askGenerateRandomWindow)
                    return False
    except:
        tkMessageBox.showerror("Error", "Invalid last frame", parent = askGenerateRandomWindow)
        return False

    return True

def cancelGenerateRandom():

    global askGenerateRandomWindow, blockMain, mainCanvas

    askGenerateRandomWindow.grab_release()
    askGenerateRandomWindow.destroy()

    blockMain = False

def toggleStepType():

    global genRandMultiFrameEntry, genRandStepType

    if(genRandStepType.get() != "MULTI"):
        genRandMultiFrameEntry.config(state = "readonly")
        genRandOffsetEntry.config(state = "readonly")
        genRandOffsetLabel.config(state = Tkinter.DISABLED)
    else:
        genRandMultiFrameEntry.config(state = Tkinter.NORMAL)
        genRandOffsetEntry.config(state = Tkinter.NORMAL)
        genRandOffsetLabel.config(state = Tkinter.NORMAL)

def onClickMultiFrame(click):

    global genRandStepType

    genRandStepType.set("MULTI")
    toggleStepType()
    
def generateRandom():

    global blockMain, askGenerateRandomWindow, genRandCharTextField, genRandCharsString, genRandAnyChar, genRandAnyFg, genRandBgcolorTextField
    global genRandFgcolorsString, genRandFgcolorTextField, genRandAnyBg, genRandBgcolorsString, genRandFirstFrameString, currentFrame, genRandFirstFrameEntry
    global genRandFirstFrameString, genRandLastFrameString, genRandLastFrameEntry, genRandThisFrameOnly, genRandAllFrames, genRandScope, genRandInSelectionRBtn
    global genRandStepType, genRandStepSizeString, genRandMultiFrameEntry, genRandOffsetString, genRandSeedString, genRandOffsetEntry, genRandOffsetLabel

    blockMain = True

    askGenerateRandomWindow = Tkinter.Toplevel()

    askGenerateRandomWindow.protocol("WM_DELETE_WINDOW", cancelGenerateRandom)

    askGenerateRandomWindow.grab_set()
    askGenerateRandomWindow.title("Find and Replace")

    leftGenRandFrame = Tkinter.Frame(askGenerateRandomWindow)
    leftGenRandFrame.grid(row = 0, column = 0, padx = 5, rowspan = 2)

    rightGenRandFrame = Tkinter.Frame(askGenerateRandomWindow)
    rightGenRandFrame.grid(row = 0, column = 1, padx = 5, rowspan = 2, pady = 5)

    genRandCharLabel = Tkinter.Label(leftGenRandFrame, text = "Characters", justify = Tkinter.LEFT)
    genRandCharLabel.grid(row = 0, column = 0, sticky = "w")

    genRandCharTextField = Tkinter.Entry(leftGenRandFrame, textvariable = genRandCharsString)
    genRandCharTextField.grid(row = 1, column = 0, columnspan = 2)

    genRandCharChkChange()

    genRandAnyCharChk = Tkinter.Checkbutton(leftGenRandFrame, text = "Any", justify = Tkinter.RIGHT, variable = genRandAnyChar, command = genRandCharChkChange)
    genRandAnyCharChk.grid(row = 0, column = 1, sticky = "e")

    genRandSeparator1 = ttk.Separator(leftGenRandFrame, orient = Tkinter.HORIZONTAL);
    genRandSeparator1.grid(row = 2, column = 0, columnspan = 2, sticky="ew", pady = 5)

    genRandFgcolorLabel = Tkinter.Label(leftGenRandFrame, text = "Fg. color", justify = Tkinter.LEFT)
    genRandFgcolorLabel.grid(row = 3, column = 0, sticky = "w")

    genRandAnyFgcolorChk = Tkinter.Checkbutton(leftGenRandFrame, text = "Any", justify = Tkinter.RIGHT, variable = genRandAnyFg, command = genRandFgChkChange)
    genRandAnyFgcolorChk.grid(row = 3, column = 1, sticky = "e")

    genRandFgcolorTextField = Tkinter.Entry(leftGenRandFrame, textvariable = genRandFgcolorsString)
    genRandFgcolorTextField.grid(row = 4, column = 0, columnspan = 2)

    genRandFgChkChange()

    genRandSeparator2 = ttk.Separator(leftGenRandFrame, orient = Tkinter.HORIZONTAL);
    genRandSeparator2.grid(row = 5, column = 0, columnspan = 2, sticky="ew", pady = 5)

    genRandBgcolorLabel = Tkinter.Label(leftGenRandFrame, text = "Bg. colors", justify = Tkinter.LEFT)
    genRandBgcolorLabel.grid(row = 6, column = 0, sticky = "w")

    genRandAnyBgcolorChk = Tkinter.Checkbutton(leftGenRandFrame, text = "Any", justify = Tkinter.RIGHT, variable = genRandAnyBg, command = genRandBgChkChange)
    genRandAnyBgcolorChk.grid(row = 6, column = 1, sticky = "e")

    genRandBgcolorTextField = Tkinter.Entry(leftGenRandFrame, textvariable = genRandBgcolorsString)
    genRandBgcolorTextField.grid(row = 7, column = 0, columnspan = 2)

    genRandBgChkChange()

    if(genRandFirstFrameString.get() == ""):
        genRandFirstFrameString.set(str(currentFrame))

    if(genRandLastFrameString.get() == ""):
        genRandLastFrameString.set(str(currentFrame))

    genRandFirstFrameLabel = Tkinter.Label(rightGenRandFrame, text = "First frame", justify = Tkinter.LEFT)
    genRandFirstFrameLabel.grid(row = 0, column = 0)

    genRandFirstFrameEntry = Tkinter.Entry(rightGenRandFrame, width = 10, textvariable = genRandFirstFrameString)
    genRandFirstFrameEntry.grid(row = 0, column = 1)

    genRandLastFrameLabel = Tkinter.Label(rightGenRandFrame, text = "Last frame", justify = Tkinter.LEFT)
    genRandLastFrameLabel.grid(row = 1, column = 0)

    genRandLastFrameEntry = Tkinter.Entry(rightGenRandFrame, width = 10, textvariable = genRandLastFrameString)
    genRandLastFrameEntry.grid(row = 1, column = 1)

    genRandUseThisFrameChkBtn = Tkinter.Checkbutton(rightGenRandFrame, text = "Current frame only", justify = Tkinter.LEFT, variable = genRandThisFrameOnly, command = genRandToggleThisFrameOnly)
    genRandUseThisFrameChkBtn.grid(row = 2, column = 0, columnspan = 2, sticky = "w")

    genRandUseAllFramesChkbtn = Tkinter.Checkbutton(rightGenRandFrame, text = "All frames", justify = Tkinter.LEFT, variable = genRandAllFrames, command = genRandToggleAllFrames)
    genRandUseAllFramesChkbtn.grid(row = 3, column = 0, columnspan = 2, sticky = "w")

    genRandSeparator4 = ttk.Separator(rightGenRandFrame, orient = Tkinter.HORIZONTAL)
    genRandSeparator4.grid(row = 4, column = 0, sticky = "ew", columnspan = 2, pady = 5)

    genRandInSelectionRBtn = Tkinter.Radiobutton(rightGenRandFrame, text = "Generate in selection", justify = Tkinter.LEFT, variable = genRandScope, value = "SELECTION")
    genRandInSelectionRBtn.grid(row = 5, column = 0, sticky = "w", columnspan = 2)

    genRandInFrameRBtn = Tkinter.Radiobutton(rightGenRandFrame, text = "Generate in whole frame", justify = Tkinter.LEFT, variable = genRandScope, value = "FRAME")
    genRandInFrameRBtn.grid(row = 6, column = 0, sticky = "w", columnspan = 2)

    genRandSeparator5 = ttk.Separator(rightGenRandFrame, orient = Tkinter.HORIZONTAL)
    genRandSeparator5.grid(row = 7, column = 0, sticky = "ew", columnspan = 2, pady = 5)

    genRandSeedLabel = Tkinter.Label(rightGenRandFrame, text = "Seed:", justify = Tkinter.LEFT)
    genRandSeedLabel.grid(row = 8, column = 0, sticky = "w")

    genRandSeedEntry = Tkinter.Entry(rightGenRandFrame, width = 10, textvariable = genRandSeedString, justify = Tkinter.LEFT)
    genRandSeedEntry.grid(row = 8, column = 1, sticky = "w")

    if(selectedNumber == 0):
        genRandInSelectionRBtn.config(state = Tkinter.DISABLED)
        genRandScope.set("FRAME")

    #step frame

    genRandStepFrame = Tkinter.Frame(askGenerateRandomWindow)
    genRandStepFrame.grid(row = 0, column = 2, sticky = "n", pady = 5, padx = 5)

    genRandStepLabel = Tkinter.Label(genRandStepFrame, text = "Generation step duration", justify = Tkinter.LEFT)
    genRandStepLabel.grid(row = 0, columnspan = 3)

    genRandSeparator6 = ttk.Separator(genRandStepFrame, orient = Tkinter.HORIZONTAL)
    genRandSeparator6.grid(row = 1, column = 0, sticky = "ew", columnspan = 3, pady = 5)

    genRandConstantRBtn = Tkinter.Radiobutton(genRandStepFrame, text = "Constant", justify = Tkinter.LEFT, variable = genRandStepType, value = "CONST",
                                              command = toggleStepType)
    genRandConstantRBtn.grid(row = 2, column = 0, columnspan = 3, sticky = "w")

    genRandOneFrameRBtn = Tkinter.Radiobutton(genRandStepFrame, text = "1-frame varying", justify = Tkinter.LEFT, variable = genRandStepType, value = "ONE",
                                              command = toggleStepType)
    genRandOneFrameRBtn.grid(row = 3, column = 0, columnspan = 3, sticky = "w")

    genRandMultiFrameRBtn = Tkinter.Radiobutton(genRandStepFrame, text = "", justify = Tkinter.LEFT, variable = genRandStepType, value = "MULTI",
                                                command = toggleStepType)
    genRandMultiFrameRBtn.grid(row = 4, column = 0, sticky = "w")

    genRandMultiFrameEntry = Tkinter.Entry(genRandStepFrame, width = 5, textvariable = genRandStepSizeString)
    genRandMultiFrameEntry.grid(row = 4, column = 1, sticky = "w")
    genRandMultiFrameEntry.bind("<Button-1>",onClickMultiFrame)

    genRandMultiFrameLabel = Tkinter.Label(genRandStepFrame, text = "-frame varying", justify = Tkinter.LEFT)
    genRandMultiFrameLabel.grid(row = 4, column = 2, sticky = "w")
    genRandMultiFrameLabel.bind("<Button-1>",onClickMultiFrame)

    genRandOffsetSubFrame = Tkinter.Frame(genRandStepFrame)
    genRandOffsetSubFrame.grid(row = 5, column = 0, columnspan = 3, sticky = "e", padx = 5)

    genRandOffsetLabel = Tkinter.Label(genRandOffsetSubFrame, text = "Offset", justify = Tkinter.RIGHT)
    genRandOffsetLabel.grid(row = 0, column = 0, sticky = "e")

    genRandOffsetEntry = Tkinter.Entry(genRandOffsetSubFrame, width = 10, justify = Tkinter.RIGHT, textvariable = genRandOffsetString)
    genRandOffsetEntry.grid(row = 0, column = 1, sticky = "e")

    toggleStepType()

    genRandSeparator7 = ttk.Separator(genRandStepFrame, orient = Tkinter.HORIZONTAL)
    genRandSeparator7.grid(row = 6, column = 0, sticky = "ew", columnspan = 3, pady = 5)

    #button frame

    genRandButtonFrame = Tkinter.Frame(askGenerateRandomWindow)
    genRandButtonFrame.grid(row = 1, column = 2, sticky = "s", pady = 5, padx = 5)

    OKBtn = Tkinter.Button(genRandButtonFrame, text = "OK", command = generateRandomFunc)
    OKBtn.grid(row = 2, column = 0, sticky = "s")

    cancelBtn = Tkinter.Button(genRandButtonFrame, text = "Cancel", command = cancelGenerateRandom)
    cancelBtn.grid(row = 2, column = 1, sticky = "s")

    genRandToggleThisFrameOnly()
    genRandToggleAllFrames()

def traceSelection():

    # might not work for some non-4-values-per-pixel images

    global currentFrame, unprintable, images, select_matrix, selectedNumber, mainCanvas, data_matrix, picDict, enterChars, traceType, blockMain, traceChars
    global askTraceWindow, traceFGColors, colorType, fgColorEntry, traceBGColors, bgColorEntry, currentFrame, firstEntry, lastEntry, firstFrame, lastFrame
    global traceFrames

    if not str(currentFrame) in picDict:

        return

    blockMain = True

    askTraceWindow = Tkinter.Toplevel()

    askTraceWindow.protocol("WM_DELETE_WINDOW", cancelTrace)

    askTraceWindow.grab_set()
    askTraceWindow.title("Trace selection")

    traceType = Tkinter.StringVar()
    traceType.set("ALL")

    traceChars = Tkinter.StringVar()

    traceFGColors = Tkinter.StringVar()
    traceFGColors.set("15")

    traceBGColors = Tkinter.StringVar()
    traceBGColors.set("0")

    colorType = Tkinter.StringVar()
    colorType.set("BW")

    bAll = Tkinter.Radiobutton(askTraceWindow, text = "Use whole palette", variable = traceType, value = "ALL", command = selectTraceType)
    bAll.grid(row = 0, column = 0, columnspan = 3)

    bRestricted = Tkinter.Radiobutton(askTraceWindow, text = "Use the following characters:", variable = traceType, value = "RSTR", command = selectTraceType)
    bRestricted.grid(row = 1, column = 0, columnspan = 3)
    
    enterChars = Tkinter.Entry(askTraceWindow, textvariable = traceChars, state = Tkinter.DISABLED)
    enterChars.grid(row=2, column=0, columnspan = 3)

    bBW = Tkinter.Radiobutton(askTraceWindow, text = "Use black and white", variable = colorType, value = "BW", command = selectColorType)
    bBW.grid(row = 3, column=0, columnspan = 3)

    bColors = Tkinter.Radiobutton(askTraceWindow, text = "Use the following FG/BG colors", variable = colorType, value = "C", command = selectColorType)
    bColors.grid(row = 4, column=0, columnspan = 3)

    fgMsg = Tkinter.Message(askTraceWindow, text = "FG: ")
    fgMsg.grid(row = 5, column = 0)

    fgColorEntry = Tkinter.Entry(askTraceWindow, textvariable = traceFGColors, state = Tkinter.DISABLED)
    fgColorEntry.grid(row = 5, column=1, columnspan = 2)

    bgMsg = Tkinter.Message(askTraceWindow, text = "BG: ")
    bgMsg.grid(row = 6, column = 0)

    bgColorEntry = Tkinter.Entry(askTraceWindow, textvariable = traceBGColors, state = Tkinter.DISABLED)
    bgColorEntry.grid(row = 6, column=1, columnspan = 2)

    traceFrames = Tkinter.StringVar()
    traceFrames.set("1")

    bSingleFrame = Tkinter.Radiobutton(askTraceWindow, text = "Trace on current frame", variable = traceFrames, value = "1", command = selectTraceFrames)
    bSingleFrame.grid(row = 7, column = 0, columnspan = 3)

    bMoreFrames = Tkinter.Radiobutton(askTraceWindow, text = "Trace on multiple frames", variable = traceFrames, value = "2", command = selectTraceFrames)
    bMoreFrames.grid(row = 8, column = 0, columnspan = 3)

    firstMsg = Tkinter.Message(askTraceWindow, text = "First: ")
    firstMsg.grid(row = 9, column = 0)

    firstFrame = Tkinter.StringVar()
    firstFrame.set(str(currentFrame))
    
    firstEntry = Tkinter.Entry(askTraceWindow, textvariable = firstFrame, state = Tkinter.DISABLED)
    firstEntry.grid(row = 9, column = 1, columnspan = 2)

    lastMsg = Tkinter.Message(askTraceWindow, text = "Last: ")
    lastMsg.grid(row = 10, column = 0)

    lastFrame = Tkinter.StringVar()
    lastFrame.set(str(currentFrame))

    lastEntry = Tkinter.Entry(askTraceWindow, textvariable = lastFrame, state = Tkinter.DISABLED)
    lastEntry.grid(row = 10, column = 1, columnspan = 2)

    LQButton = Tkinter.Button(askTraceWindow, text = "LQ trace", command = okTraceLQ)
    LQButton.grid(row=11, column=0)

    HQButton = Tkinter.Button(askTraceWindow, text = "HQ trace", command = okTraceHQ)
    HQButton.grid(row=11, column=1)

    CancelButton = Tkinter.Button(askTraceWindow, text = "Cancel", command = cancelTrace)
    CancelButton.grid(row=11, column=2)

def traceSelectionBWHQ():

    # might not work for some non-4-values-per-pixel images

    global currentFrame, unprintable, images, select_matrix, selectedNumber, mainCanvas, data_matrix, picDict, isSaved

    if not str(currentFrame) in picDict:

        return

    theImage = Image.open(picDict[str(currentFrame)][2])
    imageInfo = list(theImage.getdata())

    isSaved = False

    for i in range(50):
        for j in range(80):

            if select_matrix[i][j] != None:

                minDifference = 10000000
                minDifPos = 32
                
                for k in range(256):

                    if k in unprintable:

                        continue

                    letterInfo = list(images[15*256+k].getdata())
                    #print letterInfo
                    difference = 0
                    
                    for i1 in range(8):
                        for j1 in range(8):

                            pixValueLetter = (letterInfo[i1*8+j1][0] + letterInfo[i1*8+j1][1] + letterInfo[i1*8+j1][2]) * (letterInfo[i1*8+j1][3] / 255.0)
                            pixValuePic = (imageInfo[(i*8 + i1) * 640 + j*8 + j1][0] + imageInfo[(i*8 + i1) * 640 + j*8 + j1][1] + imageInfo[(i*8 + i1) * 640 + j*8 + j1][2]) * (imageInfo[(i*8 + i1) * 640 + j*8 + j1][3] / 255.0)
                            #print pixValueLetter, pixValuePic
                            #if pixValuePic!=0:
                                #print pixValueLetter, pixValuePic
                            difference += abs(pixValueLetter - pixValuePic)

                    #print difference

                    if difference < minDifference:

                        minDifference = difference
                        minDifPos = k
                        if minDifference == 0:
                            break
                        #print
                        #print minDifference, minDifPos

                data_matrix[currentFrame][i][j] = (minDifPos,15,0)

    repaint()

def onQuit():

    global isSaved, root

    if not(isSaved):
        doSave = tkMessageBox.askquestion("File not saved", "Save?", type = tkMessageBox.YESNOCANCEL, parent = root)
        if doSave == "cancel":
            return
        if doSave == "yes":
            saveFile()
            return

    root.destroy()

def openFileToMerge():

    global askMergeWindow

    openOptions = {}
    openOptions["parent"] = askMergeWindow
    openOptions["filetypes"] = [("Ascii data", ".asc")]
    openMergeFileName = tkFileDialog.askopenfilename(**openOptions)

    return openMergeFileName

def firstFileBrowse():

    global firstFile

    firstFileString = openFileToMerge()

    if firstFileString != None and firstFileString != "":

        firstFile.set(firstFileString)

def secondFileBrowse():

    global secondFile

    secondFileString = openFileToMerge()

    if secondFileString != None and secondFileString != "":

        secondFile.set(secondFileString)

def outputFileBrowse():

    global outputFile

    outputFileOptions = {}
    outputFileOptions["parent"] = askMergeWindow
    outputFileOptions["filetypes"] = [("Ascii data", ".asc")]
    outputFileString = tkFileDialog.asksaveasfilename(**outputFileOptions)

    if outputFileString != None and outputFileString != "":

        outputFile.set(outputFileString)

def cancelMerge():

    global blockMain, askMergeWindow

    askMergeWindow.grab_release()
    askMergeWindow.destroy()

    blockMain = False

def OKMerge():

    global askMergeWindow, mergeType, blockMain

    if not checkMergeEntries():

        return

    askMergeWindow.grab_release()
    askMergeWindow.destroy()

    blockMain = False

    if mergeType.get() == "A":

        appendFiles()

    else:

        overlapFiles()

def appendFiles():

    global firstFile, secondFile, outputFile, firstFileFirstFrame, firstFileLastFrame, secondFileFirstFrame, secondFileLastFrame

    ffff = int(firstFileFirstFrame.get())
    fflf = int(firstFileLastFrame.get())

    sfff = int(secondFileFirstFrame.get())
    sflf = int(secondFileLastFrame.get())

    output = open(outputFile.get(), "wb")

    file1 = open(firstFile.get(), "rb")
    file2 = open(secondFile.get(), "rb")

    file1.seek(ffff * 8000)
    file2.seek(sfff * 8000)

    output.write(file1.read((fflf - ffff + 1) * 8000))
    output.write(file2.read((sflf - sfff + 1) * 8000))

    output.close()
    file2.close()
    file1.close()

def overlapFiles():

    global firstFile, secondFile, outputFile, firstFileFirstFrame, firstFileLastFrame, secondFileFirstFrame, secondFileLastFrame, secondFileOffset

    ffff = int(firstFileFirstFrame.get())
    fflf = int(firstFileLastFrame.get())

    sfff = int(secondFileFirstFrame.get())
    sflf = int(secondFileLastFrame.get())

    if (secondFileOffset.get())[0] == "-":

        sfo = -int((secondFileOffset.get())[1:])

    else:

        if (secondFileOffset.get())[0] == "+":

            sfo = int((secondFileOffset.get())[1:])

        else:

            sfo = int(secondFileOffset.get())

    output = open(outputFile.get(), "wb")

    file1 = open(firstFile.get(), "rb")
    file2 = open(secondFile.get(), "rb")

    file1.seek(ffff * 8000)
    file2.seek(sfff * 8000)

    if sfo > 0:

        output.write(file1.read(sfo * 8000))

    else:

        output.write(file2.read(-sfo * 8000))

    f1List = file1.read((fflf - ffff + 1) * 8000)
    f2List = file2.read((sflf - sfff + 1) * 8000)

    for i in range(0, min(len(f1List), len(f2List)), 2):

        if ord(f1List[i]) % 8 == 0 and ord(f1List[i + 1]) == 32:

            output.write(f2List[i:i+2])

        else:

            output.write(f1List[i:i+2])

    if len(f1List) > len(f2List):

        output.write(f1List[len(f2List):])

    if len(f1List) < len(f2List):

        output.write(f2List[len(f1List):])

    output.close()
    file1.close()
    file2.close()

def selectMergeType():

    global mergeType, secondFileOffsetEntry

    if mergeType.get() == "A":

        secondFileOffsetEntry.config(state = Tkinter.DISABLED)

    else:

        secondFileOffsetEntry.config(state = Tkinter.NORMAL)

def checkFirstFileEntry():

    global firstFile

    if ((firstFile.get())[-4:]).lower() != ".asc":

        return False

    if not os.path.exists(firstFile.get()):

        return False

    return True

def checkSecondFileEntry():

    global secondFile

    if ((secondFile.get())[-4:]).lower() != ".asc":

        return False

    if not os.path.exists(secondFile.get()):

        return False

    return True

def checkMergeEntries():

    global outputFile, firstFileFirstFrame, firstFileLastFrame, secondFileFirstFrame, secondFileLastFrame, firstFile, secondFile
    global mergeType, secondFileOffset

    selectFirstFileFramesTypeNoChange()
    selectSecondFileFramesTypeNoChange()

    if not checkFirstFileEntry:

        tkMessageBox.showerror("Error", "Invalid first input file")
        return False

    if not checkSecondFileEntry:

        tkMessageBox.showerror("Error", "Invalid second input file")
        return False

    if (outputFile.get()[-4:]) != ".asc":

        outputFile.set(outputFile.get() + ".asc")

    try:

        out = open(outputFile.get(), "wb")
        out.close()

    except:

        tkMessageBox.showerror("Error", "Invalid output file")
        return False

    if not firstFileFramesType == "ALL":

        if not firstFileFirstFrame.get().isdigit() or int(firstFileFirstFrame.get()) >= (os.path.getsize(firstFile.get()) / 8000):

            tkMessageBox.showerror("Error", "Invalid first frame for first file")
            return False

        if not firstFileLastFrame.get().isdigit() or int(firstFileLastFrame.get()) >= (os.path.getsize(firstFile.get()) / 8000):

            tkMessageBox.showerror("Error", "Invalid last frame for first file")
            return False

        if int(firstFileLastFrame.get()) < int(firstFileFirstFrame.get()):

            tkMessageBox.showerror("Error", "For first file, last frame must be greater than first frame")
            return False

    if not secondFileFramesType == "ALL":

        if not secondFileFirstFrame.get().isdigit() or int(secondFileFirstFrame.get()) >= (os.path.getsize(secondFile.get()) / 8000):

            tkMessageBox.showerror("Error", "Invalid first frame for second file")
            return False

        if not secondFileLastFrame.get().isdigit() or int(secondFileLastFrame.get()) >= (os.path.getsize(secondFile.get()) / 8000):

            tkMessageBox.showerror("Error", "Invalid last frame for second file")
            return False

        if int(secondFileLastFrame.get()) < int(secondFileFirstFrame.get()):

            tkMessageBox.showerror("Error", "For second file, last frame must be greater than first frame")
            return False

    if mergeType == "O":

        if not (((secondFileOffset.get())[1:]).isdigit() and (secondFileOffset[0] == "+" or secondFileOffset == "-" or ((secondFileOffset.get())[0]).isdigit())):

            tkMessageBox.showerror("Error", "Invalid second file offset")
            return False

        else:

            if ((secondFileOffset.get())[0]).isdigit() and int(secondFileOffset.get()) > int(firstFileLastFrame) - int(firstFileFirstFrame) + 1:

                tkMessageBox.showerror("Error", "Positive second file offset cannot be greater than the number of frames used from the first file")
                return False

            if (secondFileOffset.get())[0] == "+" and int((secondFileOffset.get())[1:]) > int(firstFileLastFrame) - int(firstFileFirstFrame) + 1:

                tkMessageBox.showerror("Error", "Positive second file offset cannot be greater than the number of frames used from the first file")
                return False

            if (secondFileOffset.get())[0] == "-" and -int((secondFileOffset.get())[1:]) > int(firstFileLastFrame) - int(firstFileFirstFrame) + 1:

                tkMessageBox.showerror("Error", "Negative second file offset cannot be greater than the number of frames used from the second file")
                return False
                
    return True

def selectFirstFileFramesType():

    global firstFileFramesType, firstFileFirstFrame, firstFileLastFrame, firstFileFirstFrameEntry, firstFileLastFrameEntry, firstFile

    if firstFileFramesType.get() == "ALL":

        firstFileFirstFrameEntry.config(state = Tkinter.DISABLED)
        firstFileLastFrameEntry.config(state = Tkinter.DISABLED)

        if checkFirstFileEntry():

            firstFileFirstFrame.set("0")
            firstFileLastFrame.set(str(os.path.getsize(firstFile.get()) / 8000 - 1))

        else:

            firstFileFirstFrame.set("")
            firstFileLastFrame.set("")

    else:

        if checkFirstFileEntry():
        
            firstFileFirstFrameEntry.config(state = Tkinter.NORMAL)
            firstFileLastFrameEntry.config(state = Tkinter.NORMAL)

            firstFileFirstFrame.set("")
            firstFileLastFrame.set("")

def selectFirstFileFramesTypeNoChange():

    global firstFileFramesType, firstFileFirstFrame, firstFileLastFrame, firstFileFirstFrameEntry, firstFileLastFrameEntry, firstFile

    if firstFileFramesType.get() == "ALL":

        firstFileFirstFrame.set("0")
        firstFileLastFrame.set(str(os.path.getsize(firstFile.get()) / 8000 - 1))

def selectSecondFileFramesType():

    global secondFileFramesType, secondFileFirstFrame, secondFileLastFrame, secondFileFirstFrameEntry, secondFileLastFrameEntry, secondFile

    if secondFileFramesType.get() == "ALL":

        secondFileFirstFrameEntry.config(state = Tkinter.DISABLED)
        secondFileLastFrameEntry.config(state = Tkinter.DISABLED)

        if checkSecondFileEntry():

            secondFileFirstFrame.set("0")
            secondFileLastFrame.set(str(os.path.getsize(secondFile.get()) / 8000 - 1))

        else:

            secondFileFirstFrame.set("")
            secondFileLastFrame.set("")

    else:

        if checkSecondFileEntry():
        
            secondFileFirstFrameEntry.config(state = Tkinter.NORMAL)
            secondFileLastFrameEntry.config(state = Tkinter.NORMAL)

            secondFileFirstFrame.set("")
            secondFileLastFrame.set("")

def selectSecondFileFramesTypeNoChange():

    global secondFileFramesType, secondFileFirstFrame, secondFileLastFrame, secondFileFirstFrameEntry, secondFileLastFrameEntry, secondFile

    if secondFileFramesType.get() == "ALL":

        secondFileFirstFrame.set("0")
        secondFileLastFrame.set(str(os.path.getsize(secondFile.get()) / 8000 - 1))

def mergeFiles():

    global blockMain, askMergeWindow, mergeType, firstFileEntry, firstFileFramesType, firstFileFirstFrame, firstFileLastFrame, firstFile
    global FileEntry, secondFileFramesType, secondFileFirstFrame, secondFileLastFrame, secondFile, secondFileOffsetEntry, secondFileOffset, outputFile
    global firstFileFirstFrameEntry, firstFileLastFrameEntry, secondFileFirstFrameEntry, secondFileLastFrameEntry

    blockMain = True

    askMergeWindow = Tkinter.Toplevel()
    askMergeWindow.grab_set()
    askMergeWindow.protocol("WM_DESTROY_WINDOW", cancelMerge)

    mergeType = Tkinter.StringVar()
    mergeType.set("A")

    appendBtn = Tkinter.Radiobutton(askMergeWindow, text = "Append", variable = mergeType, value = "A", command = selectMergeType, anchor = Tkinter.W)
    appendBtn.grid(row = 0, column = 0, columnspan = 2, sticky = "w")

    overlapBtn = Tkinter.Radiobutton(askMergeWindow, text = "Overlap", variable = mergeType, value = "O", command = selectMergeType, anchor = Tkinter.W)
    overlapBtn.grid(row = 1, column = 0, columnspan = 2, sticky = "w")

    sep1 = ttk.Separator(askMergeWindow)
    sep1.grid(row = 2, column = 0, columnspan = 2, sticky = Tkinter.E + Tkinter.W, pady = 15)

    firstFileMsg = Tkinter.Message(askMergeWindow, text = "First file:", width = 150, justify = Tkinter.LEFT)
    firstFileMsg.grid(row = 3, column = 0, columnspan = 2, sticky = "w")

    firstFile = Tkinter.StringVar()
    firstFile.set("")

    firstFileEntry = Tkinter.Entry(askMergeWindow, textvariable = firstFile)
    firstFileEntry.grid(row = 4, column = 0)

    firstFileBrowseBtn = Tkinter.Button(askMergeWindow, command = firstFileBrowse, text = "Browse...")
    firstFileBrowseBtn.grid(row = 4, column = 1)

    firstFileFramesType = Tkinter.StringVar()
    firstFileFramesType.set("ALL")

    firstFileUAFBtn = Tkinter.Radiobutton(askMergeWindow, anchor = Tkinter.W, command = selectFirstFileFramesType, text = "Use all frames", value = "ALL", variable = firstFileFramesType)
    firstFileUAFBtn.grid(row = 5, column = 0, columnspan = 2, sticky = "w")

    firstFileUFFBtn = Tkinter.Radiobutton(askMergeWindow, anchor = Tkinter.W, command = selectFirstFileFramesType, text = "Use the following frames:", value = "SOME", variable = firstFileFramesType)
    firstFileUFFBtn.grid(row = 6, column = 0, columnspan = 2, sticky = "w")

    firstFileFirstFrame = Tkinter.StringVar()
    firstFileFirstFrame.set("")

    firstFileFirstFrameEntry = Tkinter.Entry(askMergeWindow, textvariable = firstFileFirstFrame, state = Tkinter.DISABLED)
    firstFileFirstFrameEntry.grid(row = 7, column = 0, columnspan = 2)

    firstFileLastFrame = Tkinter.StringVar()
    firstFileLastFrame.set("")

    firstFileLastFrameEntry = Tkinter.Entry(askMergeWindow, textvariable = firstFileLastFrame, state = Tkinter.DISABLED)
    firstFileLastFrameEntry.grid(row = 8, column = 0, columnspan = 2)

    sep2 = ttk.Separator(askMergeWindow)
    sep2.grid(row = 9, column = 0, columnspan = 2, sticky = Tkinter.E + Tkinter.W, pady = 15)

    secondFileMsg = Tkinter.Message(askMergeWindow, text = "Second file:", width = 150, justify = Tkinter.LEFT)
    secondFileMsg.grid(row = 10, column = 0, columnspan = 2, sticky = "w")

    secondFile = Tkinter.StringVar()
    secondFile.set("")

    secondFileEntry = Tkinter.Entry(askMergeWindow, textvariable = secondFile)
    secondFileEntry.grid(row = 11, column = 0)

    secondFileBrowseBtn = Tkinter.Button(askMergeWindow, command = secondFileBrowse, text = "Browse...")
    secondFileBrowseBtn.grid(row = 11, column = 1)

    secondFileFramesType = Tkinter.StringVar()
    secondFileFramesType.set("ALL")

    secondFileUAFBtn = Tkinter.Radiobutton(askMergeWindow, anchor = Tkinter.W, command = selectSecondFileFramesType, text = "Use all frames", value = "ALL", variable = secondFileFramesType)
    secondFileUAFBtn.grid(row = 12, column = 0, columnspan = 2, sticky = "w")

    secondFileUFFBtn = Tkinter.Radiobutton(askMergeWindow, anchor = Tkinter.W, command = selectSecondFileFramesType, text = "Use the following frames:", value = "SOME", variable = secondFileFramesType)
    secondFileUFFBtn.grid(row = 13, column = 0, columnspan = 2, sticky = "w")

    secondFileFirstFrame = Tkinter.StringVar()
    secondFileFirstFrame.set("")

    secondFileFirstFrameEntry = Tkinter.Entry(askMergeWindow, textvariable = secondFileFirstFrame, state = Tkinter.DISABLED)
    secondFileFirstFrameEntry.grid(row = 14, column = 0, columnspan = 2)

    secondFileLastFrame = Tkinter.StringVar()
    secondFileLastFrame.set("")

    secondFileLastFrameEntry = Tkinter.Entry(askMergeWindow, textvariable = secondFileLastFrame, state = Tkinter.DISABLED)
    secondFileLastFrameEntry.grid(row = 15, column = 0, columnspan = 2)

    secondFileOffsetMsg = Tkinter.Message(askMergeWindow, text = "Second file offset (+/-):", width = 150, justify = Tkinter.LEFT)
    secondFileOffsetMsg.grid(row = 16, column = 0, columnspan = 2, sticky = "w")

    secondFileOffset = Tkinter.StringVar()
    secondFileOffset.set("0")

    secondFileOffsetEntry = Tkinter.Entry(askMergeWindow, textvariable = secondFileOffset, state = Tkinter.DISABLED)
    secondFileOffsetEntry.grid(row = 17, column = 0, columnspan = 2)

    sep3 = ttk.Separator(askMergeWindow)
    sep3.grid(row = 18, column = 0, columnspan = 2, sticky = Tkinter.E + Tkinter.W, pady = 15)

    outputMsg = Tkinter.Message(askMergeWindow, text = "Output file:", width = 150, justify = Tkinter.LEFT)
    outputMsg.grid(row = 19, column = 0, columnspan = 2, sticky = "w")

    outputFile = Tkinter.StringVar()
    outputFile.set("")

    outputFileEntry = Tkinter.Entry(askMergeWindow, textvariable = outputFile)
    outputFileEntry.grid(row = 20, column = 0)

    outputFileBrowseBtn = Tkinter.Button(askMergeWindow, text = "Browse...", command = outputFileBrowse)
    outputFileBrowseBtn.grid(row = 20, column = 1)

    sep4 = ttk.Separator(askMergeWindow)
    sep4.grid(row = 21, column = 0, columnspan = 2, sticky = Tkinter.E + Tkinter.W, pady = 15)

    OKCancelFrame = Tkinter.Frame(askMergeWindow)
    OKCancelFrame.grid(row = 22, column = 0, columnspan = 2)

    MergeOKButton = Tkinter.Button(OKCancelFrame, text = "OK", command = OKMerge)
    MergeOKButton.grid(row = 0, column = 0, sticky = "e")

    MergeCancelButton = Tkinter.Button(OKCancelFrame, text = "Cancel", command = cancelMerge)
    MergeCancelButton.grid(row = 0, column = 1, sticky = "w")

    

# interface

mainFrame=Tkinter.Frame(root,bd=0)
mainFrame.grid(row=0,column=0)

mainCanvas=Tkinter.Canvas(mainFrame,height=410,width=650)
mainCanvas.grid(row=0,column=0,rowspan=3)

paletteCanvas=Tkinter.Canvas(mainFrame,height=330, width=85)
paletteCanvas.grid(row=0, column=1)

bgCanvas=Tkinter.Canvas(mainFrame, height=12, width= 85)
bgCanvas.grid(row=1, column=1)

fgCanvas=Tkinter.Canvas(mainFrame, height=24, width=85)
fgCanvas.grid(row=2, column=1)

# frameCanvas = Tkinter.Canvas(mainFrame, height=16, width = 610, bg = "gray")
# frameCanvas.grid(row=3, column=0)

#frameCanvas.create_rectangle(i_offset, j_offset,

mainCanvas.bind("<Button-1>",onClick)
mainCanvas.bind("<B1-Motion>",onDrag)
mainCanvas.bind("<ButtonRelease-1>",onRelease)
mainCanvas.bind("<Button-3>",onSelect)
mainCanvas.bind("<B3-Motion>",onSelectDrag)
mainCanvas.bind("<ButtonRelease-3>",onSelectRelease)

mainCanvas.bind_all("<Return>",onEnter)
mainCanvas.bind_all("<Control-x>",onCut)
mainCanvas.bind_all("<Control-c>",onCopy)
mainCanvas.bind_all("<Control-v>",onPaste)
mainCanvas.bind_all("<Control-z>",onUndo)
mainCanvas.bind_all("<Control-y>",onRedo)

paletteCanvas.bind("<Button-1>",onClickLetter)

bgCanvas.bind("<Button-1>",onClickBg)

fgCanvas.bind("<Button-1>",onClickFg)

# frameCanvas.bind("<Button-3>",showFramePopup)

menubar = Tkinter.Menu(root)

fileMenu = Tkinter.Menu(menubar,tearoff=0)
fileMenu.add_command(label="New",command=newFile)
fileMenu.add_command(label="Open",command=openFile)
fileMenu.add_command(label="Save",command=saveFile)
fileMenu.add_separator()
fileMenu.add_command(label="Export current frame",command=exportCurrentFrameDialog)
fileMenu.add_command(label="Export image sequence",command=exportImageSequenceDialog)
fileMenu.add_separator()
fileMenu.add_command(label="Merge files...", command = mergeFiles)
menubar.add_cascade(label="File",menu=fileMenu)

editMenu = Tkinter.Menu(menubar,tearoff=0)
editMenu.add_command(label="Flip selection horizontally",command=flipSelectionHoriz)
editMenu.add_command(label="Flip selection vertically",command=flipSelectionVert)
editMenu.add_command(label="Remove spaces from selection",command=removeSpacesFromSelection)
editMenu.add_command(label="Select spaces in selection",command=selectSpacesInSelection)
editMenu.add_command(label="Trace selection", command=traceSelection)
editMenu.add_command(label="Find and replace", command=findAndReplace)
editMenu.add_command(label="Generate random", command=generateRandom)
editMenu.add_separator()
editMenu.add_command(label="Insert image",command=insertImage)
editMenu.add_command(label="Insert image sequence",command=insertImageSequence)
editMenu.add_command(label="Clear this image", command=clearThisImage)
editMenu.add_command(label="Clear all images", command=clearPicDict)
editMenu.add_separator()
editMenu.add_command(label="Clear float and selection", command=resetFloatAndSelection)
editMenu.add_command(label="Reset undo", command=resetUndo)
menubar.add_cascade(label="Edit",menu=editMenu)

root.config(menu=menubar)

buttonFrame1=Tkinter.Frame(root,bd=0)
buttonFrame1.grid(row=1,column=0)

buttonFrame2 = Tkinter.Frame(root,bd=0)
buttonFrame2.grid(row=2,column=0)

buttonFrame3 = Tkinter.Frame(root,bd=0)
buttonFrame3.grid(row=3,column=0)

firstFrameButton = Tkinter.Button(buttonFrame1,text="<<",command=gotoFirstFrame)
firstFrameButton.grid(row=0,column=0)

prevFrameButton = Tkinter.Button(buttonFrame1,text="<",command=gotoPrevFrame)
prevFrameButton.grid(row=0,column=1)

currentFrameString = Tkinter.StringVar()
currentFrameString.set(str(currentFrame))

currentFrameEntry = Tkinter.Entry(buttonFrame1, justify = Tkinter.CENTER, textvariable = currentFrameString, width = 4)
currentFrameEntry.grid(row=0,column=2)

nextFrameButton = Tkinter.Button(buttonFrame1,text=">",command=gotoNextFrame)
nextFrameButton.grid(row=0,column=3)

lastFrameButton = Tkinter.Button(buttonFrame1,text=">>",command=gotoLastFrame)
lastFrameButton.grid(row=0,column=4)

undoButton = Tkinter.Button(buttonFrame2,text="Undo",command=undo)
undoButton.grid(row=1,column=0)

redoButton = Tkinter.Button(buttonFrame2,text="Redo",command=redo)
redoButton.grid(row=1,column=1)

insertFrameButton = Tkinter.Button(buttonFrame2,text="+",command=insertFrame)
insertFrameButton.grid(row=1,column=2)

deleteFrameButton = Tkinter.Button(buttonFrame2,text="-",command=deleteFrame)
deleteFrameButton.grid(row=1,column=3)

duplicateFrameButton = Tkinter.Button(buttonFrame3,text="Duplicate frame",command=duplicateFrame)
duplicateFrameButton.grid(row=0,column=0)

hideShowImagesButton = Tkinter.Button(buttonFrame3,text="Hide/Show images",command=hideShowImages)
hideShowImagesButton.grid(row=0,column=1)

imagesFrontBackButton = Tkinter.Button(buttonFrame3,text="Images front/back",command=imagesFrontBack)
imagesFrontBackButton.grid(row=0,column=2)

palette_bg = paletteCanvas.create_rectangle(1,1,83,323,fill=pBrush.bgColor[0],width=1,outline=pBrush.bgColor[0])

for i in range(4096):
    images+=[Image.open("letters/l/"+str(i)+".png")]
    letters+=[ImageTk.PhotoImage(images[i])]

flipFileHoriz = open("fliph.cfg")
flipListHoriz = []
flipFileVert = open("flipv.cfg")
flipListVert = []

for i in range(256):

    s = flipFileHoriz.readline()
    flipListHoriz += [int(s[:-1])]

    s = flipFileVert.readline()
    flipListVert += [int(s[:-1])]

flipFileHoriz.close()
flipFileVert.close()

spacecopy = ImageTk.PhotoImage(images[32])

# frameRects = []
# frameTexts = []

# frameRects += [frameCanvas.create_rectangle(j_offset, 4, j_offset+8, 16, fill=fgColorDict["lightcyan"][0], width=0)]
# frameTexts += [frameCanvas.create_image(j_offset, 6, anchor=Tkinter.NW, image = letters[254+256*fgColorDict["white"][1]])]

# for j in range(1,60):
    # frameRects += [frameCanvas.create_rectangle(j*10+j_offset, 4, j*10+j_offset+8, 16, fill=fgColorDict["white"][0], width=0)]
    # frameTexts += [frameCanvas.create_image(j*10+j_offset, 6, anchor=Tkinter.NW, image = letters[32+256*15])]

for i in range(32):
    for j in range(8):
        rectsPalette+=[paletteCanvas.create_image(j*10+j_offset_p+2,i*10+i_offset_p+2,anchor=Tkinter.NW,image=letters[256*pBrush.fgColor[1]+i*8+j])]
        
for j in range(50):
    for i in range(80):
        rects+=[mainCanvas.create_rectangle(i*8+i_offset,j*8+j_offset,i*8+8+i_offset,j*8+8+j_offset,fill=pBrush.bgColor[0],width=0)]

for j in range(50):
    data_matrix[0] += [[]]
    for i in range(80):
        texts+=[mainCanvas.create_image(i*8+i_offset,j*8+j_offset,anchor=Tkinter.NW,image=spacecopy)]
        data_matrix[0][j]+=[(32,pBrush.fgColor[1],pBrush.bgColor[1])]

for j in range(50):
    select_matrix += [[None]*80]

#print letters[256*pBrush.fgColor[1]+pBrush.letter].height()
#print letters[256*pBrush.fgColor[1]+pBrush.letter].width()

bgcolors = ["black","blue","green","cyan","red","magenta","brown","lightgray"]
fgcolors = bgcolors + ["darkgray","lightblue","lightgreen","lightcyan","lightred","lightmagenta","yellow","white"]

for i in range(8):
    rectsBg+=[bgCanvas.create_rectangle(i*10+4,4,i*10+12,12,fill=bgColorDict[bgcolors[i]][0],width=0)]

bgColor_select_bg = bgCanvas.create_rectangle(pBrush.bgColor[1]*10+3,3,pBrush.bgColor[1]*10+12,12,width=2,outline="blue")

for i in range(2):
    for j in range(8):
        rectsFg+=[fgCanvas.create_rectangle(j*10+4,i*10+4,j*10+12,i*10+12,fill=fgColorDict[fgcolors[i*8+j]][0],width=0)]

fgColor_select_bg = fgCanvas.create_rectangle(pBrush.fgColor[1]%8*10+3,pBrush.fgColor[1]/8*10+3,pBrush.fgColor[1]%8*10+12,pBrush.fgColor[1]/8*10+12,width=2,outline="blue")

palette_select_bg = paletteCanvas.create_rectangle(-10,-10,-5,-5,outline = "blue",width=2)

root.protocol("WM_DELETE_WINDOW", onQuit)

root.mainloop()
