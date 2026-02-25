class Element:
    def __init__(self, elementType: str, canvasElement: any, properties: dict, x = 0, y = 0, width = 1, height = 1):
        self.elementType = elementType
        self.x = x
        self.y = y
        self.sizeX = width
        self.sizeY = height
        self.canvasElement = canvasElement

        self.properties = dict()

        for key, value in properties.items():
            self.properties[key] = value
