##
# Aces Up
# Written by Patrick Barnum
##


class Recorder:
    def __init__(self, canUndo):
        self.toggleUndos(canUndo)
        self.reset()

    def __getStateChangeCount(self):
        return len(self.__state)

    def pushState(self, state):
        self.__state.append(state)

    def popState(self):
        # Return nothing if nothing to return
        if self.__getStateChangeCount() == 0:
            return None

        state = self.getStateAt(self.__getStateChangeCount() - 1)
        del self.__state[-1]
        return state

    def getStateAt(self, position):
        try:
            return self.__state[position]
        except IndexError:
            return None

    def toggleUndos(self, canUndo):
        self.__canUndo = canUndo

    def reset(self):
        self.__state = []

    def canUndo(self):
        return self.__canUndo

    def undo(self):
        return self.popState()
