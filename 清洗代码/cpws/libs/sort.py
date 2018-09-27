
# sort person
def sort(person):
    return sorted(person, key=lambda x: x['local'])

if __name__ == '__main__':
    a = [{'local': 1, 'name': '北京银行股份有限公司西安分行', 'resume': '住所地西安市碑林区和平路116号', 'role': '申请执行人'}, {'local': 3, 'name': '杨飞', 'resume': '男，1980年12月7日出生，汉族，府谷县三道沟镇野猪峁养殖有限责任公司总经理，住陕西省府谷县三道沟乡玉则墕村野猪峁自然村001号', 'role': '被执行人'}, {'local': 2, 'name': '赵政党', 'resume': '行长', 'role': '负责人'}]
    print(sort(a))