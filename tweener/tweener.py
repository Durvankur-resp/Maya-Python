from maya import cmds


def tween(percentage, obj=None, attrs=None, selection=True):
    
   
    if not obj and not selection:
       
        raise ValueError("No object given to tween")

   
    if not obj:
       
        obj = cmds.ls(sl=1)[0]

   
    if not attrs:
        attrs = cmds.listAttr(obj, keyable=True)

   
    currentTime = cmds.currentTime(query=True)

   
    for attr in attrs:
        
        attrFull = '%s.%s' % (obj, attr)

        keyframes = cmds.keyframe(attrFull, query=True)

       
        if not keyframes:
            
            continue

       
        previousKeyframes = []
      
        for k in keyframes:
            
            if k < currentTime:
                
                previousKeyframes.append(k)

    
        laterKeyframes = [frame for frame in keyframes if frame > currentTime]

        if not previousKeyframes and not laterKeyframes:
            continue

        if previousKeyframes:
           
            previousFrame = max(previousKeyframes)
        else:
          
            previousFrame = None

        nextFrame = min(laterKeyframes) if laterKeyframes else None

      
        if previousFrame is None:
            previousFrame = nextFrame

        # SImilar to the above if statement, we can condense it to a single line
        nextFrame = previousFrame if nextFrame is None else nextFrame

       
        previousValue = cmds.getAttr(attrFull, time=previousFrame)
        nextValue = cmds.getAttr(attrFull, time=nextFrame)

        if nextFrame is None:
          
            currentValue = previousValue
        elif previousFrame is None:
           
            currentValue = nextValue
        elif previousValue == nextValue:

            currentValue = previousValue
        else:
            
            difference = nextValue - previousValue
            biasedDifference = (difference * percentage) / 100.0
            currentValue = previousValue + biasedDifference

       
        cmds.setAttr(attrFull, currentValue)
       
        cmds.setKeyframe(attrFull, time=currentTime, value=currentValue)



class TweenerWindow(object):
  
    windowName = "TweenerWindow"


    def show(self):
       
        if cmds.window(self.windowName, query=True, exists=True):
           
            cmds.deleteUI(self.windowName)

      
        cmds.window(self.windowName)

       
        self.buildUI()

        cmds.showWindow()

    def buildUI(self):
       
        # A layout is a UI object that lays out its children, in this case in a column
        column = cmds.columnLayout()

        
        cmds.text(label="Use this slider to set the tween amount")

      
        row = cmds.rowLayout(numberOfColumns=2)

       
        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)

        cmds.button(label="Reset", command=self.reset)

       
        cmds.setParent(column)

        # We add a button to close our UI
        cmds.button(label="Close", command=self.close)

   
    # It basically means I do not know how many arguments I will get, so please put them all inside this one list (tuple) called args
    def reset(self, *args):
        # This resets the slider to its default value
        cmds.floatSlider(self.slider, edit=True, value=50)

    def close(self, *args):
        # This will delete our UI, thereby closing it
        cmds.deleteUI(self.windowName)