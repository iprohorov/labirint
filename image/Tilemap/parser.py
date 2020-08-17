import xml.etree.ElementTree as ET
tree = ET.parse('coloredt3.tsx')
root = tree.getroot()
# main Sprite name 
class Title ():
    def __init__(self, tile, sourse, tilewidth, tileheight, spacing, tilecount, columns):
        self.id = tile.attrib["id"]
        self.property = []
        for properties_ in tile:
            for property_ in properties_:
                self.property.append(property_.attrib)
    def getImg(self):
        pass
        

for child in root:
    print(child.tag, child.attrib)
    if child.tag == "tile":
        Title(child)

print(root.attrib)
print(root)