"""
FILE: skeleton_parser.py
------------------
Author: Garrett Schlesinger (gschles@cs.stanford.edu)
Author: Chenyu Yang (chenyuy@stanford.edu)
Modified: 10/13/2012
Skeleton parser for cs3057 lab #6. Has useful imports and functions for parsing,
including:
1) Directory handling -- the parser takes a list of eBay xml files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the xml files store dollar value amounts in 
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the xml files store dates/ times in the form 
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.
4) A function to get the #PCDATA of a given element (returns the empty string
if the element is not of #PCDATA type)
5) A function to get the #PCDATA of the first subelement of a given element with
a given tagname. (returns the empty string if the element doesn't exist or 
is not of #PCDATA type)
6) A function to get all elements of a specific tag name that are children of a
given element
7) A function to get only the first such child
Your job is to implement the parseXml function, which is invoked on each file by
the main function. We create the dom for you; the rest is up to you! Get familiar 
with the functions at http://docs.python.org/library/xml.dom.minidom.html and 
http://docs.python.org/library/xml.dom.html
Happy parsing!
"""

import sys
from xml.dom.minidom import parse
from re import sub

columnSeparator = "<>"
ctgory = []    #array de categorias
placename = []   #array de locaciones
user = []    #array de usuario
rel = []    #array de relacion entre item y categoria

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
                'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


"""
Returns true if a file ends in .xml
"""
def isXml(f):
    return len(f) > 4 and f[-4:] == '.xml'

"""
Non-recursive (NR) version of dom.getElementsByTagName(...)
"""
def getElementsByTagNameNR(elem, tagName):
    elements = []
    children = elem.childNodes
    for child in children:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
            elements.append(child)
    return elements

"""
Returns the first subelement of elem matching the given tagName,
or null if one does not exist.
"""
def getElementByTagNameNR(elem, tagName):
    children = elem.childNodes
    for child in children:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
            return child
    return None

"""
Parses out the PCData of an xml element
"""
def pcdata(elem):
        return elem.toxml().replace('<'+elem.tagName+'>','').replace('</'+elem.tagName+'>','').replace('<'+elem.tagName+'/>','')

"""
Return the text associated with the given element (which must have type
#PCDATA) as child, or "" if it contains no text.
"""
def getElementText(elem):
    if len(elem.childNodes) == 1:
        return pcdata(elem) 
    return ''

"""
Returns the text (#PCDATA) associated with the first subelement X of e
with the given tagName. If no such X exists or X contains no text, "" is
returned.
"""
def getElementTextByTagNameNR(elem, tagName):
    curElem = getElementByTagNameNR(elem, tagName)
    if curElem != None:
        return pcdata(curElem)
    return ''

def getElementsTextByTagNameNR(elem, tagName):
    elements = []
    curElems = getElementsByTagNameNR(elem, tagName)
    return curElems

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon] 
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Revisa si se encuentra el objeto, lo agrega unicamente si es necesario 
de lo contrario, regresa el id correspondiente a ese objeto
"""

def addCategory(catgory):
    if catgory in ctgory:
        return ctgory.index(catgory)
    else: 
        ctgory.append(catgory)
        return len(ctgory)-1

def addPlaceName(locatn):
    if locatn in placename:
        return placename.index(locatn)
    else: 
        placename.append(locatn)
        return len(placename)-1

def addUser(usrs):
    if usrs in user:
        return user.index(usrs)
    else: 
        user.append(usrs)
        return len(user)-1

"""
Parses a single xml file. Currently, there's a loop that shows how to parse
item elements. Your job is to mirror this functionality to create all of the necessary SQL tables
"""
def parseXml(f):
    dom = parse(f) # creates a dom object for the supplied xml file
    """
    TO DO: traverse the dom tree to extract information for your SQL tables
    """

    element = getElementByTagNameNR(dom, "Items")
    item = getElementsByTagNameNR(element, "Item")
    #parceo de cada item
    for i in range(len(item)):

       fileItems.write(item[i].getAttribute('ItemID')  + '<>')

    global indexAcc
        #revisa cada categoria encontrada en un item
    categories = getElementsByTagNameNR(item[i],"Category")
    for o in range(len(categories)):
        category = getElementText(categories[o])
        rel.append(category)
        fileItemCateg.write(str(indexAcc)+"<>"+str(addCategory(category))+'\n')
            
        indexAcc = indexAcc +1
        seller = getElementByTagNameNR(item[i],"Seller")
        usu = addUser(seller.getAttribute('UserID')+"<>"+seller.getAttribute('Rating'))
        fileItems.write(str(usu) + '<>')

        location = getElementTextByTagNameNR(item[i], "Location")
        country  = getElementTextByTagNameNR(item[i], "Country")
        loc = addPlaceName ( str(location)+"<>"+str(country)) 
        fileItems.write(str(loc)+"<>") 

        name = getElementTextByTagNameNR(item[i], 'Name')
        fileItems.write(str(name) + '<>')

        description  = getElementTextByTagNameNR(item[i], 'Description')
        if description  != '' :
           fileItems.write(str(description)  + '<>')
        else:
           fileItems.write('NULL<>')

        bprice = getElementTextByTagNameNR(item[i], 'Buy_Price')
        if bprice != '' :
           fileItems.write(transformDollar(bprice) + '<>')
        else:
           fileItems.write('NULL<>')

        currently = getElementTextByTagNameNR(item[i], 'Currently')
        fileItems.write(transformDollar(currently) + '<>')

        fBid = getElementTextByTagNameNR(item[i], 'First_Bid')
        fileItems.write(transformDollar(fBid) + '<>')

        nBids = getElementTextByTagNameNR(item[i], 'Number_of_Bids')
        fileItems.write(nBids + '<>')

        start = getElementTextByTagNameNR(item[i], 'Started')
        if start != '' :
           fileItems.write(transformDttm(start) + '<>')
        else:
           fileItems.write('NULL<>')
        end = getElementTextByTagNameNR(item[i], 'Ends')
        if end != '' :
           fileItems.write(transformDttm(end) + '\n')
        else:
           fileItems.write('NULL\n')

        global indexSec

        #revisa cada bid encontrada en un item
        bids = getElementByTagNameNR(item[i], "Bids")
        bid = getElementsByTagNameNR(bids, "Bid")
        for o in range(len(bid)):
            bidtime = getElementTextByTagNameNR(bid[o],"Time")
            amount = getElementTextByTagNameNR(bid[o],"Amount")

            bidder = getElementByTagNameNR(bid[o],"Bidder")

            location = getElementTextByTagNameNR(bidder, "Location")
            country  = getElementTextByTagNameNR(bidder, "Country")
            loc = addPlaceName ( str(location)+"<>"+str(country)) 

            usu = addUser(seller.getAttribute('UserID')+"<>"+seller.getAttribute('Rating'))
            fileBids.write(str(indexSec)+"<>"+str(usu)+"<>"+str(loc)+"<>"+str(transformDttm(bidtime))+"<>"+str(transformDollar(amount))+'\n')
        indexSec = indexSec + 1
    
    dom.unlink()
"""
Loops through each xml files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python parser.py <path to xml files>'
        sys.exit(1)

    #Abre los archivos para escribir en ellos
    global fileItemCateg
    global fileBids
    global fileItems

    fileItemCateg = open("ItemCateg.dat",'w')
    fileBids = open("Bids.dat",'w')
    fileItems = open('Publications.dat', 'w')
  
    global indexAcc
    global indexSec
    
    indexAcc = 0 
    indexSec = 0 #Donde es el indice secundario 

    #Parceo de data y escritura mientras los archivos se encuentran abiertos 
    # loops over all .xml files in the argument
    for f in argv[1:]:
        if isXml(f):
            parseXml(f)
            print "Success parsing " + f

    #cerrar archivos
    fileItemCateg.close()
    fileBids.close()
    fileItems.close()

    #se agregan los atributos recolectados en archivos
    fileCategory=open("FileCategories.dat",'w')
    for i in range(len(ctgory)):
        fileCategory.write(str(i)+"<>"+str(ctgory[i])+'\n')
    fileCategory.close()

    fileLocations = open('FilePlacesNames.dat', 'w')
    for i in range(len(placename)):
        fileLocations.write(str(i) + '<>' + str(placename[i]) + '\n')
    fileLocations.close()

    fileUsers= open('FileUsers.dat', 'w')
    for i in range(len(user)):
        fileUsers.write(str(i) + '<>' + str(user[i])+ '\n')
    fileUsers.close()

if __name__ == '__main__':
    main(sys.argv)

"""
Modificado por:
Maria Mercedes Retolaza 
Jose Rodolfo Perez 
Universidad del Valle de Guatemala 
Bases de Datos, Laboratorio 6 2018 
"""