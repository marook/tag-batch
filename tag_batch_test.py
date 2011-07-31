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

from tag_batch import Condition, parseRules, RuleParseException

import re
import os

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

class TestParseRules(TestCase):

    def setUp(self):
        self.rulesDir = os.path.join('.', 'rules')

    def parseTestRules(self, ruleFileName):
        return parseRules(os.path.join(self.rulesDir, ruleFileName))

    def testParseEmptyFile(self):
        rules = list(self.parseTestRules('empty.rule'))

        self.assertEqual([], rules)

    def testConditionBeforeRuleFail(self):
        try:
            list(self.parseTestRules('conditionBeforeRule.rule'))
        except RuleParseException as e:
            self.assertEqual(2, e.lineNo)

            return

        self.fail('Expected exception')

    def testTaggingBeforeRuleFail(self):
        try:
            list(self.parseTestRules('taggingBeforeRule.rule'))
        except RuleParseException as e:
            self.assertEqual(2, e.lineNo)

            return

        self.fail('Expected exception')

    def testInvalidSyntaxFail(self):
        try:
            list(self.parseTestRules('invalidSyntax.rule'))
        except RuleParseException as e:
            self.assertEqual(2, e.lineNo)

            return

        self.fail('Expected exception')

    def testOneValidRule(self):
        rules = list(self.parseTestRules('oneRule.rule'))

        self.assertEqual(1, len(rules))

        rule = rules[0]

        self.assertEqual('rule', rule.name)
        
        self.assertEqual(1, len(rule.conditions))
        condition = rule.conditions[0]
        self.assertEqual('conditionContext', condition.context)
        self.assertTrue(condition.valuePattern.match('test'))

        self.assertEqual(1, len(rule.taggings))
        tagging = rule.taggings[0]
        self.assertEqual('tagContext', tagging.context)
        self.assertEqual('tagValue', tagging.value)

if __name__ == '__main__':
    main()
