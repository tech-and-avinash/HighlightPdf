import xml.etree.ElementTree as ET
import re
import copy
import fitz
import os
os.system("pdf2txt.py -o Bauman.xml Bauman.pdf") # <-- Edit info

tree = ET.parse('D:/ReadPDF/pdfprocess/Bauman.xml') # <-- Edit info
root = tree.getroot()
requiredFont = "CourierNewPSMT"
answers = ''
paragraph = []
sentence_words = []
sentences = []
givenDictionary = [{'cat':'communication', 'syn' : ['I am straight', 'determined', 'forward'], 'color': (1, 0, 0)}, {'cat':'planning', 'syn' : ['challenge'], 'color': (1, 1, 0)}] # <-- Edit info
# actualDictionary = {"Commnunication": ['I am straight', 'determined', 'forward'], "Staffing": ['challenge']}
actualDictionary = {}

for items in givenDictionary:
    keys = list(items.keys())
    category = items[keys[0]]
    matchWords = items[keys[1]]
    actualDictionary[category] = matchWords

# print(actualDictionary)
matchedSentences = copy.copy(actualDictionary)

for category in matchedSentences:
    matchedSentences[category] = []

for pages in root:
    # print(pages.tag, pages.attrib)
    for textbox in pages:
        # print(textbox.tag, textbox.attrib)
        for textline in textbox:
            # print(textline.tag, textline.attrib)
            for text in textline:
                # print(dir(text))
                # print(text.tag, text.attrib)
                # print "Attribute Name : ", s.attributes['name'].value
                font = text.get('font')
                if text.get('font') == requiredFont:
                    # print(text.text)
                    if(text.text == None):
                        text.text = " "
                    answers = answers+text.text
# print(answers)
paragraph.append(answers)

for element in paragraph:
    sentence_words += re.split(r"(?<=[.!?])\s+", element)

# for lines in sentence_words:
    # print(lines)
    # isFound = lines.find()
    # print(isFound)

for words in actualDictionary:
    # print(dictionary[words])
    keywordsList = actualDictionary[words]
    for keys in keywordsList:
        for lines in sentence_words:
            isFound = lines.find(keys)
            if isFound != -1:
                categories = matchedSentences[words]
                checkIfexists = lines in categories
                # print(checkIfexists)
                if checkIfexists == False:
                    matchedSentences[words].append(lines)
                # print(lines)
# print(matchedSentences)
doc = fitz.open('Bauman.pdf') # <-- Edit info
getTotalNoOfPages = doc.pageCount
# print('getTotalNoOfPages', getTotalNoOfPages)

# ITERATE OVER PAGES AND KEYWORDS
for pageNumber in range(getTotalNoOfPages):
    # print('pageNumber', pageNumber)
    currentPage = doc[pageNumber]
    
    for categories in matchedSentences:
        # print(matchedSentences[categories])
        tobeHighlighted = matchedSentences[categories]
        # print(tobeHighlighted)
        givenCategory = next(item for item in givenDictionary if item[list(item.keys())[0]] == categories)
        givenColor = givenCategory[list(givenCategory.keys())[2]]
        for sentence in tobeHighlighted:
            text_instances = currentPage.searchFor(sentence)
            for inst in text_instances:
                highlight = currentPage.addUnderlineAnnot(inst)
                highlight = currentPage.addHighlightAnnot(inst)
                highlight.setColors({"stroke": givenColor}) # yellow
                highlight.update()

doc.save("output.pdf", garbage=4, deflate=True, clean=True)
