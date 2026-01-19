import abc
import os
import re
class Movement(abc.ABC):
    def __init__(
        self,
        initialColor: tuple[str],
        finalColor: tuple[str],
        colorPatternSet: set[str],
        currentColorIndex: int,
        movementId: str,
    ) -> None:
        self._initialColor = initialColor
        self._finalColor = finalColor
        self._colorPatternSet = colorPatternSet
        self._currentColorIndex = currentColorIndex
        self._id = movementId

    @abc.abstractmethod
    def move(self):
        """
        main method to implement
        """
        pass
    
    @abc.abstractmethod
    def moveTest(self):
        """
        main method to implement
        """
        pass

    def getId(self) -> str:
        return self._id

    def getInitialColor(self) -> tuple[str]:
        return self._initialColor

    def getFinalColor(self) -> tuple[str]:
        return self._finalColor

    def getColorPatternSet(self) -> set[str]:
        return self._colorPatternSet

    def getCurrentColorIndex(self) -> int:
        return self._currentColorIndex
    
    def setCurrentColorIndex(self, index: int):
        self._currentColorIndex = index



