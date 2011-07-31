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

from tag_utils.dom import Item, Tagging
from tag_utils.tag_io import parseDirectory, writeFile

class Condition(object):

    def __init__(self, context, valuePattern):
        self.context = context
        self.valuePattern = valuePattern

    def matches(self, item):
        for value in item.getContextValues(self.context):
            if self.valuePattern.match(value):
                return True

        return False

    def __str__(self):
        return 'Condition(%s, %s)' % (self.context, self.valuePattern)

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

class RuleParseException(Exception):
    
    def __init__(self, message, lineNo):
        self.message = message
        self.lineNo = lineNo

    def __str__(self):
        return 'RuleParseException in line %s: %s' % (self.lineNo, self.message)

# [rule]
# !context=^value$
# !context2=^value2$
# :newContext=value
def parseRules(path):
    import re

    ignorePattern = re.compile('^[\s]*([#].*)?$')
    rulePattern = re.compile('^[\s]*\[([^\]]+)\][\s]*$')
    conditionPattern = re.compile('^[\s]*!([^=]+)=(.*)$')
    taggingPattern = re.compile('^[\s]*:([^=]+)=(.*)$')

    with open(path, 'r') as f:
        rule = None

        for lineNo, line in enumerate(f):
            try:
                if ignorePattern.match(line):
                    continue

                matcher = rulePattern.match(line)
                if matcher:
                    ruleName = matcher.group(1)

                    if not rule is None:
                        yield rule

                    rule = Rule(ruleName, [], [])

                    continue

                matcher = conditionPattern.match(line)
                if matcher:
                    context = matcher.group(1)
                    condition = matcher.group(2)

                    pattern = re.compile(condition)

                    rule.conditions.append(Condition(context, pattern))

                    continue

                matcher = taggingPattern.match(line)
                if matcher:
                    context = matcher.group(1)
                    value = matcher.group(2)

                    rule.taggings.append(Tagging(context, value))

                    continue

                raise RuleParseException('Invalid syntax: %s' % line, lineNo + 1)

            except Exception as e:
                raise RuleParseException('Rule parse error %s' % e, lineNo + 1)

        if not rule is None:
            yield rule

def main():
    import sys

    if len(sys.argv) < 2:
        print 'Usage %s: [rule file] [items...]' % (sys.argv[0])

        sys.exit(1)

    rulesFilePath = sys.argv[1]

    rules = list(parseRules(rulesFilePath))
    if len(rules) == 0:
        return

    for itemPath in sys.argv[2:]:
        item = parseDirectory(itemPath)

        for rule in rules:
            rule.applyRule(item)

        writeFile(item, item.fileName)

if __name__ == '__main__':
    main()
