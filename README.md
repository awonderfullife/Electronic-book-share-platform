# Electronic-book-share-platform

In project_database folder:<br>
`sql_operate.py` : I create a python class in this file, you could connected to our database throw it<br>
`import_data.py` : You could insert data in the diagram on our database by this file<br>

Server: SQLServer<br>
ip: 192.168.0.109<br>
port: 1434<br>
account: EBook<br>
password: ebook<br>
database: ebookdata<br>
Attention: To connect to the database, you need to connect same local area network with server.<br>

Database Diagrams:<br>
PaperAuthorRadius: PaperID   Author  Radius (ie:weight of the paper)<br>
PaperField: PaperID   LevelOneField  LevelTwoField<br>


In Map folder:<br>
`img_produce.py`: create different levels debris of the Map. <br>
`img_combiner.py`: connect debris of different levels to get whole Map of different levels.<br>