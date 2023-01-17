from maya import cmds

SUFFIXES = {
    "mesh": "geo",
    "joint": "jnt",
    "camera": None,
}

DEFAULT = "grp"

def rename(selection=False):

  

    # The ls function also takes an input called selection, and we can just pass that through
    objects = cmds.ls(selection=selection, dag=True)

    if selection and not objects:
       
        # This will end our function and display a detailed error message (traceback) to our users
        raise RuntimeError("You don't have anything selected")

    # Now we need to sort our items from longest to shortest again so that we don't rename parents before children
    objects.sort(key=len, reverse=True)

    # Now we loop through all the objects we have
    for obj in objects:

        # We get the shortname again by splitting at the last |
        shortName = obj.split('|')[-1]

        # This is in case we receive a transform and not its shape
        children = cmds.listRelatives(obj, children=True) or []
        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)

        # If the dictionary doesn't hold the item, it will return the default value instead that we ask it for
        suffix = SUFFIXES.get(objType, DEFAULT)

       
        # Continue means that we will continue on to the next item and skip the logic for this one
        if not suffix:
            continue

        # To prevent adding the suffix twice, we'll check if it already has the suffix and skip it if it does
        if shortName.endswith('_'+suffix):
            continue

        # Instead of using the + symbol, we can use the %s symbol to insert strings
        newName = '%s_%s' % (shortName, suffix)
        cmds.rename(shortName, newName)

        # Now we find where in the list of objects our current object is
        index = objects.index(obj)

        objects[index] = obj.replace(shortName, newName)
    return objects