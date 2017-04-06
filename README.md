# Electronic-book-share-platform

IN project_database folder:
sql_operate.py : I creat a python class in this file, you could connected to our database throw it
import_data.py : You could insert data in the diagram on our database by this file 

Server ：SQLserver
ip：192.168.0.109
port ：1434
account ：EBook
password ：ebook
database：ebookdata
Attention : To connect to the database, you need to connect same local area network with server.

Database Diagrams：
PaperAuthorRadius : PaperID   Author  Radius (ie:weight of the paper)
PaperField ：PaperID   LevelOneField  LevelTwoField



IN Map folder:
img_produce.py : create different levels debris of the Map 
img_combiner.py : connect debris of different levels to get whole Map of different levels