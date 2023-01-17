from Qt import QtWidgets, QtCore, QtGui
import json
import os
import pprint

from maya import cmds

DIRECTORY = os.path.join( cmds.internalVar(userAppDir=True), 'controllerLibrary')


class ControllerLibrary(dict):

    def createDir(self, directory=DIRECTORY):
        
        if not os.path.exists(directory):
           
            os.mkdir(directory)

   
    def save(self, name, screenshot=True, directory=DIRECTORY, **info):
        
        
        self.createDir(directory)
        path = os.path.join(directory, '%s.ma' % name)
        infoFile = os.path.join(directory, '%s.json' % name)

        if screenshot:
            info['screenshot'] = self.saveScreenshot(name, directory=directory)
        info['name'] = name
        info['path'] = path

        
        cmds.file(rename=path)

        if cmds.ls(selection=True):
            cmds.file(force=True, exportSelected=True)
        else:
            cmds.file(save=True, force=True)

        self[name] = info
        with open(infoFile, 'w') as f:
          
            json.dump(info, f, indent=4)

    def find(self, directory=DIRECTORY):
        if not os.path.exists(directory):
            return
        files = os.listdir(directory)

        mayaFiles = [f for f in files if f.endswith('.ma')]

        for ma in mayaFiles:
            name, ext = os.path.splitext(ma)

            infoFile = '%s.json' % name
            screenshot = '%s.jpg' % name

            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)

                with open(infoFile, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
            if screenshot in files:
                data['screnshot'] = os.path.join(directory, screenshot)

            data['name'] = name
            data['path'] = os.path.join(directory, ma)

            self[name] = data

    def load(self, name):
        path = self[name]['path']
        cmds.file(path, i=True, usingNamespaces=False)

    def saveScreenshot(self, name, directory=DIRECTORY):
        path = os.path.join(directory, '%s.jpg' % name)

        cmds.viewFit()

        cmds.setAttr("defaultRenderGlobals.imageFormat", 8)

    
        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=1, endTime=1, viewer=False)

        return path



class ControllerLibraryUI(QtWidgets.QDialog):

    def __init__(self):

        super(ControllerLibraryUI, self).__init__()
        self.setWindowTitle('Controller Library UI')

        self.library = ControllerLibrary()

        self.buildUI()

    def buildUI(self):
        
        layout = QtWidgets.QVBoxLayout(self)
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)
        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)
        saveBtn = QtWidgets.QPushButton('Save')
        saveLayout.addWidget(saveBtn)
        size = 64
   
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+12, size+12))
        layout.addWidget(self.listWidget)
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)
        importBtn = QtWidgets.QPushButton('Import!')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

        self.populate()

    def load(self):
        currentItem = self.listWidget.currentItem()

 
        if not currentItem:
            return

        name = currentItem.text()
        self.library.load(name)

    def save(self):

        name = self.saveNameField.text()

        if not name.strip():
            cmds.warning("You must give a name!")
            return

        self.library.save(name)

        self.populate()

        self.saveNameField.setText('')

    def populate(self):
        self.listWidget.clear()
        self.library.find()
        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)

            item.setToolTip(pprint.pformat(info))

            
            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            
            self.listWidget.addItem(item)

def showUI():
    ui = ControllerLibraryUI()
    ui.show()
    return ui