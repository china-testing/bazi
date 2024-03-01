#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 钉钉或微信pythontesting 钉钉群21734177
# CreateDate: 2019-2-21

import argparse
import collections
import pprint
import datetime

from bidict import bidict

from datas import *
from ganzhi import *
from sizi import summarys

def check_gan(gan, gans):
    result = ''
    if ten_deities[gan]['合'] in gans:
        result += "合" + ten_deities[gan]['合']
    if ten_deities[gan]['冲'] in gans:
        result += "冲" + ten_deities[gan]['冲']
    return result

def yinyang(item):
    if item in Gan:
        return '＋' if Gan.index(item)%2 == 0 else '－'
    else:
        return '＋' if Zhi.index(item)%2 == 0 else '－'
    
def yinyangs(zhis):
    result = []
    for item in zhis:
        result.append(yinyang(item))
    if set(result) == set('＋'):
        print("四柱全阳")
    if set(result) == set('－'):
        print("四柱全阴")
    
    
    
    
def get_empty(zhu, zhi):
    empty = empties[zhu]
    if zhi in empty:
        return "空"
    return ""

def get_zhi_detail(zhi, me, multi=1):
    out = ''
    for gan in zhi5[zhi]:
        out = out + "{}{}{}{} ".format(gan, gan5[gan], zhi5[zhi][gan]*multi,  
                                       ten_deities[me][gan])
    return out

def check_gong(zhis, n1, n2, me, hes, desc='三合拱'):
    result = ''
    if zhis[n1] + zhis[n2] in hes:
        gong = hes[zhis[n1] + zhis[n2]] 
        if gong not in zhis:
            result += "\t{}：{}{}-{}[{}]".format(
                desc, zhis[n1], zhis[n2], gong, get_zhi_detail(gong, me))
    return result