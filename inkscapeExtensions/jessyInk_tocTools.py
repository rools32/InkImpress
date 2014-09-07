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
import re

try:
    from subprocess import Popen, PIPE
    bsubprocess = True
except:
    bsubprocess = False


""" Function from the perspective extension
"""
def boundingBox(self, iD):
    q = {'x':0,'y':0,'width':0,'height':0}
    file = self.args[-1]
    for query in q.keys():
        if bsubprocess:
            p = Popen('inkscape --query-%s --query-id=%s "%s"' \
                    % (query,iD,file), shell=True, stdout=PIPE, stderr=PIPE)
            rc = p.wait()
            q[query] = float(p.stdout.read())
            err = p.stderr.read()
        else:
            f,err = os.popen3('inkscape --query-%s --query-id=%s "%s"' \
                    % (query,iD,file))[1:]
            q[query] = float(f.read())
            f.close()
            err.close()
    return(q)


def TOC_buildList(root):
    tocList = []
    sectionIndex = 0
    subsectionIndex = 0
    for node in root:
        if node.tag == '{http://www.w3.org/2000/svg}g':
            if node.attrib['{http://www.inkscape.org/namespaces/inkscape}'+
                    'groupmode'] == 'layer':
                label = node.attrib\
                        ['{http://www.inkscape.org/namespaces/inkscape}label']
                titlePattern = re.compile("^\#(sub)?section ")
                if re.match(titlePattern, label):
                    sectionPattern = re.compile("^\#section ")
                    if re.match(sectionPattern, label):
                        sectionIndex = sectionIndex+1
                        subsectionIndex = 0
                    else:
                        if sectionIndex == 0:
                            inkex.errormsg("Subsection outside any section")
                            return []
                        subsectionIndex = subsectionIndex+1
                    index = (sectionIndex, subsectionIndex)
                    title = label.split(' ', 1)[1]
                    tocList.append({'id':node.attrib['id'],
                        'title':title, 'index':index})
    return(tocList)
            
def TOC_findMaster(effect):
    return(effect.getElementById('toc_master'))

def createLayer(parent, iD, label):
        layer = inkex.etree.SubElement(parent, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), label)
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        layer.set(inkex.addNS('id'), iD)
        return(layer)
