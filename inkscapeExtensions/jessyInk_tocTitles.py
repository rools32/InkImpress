#!/usr/bin/env python
# Copyright 2008, 2009, 2010, 2011 Hannes Hochreiner
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
# along with this program.  If not, see http://www.gnu.org/licenses/.

import os
from pprint import pprint, pformat

# These lines are only needed if you don't put the script directly into
# the installation directory
import sys
# Unix
sys.path.append('/usr/share/inkscape/extensions')
# OS X
sys.path.append('/Applications/Inkscape.app/Contents/Resources/extensions')
# Windows
sys.path.append('C:\Program Files\Inkscape\share\extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
import simplestyle
import re
from jessyInk_tocTools import *

def generateTitle(elm, format):
    text = format
    text = text.replace('%title', elm['title'])
    text = text.replace('%section', str(elm['index'][0]))
    text = text.replace('%subsection', str(elm['index'][1]))
    return(text)

def createUpdateText(textObject, iD, text, coords, font, position):
    if textObject is None:
        textObject = inkex.etree.Element(inkex.addNS('text','svg'))
        textObject.set('id', iD)
        style = 'text-align:;text-anchor:;font-size:;font-family:;'
    else:
        style = textObject.get('style')

    if text:
        textObject.text = unicode(text)

    if coords:
        textObject.set('x', unicode(coords[0]))
        textObject.set('y', unicode(coords[1]))

    if position:
        style = re.sub('text-align:.*?;', 'text-align:%s;' % position[1], style)
        style = re.sub('text-anchor:.*?;', 'text-anchor:%s;' % position[0], style)

    if font:
        style = re.sub('font-size:.*?;', 'font-size:%s;' % str(font[1])+'px', style)
        style = re.sub('font-family:.*?;', 'font-family:%s;' % font[0], style)

    textObject.set('style', style)

    # TODO retourner le nombre de ligne ou la hauteur en trop pour pouvoir decaler
    # probleme c'est qu'il faut regarder le ligne de base et non la bbox
    return(textObject)



class JessyInk_TOCTitles(inkex.Effect):
        def __init__(self):
                # Call the base class constructor.
                inkex.Effect.__init__(self)

                self.OptionParser.add_option('--section_prespacing', action = 'store', type = 'float', dest = 'section_prespacing', default = '0')
                self.OptionParser.add_option('--section_postspacing', action = 'store', type = 'float', dest = 'section_postspacing', default = '0')
                self.OptionParser.add_option('--section_fontname', action = 'store', type = 'string', dest = 'section_fontname', default = 'DejaVu Sans')
                self.OptionParser.add_option('--section_fontsize', action = 'store', type = 'int', dest = 'section_fontsize', default = '72')
                self.OptionParser.add_option('--section_anchor', action = 'store', type = 'string', dest = 'section_anchor', default = 'start')
                self.OptionParser.add_option('--section_align', action = 'store', type = 'string', dest = 'section_align', default = 'left')
                self.OptionParser.add_option('--section_format', action = 'store', type = 'string', dest = 'section_format', default = '%title')
                self.OptionParser.add_option('--subsection_prespacing', action = 'store', type = 'float', dest = 'subsection_prespacing', default = '0')
                self.OptionParser.add_option('--subsection_postspacing', action = 'store', type = 'float', dest = 'subsection_postspacing', default = '0')
                self.OptionParser.add_option('--subsection_hshift', action = 'store', type = 'float', dest = 'subsection_hshift', default = '0')
                self.OptionParser.add_option('--subsection_vshift', action = 'store', type = 'float', dest = 'subsection_vshift', default = '0')
                self.OptionParser.add_option('--subsection_fontname', action = 'store', type = 'string', dest = 'subsection_fontname', default = 'DejaVu Sans')
                self.OptionParser.add_option('--subsection_fontsize', action = 'store', type = 'int', dest = 'subsection_fontsize', default = '58')
                self.OptionParser.add_option('--subsection_anchor', action = 'store', type = 'string', dest = 'subsection_anchor', default = 'start')
                self.OptionParser.add_option('--subsection_align', action = 'store', type = 'string', dest = 'subsection_align', default = 'left')
                self.OptionParser.add_option('--subsection_format', action = 'store', type = 'string', dest = 'subsection_format', default = '%title')
                self.OptionParser.add_option('--hasSpacing', action = 'store', type = 'inkbool', dest = 'hasSpacing', default = True)
                self.OptionParser.add_option('--hasFont', action = 'store', type = 'inkbool', dest = 'hasFont', default = True)
                self.OptionParser.add_option('--tab', action="store", type="string", dest="tab")



        def effect(self):
                root = self.document.getroot()
                master = TOC_findMaster(effect)
                if master == None:
                    master = createLayer(root, 'toc_master', 'TOC_Master')

                tocList =  TOC_buildList(root)

                format = (self.options.section_format, self.options.subsection_format)
                if self.options.hasSpacing:
                    spacing = (
                            (self.options.section_prespacing,
                                self.options.section_postspacing),
                            (self.options.subsection_prespacing,
                                self.options.subsection_postspacing))
                    subshift = (self.options.subsection_hshift,
                            self.options.subsection_vshift)
                    position = (
                            (self.options.section_anchor,
                                self.options.section_align),
                            (self.options.subsection_anchor,
                                self.options.subsection_align))

                else:
                    spacing = None
                    subshift = None
                    position = None

                if self.options.hasFont:
                    font = (
                            (self.options.section_fontname,
                                self.options.section_fontsize),
                            (self.options.subsection_fontname,
                                self.options.subsection_fontsize))
                else:
                    font = None

                self.TOC_addTitles(tocList, master, format, spacing, subshift, font, position)

        def TOC_addTitles(effect, tocList, toc_layer,
                format=('%title','%section.%subsection)%title'),
                spacing=((1.2,0.2),(1.2,0.2)), subshift=(1, 0),
                font=(('DejaVu Sans',72),('DejaVu Sans',66)),
                position=(('middle', 'left'), ('middle', 'left'))):
            # First we create the layer for all the titles
        
            layerId = 'toc_titles'
            layer = effect.getElementById(layerId)
            if layer is None: layer = createLayer(toc_layer, layerId, layerId)
        
            # Then we add the texts
            x = 0
            y = 0
            first = True
            for t in tocList:
                # Determines the type of the title
                if t['index'][1] == 0:
                    kind = 0
                else:
                    kind = 1
                text = generateTitle(t, format[kind])
                iD = 'toc_title_' + str(t['index'][0]) + ['', '.'+str(t['index'][1])][kind]
                textObject = effect.getElementById(iD)
        
                if font:
                    fontSize = font[kind][1]
                    f = font[kind]
                else:
                    if textObject is None:
                        inkex.errormsg(error_font)
                        return()
                    pattern = re.compile('font-size:.*px?;')
                    s = pattern.search(textObject.get('style'))
                    if s is None:
                        inkex.errormsg(error_font)
                        return()
                    fontSize = float(s.group(0)[10:-3])
                    f = None
        
                if spacing:
                    if first: y = 0
                    else: y = y+fontSize*spacing[kind][0]
                    if kind: c = (x+fontSize*subshift[0], y+fontSize*subshift[1])
                    else: c = (x, y)
                    p = position[kind]
                else:
                    c = None
                    p = None
                first = False
        
                textObject = createUpdateText(textObject, iD, text, c, f, p)
                textObject.set('layerId', t['id'])
                layer.append(textObject)
        
                if spacing:
                    y = y+fontSize*spacing[kind][1]
        
            # Finally we remove the removed sections
            # TODO

error_font = "You must choose a font"

# Create effect instance
effect = JessyInk_TOCTitles()
effect.affect()

#/usr/bin/python2 jessyInk_tocTitles.py --tab="help" /tmp/ink_ext_XXXXXX.svg7DNYLX
#import sys
#sys.argv = ["jessyInk_truc.py", '--tab="help"', "/tmp/test.svg"]
#execfile("jessyInk_truc.py")
