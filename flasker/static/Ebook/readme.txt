sql_operate.py中分装好了一个访问数据库的类，可通过它进行访问
import_data.py用于像数据库表单中插入数据

（需要同一个局域网下才能连接）
数据库服务器类型：SQLserver
数据库host的ip：192.168.0.109
端口：1434
登录账号：EBook
密码：ebook
database：ebookdata

数据库表格：
PaperAuthorRadius : 记录文章的ID,作者以及权重（列：PaperID   Author  Radius）
PaperField ：记录文章所从属的一级领域和二级领域（列：PaperID   LevelOneField  LevelTwoField）

json数据层次解析：
第一层：count，name，child // count代表总论文数量，name表示地图名字（Acmap），child代表一级领）
第二层：count，name，color，r，child  // color代表颜色，r代表半径，name（Environmental science），child代表二级领域
第三层：count，name，color，r，papers // papers代表论文（和child一样是“数组”），name（Waste management）
第四层：author，color，r，y，x，ID // y，x代表出现坐标，ID表示论文编号
建议根据r的大小，减少第四层（paper）层的数量

在Map文夹夹中，包含了地图切片生成以及地图连接的代码

PS:平时我不会开启数据库，如果需要启动的话，请联系我