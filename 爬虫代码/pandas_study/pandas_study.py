import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import  datetime as dt
#创建Series字典对象

#//默认以数字从0开始作为键值,使用np.nan表示为空，不参与计算
s = pd.Series([1,3,5,np.nan,6,8])
print(s)

#传入键和值
s = pd.Series(data=[1,2,3,4],index=['a','b','c','d'])
print(s)
print(s.index)#获取键列表
print(s.values)#获取值列表


#DataFrame表格对象
df2 = pd.DataFrame({
    'A':1,
    'B':pd.Timestamp('20180702'),
    'C':pd.Series(1,index=(range(1,5)),dtype='int32'),#传入键，并公用
    'D':np.array([3]*4,dtype='int32'),
    'E':pd.Categorical(['test','train','test','train']),
    'F':'foo'
})
print(df2)

#pd.Timestamp的用法
p1 = pd.Timestamp(2018,7,2)
print(p1)#年月日小时分秒

p2 = pd.Timestamp(dt(2018,7,2,hour=9,minute=12,second=45))
print(p2)

p3 = pd.Timestamp("2018-7-2")
print(p3)

#pd.Categorical的用法，这是用来分类的函数

s1 = pd.Series(['a','b','c','a'],dtype='category')
print(s1)
#传入的元素有4个，但类别只有3个

s2 = pd.Categorical(['a','b','c','d','a','c',0],['a','c','b',0],ordered=True)
print(s2)
#第二个参数表示类别，不在类别中的返回NaN

#pd.date_range的用法
#pd.date_range(start=None,end=None,periods=None,freq='D',tz=None,
              #normalize=False,name=None,closed=None)

#start：string或datetime-like，默认值是None，表示日期的起点。
#end：string或datetime-like，默认值是None，表示日期的终点。
#periods：integer或None，默认值是None，表示你要从这个函数产生多少个日期索引值；
# 如果是None的话，那么start和end必须不能为None
#freq：string或DateOffset，默认值是’D’，表示以自然日为单位，
# 这个参数用来指定计时单位，比如’5H’表示每隔5个小时计算一次。
#tz：string或None，表示时区，例如：’Asia/Hong_Kong’。
#normalize：bool，默认值为False，如果为True的话，那么在产生时间索引值之前会先把start和end都转化为当日的午夜0点。
#name：str，默认值为None，给返回的时间索引指定一个名字。
#closed：string或者None，默认值为None，表示start和end这个区间端点是否包含在区间内，可以有三个值，’left’表示左闭右开区间，
# ’right’表示左开右闭区间，None表示两边都是闭区间。

date = pd.date_range(start='20180601',end='20180701',periods=6)
df = pd.DataFrame(np.random.randn(6,4),index=date,columns=list('ABCD'))
print(df)
#np.random.randn(),从标准正态分布中随机生成一个或多个，一维或二维随机数
#np.random.rand()从标准正态分布中随机生成一个或多个，一维或二维随机数,且样本位于[0,1]

#查看头尾数据
print(df.head(3))#查看前3行，默认值为5
print(df.tail(3))#查看后3行，默认值为5
print(df.columns)#查看列键
print(df.index)#查看行键
print(df.values)#查看值
print(df.describe())#查看概况
print(df.mean())#求列平均
print(df.mean(1))#求行平均


print(df.T)#转置
print(df.sort_index(axis=1,ascending=False))#根据列名排序
print(df.sort_values(by='B'))#根据某一列的值排序

print(df['A'])#选择单列
print(df[0:3])#选择局部

#标签选择,通过行键，列键
print(df.loc[date[0]])#选择一行
print(df.loc[:,['A','B']])#局部选择
print(df.loc['20180601':'20180613',['A','C']])
print(df.loc[date[0],'A'])#具体选择某个元素
print(df.at[date[0],'A'])

#位置选择，存在一个从0开始，类似于数组
print(df)
print(df.iloc[3])#第四行
print(df.iloc[3:5,0:2])
print(df.iloc[[1,2,4],[0,2]])
print(df.iloc[1,1])
print(df.iat[1,1])

#布尔索引
print(df[df.A > 0])
print(df[df > 0])
df2 = df.copy()
df2['E'] = ['one','two','three','four','five','six']
print(df2)

#修改数据
df['new'] = df['A'].map(str)+df['B'].map(str)+df['C'].map(str)+df['D'].map(str)#要先把他转为字符串，如果是数字类型的那么会直接相加，虽然字符串也是直接相加的
print(type(df.iloc[1,4]))
df.at[date[0],'A'] = 0 #赋值单个元素
df.iat[0,1]=0

df.loc[:,'D'] = np.array([5]*len(df)) #通过numpy赋值列


df = pd.DataFrame(np.random.randn(6,4),index=date,columns=list('ABCD'))

df3 = df.copy()
df3[df3 > 0] = -df
print(df3)

#修改索引
df1 = df.reindex(index=date[0:4],columns = list(df.columns) + ['H'])
print(df1)

#缺失值处理
#去掉缺失行
print(df1.dropna(how='any'))#去掉任何一个有缺失值的行

#填充缺失值
df4 = df1.fillna(value=6)#并没有对df1进行修改
print(df4)
#判断是否为缺失值
print(pd.isnull(df1))

s = pd.Series([1,3,5,np.nan,6,8],index=date)
print(s)
print(s.shift(2))