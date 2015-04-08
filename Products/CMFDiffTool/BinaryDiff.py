# -*- coding: utf-8 -*-
from os import linesep
from App.class_init import InitializeClass
from Products.CMFDiffTool.BaseDiff import _getValue
from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFPlone.utils import safe_unicode


class BinaryDiff(FieldDiff):
    """Simple binary difference"""

    meta_type = "Binary Diff"
    inlinediff_fmt = u"""
<div class="%s">
    <del>%s</del>
    <ins>%s</ins>
</div>
"""

    def _parseField(self, value, filename=None):
        """Parse a field value in preparation for diffing"""
        if filename is None:
            # Since we only want to compare the filename for
            # binary files, return an empty list
            return []
        else:
            return [self.filenameTitle(safe_unicode(filename)).encode('utf-8')]

    def testChanges(self, ob):
        """Test the specified object to determine if the change set will apply without errors"""
        value = _getValue(ob, self.field)
        if not self.same and value != self.oldValue:
            raise ValueError, ("Conflict Error during merge", self.field, value, self.oldValue)

    def applyChanges(self, ob):
        """Update the specified object with the difference"""
        # Simplistic update
        self.testChanges(ob)
        if not self.same:
            setattr(ob, self.field, self.newValue)

    def inline_diff(self):
        """Simple inline diff that just checks that the filename
        has changed."""
        css_class = 'FilenameDiff'
        html = []
        if self.oldFilename != self.newFilename:
            line = self.inlinediff_fmt % (
                css_class,
                self.filenameTitle(safe_unicode(self.oldFilename)),
                self.filenameTitle(safe_unicode(self.newFilename)))
            html.append(line.encode('utf-8'))

        if html:
            return linesep.join(html)

InitializeClass(BinaryDiff)
