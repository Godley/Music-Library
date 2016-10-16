from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMenu, QAction
from PyQt4.Qt import QObject

def click(widget, btn=Qt.LeftButton):
    QTest.mouseClick(widget, btn)

def key_press(widget, key=Qt.DownArrow):
    pass

def action_click(index, menu):
    actions = menu.actions()
    assert len(actions) > 0
    for action in range(index):
        QTest.keyClick(menu, Qt.Key_Down)
        QTest.qWait(1000)
    QTest.keyClick(menu, Qt.Key_Enter)
    return actions[index]