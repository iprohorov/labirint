import xml.etree.ElementTree as ET
tree = ET.parse('image\Tilemap\coloredt3.tsx')
root = tree.getroot()
print(root.attrib)
print(root)