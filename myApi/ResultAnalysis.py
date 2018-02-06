#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-
from collections import Counter


#结果分析：
def resultType(result):

    count = 0
    indexNum = list()
    for kk in range(len(result)):
        if(result[count][result[count].argmax()]>=0.5):
            index = result[count].argmax()+1     #判断最大值是否大于0.5,大于则统计，不大于则舍弃
            indexNum.append(index)
        count += 1
    #统计分析最大值的出现次数与最大值下标,如果次数大于总结过次数的一半再减一，则返回下标，否则返回0；
    index=Counter(indexNum)
    if(index.__len__()!=0):
        maxIndex,maxValue=index.most_common(1).pop()
        if (maxValue >= len(result) / 2 - 1):
            return maxIndex
        else:
            return 0
    else:
        return 0
