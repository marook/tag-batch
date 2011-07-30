#!/usr/bin/env python
#
# Copyright 2011 Markus Pielmeier
#
# This file is part of tag-batch.
#
# tag-batch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tag-batch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tag-batch.  If not, see <http://www.gnu.org/licenses/>.
#

from tag_utils.dom import Item
from tag_utils.tag_io import parseDirectory

class Condition(object):

    def __init__(self, context, valuePattern):
        self.context = context
        self.valuePattern = valuePattern

    def matches(self, item):
        for value in item.getContextValues(self.context):
            if self.valuePattern.match(value):
                return True

        return False

class Rule(object):

    def __init__(self, name, conditions, taggings):
        self.name = name
        self.conditions = conditions
        self.taggings = taggings

    def isMatching(self, item):
        for c in self.conditions:
            if not c.matches(item):
                return False

        return True

    def applyRule(self, item):
        if not self.isMatching(item):
            return

        for t in self.taggings:
            item.appendEntry(t)

def parseRules(path):
    # TODO
    pass

def main():
    import sys

    rulesFilePath = sys.argv[1]

    rules = parseRules(rulesFilePath)
    if len(rules) == 0:
        return

    for itemPath in sys.argv[2:]:
        item = parseDirectory(itemPath)

        for rule in rules:
            rule.applyRule(item)

        writeFile(item, item.fileName)

if __name__ == '__main__':
    main()
