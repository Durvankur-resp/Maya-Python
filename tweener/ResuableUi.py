from maya import cmds
import tweener
from gearCreator import gears2 as gear



# This will have just the bare functionality to make a window
class BaseWindow(object):
    windowName = "BaseWindow"

    def show(self):
        if cmds.window(self.windowName, query=True, exists=True):
            self.close()

        cmds.window(self.windowName)
        self.buildUI()
        cmds.showWindow()

    def buildUI(self):
    
        pass

   
    def reset(self, *args):
        # This is a placeholder method
        pass

    def close(self, *args):
        cmds.deleteUI(self.windowName)



# This means that it will get all the attributes and methods that the Base Window has
class TweenerWindow(BaseWindow):
   
    
    #       different attributes than its parent
    windowName = "TweenerWindow"

   
    # When buildUI is called in any methods from BaseWindow, it will know to refer to our overriden variable here
    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use this slider to set the tween amount")

        cmds.rowLayout(numberOfColumns=2)
        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tweener.tween)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def reset(self, *arg):
        cmds.floatSlider(self.slider, edit=True, value=50)


class GearWindow(BaseWindow):
    # We redefine the window name
    windowName = "GearWindow"


    def __init__(self):
       
        self.gear = None

   
    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use the slider to modify the number of teeth the gear will have")

        cmds.rowLayout(numberOfColumns=4)

       
        self.label = cmds.text(label="10")
       
        self.slider = cmds.intSlider(min=5, max=30, value=10, step=1, dragCommand=self.modifyGear)
        cmds.button(label="Make Gear", command=self.makeGear)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def makeGear(self, *args):
      
        teeth = cmds.intSlider(self.slider, query=True, value=True)

    
        self.gear = gear.Gear()

        
        self.gear.create(teeth=teeth)

    def modifyGear(self, teeth):


        cmds.text(self.label, edit=True, label=str(teeth))

        # If there is a gear already made, then we will set the slider to edit it
        if self.gear:
            self.gear.changeTeeth(teeth=teeth)

    def reset(self, *args):
     
        self.gear = None

        # We will reset the slider value
        cmds.intSlider(self.slider, edit=True, value=10)

       
        cmds.text(self.label, edit=True, label=str(10))