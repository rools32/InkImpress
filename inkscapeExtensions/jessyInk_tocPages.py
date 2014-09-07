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

# Thanks to http://www.hoboes.com/Mimsy/hacks/parsing-and-setting-colors-inkscape-extensions/
def colorStrToHexaAlpha(color):
    num = long(color) & 0xFFFFFFFF
    hexa = hex(num)[2:-3].rjust(6, '0')
    alpha = num%256/255.0

    return('#'+hexa, alpha)

def createClone(layer, iD):
    attribs = { inkex.addNS('href','xlink'): '#'+iD }
    clone = inkex.etree.SubElement(layer, inkex.addNS('use','svg'), attribs)
    return(clone)


class JessyInk_TOCPages(inkex.Effect):
        def __init__(self):
                # Call the base class constructor.
                inkex.Effect.__init__(self)

                self.OptionParser.add_option('--section_me_style', action = 'store', type = 'string', dest = 'section_me_style', default = 'none')
                self.OptionParser.add_option('--section_ss_style', action = 'store', type = 'string', dest = 'section_ss_style', default = 'hidden')
                self.OptionParser.add_option('--section_ps_style', action = 'store', type = 'string', dest = 'section_ps_style', default = 'hidden')
                self.OptionParser.add_option('--section_ns_style', action = 'store', type = 'string', dest = 'section_ns_style', default = 'hidden')
                self.OptionParser.add_option('--section_pss_style', action = 'store', type = 'string', dest = 'section_pss_style', default = 'hidden')
                self.OptionParser.add_option('--section_nss_style', action = 'store', type = 'string', dest = 'section_nss_style', default = 'hidden')
                self.OptionParser.add_option('--subsection_me_style', action = 'store', type = 'string', dest = 'subsection_me_style', default = 'none')
                self.OptionParser.add_option('--subsection_cs_style', action = 'store', type = 'string', dest = 'subsection_cs_style', default = 'hidden')
                self.OptionParser.add_option('--subsection_psi_style', action = 'store', type = 'string', dest = 'subsection_psi_style', default = 'hidden')
                self.OptionParser.add_option('--subsection_nsi_style', action = 'store', type = 'string', dest = 'subsection_nsi_style', default = 'hidden')
                self.OptionParser.add_option('--subsection_ps_style', action = 'store', type = 'string', dest = 'subsection_ps_style', default = 'hidden')
                self.OptionParser.add_option('--subsection_ns_style', action = 'store', type = 'string', dest = 'subsection_ns_style', default = 'hidden')
                self.OptionParser.add_option('--subsection_pss_style', action = 'store', type = 'string', dest = 'subsection_pss_style', default = 'hidden')
                self.OptionParser.add_option('--subsection_nss_style', action = 'store', type = 'string', dest = 'subsection_nss_style', default = 'hidden')
                
                self.OptionParser.add_option('--section_me_rgba', action = 'store', type = 'string', dest = 'section_me_rgba', default = '0')
                self.OptionParser.add_option('--section_ss_rgba', action = 'store', type = 'string', dest = 'section_ss_rgba', default = '0')
                self.OptionParser.add_option('--section_ps_rgba', action = 'store', type = 'string', dest = 'section_ps_rgba', default = '0')
                self.OptionParser.add_option('--section_ns_rgba', action = 'store', type = 'string', dest = 'section_ns_rgba', default = '0')
                self.OptionParser.add_option('--section_pss_rgba', action = 'store', type = 'string', dest = 'section_pss_rgba', default = '0')
                self.OptionParser.add_option('--section_nss_rgba', action = 'store', type = 'string', dest = 'section_nss_rgba', default = '0')
                self.OptionParser.add_option('--subsection_me_rgba', action = 'store', type = 'string', dest = 'subsection_me_rgba', default = '0')
                self.OptionParser.add_option('--subsection_cs_rgba', action = 'store', type = 'string', dest = 'subsection_cs_rgba', default = '0')
                self.OptionParser.add_option('--subsection_psi_rgba', action = 'store', type = 'string', dest = 'subsection_psi_rgba', default = '0')
                self.OptionParser.add_option('--subsection_nsi_rgba', action = 'store', type = 'string', dest = 'subsection_nsi_rgba', default = '0')
                self.OptionParser.add_option('--subsection_ps_rgba', action = 'store', type = 'string', dest = 'subsection_ps_rgba', default = '0')
                self.OptionParser.add_option('--subsection_ns_rgba', action = 'store', type = 'string', dest = 'subsection_ns_rgba', default = '0')
                self.OptionParser.add_option('--subsection_pss_rgba', action = 'store', type = 'string', dest = 'subsection_pss_rgba', default = '0')
                self.OptionParser.add_option('--subsection_nss_rgba', action = 'store', type = 'string', dest = 'subsection_nss_rgba', default = '0')

                self.OptionParser.add_option('--tab', action="store", type="string", dest="tab") 


        def effect(self):
                root = self.document.getroot()
                master = TOC_findMaster(effect)
                if master == None:
                    inkex.errormsg(error_textFirst)
                    return()
                tocList =  TOC_buildList(root)

                pagesLayerId = 'toc_pages'
                pagesLayer = self.getElementById(pagesLayerId)
                if pagesLayer != None:
                    master.remove(pagesLayer)
                pagesLayer = createLayer(master, pagesLayerId, pagesLayerId)

                PSect = []
                CSect = []
                NSect =  [ t for t in tocList if t['index'][1]==0 ]

                PSubs = []
                PSibl = []
                CSubs = []
                NSibl = []
                NSubs = [ t for t in tocList if t['index'][1]==1 ]

                for t in tocList:
                    isSection = (t['index'][1] == 0)
                    if isSection:
                        PSect = PSect+CSect
                        CSect = [t]
                        NSect = NSect[1:]

                        PSubs = PSubs+PSibl+CSubs+NSibl 
                        PSibl = []
                        CSubs = []
                        NSibl = [ n for n in NSubs if n['index'][0] == t['index'][0] ]
                        NSubs = NSubs[len(NSibl):]

                        strIndex = str(t['index'][0])
                        titleObejct = self.getElementById('toc_title_' + str(t['index'][0]))

                    else:
                        PSibl = PSibl+CSubs
                        CSubs = [t]
                        NSibl = NSibl[1:]

                        strIndex = str(t['index'][0]) + '.' + str(t['index'][1])

                    # Check that the toc layers have not changed
                    titleObject = self.getElementById('toc_title_'+strIndex)
                    if titleObject == None or t['id'] != titleObject.get('layerId'):
                        inkex.errormsg(error_textFirst)
                        return()

                    # Check that the text is the same
                    lastText = titleObject.text
                    if t['title'] != lastText:
                        inkex.debug('The text has changed (maybe)')
                        # FIXME consider the format (lastText could be
                        # different thant the real text because of that)

                    # Create the layer
                    pageLayerId = 'toc_page_'+strIndex
                    pageLayer = createLayer(pagesLayer, pageLayerId, pageLayerId)

                    # We add a clone of the pageLayer to the real (displayed) layer
                    sectionLayer = self.getElementById(t['id'])
                    cloneId = pageLayerId+'clone'
                    if self.getElementById(cloneId) == None:
                        clone = createClone(sectionLayer, pageLayerId)
                        clone.set('id', cloneId)

                    if isSection:
                        operations = [
                                (CSect, self.options.section_me_style, self.options.section_me_rgba),
                                (NSibl, self.options.section_ss_style, self.options.section_ss_rgba),
                                (PSect, self.options.section_ps_style, self.options.section_ps_rgba),
                                (NSect, self.options.section_ns_style, self.options.section_ns_rgba),
                                (PSubs, self.options.section_pss_style, self.options.section_pss_rgba),
                                (NSubs, self.options.section_nss_style, self.options.section_nss_rgba),
                                ]
                    else:
                        operations = [
                                (CSubs, self.options.subsection_me_style, self.options.subsection_me_rgba),
                                (CSect, self.options.subsection_cs_style, self.options.subsection_cs_rgba),
                                (PSibl, self.options.subsection_psi_style, self.options.subsection_psi_rgba),
                                (NSibl, self.options.subsection_nsi_style, self.options.subsection_nsi_rgba),
                                (PSect, self.options.subsection_ps_style, self.options.subsection_ps_rgba),
                                (NSect, self.options.subsection_ns_style, self.options.subsection_ns_rgba),
                                (PSubs, self.options.subsection_pss_style, self.options.subsection_pss_rgba),
                                (NSubs, self.options.subsection_nss_style, self.options.subsection_nss_rgba),
                                ]

                    for (l, t, v) in operations:
                        if t != "hidden":
                            color = colorStrToHexaAlpha(v)

                            style = ""
                            if t in ("color", "both"):
                                style = style+"fill:"+color[0]+";"
                            if t in ("alpha", "both"):
                                style = style+"opacity:"+str(color[1])+";"

                            for e in l:
                                iD = 'toc_title_'+str(e['index'][0])
                                if e['index'][1] != 0:
                                    iD = iD+'.'+str(e['index'][1])
                                clone = createClone(pageLayer, iD)
                                clone.set('style', style)

error_textFirst = 'You must update the titles first'

# Create effect instance
effect = JessyInk_TOCPages()
effect.affect()

#/usr/bin/python2 jessyInk_tocPages.py --tab="help" /tmp/ink_ext_XXXXXX.svg7DNYLX
#import sys
#sys.argv = ["jessyInk_truc.py", '--tab="help"', "/tmp/test.svg"]
#execfile("jessyInk_truc.py")
