# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"(move|clip|pos|org|fs)(\()?((?:\,?\-?\d{1,3}\.?\d{1,3}){1,4})|(m)(\s.+\d)"

test_str = r"Dialogue: 1,0:03:32.85,0:03:32.90,Signs,,0,0,0,,{=395}{\1a&H00&\clip(615,87.14,616,132.14)\pos(752,138.62)\fscx95\fscy70\fnDesyrel\b1\org(482.4,674.54)\fry0.14\frx-1.89\frz-0.93\fax-0.02\blur0.8\c&H596D99&}Que você melhore logo!"

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):

    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1

        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
