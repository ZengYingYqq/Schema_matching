import pandas as pd
import pymysql
import numpy as np
import random
from bert_serving.client import BertClient

bc = BertClient(ip='localhost')

train = []
train_label = []
data = []

df = pd.read_excel('pkrk.xlsx', sheet_name='SheetJS')

new_column_names = ['rk_table', 'rk1', 'rk2', 'rk3', 'pk_table1',
                    'pk_table2', 'pk_table3']

df.columns = new_column_names

for i in range(0, 80):
    if pd.notna(df.iloc[i, 2]):
        new_row = pd.DataFrame({'rk_table': [df.iloc[i, 0]], 'rk1': [df.iloc[i, 2]], 'pk_table1': [df.iloc[i, 5]]})
        df = pd.concat([df, new_row], ignore_index=True)

    if pd.notna(df.iloc[i, 3]):
        new_row = pd.DataFrame({'rk_table': [df.iloc[i, 0]], 'rk1': [df.iloc[i, 3]], 'pk_table1': [df.iloc[i, 6]]})
        df = pd.concat([df, new_row], ignore_index=True)

df = df.drop(columns=['rk2', 'rk3', 'pk_table2', 'pk_table3'], axis=1)

print("df is ok")

# 连接 MySQL 数据库
conn = pymysql.connect(

    host='192.168.123.100',  # 主机名
    port=3306,  # 端口号，MySQL默认为3306
    user='zy',  # 用户名
    password='yqq000702',  # 密码
    database='alidb',  # 数据库名称
)

print("conn is ok")

cursor = conn.cursor()

# pk rk is matching
for i in range(0, df.shape[0]):
    pk = 'SELECT column_name, column_comment ' \
         'FROM information_schema.columns ' \
         'where table_schema = "alidb" ' \
         'AND table_name = "{}" ' \
         'AND column_name = "{}"'.format(df.iloc[i, 0], df.iloc[i, 1])

    rk = 'SELECT column_name, column_comment ' \
         'FROM information_schema.columns ' \
         'where table_schema = "alidb" ' \
         'AND table_name = "{}" ' \
         'AND column_name = "id"'.format(df.iloc[i, 2])

    cursor.execute(pk)
    pk = cursor.fetchall()
    cursor.execute(rk)
    rk = cursor.fetchall()

    pk_rk_em = bc.encode([pk[0][0], pk[0][1] + '|||' + rk[0][0], rk[0][1]])

    train.append(np.array(pk_rk_em[1]))

    train_label.append(1)

print("pk rk ok")


att = 'SELECT column_name, column_comment, DATA_TYPE ' \
      'FROM information_schema.columns ' \
      'WHERE table_schema = "alidb"'

cursor.execute(att)
att = cursor.fetchall()
att_num = len(att)
print("att num is : {}.".format(att_num))
test_att_num = int(att_num/500)
# temp = bc.encode(["a"])
# att_em = np.empty((test_att_num, temp.shape[1]))
result = []

# self desc
for i in range(0, 400):
    temp = random.randint(0, att_num)
    if att[temp][1]:
        em = bc.encode([att[temp][0], att[temp][1] + ' ||| ' + att[temp][0], att[temp][1]])[1]
    else:
        em = bc.encode([att[temp][0] + ' ||| ' + att[temp][0]])[1]
    train.append(em)
    train_label.append(1)


print("self is ok")
# for i in range(0, 400):
#     temp = random.randint(0, att_num)
#     em = bc.encode([att[temp][0], att[temp][1] + ' ||| ' + att[temp][0], att[temp][1]])[1]
#     train.append(em)
#     train_label.append(1)


# type not matching
count = 0
while count < 500:
    random_att1 = random.randint(0, att_num)
    random_att2 = random.randint(0, att_num)
    if att[random_att1][2] != att[random_att2][2]:
        if att[random_att1][1] and att[random_att2][1]:
            em = bc.encode([att[random_att1][0], att[random_att1][1] + '|||' + att[random_att2][0], att[random_att2][1]])[1]
        else:
            em = bc.encode([att[random_att1][0] + '|||' + att[random_att2][0]])[1]
        train.append(em)
        train_label.append(0)
        count = count + 1

print("type is ok")


for i in range(0, test_att_num):
    for j in range(0, test_att_num):
        result.append(att[i][0] + " and "+att[j][0] + ' matching score is : ')
        em = bc.encode([att[i][0], att[i][1] + '|||' + att[j][0], att[j][1]])[1]
        data.append(em)

print("data is ok")

# shuffle the train data
combined = list(zip(train, train_label))
random.shuffle(combined)
train, train_label = zip(*combined)
print(train_label)

train = np.array(train)
train_label = np.array(train_label)
data = np.array(data)

