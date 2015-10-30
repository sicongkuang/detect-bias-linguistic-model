__author__ = 'wxbks'
from unidecode import unidecode
from nltk.corpus import stopwords


def dataclean_2508():
    stop = stopwords.words('english')
    distance4 = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7singleBiaW_col9NotEmp_biasWordNotinTit_col7col8NotdifHyperL_col8within5_col7col8editDisGreat4_Oct28.txt','r')
    noStop = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7singleBiaW_col9NotEmp_biasWordNotinTit_col7col8NotdifHyperL_col8within5_col7col8editDisGreat4_noStopWord_Oct28.txt','w')
    isStop = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7singleBiaW_col9NotEmp_biasWordNotinTit_col7col8NotdifHyperL_col8within5_col7col8editDisGreat4_isStopWord_Oct28.txt','w')
    num_tup = 0
    isStop_tup = 0
    for line in distance4:
        line = line.decode('utf8')
        line = unidecode(line)
        line = line.lower()
        nline = line.rstrip('\n').split('\t')
        print nline
        ## check if col6 is a stop word
        if nline[6] not in stop:
            num_tup+=1
            noStop.write(line)
        else:
            ## col6 is a stopword
            isStop_tup+=1
            isStop.write(line)

    noStop.close()
    isStop.close()
    distance4.close()
    print "good tuple number:%d ;eliminated stopwords tuple number:%d" % (num_tup,isStop_tup)


def test():
    # noStop = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/testdataclean_col4True_col7singleBiaW_col9NotEmp_biasWordNotinTit_col7col8NotdifHyperL_col8within5_col7col8editDisGreat4_noStopWord_Oct28.txt','r')
    noStop = open('/Volumes/Seagate Backup Plus Drive/npov_paper_data/npovTrail2/dataclean_col4True_col7singleBiaW_col9NotEmp_biasWordNotinTit_col7col8NotdifHyperL_col8within5_col7col8editDisGreat4_noStopWord_Oct28.txt','r')


    for line in noStop:
        line = line.decode('utf8')
        line = unidecode(line)
        line = line.lower()
        nline = line.rstrip('\n').split('\t')
        print nline[6] + ' ---> ' + nline[7]



    noStop.close()
test()
# dataclean_2508()