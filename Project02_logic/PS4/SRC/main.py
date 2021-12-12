# Nguyễn Lê Quang
# 19120121

import os

def sortAlphabet(l):
    n=len(l)
    for i in range(0,n-1):
        for j in range(i+1,n):
            first=l[i]
            second=l[j]
            if first[0]=='-':
                first=first[1]
            if second[0]=='-':
                second=second[1]
            if second<=first:
                temp=l[i]
                l[i]=l[j]
                l[j]=temp
    return l


def converLiteral(literal):
    if len(literal)==2:
        return literal[1]
    else:
        return "-"+literal


def converLink(link):
    if link=='OR':
        return 'AND'
    else:
        return 'OR'

def converSentence(sen):
    literals=sen.split(' ')
    l=len(literals)
    for i in range(0,l):
        if i%2==0:
            literals[i]=converLiteral(literals[i])
        else:
            literals[i]=converLink(literals[i])
    return (' ').join(literals)

def isOppositeLiteral(a,b):
    if len(a)==len(b):
        return False
    else:
        if len(a)==2:
            a=a[1]
        if len(b)==2:
            b=b[1]
        return a==b

def isContainOpposit(a,b):
    list_first=a.split(' OR ')
    list_second=b.split(' OR ')
    conver_first_list=[]
    for e in list_first:
        conver_first_list.append(converLiteral(e))
    for ele in conver_first_list:
        if ele in list_second:
            return True
    return False


def factoring(first_sen,second_sen):
    list_first=first_sen.split(' OR ')
    list_second=second_sen.split(' OR ')
    first_index=[]
    second_index=[]
    for i in range(0,len(list_first)):
        for j in range(0,len(list_second)):
            if isOppositeLiteral(list_first[i],list_second[j]):
                first_index.append(i)
                second_index.append(j)
    if len(first_index)!=1 or len(second_index)!=1:
        return 'null'
    list_first.remove(list_first[first_index[0]])
    list_second.remove(list_second[second_index[0]])
    list_res=[]
    list_res.extend(list_first)
    list_res.extend(list_second)
    list_res=list(set(list_res))
    list_res=sortAlphabet(list_res)
    if len(list_res)==0:
        return '{}'
    return ' OR '.join(list_res)

def sortInputAlphabet(sens):
    l=sens.split(' OR ')
    sorted_list=sortAlphabet(l)
    return ' OR '.join(sorted_list)

    
def PL_RESOLUTION(f_in,f_out):
    fin=open('input/'+f_in,"r")
    fout= open('output/'+f_out,"w")    
    alpha=fin.readline()
    alpha=alpha[0:len(alpha)-1]
    n=int(fin.readline())
    sentences=[]
    if len(alpha)<=2:
        sentences.append(converLiteral(alpha))
    else:
        x=converSentence(alpha)
        list_x=x.split(' AND ')
        for e in list_x:
            sentences.append(e)

    for i in range(0,n-1):
        sen=fin.readline()
        sentences.append(sen[0:len(sen)-1])
    sentences.append(fin.readline())
    for e in sentences:
        if len(e)>2:
            e=sortInputAlphabet(e)
    fin.close()
    first_index=0
    second_index=1
    while True:
        additionList=[]
        for i in range(first_index,len(sentences)-1):
            for j in range(second_index,len(sentences)):
                if i<j:
                    if isContainOpposit(sentences[i],sentences[j]):
                        factor=factoring(sentences[i],sentences[j])
                        # print('('+sentences[i]+') hop giai voi ( '+sentences[j]+"===>"+factor)
                        additionList.append(factor)
        # print('----------------')
        if len(additionList)==0:
            fout.write("0\n")
            fout.write('NO')
            break
        else:
            additionList=list(set(additionList))
            additionList=sortAlphabet(additionList)
            
            if 'null' in additionList:
                additionList.remove('null')
            second_index=len(sentences)
            
            temp=[]
            for e in additionList:
                if e in sentences:
                    temp.append(e)
            for e in temp:
                additionList.remove(e)
            if len(additionList)!=0:
                fout.write(str(len(additionList)))
                fout.write('\n')
            
            for e in additionList:
                    fout.write(e)
                    fout.write('\n')
                    sentences.append(e)
        if '{}' in sentences:
            fout.write('YES')
            break
    fout.close()

#ham Main

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_INPUT=ROOT_DIR+'\input'
ROOT_OUTPUT=ROOT_DIR+'\output'

for file in os.listdir(ROOT_INPUT):
    file_input=file
    print(file)
    file_output='output'+file[file.find('_'):]
    print(file_output)
    PL_RESOLUTION(file_input,file_output)
