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

from unittest import TestCase, main

from tag_utils.dom import Item
from tag_utils.dom import Tagging

from tag_batch import Condition

import re

def createItem(taggings):
    entries = []

    for t in taggings:
        context, value = t

        entries.append(Tagging(context, value))

    return Item(entries)

class TestCondition(TestCase):

    def testNoMatchingItemTagging(self):
        item = createItem([[None, 'value'], ['otherContext', 'value']])

        c = Condition('context', re.compile('^value$'))

        self.assertFalse(c.matches(item))

    def testMatchingItemTagging(self):
        item = createItem([['context', 'value'],])

        c = Condition('context', re.compile('^value$'))

        self.assertTrue(c.matches(item))

if __name__ == '__main__':
    main()
