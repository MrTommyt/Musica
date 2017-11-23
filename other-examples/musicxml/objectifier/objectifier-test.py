####################################################################################################
#
# Musica - A Music Theory Package for Python
# Copyright (C) 2017 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from Musica.Xml.Objectifier import XmlObjectifierFactory

####################################################################################################

doctype = '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">'
factory = XmlObjectifierFactory(doctype=doctype, node_hints=('Print', 'Rest'))

####################################################################################################

# .mxl is a zip azchive

file_path = 'musicxml-samples/samples/example1.xml'
root = factory.parse(file_path)

####################################################################################################

root.write_xml('out.xml', doctype=doctype)

####################################################################################################

with open('MusicXML.py', 'w') as output:
    output.write('from Musica.Xml.Objectifier import XmlObjectifierNode, XmlObjectifierLeaf\n')
    for cls in sorted(factory, key=lambda cls: cls.__name__):
        output.write(str(cls.class_to_python()) + '\n')

with open('musicxml-example.py', 'w') as output:
    output.write('from MusicXML import *\n\n')
    output.write(root.to_python() + '\n')
    output.write('\n')
    output.write("score_partwise_0.write_xml('out2.xml', doctype='{}')\n".format(doctype))
