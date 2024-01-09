import maya.cmds as cmds

# Name
def indexToID(index):
    if index >= 0:
        ID = 'P' + str(index)
    else:
        ID = 'N' + str(abs(index))
    return ID
def IDToIndex(ID):
    if ID[0] == 'P':
        index = int(ID[1:])
    elif ID[0]== 'N':
        index = -1 * int(ID[1:])
    else:
        return 0
    return index
def iToShaderName(i):
    return f'MB_S_Ramp_{i}'
def indexToMeshName(index):
    meshName = 'MB_Mesh_' + indexToID(index)
    return meshName
def IDToMeshName(ID):
    meshName =  'MB_Mesh_' + ID
    return meshName
def IDToMeshShapeNode(ID):
    return 'MB_Mesh_' + ID +'Shape'
def meshNameToIndex(meshName):
    ID = meshName[8:]
    index = IDToIndex(ID)
    return index
def meshNameToID(meshName):
    return meshName[8:]
def indexToJntName(index):
    return 'MB_Jnt_' + indexToID(index)
def IDToJntName(ID):
    return 'MB_Jnt_' + ID
def jntNameToIndex(jntName):
    return IDToIndex(jntName[8:])
def jntNameToID(jntName):
    return jntName[8:]
def jntAddSuffix(jntName, i):
    return jntName + '_' + str(i)
def indexToSkinClusterName(index):
    return 'MB_SkinCluster_' + indexToID(index)
def IDToSkinClusterName(ID):
    return 'MB_SkinCluster_' + ID
def skinClusterNameToIndex(skinClusterName):
    return IDToIndex(skinClusterName[15:])
def skinClusterNameToID(skinClusterName):
    return skinClusterName[15:]
def indexToCrvName(index):
    return 'MB_Crv_' + indexToID(index)
def IDToCrvName(ID):
    return 'MB_Crv_' + ID
def IDToCrvShapeName(ID):
    return 'MB_Crv_Shape_' + ID
def crvNameToIndex(crvName):
    return IDToIndex(crvName[8:])
def crvNameToID(crvName):
    return crvName[8:]
def indexToIKHandleName(index):
    return 'MB_IKHandle_' + indexToID(index)
def IDToIKHandleName(ID):
    return 'MB_IKHandle_' + ID
def IKHandleNameToIndex(ikhandleName):
    return IDToIndex(ikhandleName[12:])
def IKHandleNameToID(ikhandleName):
    return ikhandleName[12:]
def IDToControlerName(ID):
    return 'MB_Ctrler_' + ID
def controlerNameToID(controlerName):
    return controlerName[10:]
def IDToBSName(ID):
    return 'MB_BS_'+ID
def IDToComputeCoreName():
    return 'MB_CmptCore_'+ID
def indexToMiddleIDs(middleTotalIndex):
    return [f'Mid{id}' for id in range(middleTotalIndex)]
def BSIDToIndex(BSID):
    return int(BSID[2:])
# Create Rig
def indexRange(totalIndex):
    return range(-1 * totalIndex, totalIndex + 1)
def createMBShader(colorList):
    rampfix = []
    for i in colorList:
        tubfix = [x / 255 for x in i]
        rampfix.append(tubfix)
    for index in range(len(colorList)):
        shaderBallName = f'MB_S_Ramp_{index}'
        deleteIfExist(shaderBallName)
        MB_S_Ramp = cmds.shadingNode('blinn',asShader=True,name = shaderBallName)
        cmds.setAttr(MB_S_Ramp+'.color',rampfix[index][0],rampfix[index][1],rampfix[index][2],type='double3')
        cmds.setAttr(MB_S_Ramp + '.transparency', 0.3, 0.3,0.3, type='double3')
def deleteIfExist(name):
    if cmds.objExists(name):
        cmds.delete(name)
def getJntPosList(width, subDivWidth):
    jntPosList = []
    for i in range(subDivWidth + 1):
        y = i * width / subDivWidth
        pos = (0, y, 0)
        jntPosList.append(pos)

    return jntPosList
def getCVsPosList(cvsMaxIndex, width):
    cvsList = []
    interval = width / (cvsMaxIndex - 1)

    for i in range(cvsMaxIndex):
        y = interval * i
        pos = (0, y, 0)
        cvsList.append(pos)

    return cvsList
def createRigTree():
    # MagicBookGrp
    # Main
    # CtrlCenter
    # DeformationSystem
    # CurveGrp
    # IKHandleGrp
    # JntGrp
    # Geo
    cmds.select(clear=True)
    levelName = 'MagicBookGrp'
    parentName = None
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'Main'
    parentName = 'MagicBookGrp'
    deleteIfExist(levelName)
    cmds.circle(n=levelName, normal=[0, 1, 0], radius=5)
    cmds.parent(levelName, parentName)

    levelName = 'Geo'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)
    cmds.setAttr('Geo.inheritsTransform',False)

    levelName = 'CtrlCenter'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'DeformationSystem'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'CurveGrp'
    parentName = 'DeformationSystem'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'IKHandleGrp'
    parentName = 'DeformationSystem'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'JntGrp'
    parentName = 'DeformationSystem'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'BSGrp'
    parentName = 'DeformationSystem'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)
def createMesh(ID, width, height, subDivWidth, subDivHeight):
    cmds.select(clear=True)
    meshName = IDToMeshName(ID)
    deleteIfExist(meshName)
    mesh = cmds.polyPlane(name=meshName, w=width, h=height, sw=subDivWidth, sh=subDivHeight)
    plugHandle = '.rotatePivotX'
    cmds.setAttr(meshName + plugHandle, -width / 2)
    plugHandle = '.tx'
    cmds.setAttr(meshName + plugHandle, width / 2)
    plugHandle = '.rz'
    cmds.setAttr(meshName + plugHandle, 90)
    cmds.makeIdentity(mesh, apply=True, rotate=True, scale=True, translate=True)
    cmds.delete(constructionHistory=True)
    cmds.parent(meshName, 'Geo')
def createJointChain(ID, width, subDivWidth):
    cmds.select('JntGrp')
    jntName = IDToJntName(ID)
    jntPosList = getJntPosList(width, subDivWidth)
    for jntIndex in range(len(jntPosList)):
        jntNameSuffix = jntAddSuffix(jntName, jntIndex)
        jntPos = jntPosList[jntIndex]
        deleteIfExist(jntNameSuffix)
        cmds.joint(n=jntNameSuffix, p=jntPos, radius=0.1)
def bindSkin(ID):
    meshName = IDToMeshName(ID)
    jntName = IDToJntName(ID)
    jntName = jntAddSuffix(jntName, 0)
    skinClusterName = IDToSkinClusterName(ID)
    if not (cmds.objExists(meshName) and cmds.objExists(jntName)):
        print(meshName, 'or', jntName, 'missing')
        return
    deleteIfExist(skinClusterName)
    cmds.skinCluster(jntName, meshName, name=skinClusterName)
def injectJntWeight(ID, subDivWidth, subDivHeight):
    skinClusterName = IDToSkinClusterName(ID)
    weightListHandle = '.weightList'
    weightsHandle = '.weights'
    totalJntIndex = subDivWidth + 1
    totalPointIndex = (subDivWidth + 1) * (subDivHeight + 1)
    for point in range(totalPointIndex):
        column = point % (subDivWidth + 1)
        for joint in range(totalJntIndex):
            attributeName = f'{skinClusterName}{weightListHandle}[{point}]{weightsHandle}[{joint}]'
            if joint == column:
                cmds.setAttr(attributeName, 1.0)
            else:
                cmds.setAttr(attributeName, 0.0)
def createCVCurve(ID, width, cvsMaxIndex=4):
    cmds.select(clear=True)
    crvName = IDToCrvName(ID)
    deleteIfExist(crvName)
    cvsList = getCVsPosList(cvsMaxIndex, width)
    cmds.curve(name=crvName, p=cvsList)
    cmds.parent(crvName, 'CurveGrp')
    children = cmds.listRelatives(crvName, children=True, fullPath=False)
    crvShapeName = IDToCrvShapeName(ID)
    cmds.rename(children[0],crvShapeName)
    cmds.hide(crvShapeName)
def createIKHandle(ID, subDivWidth):
    cmds.select(clear=True)
    ikHandleName = IDToIKHandleName(ID)
    curveName = IDToCrvName(ID)
    jointName = IDToJntName(ID)
    jointStart = jntAddSuffix(jointName, 0)
    jointEnd = jntAddSuffix(jointName, subDivWidth)
    deleteIfExist(ikHandleName)
    cmds.ikHandle(name=ikHandleName, startJoint=jointStart, endEffector=jointEnd, createCurve=False,
                  curve=curveName, solver='ikSplineSolver',parentCurve=False)
    cmds.parent(ikHandleName, 'IKHandleGrp')
    cmds.hide(ikHandleName)
def createControler(ID,width,cvsMaxIndex=4):
    controlerName = IDToControlerName(ID)
    curveName = IDToCrvName(ID)
    curveShapeName = IDToCrvShapeName(ID)
    cvsList = getCVsPosList(cvsMaxIndex, width)
    for i in range(cvsMaxIndex):
        controlerName_suffix = controlerName+'_'+str(i)
        cmds.sphere(name=controlerName_suffix,radius=0.5,sections=1)
        plugHandle = '.tx'
        cmds.setAttr(controlerName_suffix+plugHandle,cvsList[i][0])
        plugHandle = '.ty'
        cmds.setAttr(controlerName_suffix + plugHandle, cvsList[i][1])
        plugHandle = '.tz'
        cmds.setAttr(controlerName_suffix + plugHandle, cvsList[i][2])
        plugHandle = '.rz'
        cmds.setAttr(controlerName_suffix + plugHandle, 90)
        cmds.makeIdentity(controlerName_suffix, apply=True, rotate=True, scale=True, translate=False)
        cmds.parent(controlerName_suffix,curveName)
        cmds.delete(constructionHistory=True)
        shapeNodePlug = f'.controlPoints[{i}]'

        plugHandle = '.tx'
        dsPlugHandle = '.xValue'
        cmds.connectAttr(controlerName_suffix+plugHandle,curveShapeName+shapeNodePlug+dsPlugHandle)

        plugHandle = '.ty'
        dsPlugHandle = '.yValue'
        cmds.connectAttr(controlerName_suffix + plugHandle, curveShapeName + shapeNodePlug + dsPlugHandle)

        plugHandle = '.tz'
        cmds.setAttr(controlerName_suffix + plugHandle,lock=True,keyable=False,channelBox=False)
        plugHandle = '.rx'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.ry'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.rz'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.sx'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.sy'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.sz'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.v'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)

        shaderName = f'MB_S_Ramp_{i}'
        cmds.hyperShade(assign=shaderName)

def createGuides(width, height, subDivWidth, subDivHeight, cvsMaxIndex):
    GuideIDs=['LL','LR','RL','RR']
    for i in range(len(GuideIDs)):
        shaderName = iToShaderName(4+i)
        ID = GuideIDs[i]
        createMesh(ID, width, height, subDivWidth, subDivHeight)
        cmds.hyperShade(assign=shaderName)
        createJointChain(ID, width, subDivWidth)
        bindSkin(ID)
        injectJntWeight(ID, subDivWidth, subDivHeight)
        createCVCurve(ID, width, cvsMaxIndex)
        createIKHandle(ID, subDivWidth)
        createControler(ID,width,cvsMaxIndex)

def createMiddles(middleTotalIndex,width, height, subDivWidth, subDivHeight, cvsMaxIndex):
    MiddleIDs = indexToMiddleIDs(middleTotalIndex)
    for i in range(len(MiddleIDs)):
        shaderName = iToShaderName(4+i)
        ID = MiddleIDs[i]
        createMesh(ID, width, height, subDivWidth, subDivHeight)
        cmds.hyperShade(assign=shaderName)
        createJointChain(ID, width, subDivWidth)
        bindSkin(ID)
        injectJntWeight(ID, subDivWidth, subDivHeight)
        createCVCurve(ID, width, cvsMaxIndex)
        createIKHandle(ID, subDivWidth)
        createControler(ID,width,cvsMaxIndex)

def createPage(ID, width, height, subDivWidth, subDivHeight,cvsMaxIndex):
    createMesh(ID, width, height, subDivWidth, subDivHeight)
    createJointChain(ID, width, subDivWidth)
    bindSkin(ID)
    injectJntWeight(ID, subDivWidth, subDivHeight)
    createCVCurve(ID, width, cvsMaxIndex)
    createIKHandle(ID, subDivWidth)
    createControler(ID,width,cvsMaxIndex)

def createBSTarget(BSID, width, height, subDivWidth, subDivHeight):
    createMesh(BSID, width, height, subDivWidth, subDivHeight)
    BSName = IDToMeshName(BSID)
    cmds.parent(BSName,'BSGrp')


def conductBS(BSID,ID):
    pageName = IDToMeshName(ID)
    BSTargetName = IDToMeshName(BSID)
    BSNodeName = IDToBSName(ID)
    BSIndex = BSIDToIndex(BSID)

    if not cmds.objExists(BSNodeName):
        cmds.blendShape(BSTargetName,pageName,name=BSNodeName)
        skinCluster = IDToSkinClusterName(ID)
        meshShapeNode = IDToMeshShapeNode(ID)
        if cmds.objExists(skinCluster):
            try:
                cmds.reorderDeformers(skinCluster, BSNodeName, meshShapeNode)
            except:
                pass
    else:
        cmds.blendShape(BSNodeName,edit=True,target=(pageName, BSIndex, BSTargetName, 1.0))

def disableBS(ID):
    BSNodeName = IDToBSName(ID)
    plugHandle = '.envelope'
    cmds.setAttr(BSNodeName+plugHandle,0)

def enableBS(ID):
    BSNodeName = IDToBSName(ID)
    plugHandle = '.envelope'
    cmds.setAttr(BSNodeName + plugHandle, 1)

def resetControler(ID,cvsMaxIndex,width):
    cvsPosList = getCVsPosList(cvsMaxIndex, width)
    for cvsIndex in range(len(cvsPosList)):
        controler = IDToControlerName(ID)+'_'+str(cvsIndex)
        cmds.setAttr(f'{controler}.tx',cvsPosList[cvsIndex][0])
        cmds.setAttr(f'{controler}.ty', cvsPosList[cvsIndex][1])

# 定义参数
totalIndex = 5
width = 10
height = 15
subDivWidth = 5
subDivHeight = 10
cvsMaxIndex = 4
middleTotalIndex = 3
shaderColorList = [(29, 43, 83),(126, 37, 83),(255, 0, 77),(250, 239, 93), (54, 84, 134),(127, 199, 217),(255, 0, 77),(126, 37, 83)]
index = 0
ID = indexToID(index)


# 准备
cmds.file(new=True,force=True)
createMBShader(shaderColorList)
createRigTree()

# 创建引导
createGuides(width, height, subDivWidth, subDivHeight,cvsMaxIndex)
# 创建中间页
createMiddles(middleTotalIndex,width, height, subDivWidth, subDivHeight, cvsMaxIndex)
# 循环 创建MBPage
createPage(ID, width, height, subDivWidth, subDivHeight,cvsMaxIndex)

# 创建BS
BSID='BS0'
createBSTarget(BSID, width, height, subDivWidth, subDivHeight)
# 循环 应用BS
conductBS(BSID,ID)

# 创建BS
BSID='BS1'
createBSTarget(BSID, width, height, subDivWidth, subDivHeight)
# 循环 应用BS
conductBS(BSID,ID)

# 写一个计算点插值的函数

