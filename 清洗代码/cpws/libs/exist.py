

def is_exist(keywords, sentence):
    """判断是否句子中是否存在某个关键词"""
    for word in keywords:
        if word in sentence:
            return False
    else:
        return True

def is_exist_test():
    keywords = ['生活']
    sentence1 = '生活在这样的'
    sentence2 = '汪峰喜欢谁'
    assert is_exist(keywords, sentence1) == True
    assert is_exist(keywords, sentence2) == False

if __name__ == '__main__':
    is_exist_test()