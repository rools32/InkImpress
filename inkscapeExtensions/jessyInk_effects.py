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
import gettext
_ = gettext.gettext

class JessyInk_Effects(inkex.Effect):
	def __init__(self):
		# Call the base class constructor.
		inkex.Effect.__init__(self)

		self.OptionParser.add_option('--tab', action = 'store', type = 'string', dest = 'what')
		self.OptionParser.add_option('--effectInOrder', action = 'store', type = 'string', dest = 'effectInOrder', default = 1)
		self.OptionParser.add_option('--effectInDuration', action = 'store', type = 'float', dest = 'effectInDuration', default = 0.8)
		self.OptionParser.add_option('--effectIn', action = 'store', type = 'string', dest = 'effectIn', default = 'none')
		self.OptionParser.add_option('--effectOutOrder', action = 'store', type = 'string', dest = 'effectOutOrder', default = 2)
		self.OptionParser.add_option('--effectOutDuration', action = 'store', type = 'float', dest = 'effectOutDuration', default = 0.8)
		self.OptionParser.add_option('--effectOut', action = 'store', type = 'string', dest = 'effectOut', default = 'none')

		inkex.NSS["jessyink"] = "https://launchpad.net/jessyink"

	def effect(self):
		# Check version.
		scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.6']", namespaces=inkex.NSS)

		if len(scriptNodes) != 1:
			inkex.errormsg(_("The JessyInk script is not installed in this SVG file or has a different version than the JessyInk extensions. Please select \"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" menu to install or update the JessyInk script.\n\n"))

		if len(self.selected) == 0:
			inkex.errormsg(_("No object selected. Please select the object you want to assign an effect to and then press apply.\n"))

		for id, node in list(self.selected.items()):
			if self.options.effectIn in ("appear", "fade", "pop"):
				attribs = { inkex.addNS('href','xlink'): '#'+id }
				clone = inkex.etree.SubElement(self.current_layer, inkex.addNS('use','svg'), attribs)
				clone.set("{" + inkex.NSS["jessyink"] + "}effectIn","name:" + self.options.effectIn  + ";order:" + self.options.effectInOrder + ";length:" + str(int(self.options.effectInDuration * 1000)))
				# Remove possible view argument.
				if "{" + inkex.NSS["jessyink"] + "}view" in node.attrib:
					del node.attrib["{" + inkex.NSS["jessyink"] + "}view"]
		
			if self.options.effectOut in ("appear", "fade", "pop"):
				attribs = { inkex.addNS('href','xlink'): '#'+id }
				clone = inkex.etree.SubElement(self.current_layer, inkex.addNS('use','svg'), attribs)
				clone.set("{" + inkex.NSS["jessyink"] + "}effectOut","name:" + self.options.effectOut  + ";order:" + self.options.effectOutOrder + ";length:" + str(int(self.options.effectOutDuration * 1000)))
				# Remove possible view argument.
				if "{" + inkex.NSS["jessyink"] + "}view" in node.attrib:
					del node.attrib["{" + inkex.NSS["jessyink"] + "}view"]

# Create effect instance
effect = JessyInk_Effects()
effect.affect()

