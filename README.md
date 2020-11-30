# cn-zb-probase
武器装备概念图谱
以环球军事网数据为基础，从百科中搜集数据进行关系补全
实现应用：智慧推荐

########neo4j导入命令########

LOAD CSV WITH HEADERS  FROM "file:///new_military_b.csv" AS line  
CREATE (p:WuqiItem{id:line.id,Name:line.Name,Country:line.Country,leibie:line.leibie,type:line.type})  


CREATE CONSTRAINT ON (c:WuqiItem)
ASSERT c.id IS UNIQUE
//下面数据项有重复
// 59式57毫米高射炮、53-65KE反舰鱼雷、 81式107毫米轮式自行火箭炮

//导入节点
LOAD CSV WITH HEADERS FROM "file:///leixing.csv" AS line
MERGE (:wuqileixing { type: line.type })

//添加索引
CREATE CONSTRAINT ON (c:wuqileixing)
ASSERT c.type IS UNIQUE

//导入节点
LOAD CSV WITH HEADERS FROM "file:///leibie.csv" AS line
MERGE (:wuqileibie { leibie: line.leibie })

//添加索引
CREATE CONSTRAINT ON (c:wuqileixing)
ASSERT c.leibie IS UNIQUE

LOAD CSV  WITH HEADERS FROM "file:///relation1.csv" AS line
MATCH (entity1:wuqileixing{type:line.type}) , (entity2:wuqileibie{leibie:line.leibie})
CREATE (entity1)-[:subclassOf { type: line.relation }]->(entity2)

LOAD CSV  WITH HEADERS FROM "file:///relation2.csv" AS line
MATCH (entity1:WuqiItem{Name:line.Name}) , (entity2:wuqileixing{type:line.type})
CREATE (entity1)-[:instanceOf { type: line.relation }]->(entity2)


MATCH (n)
OPTIONAL MATCH (n)-[r]-()
DELETE n,r
