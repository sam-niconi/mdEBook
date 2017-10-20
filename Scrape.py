# Read lines
import sys, re

excluded_refs = [
    'Book of Common Prayer',
    'Milton R. Hunter',
    'Welfare Handbook',
    'James E. Talmage',
    'Compendium',
    'James L. Barker',
    'Man: Origin and Destiny',
    'Doctrines of Salvation',
    'Outlines of Ecclesiastical History',
    'Improvement Era',
    'Journal of Discourses',
    'Conf. Rep',
    'Catholic Encyclopedia',
    'Times and Seasons',
    'Teachings',
    'Discourses',
    'Articles of Faith',
    'John A. Widtsoe',
    'Essentials in Church History',
    'Dummelow',
    'Joseph Fielding Smith',
    'Apocrypha',
    'Mediation and Atonement',
    'Way to Perfection',
    'John Taylor',
    'History of the Church',
    'Parley P. Pratt',
    'Saturday Night Thoughts',
    'Lectures on Faith',
    'Sidney B. Sperry',
    'Progress of Man',
    'George Q. Cannon',
    'Are We of Israel',
    'Manuscript History of the Church',
    'Discourses of Wilford Woodruff',
    'James Cardinal Gibbons',
    'The Father and the Son',
    'Reynolds',
    'Encyclopedia Britannica',
    'Hunter',
    "Smith's Bible Dictionary",
    'Gospel Kingdom',
    'Era',
    'J. Paterson Smyth',
    'Rel. Soc. Mag.',
    'Orson F. Whitney',
    'Will Durant',
    'Cited',
    "Peloubet's Bible Dictionary",
    'Francis W. Kirkham',
    'Juvenile Instructor',
    'Albert E. Bowen',
    'Bowen, The Church Welfare Plan',
    'J. M. Sjodahl The Reign of Antichrist',
    'Hugh Nibley',
    'J. Reuben Clark, Jr.',
    'Man: His Origin and Destiny',
    'Doctrines Salvation',
    'Doctrine of Salvation',
    'Voice of Warning',
    'Journal History',
    'Man: HisOrigin and Destiny',
    'Gospel Doctrine',
    'The House of the Lord',
    'the',
    'omitting',
    'meaning',
    'Jos. Smith',
    'called',
    'covering',
    'sometimes',
    'Teaching',
    'consisting',
    'which',
    'about',
    'completed',
    'also',
    'vol',
    'in',
]

scripture_path_mappings = {
    '1 Ne.':'',
    '2 Ne.':'',
    'Jacob':'',
    'Enos':'',
    'Jarom':'',
    'Omni':'',
    'Words of Morm.':'',
    'Mosiah':'',
    'Alma':'',
    'Hela.':'',
    '3 Ne.':'',
    '4 Ne.':'',
    'Morm.':'',
    'Ether':'',
    'Moro.':'',

    'D.&C.':'',

    'Moses': '',
    'Abra.': '',
    'Tenth Article of Faith':'',

    'Gen.':'',
    'Ex.':'',
    'Lev.':'',
    'Num.':'',
    'Deut.':'',
    'Josh.':'',
    'Judges':'',
    'Ruth':'',
    '1 Sam.':'',
    '2 Sam.':'',
    '1 Kings':'',
    '2 Kings':'',
    '1 Chron.':'',
    '2 Chron.':'',
    'Ezra':'',
    'Neh.':'',
    'Esther':'',
    'Job':'',
    'Ps.':'',
    'Prov.':'',
    'Eccles.':'',
    'Isa.':'',
    'Jer.':'',
    'Lam.':'',
    'Ezekiel':'',
    'Dan.':'',
    'Hosea':'',
    'Joel':'',
    'Amos':'',
    'Obad.':'',
    'Jonah':'',
    'Micah':'',
    'Nah.':'',
    'Hab.':'',
    'Zeph.':'',
    'Hag.':'',
    'Zech.':'',
    'Mal.': '',

    'Matt.': '',
    'Mark':'',
    'Luke':'',
    'John':'',
    'Acts':'',
    'Rom.':'',
    '1 Cor.':'',
    '2 Cor.':'',
    'Gal.':'',
    'Eph.':'',
    'Philip.':'',
    'Col.':'',
    '1 Thess.':'',
    '2 Thess.':'',
    '1 Tim.':'',
    '2 Tim.':'',
    'Titus':'',
    'Heb.':'',
    'Jas.':'',
    '1 Pet.':'',
    '2 Pet.':'',
    '1 John':'',
    '2 John':'',
    '3 John':'',
    'Jude':'',
    'Rev.':'',

    'Inspired Version, Matt.':'',

    # 'Mat.':'',
    # 'Ne.':'',
    # 'Ram.':'',
    # 'Enoch':'',
    # 'Nov.':'',
    # 'Cor.':'',
    # 'Jar.':'',
    # 'Psa.':'',
    # 'Tob.':'',
    # 'Hos.':'',
    # 'Mic.':'',
    # 'Tit.':'',
    # 'Jac.':'',
    # 'Ezek.':'',
    # 'Mai.':'',
}


def loadSource(path):
    lines = [line.rstrip('\n') for line in open(path)]
    lines = lines
    n = len(lines)
    return lines, n

def tidyTitles(lines, maxSearchDistance):
    terms = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        strippedLine = line.strip()

        if len(strippedLine) > 0 and strippedLine[0] == '(' and strippedLine[len(strippedLine) - 1] == ')':
            potentialTerm = strippedLine[1: len(strippedLine) - 1]
            potentialTerm = potentialTerm.strip()

            found = False
            iSearch = i
            while iSearch < (i + maxSearchDistance) and iSearch < n:
                compareLine = lines[iSearch].strip()
                if compareLine.lower() == potentialTerm.lower():
                    lines[iSearch] = ""
                    lines[i] = "~" + potentialTerm
                    found = True
                    break
                iSearch = iSearch + 1

            if found == False:
                iSearch = i
                while iSearch > (i - maxSearchDistance) and iSearch >= 0:
                    compareLine = lines[iSearch].strip()
                    if compareLine.lower() == potentialTerm.lower():
                        lines[iSearch] = ""
                        lines[i] = "~" + potentialTerm
                        break
                    iSearch = iSearch - 1

            if found == True:
                terms.append(potentialTerm)
                # sys.stdout.write(term)
                # sys.stdout.write('\n')

        i = i + 1

    return lines, terms

def blankDigits(lines):
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        strippedLine = line.strip()
        if strippedLine.isdigit():
            strippedLine = ''
            lines[i] = ''
        i = i + 1
    return lines


def removeDoubleBlankLines(lines):
    # Take out double lines
    i = 0
    n = len(lines)
    while i < n:
        element = lines[i]
        iNext = i + 1
        if iNext >= n:
            iNext = i
        nextElement = lines[iNext]

        if len(element) == 0 and len(nextElement) == 0:
            del lines[i]
            n = n - 1
        else:
            i = i + 1
    return lines

def joinBrokenSentence(lines):
    # Take out unneeded blank lines
    i = 1
    n = len(lines)
    while i < n:
        element = lines[i].strip()

        iNext = i + 1
        if iNext >= n:
            iNext = i
        nextElement = lines[iNext].strip()

        iPrev = i - 1
        prevElement = lines[iPrev].strip()
        if len(prevElement) == 0:
            i = i + 1
            continue

        endOfPrev = prevElement[-1]
        startOfNext = nextElement[0:1]
        if len(element) == 0 and (97 <= ord(endOfPrev) <= 122 or endOfPrev == ",") :
            del lines[i]
            n = n - 1
        else:
            i = i + 1
    return lines

def removeBlankLineAfterTitle(lines):
    i = 1
    n = len(lines)
    while i < n:
        element = lines[i].strip()

        iNext = i + 1
        if iNext >= n:
            iNext = i
        nextElement = lines[iNext].strip()

        if len(element) > 0 and element[0]=="~" and len(nextElement) == 0:
            del lines[iNext]
            n = n - 1
        else:
            i = i + 1
    return lines

def putRefsOnOneLine(lines):
    i = 1
    n = len(lines)
    while i < n:
        currentLine = lines[i].strip()

        if currentLine and currentLine[0:4]=="See ":
            iNext = i+1
            nextRefs = ""
            while iNext < n-1:
                nextLine = lines[iNext].strip()
                nextNextLine = lines[iNext+1].strip()

                if not nextLine:
                    if nextNextLine.isupper():
                        concatedLine = currentLine[4:] + " " + nextNextLine + " " + nextRefs
                        concatedLine = concatedLine.strip()
                        if concatedLine[-1] == ".":
                            concatedLine = concatedLine[:-1]
                        lines[i] = concatedLine
                        del lines[iNext]
                        del lines[iNext]
                        n = n - 2
                    else:
                        concatedLine = currentLine[4:] + " " + nextRefs
                        concatedLine = concatedLine.strip()
                        if concatedLine[-1] == ".":
                            concatedLine = concatedLine[:-1]
                        lines[i] = concatedLine
                        # del lines[iNext]
                        # n = n - 1
                    i = i + 1
                    break
                else:
                    nextRefs += nextLine + " "
                    del lines[iNext]
                    n = n - 1
        else:
            i = i + 1
    return lines

def removeRandomLines(lines):
    count = 0
    i = 1
    n = len(lines)
    while i < n:
        prevLine = lines[i-1].strip()
        thisLine = lines[i].strip()

        deleted = False
        if thisLine and len(thisLine) < 10:
            thisLast = thisLine[-1]
            thisLast2 = thisLine[-2] if len(thisLine) >= 2 else ""
            thisFirst = thisLine[0:1]

            prevLast = prevLine[-1] if prevLine else ""
            prevFirst = prevLine[0:1] if prevLine else ""

            if thisFirst != "~" and prevFirst != "~" \
                    and thisLast != "." and thisLast2 != '."' and thisLast != "?":

                if not (thisLast == ")" and prevLast == ".") \
                        and not (thisLast == ")" and prevLast == ",") \
                        and not (thisLast == ")" and prevLast == "-") \
                        and not (thisLast == ")" and prevLast == "&") \
                        and not (thisLast == ")" and prevLast == ";")\
                        and not (prevLine and thisFirst.isdigit() and thisLine.find(":") != -1 and thisLine.find(")") != -1 and thisLine.find(")") != -1)\
                        and not (thisLine.islower() and prevLast.islower())\
                        :
                    # sys.stdout.write("\n")
                    # sys.stdout.write(str(i-1) + " " + prevLine)
                    # sys.stdout.write("\n")
                    # sys.stdout.write(str(i) + " " + thisLine)
                    # sys.stdout.write("\n")
                    # sys.stdout.write(str(i+1) + " " + lines[i+1].strip())
                    # sys.stdout.write("\n")
                    del lines[i]
                    n = n - 1
                    deleted = True

                    count = count + 1
        if not deleted:
            i = i + 1
    # sys.stdout.write("\n"+str(count))


def joinLinesFromParagraph(lines):
    i = 0
    n = len(lines)
    paragraph = ""
    while i < n:
        thisLine = lines[i].strip()
        thisFirst = thisLine[0] if thisLine else ""
        nextLine = lines[i+1].strip() if i+1 < n else ""
        nextNextLine = lines[i+2].strip() if i+2 < n else ""
        nextFirst = nextLine[0] if nextLine else ""

        if thisFirst == "~":
            lines.insert(i, "")
            n = n+1
            i = i+1
            paragraph = ""
            i = i + 1
            if nextLine and nextLine.isupper():
                i = i + 1
            continue

        if not thisLine:
            if not paragraph:
                del lines[i]
                n = n - 1
                continue

            lines[i] = paragraph
            paragraph = ""
            i = i + 1
        else:
            if thisFirst == ">":
                i = i + 1
            else:
                paragraph = paragraph + lines[i]
                del lines[i]
                n = n - 1

def findUnclosedTerms(lines):
    count = 0
    i = 1
    n = len(lines)
    while i < n:
        thisLine = lines[i].strip()

        if thisLine :
            thisFirst = thisLine[0:1]
            if thisFirst == "(" and thisLine.find(")") == -1:
                sys.stdout.write("\n")
                sys.stdout.write(str(i-1) + " " + thisLine)
                count = count + 1
        i = i + 1
    sys.stdout.write("\n"+str(count))

def validateRefs(lines):
    terms = {}
    i = 0
    n = len(lines)
    while i < n:
        thisLine = lines[i].strip()

        if thisLine :
            thisFirst = thisLine[0:1]
            if thisFirst == "~":
                terms[thisLine[1:].lower()] = True
        i = i + 1
    sys.stdout.write("\nTerms:"+str(len(terms))+"\n")

    notFound = 0
    i = 0
    while i < n:
        thisLine = lines[i].strip()

        if thisLine :
            thisFirst = thisLine[0:1]
            if thisFirst == "~":
                refs = lines[i+1].strip()
                # if refs.isupper() and refs.find(";") != -1:
                #     sys.stdout.write("\n" + str(refs.count(";")) + " " + refs + "\n")

                refsList = []
                if refs.find(";") != -1 :
                    refsSections = refs.split(";")
                    if len(refsSections) == 2:
                        refsList = refsSections[0].split(",")
                        refsList.append(refsSections[1])
                    elif len(refsSections) == 3:
                        refsList = refsSections[0].split(",")
                        refsList.append(refsSections[1])
                        lastRefsList = refsSections[2].split(",")
                        refsList = refsList + lastRefsList
                    else:
                        sys.stdout.write(str(i+1) + " More ;s than expected" + refs + "\n")
                else:
                    refsList = refs.split(",")

                iRef = 0
                while refs.isupper() and iRef < len(refsList):
                    ref = refsList[iRef].lower().strip()
                    if ref and ref not in terms:
                        sys.stdout.write(str(i+1) + " " + ref + "\n")
                        notFound = notFound + 1
                    iRef = iRef+1
        i = i + 1
    sys.stdout.write("\n"+str(notFound))

def findDodgyParagraphs(lines):
    count = 0
    i = 1
    n = len(lines)
    while i < n:
        thisLine = lines[i].strip()
        thisFirst = thisLine[0] if thisLine else ""

        if thisLine :
            if thisFirst == "~" or thisFirst == ">" or thisLine.isupper():
                i = i+1
                continue

            thisLast = thisLine[-1] if thisLine else ""

            if thisLast != "." \
                    and thisLast != ":" \
                    and thisLast != ")" \
                    and thisLast != '"'\
                    and thisLast != ';'\
                    and thisLast != '?'\
                    and thisLast != "!"\
                    and thisLast != "'"\
                    :
                sys.stdout.write("\n")
                sys.stdout.write(str(i-1) + " " + thisLast + " " + thisLine)
                count = count + 1
        i = i + 1
    sys.stdout.write("\n"+str(count))

def findScripturesInParenthesis(lines):
    count = 0
    ref_books = {}
    i = 1
    n = len(lines)
    while i < n:
        thisLine = lines[i].strip()
        thisFirst = thisLine[0] if thisLine else ""

        if thisLine :
            if thisFirst == "~" or thisFirst == ">" or thisLine.isupper():
                i = i+1
                continue

            open_pos = thisLine.find('(')
            while open_pos != -1:
                close_pos = thisLine.find(')', open_pos)
                if close_pos == -1:
                    open_pos = -1
                    continue

                contents = thisLine[open_pos+1:close_pos]
                if re.search(r'\d', contents):
                    print(str(i) + " " + contents)
                    count = count + 1

                    references = contents.split(';')
                    for ref in references:
                        encountered_alpha = False
                        ref_len = len(ref)
                        index = 0;
                        while index < ref_len:
                            ch = ref[index]
                            if ch.isdigit():
                                if encountered_alpha:
                                    book = ref[0:index].strip()
                                    found_exclusion = False
                                    for excluded in excluded_refs:
                                        if book.lower().find(excluded.lower()) == 0:
                                            found_exclusion = True
                                            break

                                    if  not found_exclusion:
                                        ref_books[book] = ref_books[book] + 1 if book in ref_books else 1
                                    index = ref_len
                                    continue

                            if ch.isupper() or ch.islower():
                                encountered_alpha = True
                            index = index + 1

                open_pos = thisLine.find('(', close_pos)
        i = i + 1
    print str(count)
    print ''

    sorted_by_freq = sorted(ref_books.items(), key=lambda x: x[1])
    for element in sorted_by_freq:
        term = element[0]
        if term not in scripture_path_mappings:
            print (str(element[1]) + " " + element[0])


def writeFile(lines, path):
    # Write lines
    outFile = open(path, 'w')
    outFile.writelines(["%s\n" % line for line in lines])

###############################################################

srcLines, srcLineNum = loadSource('in.txt')

outLines = srcLines[:]

outLines, terms = tidyTitles(outLines, 50)
blankDigits(outLines)
removeDoubleBlankLines(outLines)
removeBlankLineAfterTitle(outLines)
putRefsOnOneLine(outLines)
removeRandomLines(outLines)
joinBrokenSentence(outLines)

joinLinesFromParagraph(outLines)

# findUnclosedTerms(outLines)
validateRefs(outLines)
findDodgyParagraphs(outLines)
findScripturesInParenthesis(outLines)

writeFile(outLines, 'out.txt')

