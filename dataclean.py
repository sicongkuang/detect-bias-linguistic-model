# -*- coding: utf-8 -*-
__author__ = 'wxbks'
from unidecode import unidecode
import re
import string
from nltk.metrics import *

def stripped(test_str):
    ret = ''
    skip1c = 0 #[
    skip2c = 0 #<
    skip3c = 0 #{
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '<':
            skip2c += 1
        elif i == '{':
            skip3c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ']' and skip1c == 0:
            continue
        elif i == '>'and skip2c > 0:
            skip2c -= 1
        elif i == '>' and skip2c == 0:
            continue
        elif i == '}' and skip3c > 0:
            skip3c -= 1
        elif i == '}' and skip3c == 0:
            continue
        elif skip1c == 0 and skip2c == 0 and skip3c == 0:
            ret += i
    return ret


def editsWordsList(str):
    '''
        return list of words in the string
        e.g: str = "-this is. A - sentence;one-word what's"
        """ Output:
        ['this', 'is', 'A', 'sentence', 'one-word', "what's"]
        """
    '''
    wordl = []
    # wordl = re.compile('\w+').findall(str.strip('.,/"=:<>').lower())
    wordl = filter(None,[word.strip(string.punctuation)
                 for word in str.replace(';','; ').split()
                 ])
    # print wordl
    return wordl

def checkHttpLink(lst):
    '''
    return false if the list only contain urls
    :param str2: input the list of the difference
    '''
    # urls = []
    if lst == [] or lst == ['']:
        return False # if two string equal or post is empty(delete), tuple is good
    for s in lst:
        if len(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', s)) != 0:
            lst.remove(s)
    if len(lst) == 0:
        return True # bad tuple,delete it
    else:
        return False # good tuple

# in use
def checkHttpOnly(str0,str1):
    f0 = filter(None,re.split('[\[\]\s]',str0))
    f1 = filter(None,re.split('[\[\]\s]',str1))
    nl = list(set(f1).symmetric_difference(set(f0)))
    # filter all punctuations
    # print nl
    for i,v in enumerate(nl):
        nl[i]=v.strip(string.punctuation)
    unpuncL = [i for i in nl if any(j not in string.punctuation and not j.isdigit() for j in i)]
    # print unpuncL
    return checkHttpLink(unpuncL)

def check5gram(str):
    if len(editsWordsList(stripped(str))) <= 5:
        return False
    else:
        return True

def dataclean(_file):
    file = open(_file,'r')
    ## text to record tuples deleted coz column4 is False
    column4F = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_column4False_Oct30.txt','w')
    column4T = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_column4True_Oct30.txt','w')
    tupInTitl = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7SingleBiaW_col9NotEmp_biasedWordinTitle_Oct28.txt','w')
    goodTup = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7SingleBiaW_col9NotEmp_biasedWordNotinTitle_Oct28.txt','w')
    notSingleBia = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7notsingleBiaW_Oct28.txt','w')
    col9Emp = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7singleBiaW_col9Empty_Oct28.txt','w')
    col7col8HyL = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7singleBiaW_col9NotEmp_biasWordNotinTit_col7col8difHyperL_Oct28.txt','w')
    col7col8NotHyL = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7singleBiaW_col9NotEmp_biasWordNotinTit_col7col8NotdifHyperL_Oct28.txt','w')
    after5 = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7singleBiaW_col9NotEmp_biasWordNotinTit_col7col8NotdifHyperL_col8within5_Oct28.txt','w')
    afterNot5 = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7singleBiaW_col9NotEmp_biasWordNotinTit_col7col8NotdifHyperL_col8Exceed5_Oct28.txt','w')
    distance4 = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7singleBiaW_col9NotEmp_biasWordNotinTit_col7col8NotdifHyperL_col8within5_col7col8editDisGreat4_Oct28.txt','w')
    distanceNot4 = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7singleBiaW_col9NotEmp_biasWordNotinTit_col7col8NotdifHyperL_col8within5_col7col8editDisLess4_Oct28.txt','w')

    num_line = 0
    for line in file:
        line = line.decode('utf8')
        line = unidecode(line)
        line = line.lower()
        nline = line.rstrip('\n').split('\t')
        ## check if column 4 is true
        print nline
        if nline[3] == 'true':
            column4T.write(line)
            strip_col6 = nline[6]
            res_col6 = re.findall('^[A-Za-z-]+$',strip_col6)
            if not res_col6:
                notSingleBia.write(line)
                # res_col6 is empty; no match; col6 is not single-word
            else:
                if nline[8]:
                    # further check if the biased word within title
                    str_col6 = string.join(res_col6)
                    s1='.*==.*'
                    patt = s1+str_col6+s1
                    res_pat = re.findall(patt,nline[8])
                    if not res_pat:
                        ## col4 is true;col7 is single;col9 is not null;col7 is not in title;

                        goodTup.write(line)
                        ## check if col7 and col8 only differ by hyperlink
                        if not checkHttpOnly(nline[6],nline[7]):
                            ## differ more than hyperlink
                            col7col8NotHyL.write(line)
                            ## check if after form string contained five or fewer words
                            if not check5gram(nline[7]):
                                ## after form is <=5
                                after5.write(line)
                                ## check if before form string and after form distance <4
                                n = nline[6].strip(string.punctuation)
                                m = nline[7].strip(string.punctuation)
                                if edit_distance(n,m)>=4:
                                    ## distance of before after strings >=4
                                    distance4.write(line)
                                    num_line+=1
                                else:
                                    ## distance of before after strings <4
                                    distanceNot4.write(line)
                            else:
                                ## after form is >5
                                afterNot5.write(line)

                        else:
                            ## col7 and col8 differ by hyperlink
                            col7col8HyL.write(line)

                    else:
                        ## bad in title
                        tupInTitl.write(line)

                else:
                    col9Emp.write(line)

        else:
            column4F.write(line)


    column4F.close()
    column4T.close()
    goodTup.close()
    tupInTitl.close()
    notSingleBia.close()
    col9Emp.close()
    col7col8HyL.close()
    col7col8NotHyL.close()
    after5.close()
    afterNot5.close()
    distance4.close()
    distanceNot4.close()
    file.close()
    print num_line


dataclean('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npov-edits/5gram-edits-train.tsv')