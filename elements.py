class Element:
    def __init__(self, elementType: str, canvasElement: any, properties: dict = {}, x = 0, y = 0):
        self.elementType = elementType
        self.x = x
        self.y = y
        self.canvasElement = canvasElement

        self.properties = dict()

        for key, value in properties.items():
            self.properties[key] = value

class Text(Element):
    def __init__(self, canvasElement: any, properties: dict = {}, x = 0, y = 0):
        super().__init__(elementType="Text", canvasElement=canvasElement, properties=properties, x=x, y=y)
        if "text" not in self.properties:
            self.properties["text"] = "template"
        if "font-size" not in self.properties:
            self.properties["font-size"] = 32

