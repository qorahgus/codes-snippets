import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


def xml_pprint(element):
    s = ET.tostring(element)
    print(minidom.parseString(s).toprettyxml())


# root = ET.Element("inventory")
# print(ET.dump(root))

# cheese = ET.Element("cheese")
# root.append(cheese)
# print(ET.dump(root))

# name = ET.SubElement(cheese, "name")
# name.text = "Caerphilly"
# print(ET.dump(root))

# xml_pprint(root)

# cheese.attrib["id"] = "c01"
# xml_pprint(cheese)

# text = ET.tostring(name)
# print(text)

# with open("./c1.xml", "w") as f:
#     f.write(ET.tostring(root))

# https://stackabuse.com/reading-and-writing-xml-files-in-python/
tree = ET.parse("/home/mohyun/Desktop/workspace/codes-snippets/c1.xml")
root = tree.getroot()
print(root[0][1].attrib)
