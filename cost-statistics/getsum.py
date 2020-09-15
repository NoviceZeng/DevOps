#!/root/.pyenv/shims/python
def get_sum_dic(file):
    dict_result = dict()
    with open(file,'r') as f:
        for line in f.readlines():
            key = line.split()[0].lower()
            value = float(line.split()[1])
            if key in dict_result.keys():
                dict_result[key] += value
            else :
                dict_result[key] = value
    return dict_result

def save_dic_to_file(dic):
    f1 = open('results.txt','w+')
    #遍历字典key,根据key，获取对应value
    for k in dic:
        #输出金额右对齐
        space = 40 - len(k)
        #金额保留三位小数位，做字符串拼接操作，保持右对齐
        line = k + ' '*space + str(round(dic[k],3))
        print(line)
        #存至文件
        f1.write(line + '\n')
    f1.close()

def main():
    dic = get_sum_dic('SourceData.txt')
    save_dic_to_file(dic)

if __name__ == '__main__':
    main()
