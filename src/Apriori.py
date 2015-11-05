#__author__ = 'dhs'
#-*- coding:utf-8 -*-

def get_len(slist):  #  获取列表真实长度
    num = len(slist)
    true_num = num
    i = 0
    while i < num:
        item = slist[i]
        if item in slist[i+1:]:
            true_num-=1
        i+=1
    return true_num

def perms(elements):  # 将列表中的数据全排列
    if len(elements) <=1:
        yield elements
    else:
        for perm in perms(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]


class apriori():
    def __init__(self):
        self.data = '/home/dhs/Documents/github/apriori/data/data'
        self.min_support = 0.02  # 最小支持度
        self.bef_list = []  # 存储文件内容转换后的列表
        self.allitem=[]  # 存储初始的每一项数据 [['A'],['B']……]
        self.dict = {}   # 存储初始项及出现频率
        self.pro_dict={}  #存储各种组合以及其发生的概率
        self.all_sources = []  #存储频繁项集 [[一频繁],[二频繁],……]
        self.final_dict={}  # 存储associate rule项及值
        self.length = 0 # 初始数据的个数
        self.count = 1

    def get_data(self):  # get data and times
        for line in open(self.data,'r'):
            self.bef_list.append(line.strip().split(','))
        for data_list in self.bef_list:  # 统计次数
            for item in data_list:
                if item not in self.dict:
                    self.dict.setdefault(item,1)
                else:
                    self.dict[item]+=1
        self.length = len(self.bef_list)
        for item in self.dict:  # 计算出现的概率转换成列表存储或者存储到字典中
            a=[]
            b=[]
            b.append(item)
            pro = float(self.dict[item])/float(self.length)
            self.pro_dict[str(b)] = pro
            if pro > self.min_support:
                a.append(item)
                self.allitem.append(a)
        self.all_sources.append(self.allitem)

    def get_subsets(self):  #处理的总函数
        while len(self.all_sources[-1])>0: # 判断是否继续求频繁项集
            src_list = []  # 中间暂存列表
            self.bridge(self.all_sources[self.count-1],src_list)
            self.judge(src_list)
            self.all_sources.append(src_list)
            self.count+=1
        print "The final frequency set is:"
        for item in self.all_sources[-2]:
            print item
        print "The rule is as follows:"
        for item in self.all_sources[-2]:
            self.get_results(item)
        print "The associative rule is:"
        for item in self.final_dict:
            print "%s        %4f"%(item,self.final_dict[item])

    def bridge(self,list_1,list_2):  # 把list_1自连接,生成的每一个项集都以列表的形式存入list_2
        num = len(list_1)
        i=0
        while i < num:
            j=0
            while j< num:
                if list_1[j] != list_1[i]:
                    test_list =[]
                    test_list+=list_1[i]
                    test_list+=list_1[j]
                    test_list=list(set(test_list)) # 消除重复项
                    if len(test_list) == self.count+1: # 判断是否存在重复项
                        if test_list not in list_2:  # 判断列表中是否已经存在
                            list_2.append(test_list)
                j+=1
            i+=1
        return list_2

    def judge(self,slist):  #判断列表中的元素是否为频繁项集，并加以处理
        count=0
        num = len(slist)
        while count < num:
            n = get_len(slist[count])
            if n == self.count+1:  #
                if self.get_pro(slist[count]) < self.min_support:
                    del slist[count]
                    num-=1
                else:
                    count+=1
            else:
                del slist[count]
                num-=1

    def get_pro(self,slist):  # 计算项集出现的概率
        count = 0
        for item in self.bef_list:
            if get_len(item+slist) == len(item):
                count+=1
        pro = float(count)/float(self.length)
        self.pro_dict[str(list(set(slist)))]=pro
        return pro

    def get_results(self,slist):  # 根据最后得到的项集 全排列 并消重输出
        global before_list
        global back_list
        before_list=[]
        back_list = []
        num = len(slist)
        for item in list(perms(slist)):
            i=1
            while i <= num-1:
                if list(set(item[0:i])) in before_list:
                    if list(set(item[i:])) in back_list:
                        if before_list.index(list(set(item[0:i]))) != back_list.index(list(set(item[i:]))):
                            before_list.append(list(set(item[0:i])))
                            back_list.append(list(set(item[i:])))
                    else:
                        before_list.append(list(set(item[0:i])))
                        back_list.append(list(set(item[i:])))
                else:
                    before_list.append(list(set(item[0:i])))
                    back_list.append(list(set(item[i:])))
                i+=1
        self.get_confidence(slist)


    def get_confidence(self,slist):  #获取置信度
        l = len(before_list)
        i = 0
        while i < l:
            print "%s->%s"%('^'.join(before_list[i]),'^'.join(back_list[i])),
            pro = self.pro_dict[str(list(set(slist)))] / self.pro_dict[str(list(set(before_list[i])))]
            if pro > 0.4:  # 置信度大于 设置的置信度，即添加到self.final_dict字典中
                self.final_dict['%s->%s'%('^'.join(before_list[i]),'^'.join(back_list[i]))] = pro
            print "        %4f"%pro
            i+=1

if __name__ == '__main__':
    c = apriori()
    c.get_data()
    c.get_subsets()


