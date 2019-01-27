
import sys

import pymel.core as pm
import bTools.constants as k
from maya import cmds


def moveToOrigo(node=None):
    if not node:
        for node in pm.selected():
            moveToOrigo(node)
        return
    
    pm.move(node, [0,0,0], rpr=True)
    

def moveToOrigoOrWeightHammer():
    selectedComponents = filter(lambda x: isinstance(x, (pm.MeshVertex, pm.MeshEdge, pm.MeshFace)), pm.selected())
    if not selectedComponents:
        moveToOrigo()
    else:
        pm.mel.weightHammerVerts()


def saveSelection():
    pm.optionVar[k.OptionVars.SavedSelection] = cmds.ls(sl=True)


def selectSavedSelection():
    savedSel = pm.optionVar.get(k.OptionVars.SavedSelection)
    if savedSel:
        cmds.select(savedSel, add=True)


def deselectSavedSelection():
    savedSel = pm.optionVar.get(k.OptionVars.SavedSelection)
    if savedSel:
        cmds.select(savedSel, deselect=True)

        
def exportAllToSameName():
    if not pm.sceneName():
        return
    fbxPath = pm.sceneName().replace(".ma", ".fbx").replace(".mb", ".fbx").replace("\\", "/")
    pm.mel.FBXExportFileVersion(v="FBX201400")
    pm.mel.eval('file -force -options "v=0;" -type "FBX export" -pr -ea "{}";'.format(fbxPath))
    sys.stdout.write("Exported FBX: {}\n".format(fbxPath))