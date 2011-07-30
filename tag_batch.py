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

class Condition(object):

    def __init__(self, context, valuePattern):
        self.context = context
        self.valuePattern = valuePattern

    def matches(self, item):
        for value in item.getContextValues(self.context):
            if self.valuePattern.match(value):
                return True

        return False

class Matcher(object):

    def __init__(self, conditions, taggings):
        self.conditions = conditions
        self.taggings = taggings

    def matches(line):
        pass

def main(argv):
    pass

if __name__ == '__main__':
    import sys

    main(sys.argv)
