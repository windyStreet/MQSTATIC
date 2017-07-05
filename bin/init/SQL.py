from bin.until import Path
from bin.until import JsonFileFunc
import os

P = Path.getInstance()
J = JsonFileFunc.getInstance()
path = P.confDirPath + os.sep + "data.json"

data_json = J.readFile(path)
key_datas = []
value_datas = []
for key in data_json.keys():
    key_datas.append(key)
    value_datas.append("'" + str(data_json[key]) + "'")

key_str = ",".join(key_datas)
value_str = ",".join(value_datas)

sql_str_zone = "insert into trainsignupcard3400 (" + key_str + ") values (" + value_str + ") "
sql_str_card = "insert into trainsignupzone3400 (" + key_str + ") values (" + value_str + ") "
print(sql_str_zone)
print(sql_str_card)

# NSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)
