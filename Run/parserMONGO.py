import pymongo
from lxml import etree
from xml.dom import minidom

#parseo con 1 XML para Items

testfile = open('items-0.xml', 'r')

root = etree.parse(testfile)

Items = []

for Item in root.xpath('.//Item'):
    Item = {'Name' : Item.find('Name').text,
            'Category' : Item.find('Category').text,
            'Currently' : Item.find('Currently').text,
            'First_Bid' : Item.find('First_Bid').text,
            'Number_of_Bids' : Item.find('Number_of_Bids').text,
            'Bids' : Item.find('Bids').text,
            'Location' : Item.find('Location').text,
            'Country' : Item.find('Country').text,
            'Started' : Item.find('Started').text,
            'Ends' : Item.find('Ends').text,
            'Seller' : Item.find('Seller').text,
            'Description' : Item.find('Description').text}
    Items.append(Item)
	
#Parseo para el mismo XML pero Usuario

Usuarios = []

#Para los Compradores
for Usuario in root.xpath('./Item/Bids/Bid'):
	Usuario = { 'Bidder' : Usuario.find('Bidder').text}
	Usuarios.append(Usuario)
#Para los Vendedores	
for Usuario in root.xpath('.//Item'):
    Usuario = {'Seller' : Usuario.find('Seller').text}
    Usuarios.append(Usuario)
	
	
#Ingresar los arrays a las colecciones de Mongo 
db = pymongo.MongoClient()
collection = db.test

collection.insert(Items)

collection.insert(Usuarios)

#Esto es lo unico que no funciona