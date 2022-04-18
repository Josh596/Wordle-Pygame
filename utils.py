from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Qt

def itemIndex(item:QObject):
    if not item.parent():
        return -1
    siblings = item.parent().findChildren(QWidget,options=Qt.FindDirectChildrenOnly)
    for index, sibling in enumerate(siblings):
        if (sibling == item):
            return index
    return -1 # will never happen

def previousItem(item:QObject):
    if not item.parent():
        return None
    index = itemIndex(item)
    if index > 0:
        return item.parent().findChildren(QWidget,options=Qt.FindDirectChildrenOnly)[index - 1]
    # return (index > 0)? item.parent.children[itemIndex(item) - 1]: null
    
    # returns null, if item is not parented, or is the last one

def nextItem(item:QObject):
    if not item.parent():
        return None

    index = itemIndex(item)
    siblings = item.parent().findChildren(QWidget,options=Qt.FindDirectChildrenOnly)

    if index < len(siblings) - 1:
        return siblings[index+1]

    # return (index < siblings.length - 1)? siblings[index + 1]: null

