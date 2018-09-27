import numpy

#'使用列表生成二维数组'

data = [[1,2],[3,4],[5,6]]
x = numpy.array(data)
print(x)
print(x.dtype)
print(x.ndim)
print(x.shape)

#使用zero/ones/empty 创建数组，根据shape来创建

x = numpy.zeros(6)#创建一个长度为6的，元素都为0的二位数组
print(x)
x = numpy.zeros((2,3))#创建一个2行3列的数组
print(x)
x = numpy.ones((2,3))#不止对角线，全是1
print(x)
x = numpy.empty((3,3))
print(x)

#使用arrange生成连续元素
print(numpy.arange(6))
print(numpy.arange(0,6,2))

a = [1,2,3,4,5,6]
b = numpy.array(a).reshape(3,2)
print(numpy.array(a).reshape(3,2))
for x in b[1]:
    print(x)
    #print(b[1].index(x))
print(numpy.argwhere(b==3))

