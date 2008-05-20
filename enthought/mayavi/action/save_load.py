"""Actions to save and load a MayaVi2 visualization file.

"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005, Enthought, Inc.
# License: BSD Style.

# Standard library imports.
import sys 
from os.path import isfile

# Enthought library imports.
from enthought.pyface.api import FileDialog, OK
from enthought.pyface.action.api import Action

# Local imports
from enthought.mayavi.plugins.script import get_imayavi
from enthought.mayavi.core.common import error, exception


######################################################################
# `SaveVisualization` class.
######################################################################
class SaveVisualization(Action):
    """ An action that saves the current visualization. """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """
        wildcard = 'MayaVi2 files (*.mv2)|*.mv2|' + FileDialog.WILDCARD_ALL
        dialog = FileDialog(parent=self.window.control,
                            title='Save MayaVi2 file',
                            action='save as', wildcard=wildcard
                            )
        if dialog.open() == OK:
            mv = get_imayavi(self.window)
            mv.save_visualization(dialog.path)

######################################################################
# `LoadVisualization` class.
######################################################################
class LoadVisualization(Action):
    """ An action that loads a visualization from file. """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """
        wildcard = 'MayaVi2 files (*.mv2)|*.mv2|' + FileDialog.WILDCARD_ALL
        parent = self.window.control
        dialog = FileDialog(parent=parent,
                            title='Open MayaVi2 file',
                            action='open', wildcard=wildcard
                            )
        if dialog.open() == OK:
            if not isfile(dialog.path):
                error("File '%s' does not exist"%dialog.path, parent)
                return
            
            mv = get_imayavi(self.window)
            mv.load_visualization(dialog.path)

######################################################################
# `RunScript` class.
######################################################################
class RunScript(Action):
    """ An action that runs a mayavi script.  
    
    WARNING: this can be dangerous since the file runs execfile! """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """
        wildcard = 'Python files (*.py)|*.py'
        parent = self.window.control
        dialog = FileDialog(parent=parent,
                            title='Open Python file',
                            action='open', wildcard=wildcard
                            )
        if dialog.open() == OK:
            if not isfile(dialog.path):
                error("File '%s' does not exist"%dialog.path, parent)
                return
            
            # Get the globals.
            # The following code is taken from scripts/mayavi2.py.
            g = sys.modules['__main__'].__dict__
            # Do execfile
            try:
                # If we don't pass globals twice we get NameErrors and nope,
                # using exec open(script_name).read() does not fix it.
                execfile(dialog.path, g, g)
            except Exception, msg:
                exception(str(msg))
