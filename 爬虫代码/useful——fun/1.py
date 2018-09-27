a = 'dsa'
print(isinstance(a,str))#返回Ture，他是字符串
print(isinstance(a,tuple))#返回False，他不是元组

class obja:
    pass

b = obja()
print(isinstance(b,obja))#返回Ture,他是obja类的object对象