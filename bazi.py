#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 钉钉、抖音或微信pythontesting 钉钉群21734177
# CreateDate: 2019-2-21

import sxtwl
import argparse
import collections
import pprint
import datetime

from bidict import bidict

from datas import *
from sizi import summarys
from common import *

def gan_zhi_he(zhu):
    gan, zhi = zhu
    if ten_deities[gan]['合'] in zhi5[zhi]:
        return "|"
    return ""

def get_gong_kus(zhis):
    result = []
    for i in range(3):
        zhi1 = zhis[i]
        zhi2 = zhis[i+1]
        if abs(Zhi.index(zhi1) - Zhi.index(zhi2)) == 2:
            value = Zhi[(Zhi.index(zhi1) + Zhi.index(zhi2))//2]
            if value in ("丑", "辰", "未", "戌"):
                result.append(value)
    return result


def get_shens(gans, zhis, gan_, zhi_):
    
    all_shens = []
    for item in year_shens:
        if zhi_ in year_shens[item][zhis.year]:    
            all_shens.append(item)
                
    for item in month_shens:
        if gan_ in month_shens[item][zhis.month] or zhi_ in month_shens[item][zhis.month]:     
            all_shens.append(item)
                
    for item in day_shens:
        if zhi_ in day_shens[item][zhis.day]:     
            all_shens.append(item)
                
    for item in g_shens:
        if zhi_ in g_shens[item][me]:    
            all_shens.append(item) 
    if all_shens:  
        return "  神:" + ' '.join(all_shens)
    else:
        return ""
                
                

description = '''

'''

parser = argparse.ArgumentParser(description=description,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('year', action="store", help=u'year')
parser.add_argument('month', action="store", help=u'month')
parser.add_argument('day', action="store", help=u'day')
parser.add_argument('time', action="store",help=u'time')    
parser.add_argument("--start", help="start year", type=int, default=1850)
parser.add_argument("--end", help="end year", default='2030')
parser.add_argument('-b', action="store_true", default=False, help=u'直接输入八字')
parser.add_argument('-g', action="store_true", default=False, help=u'是否采用公历')
parser.add_argument('-r', action="store_true", default=False, help=u'是否为闰月，仅仅使用于农历')
parser.add_argument('-n', action="store_true", default=False, help=u'是否为女，默认为男')
parser.add_argument('--version', action='version',
                    version='%(prog)s 1.0 Rongzhong xu 2022 06 15')
options = parser.parse_args()

Gans = collections.namedtuple("Gans", "year month day time")
Zhis = collections.namedtuple("Zhis", "year month day time")

if options.b:
    gans = Gans(year=options.year[0], month=options.month[0], 
                day=options.day[0],  time=options.time[0])
    zhis = Gans(year=options.year[1], month=options.month[1], 
                day=options.day[1],  time=options.time[1])
    jds = sxtwl.siZhu2Year(getGZ(options.year), getGZ(options.month), getGZ(options.day), getGZ(options.time), options.start, int(options.end));
    for jd in jds:
        t = sxtwl.JD2DD(jd )
        print("可能出生时间: python bazi.py -g %d %d %d %d :%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))    
    
else:

    if options.g:
        day = sxtwl.fromSolar(
            int(options.year), int(options.month), int(options.day))
    else:
        day = sxtwl.fromLunar(
            int(options.year), int(options.month), int(options.day), options.r)

    gz = day.getHourGZ(int(options.time))
    yTG = day.getYearGZ()
    mTG = day.getMonthGZ()
    dTG  = day.getDayGZ()

    #　计算甲干相合    
    gans = Gans(year=Gan[yTG.tg], month=Gan[mTG.tg], 
                day=Gan[dTG.tg], time=Gan[gz.tg])
    zhis = Zhis(year=Zhi[yTG.dz], month=Zhi[mTG.dz], 
                day=Zhi[dTG.dz], time=Zhi[gz.dz])


me = gans.day
month = zhis.month
alls = list(gans) + list(zhis)
zhus = [item for item in zip(gans, zhis)]

gan_shens = []
for seq, item in enumerate(gans):    
    if seq == 2:
        gan_shens.append('--')
    else:
        gan_shens.append(ten_deities[me][item])
#print(gan_shens)

zhi_shens = [] # 地支的主气神
for item in zhis:
    d = zhi5[item]
    zhi_shens.append(ten_deities[me][max(d, key=d.get)])
#print(zhi_shens)
shens = gan_shens + zhi_shens

zhi_shens2 = [] # 地支的所有神，包含余气和尾气
zhi_shen3 = []
for item in zhis:
    d = zhi5[item]
    tmp = ''
    for item2 in d:
        zhi_shens2.append(ten_deities[me][item2])
        tmp += ten_deities[me][item2]
    zhi_shen3.append(tmp)
shens2 = gan_shens + zhi_shens2
    


# 计算五行分数 http://www.131.com.tw/word/b3_2_14.htm

scores = {"金":0, "木":0, "水":0, "火":0, "土":0}
gan_scores = {"甲":0, "乙":0, "丙":0, "丁":0, "戊":0, "己":0, "庚":0, "辛":0,
              "壬":0, "癸":0}   

for item in gans:  
    scores[gan5[item]] += 5
    gan_scores[item] += 5


for item in list(zhis) + [zhis.month]:  
    for gan in zhi5[item]:
        scores[gan5[gan]] += zhi5[item][gan]
        gan_scores[gan] += zhi5[item][gan]


# 计算八字强弱
# 子平真诠的计算
weak = True
me_status = []
for item in zhis:
    me_status.append(ten_deities[me][item])
    if ten_deities[me][item] in ('长', '帝', '建'):
        weak = False
        

if weak:
    if shens.count('比') + me_status.count('库') >2:
        weak = False

# 计算大运
seq = Gan.index(gans.year)
if options.n:
    if seq % 2 == 0:
        direction = -1
    else:
        direction = 1
else:
    if seq % 2 == 0:
        direction = 1
    else:
        direction = -1

dayuns = []
gan_seq = Gan.index(gans.month)
zhi_seq = Zhi.index(zhis.month)
for i in range(12):
    gan_seq += direction
    zhi_seq += direction
    dayuns.append(Gan[gan_seq%10] + Zhi[zhi_seq%12])

# 网上的计算
me_attrs_ = ten_deities[me].inverse
strong = gan_scores[me_attrs_['比']] + gan_scores[me_attrs_['劫']] \
    + gan_scores[me_attrs_['枭']] + gan_scores[me_attrs_['印']]

if not options.b:
    #print("direction",direction)
    sex = '女' if options.n else '男'
    print("\n{}命".format(sex))
    print("======================================")  
    print("公历:", end='')
    print("\t{}年{}月{}日".format(day.getSolarYear(), day.getSolarMonth(), day.getSolarDay()))

    Lleap = "闰" if day.isLunarLeap() else ""
    print("农历:", end='')
    print("\t{}年{}{}月{}日 穿=害".format(day.getLunarYear(), Lleap, day.getLunarMonth(), day.getLunarDay()))
print("-"*120)
print("墓库：", str(kus).replace("'",""), "解读:钉ding或v信pythontesting", end=' ')
for item in zhus:
    print(''.join(item), end=' ')
print()
print("甲己-中正土  乙庚-仁义金  丙辛-威制水  丁壬-淫慝木  戊癸-无情火", "  三会:", str(zhi_huis).replace("'",""))
print("="*120)    

#print(zhi_3hes, "生：寅申巳亥 败：子午卯酉　库：辰戌丑未")
#print("地支六合:", zhi_6hes)
out = ''
for item in zhi_3hes:
    out = out + "{}:{}  ".format(item, zhi_3hes[item])
print('\033[1;36;40m' + ' '.join(list(gans)), ' '*5, ' '.join(list(gan_shens)) + '\033[0m',' '*5, out,)
out = ''
for item in zhi_6hes:
    out = out + "{}{} ".format(item, zhi_6hes[item])
print('\033[1;36;40m' + ' '.join(list(zhis)), ' '*5, ' '.join(list(zhi_shens)) + '\033[0m', ' '*5,  "生：寅申巳亥 败：子午卯酉　库：辰戌丑未", ' '*2,  out)
print("-"*120)
print("{1:{0}^15s}{2:{0}^15s}{3:{0}^15s}{4:{0}^15s}".format(chr(12288), '【年】{}:{}{}{}'.format(temps[gans.year],temps[zhis.year],ten_deities[gans.year].inverse['建'], gan_zhi_he(zhus[0])), 
    '【月】{}:{}{}{}'.format(temps[gans.month],temps[zhis.month], ten_deities[gans.month].inverse['建'], gan_zhi_he(zhus[1])),
    '【日】{}:{}{}'.format(temps[me], temps[zhis.day], gan_zhi_he(zhus[2])), 
    '【时】{}:{}{}{}'.format(temps[gans.time], temps[zhis.time], ten_deities[gans.time].inverse['建'], gan_zhi_he(zhus[3]))))
print("-"*120)


print("\033[1;36;40m{1:{0}<15s}{2:{0}<15s}{3:{0}<15s}{4:{0}<15s}\033[0m".format(
    chr(12288),
    '{}{}{}【{}】{}'.format(
        gans.year, yinyang(gans.year), gan5[gans.year], ten_deities[me][gans.year], check_gan(gans.year, gans)),
    '{}{}{}【{}】{}'.format(
        gans.month, yinyang(gans.month), gan5[gans.month], ten_deities[me][gans.month], check_gan(gans.month, gans)),
    '{}{}{}{}'.format(me, yinyang(me),gan5[me], check_gan(me, gans)),
    '{}{}{}【{}】{}'.format(gans.time, yinyang(gans.time), gan5[gans.time], ten_deities[me][gans.time], check_gan(gans.time, gans)),
))

print("\033[1;36;40m{1:{0}<15s}{2:{0}<15s}{3:{0}<15s}{4:{0}<15s}\033[0m".format(
    chr(12288),
    "{}{}{}【{}】{}".format(
        zhis.year, yinyang(zhis.year), ten_deities[me][zhis.year],
        ten_deities[gans.year][zhis.year], get_empty(zhus[2],zhis.year)),
    "{}{}{}【{}】{}".format(
        zhis.month, yinyang(zhis.month), ten_deities[me][zhis.month],
        ten_deities[gans.month][zhis.month], get_empty(zhus[2],zhis.month)),
    "{}{}{}".format(zhis.day, yinyang(zhis.day), ten_deities[me][zhis.day]),   
    "{}{}{}【{}】{}".format(
        zhis.time, yinyang(zhis.time), ten_deities[me][zhis.time], 
        ten_deities[gans.time][zhis.time], get_empty(zhus[2],zhis.time)),
))

statuses = [ten_deities[me][item] for item in zhis]


for seq, item in enumerate(zhis):
    out = ''
    multi = 2 if item == zhis.month and seq == 1 else 1

    for gan in zhi5[item]:
        out = out + "{}{}{}　".format(gan, gan5[gan], ten_deities[me][gan])
    print("\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), out.rstrip('　')), end='')

print()
# 输出地支关系
for seq, item in enumerate(zhis):

    output = ''
    others = zhis[:seq] + zhis[seq+1:] 
    for type_ in zhi_atts[item]:
        flag = False
        if type_ in ('害',"破","会",'刑'):
            continue
        for zhi in zhi_atts[item][type_]:
            if zhi in others:
                if not flag:
                    output = output + "　" + type_ + "：" if type_ not in ('冲','暗') else output + "　" + type_
                    flag = True
                if type_ not in ('冲','暗'):
                    output += zhi
        output = output.lstrip('　')
    print("\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), output), end='')

print()

# 输出地支minor关系
for seq, item in enumerate(zhis):

    output = ''
    others = zhis[:seq] + zhis[seq+1:] 
    for type_ in zhi_atts[item]:
        flag = False
        if type_ not in ('害',"会"):
            continue
        for zhi in zhi_atts[item][type_]:
            if zhi in others:
                if not flag:
                    output = output + "　" + type_ + "："
                    flag = True
                output += zhi
    output = output.lstrip('　')
    print("\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), output), end='')

print()
for seq, item in enumerate(zhus):

    # 检查空亡 
    result = "{}－{}".format(nayins[item], '亡') if zhis[seq] == wangs[zhis[0]] else nayins[item]
    
    # 天干与地支关系
    result = relations[(gan5[gans[seq]], zhi_wuhangs[zhis[seq]])] + result
        
    # 检查劫杀 
    result = "{}－{}".format(result, '劫杀') if zhis[seq] == jieshas[zhis[0]] else result
    # 检查元辰
    result = "{}－{}".format(result, '元辰') if zhis[seq] == Zhi[(Zhi.index(zhis[0]) + direction*-1*5)%12] else result    
    print("{1:{0}<15s} ".format(chr(12288), result), end='')

print()

    

strs = ['','','','',]


all_shens = set()

for item in year_shens:
    for i in (1,2,3):
        if zhis[i] in year_shens[item][zhis.year]:    
            strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
            all_shens.add(item)
            
for item in month_shens:
    for i in range(4):
        if gans[i] in month_shens[item][zhis.month] or zhis[i] in month_shens[item][zhis.month]:     
            strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
            if i == 2 and gans[i] in month_shens[item][zhis.month]:
                strs[i] = strs[i] + "●"
            all_shens.add(item)
            
for item in day_shens:
    for i in (0,1,3):
        if zhis[i] in day_shens[item][zhis.day]:     
            strs[i] = item if not strs[i] else strs[i] + chr(12288) + item    
            all_shens.add(item)
            
for item in g_shens:
    for i in range(4):
        if zhis[i] in g_shens[item][me]:    
            strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
            all_shens.add(item)
#print(strs)           
for seq in range(2):
    print("{1:{0}<15s} ".format(chr(12288), strs[seq]), end='')
for seq in range(2,4):
    print("{1:{0}<14s} ".format(chr(12288), strs[seq]), end='')
    


       
print()
print("-"*120)
print("调候：", tiaohous['{}{}'.format(me, zhis[1])], "\t##金不换大运：", jinbuhuan['{}{}'.format(me, zhis[1])])
print("金不换大运：说明：", jins['{}'.format(me)])

for item in all_shens:
    print(item, ":",  shens_infos[item])

print("-"*120)


children = ['食','伤'] if options.n else ['官','杀']

liuqins = bidict({'才': '婆婆' if options.n else '父亲',"财":'父亲' if options.n else '妻子', "印": '女婿'if options.n else '母亲', "枭": '母亲'if options.n else '祖父',
                  "官":'丈夫' if options.n else '女儿', "杀":'情夫' if options.n else '儿子', "劫":'兄弟' if options.n else '姐妹', "比":'姐妹' if options.n else '兄弟', 
                  "食":'女儿' if options.n else '下属', "伤":'儿子' if options.n else '孙女'})

# 六亲分析
for item in Gan:
    print("{}:{} {}-{} {} {} {}".format(item, ten_deities[me][item], liuqins[ten_deities[me][item]],  ten_deities[item][zhis[0]] ,ten_deities[item][zhis[1]], ten_deities[item][zhis[2]], ten_deities[item][zhis[3]]), end='  ')
    if Gan.index(item) == 4:
        print()
    
print()
print()

# 计算上运时间，有年份时才适用

temps_scores = temps[gans.year] + temps[gans.month] + temps[me] + temps[gans.time] + temps[zhis.year] + temps[zhis.month]*2 + temps[zhis.day] + temps[zhis.time]
print("\033[1;36;40m五行分数", scores, '  八字强弱：', strong, "通常>29为强，需要参考月份、坐支等", "weak:", weak)


print("湿度分数", temps_scores,"正为暖燥，负为寒湿，正常区间[-6,6] 拱库气：",  get_gong_kus(zhis), "\033[0m")
for item in gan_scores:  
    print("{}[{}]-{} ".format(
        item, ten_deities[me][item], gan_scores[item]),  end='  ')    
print()
print("-"*120)
yinyangs(zhis)
shen_zhus = list(zip(gan_shens, zhi_shens))

# 地网
if '辰' in zhis and '巳' in zhis:
    print("地网：地支辰巳。天罗：戌亥。天罗地网全凶。")
    
# 天罗
if '戌' in zhis and '亥' in zhis:
    print("天罗：戌亥。地网：地支辰巳。天罗地网全凶。")

# 魁罡格
if zhus[2] in (('庚','辰'), ('庚','戌'),('壬','辰'), ('戊','戌'),):
    print("魁罡格：基础96，日主庚辰,庚戌,壬辰, 戊戌，重叠方有力。日主强，无刑冲佳。")
    print("魁罡四柱曰多同，贵气朝来在此中，日主独逢冲克重，财官显露祸无穷。魁罡重叠是贵人，天元健旺喜临身，财官一见生灾祸，刑煞俱全定苦辛。")

# 金神格
if zhus[3] in (('乙','丑'), ('乙','巳'),('癸','酉')):
    print("金神格：基础97，时柱己丑、乙巳、癸酉。只有甲和己日，甲日为主，甲子、甲辰最突出。月支通金火2局为佳命。不通可以选其他格")
    
# 六阴朝阳
if me == '辛' and zhis.time == '子':
    print("六阴朝阳格：基础98，辛日时辰为子。")
    
# 六乙鼠贵
if me == '乙' and zhis.time == '子':
    print("六阴朝阳格：基础99，乙日时辰为子。忌讳午冲，丑合。月支最好通木局，水也可以，不适合金火。申酉大运有凶，午也不行。夏季为伤官。入其他格以格局论。")

# 从格
if max(scores.values()) > 25:
    print("有五行大于25分，需要考虑专格或者从格。")
    print("从旺格：安居远害、退身避位、淡泊名利,基础94;从势格：日主无根。")
    
# 建禄格
if zhi_shens[1] == '比':
    print("建禄格：最好天干有财官。如果官杀不成格，有兄弟，且任性。有争财和理财的双重性格。如果创业独自搞比较好，如果合伙有完善的财务制度也可以。")
    if gan_shens[0] in '比劫':
        print("\t建禄年透比劫凶")
    elif '财' in gan_shens and '官' in gan_shens:
        print("\t建禄财官双透，吉")
    if me in ('甲','乙'):
        print("\t甲乙建禄四柱劫财多，无祖财，克妻，一生不聚财，做事虚诈，为人大模大样，不踏实。乙财官多可为吉。甲壬申时佳；乙辛巳时佳；")

    if me in ('丙'):
        print("\t丙：己亥时辰佳；")        
    if me in ('丁'):
        print("\t丁：阴男克1妻，阳男克3妻。财官多可为吉。庚子时辰佳；")
    if me in ('戊'):
        print("\t戊：四柱无财克妻，无祖业，后代多事端。如合申子辰，子息晚，有2子。甲寅时辰佳；")       
    if me in ('己'):
        print("\t己：即使官财出干成格，妻也晚。偏财、杀印成格为佳。乙丑时辰佳；")    
    if me in ('庚'):
        print("\t庚：上半月生难有祖财，下半月较好，财格比官杀要好。丙戌时辰佳；")   
    if me in ('辛'):
        print("\t辛：干透劫财，妻迟财少；丁酉时辰佳；")      
    if me in ('壬'):
        print("\t 壬：戊申时辰佳；")  
    if me in ('癸'):
        print("\t 癸：己亥时辰佳")      
        
        
# 甲分析 

if me == '甲':
    if zhis.count('辰') > 1 or zhis.count('戌') > 1:
        print("甲日：辰或戌多、性能急躁不能忍。")
    if zhis[2] == '子':
        print("甲子：调候要火。")
    if zhis[2] == '寅':
        print("甲寅：有主见之人，需要财官旺支。")        
    if zhis[2] == '辰':
        print("甲辰：印库、性柔和而有实权。")   
    if zhis[2] == '午':
        print("甲午：一生有财、调候要水。")        
    if zhis[2] == '戌':
        print("甲戌：自坐伤官，不易生财，为人仁善。")       

# 比肩分析
if '比' in gan_shens:
    print("比：同性相斥。讨厌自己。老是想之前有没有搞错。没有持久性，最多跟你三五年。 散财，月上比肩，做事没有定性，不看重钱，感情不持久。不怀疑人家，人心很好。善意好心惹麻烦。年上问题不大。")
    print("比如果地支刑，幼年艰苦，白手自立长、兄弟不合、也可能与妻子分居。地支冲：手足不和。女命忌讳比劫和合官杀，多为任性引发困难之事。")
       
    if gan_shens[0] == '比':
        print("上面有哥或姐，出身一般。")
                
    # 比肩过多
    if shens2.count('比') > 2 and '比' in zhi_shens:
        #print(shens2, zhi_shens2)
        print('----比肩过多：女的爱子女超过丈夫；轻易否定丈夫。 换一种说法：有理想、自信、贪财、不惧内。男的双妻。')
        print('女的：你有帮夫运，多协助他的事业，多提意见，偶尔有争执，问题也不大。')
        print('善意多言，引无畏之争；难以保守秘密，不适合多言；易犯无事忙的自我表现；不好意思拒绝他人;累积情绪而突然放弃。')
        print("兄弟之间缺乏帮助。夫妻有时不太和谐。好友知交相处不会很久。女：感情啰嗦\n对人警惕性低，乐天知命;")
        print("\t天干有比，劳累命：事必躬亲。情感过程多有波折。除非有官杀制服。")
        
        if (not '官' in shens) and  (not '杀' in shens):
            print("比肩多，四柱无正官七杀，性情急躁。")            
        if gan_shens.count('比') > 1:
            print("天干2比肩：难以保守秘密,容易有言辞是非。")  
            
        if zhi_shens[2] == '比':
            print("女坐比:夫妻互恨。")  
            
        if '劫' in gan_shens:
            print("天干比劫并立，女命感情丰富，多遇争夫。")    
            
        if gan_shens[0] == '比':
            print("年干为比，不是长子，父母缘较薄，晚婚。")  
            
        if gan_shens[1] == '比':
            if zhi_shens[1] == '食':
                print("月柱比坐食，易得贵人相助。")
            if zhi_shens[1] == '伤':
                print("月柱比坐伤，一生只有小财气，难富贵。")    
            if zhi_shen[1] == '比':
                print("月柱比坐比，单亲家庭，一婚不能到头。地支三合或三会比，天干2比也如此。")
            if zhi_shen[1] == '财':
                print("月柱比坐财，不利妻，也主父母身体不佳。因亲友、人情等招财物的无谓损失。")      
            if zhi_shen[1] == '杀':
                print("月柱比坐杀，稳重。")                   
        
        
        for seq, gan_ in enumerate(gan_shens):
            if gan_ != '比':
                continue
            if zhis[seq] in  empties[zhus[2]]:
                print("比肩坐空亡，不利父亲与妻。年不利父，月不利父和妻，在时则没有关系。女：月柱30岁前结婚夫妻缘分偏薄。")
            if zhi_shens[seq] == '比':
                print("比坐比-平吉：与官杀对立，无主权。养子：克偏财，泄正印。吉：为朋友尽力；凶：受兄弟朋友拖累。父缘分薄，自我孤僻，男多迟婚")   
            if zhi_shens[seq] == '劫':
                print("父亲先亡。女比肩坐劫:夫妻互恨。还有刑冲，女恐有不测之灾：比如车祸、开刀和意外等。")     
                print("比坐劫-大凶：为忌亲友受损，合作事业中途解散，与妻子不合。如年月3见比，父缘薄或已死别。")   
                if ten_deities[gans[seq]][zhis[seq]] == '绝' and seq < 2:
                    print("比肩坐绝，兄弟不多，或者很难谋面。戊和壬的准确率偏低些。")   
            if zhi_shens[seq] == '财':
                print("比肩坐财：因亲人、人情等原因引起无谓损失。")  
            if zhi_shens[seq] == '杀':
                print("比肩坐财:稳重。")    
            if zhi_shens[seq] == '枭':
                print("比肩坐偏印：三五年发达，后面守成。")    
            if zhi_shens[seq] == '劫' and Gan.index(me) % 2 == 0:
                print("比肩坐阳刃：在年不利父，在其他有刀伤、车祸、意外灾害。")               
                        
if zhi_shens[2] == '比':
    print("日支比：男的克妻?对家务事有家长式领导；钱来得不容易且有时有小损财。自我，如有刑冲，不喜归家！")
if zhi_shens[3] == '比':
    print("时支比：子女为人公正倔强、行动力强，能得资产。")    
if '比' in (gan_shens[1],zhi_shens[1]):
    print("月柱比：三十岁以前难有成就。冒进、不稳定。女友不持久、大男子主义。")
if '比' in (gan_shens[3],zhi_shens[3]):
    print("时柱比：与亲人意见不合。")

if shens.count('比') + shens.count('劫') > 1:
    print("比劫大于2，男：感情阻碍、事业起伏不定。")
    


# 劫财分析
if '劫' in gan_shens:
    print("劫财扶助，无微不至。劫财多者谦虚之中带有傲气。凡事先理情，而后情理。先细节后全局。性刚强、精明干练、女命不适合干透支藏。")
    print("务实，不喜欢抽象性的空谈。不容易认错，比较倔。有理想，但是不够灵活。不怕闲言闲语干扰。不顾及别人面子。")
    print("合作事业有始无终。太重细节。做小领导还是可以的。有志向，自信。杀或食透干可解所有负面。女命忌讳比劫和合官杀，多为任性引发困难之事。")
    if shens2.count('劫') > 2:
        print('----劫财过多, 婚姻不好')
        if (not '官' in shens) and  (not '杀' in shens):
            print("比肩多，四柱无正官七杀，性情急躁。")   
    if zhis[2] == '劫':
        print("日坐劫财，透天干。在年父早亡，在月夫妻关系不好。比如财产互相防范；鄙视对方；自己决定，哪怕对方不同意；老夫少妻；身世有差距；斤斤计较；敢爱敢恨的后遗症，以上多针对女。\n男的一般有双妻。天干有杀或食可解。") 
            
if zhus[2] in (('壬','子'),('丙','午'), ('戊','午')):
    print("日主专位劫财，壬子和丙午，晚婚。不透天干，一般是眼光高、独立性强。对配偶不利，互相轻视；若刑冲，做事立场不明遭嫉妒，但不会有大灾。女性婚后通常还有自己的事业,能办事。") 
if ('劫','伤') in shen_zhus or ('伤','劫',) in shen_zhus:
    print("同一柱中，劫财、阳刃伤官都有，外表华美，富屋穷人，婚姻不稳定，富而不久；年柱不利家长，月柱不利婚姻，时柱不利子女。伤官的狂妄。")      

if gan_shens[0] == '劫':
    print("年干劫财：家运不济。克父，如果坐劫财，通常少年失父；反之要看地支劫财根在哪一柱子。")
        
if '劫' in (gan_shens[1],zhi_shens[1]):
    print("月柱劫：容易孤注一掷，30岁以前难稳定。男早婚不利。")
if '劫' in (gan_shens[3],zhi_shens[3]):
    print("时柱劫：只要不是去经济大权还好。")   
if zhi_shens[2] == '劫':
    print("日支劫：男的克妻，一说是家庭有纠纷，对外尚无重大损失。如再透月或时天干，有严重内忧外患。")
    
if '劫' in shens2 and  '比' in zhi_shens and '印' in shens2 and Gan.index(me) % 2 == 1:
    print("阴干比劫印齐全，单身，可入道！")
    
if zhi_shens[0] == '劫' and Gan.index(me) % 2 == 0: 
    print("年阳刃：得不到长辈福；不知足、施恩反怨。")
if zhi_shens[3] == '劫' and Gan.index(me) % 2 == 0: 
    print("时阳刃：与妻子不和，晚无结果，四柱再有比刃，有疾病与外灾。")
if zhi_shens[1] == '劫' and Gan.index(me) % 2 == 0:
    print("阳刃格：喜七杀或三四个官。基础90")  
    if me in ('庚', '壬','戊'):
        print("阳刃'庚', '壬','午'忌讳财运，逢冲多祸。庚逢辛酉凶，丁酉吉，庚辰和丁酉六合不凶。壬逢壬子凶，戊子吉；壬午和戊子换禄不凶。")
    else:
        print("阳刃'甲', '丙',忌讳杀运，逢冲多还好。甲：乙卯凶，辛卯吉；甲申与丁卯暗合吉。丙：丙午凶，壬午吉。丙子和壬午换禄不凶。")
    
 
# 偏印分析    
if '枭' in gan_shens:
    print("----偏印在天干如成格：偏印在前，偏财(财次之)在后，有天月德就是佳命(偏印格在日时，不在月透天干也麻烦)。忌讳倒食，但是坐绝没有这能力。")
    print("经典认为：偏印不能扶身，要身旺；偏印见官杀未必是福；喜伤官，喜财；忌日主无根；   女顾兄弟姐妹；男六亲似冰")
    print("偏印格干支有冲、合、刑，地支是偏印的绝位也不佳。")
    if '枭' in zhi_shens:
        print("成格基础89生财、配印；最喜偏财同时成格，偏印在前，偏财在后。最忌讳日时坐实比劫刃。")
    if shens2.count('枭') > 2:
        print("偏印过多，性格孤僻，表达太含蓄，要别人猜，说话有时带刺。偏悲观。有偏财和天月德贵人可以改善。有艺术天赋。做事大多有始无终。如四柱全阴，女性声誉不佳。")
        print("对兄弟姐妹不错。男的因才干受子女尊敬。女的偏印多，子女不多。第1克伤食，第2艺术性。")
        if '伤' in gan_shens: 
            print("女命偏印多，又与伤官同透，夫离子散。有偏财和天月德贵人可以改善。")
        
    if gan_shens.count('枭') > 1:
        print("天干两个偏印：迟婚，独身等，婚姻不好。三偏印，家族人口少，亲属不多。")
    if shen_zhus[0] == ('枭', '枭'):
        print("偏印在年，干支俱透，不利于长辈。偏母当令，正母无权，可能是领养，庶出、同父异母等。")
        
    
for seq, zhi_ in enumerate(zhi_shens):
    if zhi_ != '枭' and gan_shens[seq] != '枭':
        continue   
    if ten_deities[gans[seq]][zhis[seq]] == '绝':
        print("偏印坐绝，或者天干坐偏印为绝，难以得志。费力不讨好。")       

    
if zhi_shens[3]  == '枭' and gan_shens[0]  == '枭':
    print("偏印透年干-时支，一直受家里影响。")
    
if '枭' in (gan_shens[0],zhi_shens[0]):
    print("偏印在年：少有富贵家庭；有宗教素养，不喜享乐，第六感强。")
if '枭' in (gan_shens[1],zhi_shens[1]):
    print("偏印在月：有慧少福，能舍己为人。")
    if zhi_shens[1]  == '枭' and len(zhi5[zhis[1]]) == 1:
        print("偏印专位在月支：比较适合音乐，艺术，宗教等。")
        if gan_shens[1] == '枭':
            print("干支偏印月柱，专位入格，有慧福浅。")    
if '枭' in (gan_shens[3],zhi_shens[3]):
    print("偏印在时：女与后代分居；男50以前奠定基础，晚年享清福。")     
if zhi_shens[2] == '枭':
    print("偏印在日支：家庭生活沉闷")
    if zhus[2] in (('丁','卯'),('癸','酉')):
        print("日专坐偏印：丁卯和癸酉。婚姻不顺。又刑冲，因性格而起争端。")    
    
# 印分析    
if '印' in gan_shens:
    if '印' in zhi_shens:
        print("基础82，成格喜官杀、身弱、忌财克印。合印留财，见利忘义.透财官杀通关或印生比劫；合冲印若无他格或调候破格。日主强凶，禄刃一支可以食伤泄。")
    if shens2.count('印') > 2:
        print("正印多的：聪明有谋略，比较含蓄，不害人，识时务。正印不怕日主死绝，反而怕太强。日主强，正印多，孤寂，不善理财。")
    for seq, gan_ in enumerate(gan_shens):
        if gan_ != '印':
            continue   
        if ten_deities[gans[seq]][zhis[seq]] in ('绝', '死'):
            if seq <3:
                print("正印坐死绝，或天干正印地支有冲刑，不利母亲。时柱不算。")   
        if zhi_shens[seq] == '财':
            print("男正印坐正财，夫妻不好。月柱正印坐正财专位，必离婚。在时柱，50多岁才有正常婚姻。(男)")   
        if zhi_shens[seq] == '印':
            print("正印坐正印，专位，过于自信。务实，拿得起放得下。女的话大多晚婚。母长寿；女子息迟，头胎恐流产。女四柱没有官杀，没有良缘。男的搞艺术比较好，经商则孤僻，不聚财。")          

        if zhi_shens[seq] == '枭' and len(zhi5[zhis[seq]]) == 1:
            print("正印坐偏印专位：有多种职业;家庭不吉：亲人有疾或者特别嗜好。子息迟;财务双关。明一套，暗一套。女的双重性格。")   
            
        if zhi_shens[seq] == '伤':
            print("适合清高的职业。不适合追逐名利，女的婚姻不好。")    
            
        if zhi_shens[seq] == '劫' and me in ('甲','庚','壬'):
            print("正印坐阳刃，身心多伤，心疲力竭，偶有因公殉职。主要指月柱。工作看得比较重要。")    
                        
            
    if '杀' in gan_shens and '劫' in zhi_shens and me in ('甲','庚','壬'):
        print("正印、七杀、阳刃全：女命宗教人，否则独身，清高，身体恐有隐疾，性格狭隘缺耐心。男小疾多，婚姻不佳，恐非婚生子女。")    
            
    if '官' in gan_shens or '杀' in gan_shens: 
        print("身弱官杀和印都透天干，格局佳。")
    else:
        print("单独正印主秀气、艺术、文才。性格保守")  
    if '官' in gan_shens or '杀' in gan_shens or '比' in gan_shens: 
        print("正印多者，有比肩在天干，不怕财。有官杀在天干也不怕。财不强也没关系。")  
    else:
        print("正印怕财。") 
    if '财' in gan_shens:     
        print("印和财都透天干，都有根，最好先财后印，一生吉祥。先印后财，能力不错，但多为他人奔波。(男)") 
        
if zhi_shens[3]  == '印' and len(zhi5[zhis[3]]) == 1:
    print("时支专位正印。男忙碌到老。女的子女各居一方。亲情淡薄。")  
    
if gan_shens[3]  == '印' and '印' in zhi_shen3[3]:
    print("时柱正印格，不论男女，老年辛苦。女的到死都要控制家产。子女无缘。")   

        
# 偏财分析    
if '才' in gan_shens:
    print("偏财明现天干，不论是否有根:财富外人可见;实际财力不及外观一半。没钱别人都不相信;协助他人常超过自己的能力")
    print("偏财出天干，又与天月德贵人同一天干者。在年月有声明远扬的父亲，月时有聪慧的红颜知己。喜奉承。")
    print("偏财透天干，四柱没有刑冲，长寿。女子为孝顺女，主要针对年月。时柱表示中年以后有自己的事业，善于理财。")
    if '才' in zhi_shens:
        print("财格基础80:比劫用食伤通关或官杀制；身弱有比劫仍然用食伤通关。如果时柱坐实比劫，晚年破产。")  
    print("偏财透天干，讲究原则，不拘小节。喜奉承，善于享受。财格基础80")
    
    if '比' in gan_shens or '劫' in gan_shens and gan_shens[3] == '才':
        print("年月比劫，时干透出偏财。祖业凋零，再白手起家。有刑冲为千金散尽还复来")
    if '杀' in gan_shens and '杀' in zhi_shens:
        print("偏财和七杀并位，地支又有根，父子外合心不合。因为偏财生杀攻身。偏财七杀在日时，则为有难伺候的女朋友。")
        
    if zhi_shens[0]  == '才':
        print("偏财根透年柱，家世良好，且能承受祖业。")
        
    for seq, gan_ in enumerate(gan_shens):
        if gan_ != '才':
            pass
        if zhi_shens[seq] == '劫' :
            print("偏财坐阳刃劫财,可做父缘薄，也可幼年家贫。也可以父先亡，要参考第一大运。")   
            if len(zhi5[zhis[seq]]) == 1:
                print("偏财坐专位阳刃劫财,父亲去他乡。")   
        if get_empty(zhus[2],zhis[seq]) == '空':
            print("偏财坐空亡，财官难求。")                    
                
if shens2.count('才') > 2:
    print("偏财多的人慷慨，得失看淡。花钱一般不会后悔。偏乐观，甚至是浮夸。生活习惯颠倒。适应能力强。有团队精神。得女性欢心。小事很少失信。")
    print("乐善好施，有团队精神，女命偏财，听父亲的话。时柱偏财女，善于理财，中年以后有事业。")
if (zhi_shens[2]  == '才' and len(zhi5[zhis[2]]) == 1) or (zhi_shens[3]  == '才' and len(zhi5[zhis[3]]) == 1):
    print("日时地支坐专位偏财。不见刑冲，时干不是比劫，大运也没有比劫刑冲，晚年发达。")
    
    
    
# 财分析    
if '财' in gan_shens:
    print("男日主合财星，夫妻恩爱。如果争合或天干有劫财，双妻。")
    if '财' in zhi_shens:
        print("财格基础80:比劫用食伤通关或官杀制；身弱有比劫仍然用食伤通关。")
        
    if '官' in gan_shens:
        print("正官正财并行透出，(身强)出身书香门第。")
    if '官' in gan_shens or '杀' in gan_shens:
        print("官或杀与财并行透出，女压夫，财生官杀，老公压力大。")
    if gan_shens[0] == '财':
        print("年干正财若为喜，富裕家庭，但不利母亲。")
    if '财' in zhi_shens:
        if '官' in gan_shens or '杀' in gan_shens:
            print("男财旺透官杀，女厌夫。")
    if gan_shens.count('财') > 1:
        print("天干两正财，财源多，大多做好几种生意，好赶潮流，人云亦云。有时会做自己外行的生意。")
        if '财' not in zhi_shens2:
            print("正财多而无根虚而不踏实。重财不富。")
            
for seq, gan_ in enumerate(gan_shens):
    if gan_ != '财' and zhis[seq] != '财':
        continue   
    if zhis[seq] in day_shens['驿马'][zhis.day] and seq != 2:
        print("女柱有财+驿马，动力持家。")
    if zhis[seq] in day_shens['桃花'][zhis.day] and seq != 2:
        print("女柱有财+桃花，不吉利。")        
    if zhis[seq] in empties[zhus[2]]:
        print("财坐空亡，不持久。")    
    if ten_deities[gans[seq]][zhis[seq]] in ('绝', '墓'):
        print("男财坐绝或墓，不利婚姻。")
            
if shens2.count('财') > 2:
    print("正财多者，为人端正，有信用，简朴稳重。")
    if '财' in zhi_shens2 and (me not in zhi_shens2):
        print("正财多而有根，日主不在生旺库，身弱惧内。")   
        
if zhi_shens[1] == '财':
    print("女命月支正财，有务实的婚姻观。")
    
if zhi_shens[1] == '财':
    print("月令正财，无冲刑，有贤内助，但是母亲与妻子不和。生活简朴，多为理财人士。")
if zhi_shens[3] == '财' and len(zhi5[zhis[3]]) == 1:
    print("时支正财，一般两个儿子。")
if zhus[2] in (('戊','子'),) or zhus[3] in (('戊','子'),):
    print("日支专位为正财，得勤俭老婆。即戊子。日时专位支正财，又透正官，中年以后发达，独立富贵。") 
    
if zhus[2] in (('壬','午'),('癸','巳'),):
    print("坐财官印，只要四柱没有刑冲，大吉！") 
    
if zhus[2] in (('甲','戌'),('乙','亥'),):
    print("女('甲','戌'),('乙','亥'） 晚婚 -- 不准！") 
    
if '财' == gan_shens[3] or  '财' == zhi_shens[3]:
    
    print("未必准确：时柱有正财，口快心直，不喜拖泥带水，刑冲则浮躁。阳刃也不佳.反之有美妻佳子") 
if (not '财' in shens2) and (not '才' in shens2):
    print("四柱无财，即便逢财运，也是虚名虚利. 男的晚婚")
    
# 官分析    
if '官' in gan_shens:
    if '官' in zhi_shens:
        print("官若成格：忌伤；忌混杂；基础78。有伤用财通关或印制。混杂用合或者身官两停。日主弱则不可扶。")
    if gan_shens[3] == '官' and len(zhi5[zhis[3]]) == 1:
        print("官专位时坐地支，男有得力子息。")
    if gan_shens[0] == '官' :
        print("年干为官，身强出身书香门第。")
        if gan_shens[3] == '官':
            print("男命年干，时干都为官，对后代和头胎不利。")
    if (not '财' in gan_shens) and (not '印' in gan_shens):
        print("官独透天干成格，四柱无财或印，为老实人。")
    if '伤' in gan_shens:
        print("正官伤官通根透，又无其他格局，失策。尤其是女命，异地分居居多，婚姻不美满。")
    if '杀' in gan_shens:
        print("年月干杀和偏官，30以前婚姻不稳定。月时多为体弱多病。")
        
    if '印' in gan_shens and '印' in zhi_shens2 and '官' in zhi_shens2:
        print("官印同根透，无刑冲合，吉。")
        if '财' in gan_shens and '财' in zhi_shens2:
            print("财官印同根透，无刑冲合，吉。")
        
    if gan_shens[1] == '官' in ten_deities[me][zhis[1]] in ('绝', '墓'):
        print("官在月坐墓绝，不是特殊婚姻就是迟婚。如果与天月德同柱，依然不错。丈夫在库中：1，老夫少妻；2，不为外人所知的亲密感情；3，特殊又合法的婚姻。")
    if zhi_shens[1] == '官' and gan_shens[1] == '官':
        print("月柱正官坐正官，婚变。月柱不宜通。坐禄的。")  
    if zhi_shens[1] == '官' and '伤' in shens:
        print("月支正官，又成伤官格，难做真正夫妻。有实，无名。")
    
    for seq, gan_ in enumerate(gan_shens):
        if gan_ != '官':
            continue   
        if zhi_shens[seq] in ('劫','比') :
            print("天干正官，地支比肩或劫财，亲友之间不适合合作，但是他适合经营烂摊子。")
        if zhi_shens[seq] == '杀' :
            print("正官坐七杀，男命恐有诉讼之灾。女命婚姻不佳。月柱尤其麻烦，二度有感情纠纷。年不算，时从轻。")
        if zhi_shens[seq] == '劫' and Gan.index(me) % 2 == 0:
            print("要杀才能制服阳刃，有力不从心之事情。")   
        if zhi_shens[seq] == '印':
            print("官坐印，无刑冲合，吉")   
        
            
if shens2.count('官') > 2 and '官' in gan_shens and '官' in zhi_shens2:
    print("正官多者，虚名。为人性格温和，比较实在。做七杀看")
if zhi_shens[2]  == '官' and len(zhi5[zhis[2]]) == 1:
    print("日坐正官，淑女。")
    
    
    
# 杀分析    
if '杀' in gan_shens:
    print("七杀是非多。但是对男人有时是贵格。比如毛主席等。七杀坐刑或冲，夫妻不和。成格基础85可杀生印或食制印、身杀两停、阳刃驾杀。")
    if '杀' in zhi_shens:
        print("杀格：喜食神制，要食在前，杀在后。阳刃驾杀：杀在前，刃在后。身杀两停：比如甲寅日庚申月。杀印相生，忌食同成格。")
    if gan_shens[0] == '杀':
        print("年干七杀，早年不好。或家里穷或身体不好。")
        if gan_shens[1] == '杀':
            print("年月天干七杀，家庭复杂。")
    if '官' in gan_shens:
        print("官和杀同见天干不佳。")
    if gan_shens[1] == '杀' and zhi_shens[1] == '杀':
        print("月柱都是七杀，克得太过。有福不会享。六亲福薄。时柱没关系。")
        if '杀' not in zhi_shens2 :
            print("七杀年月浮现天干，性格好变，不容易定下来。30岁以前不行。")        
    if '杀' in zhi_shens and '劫' in zhi_shens:
        print("七杀地支有根时要有阳刃强为佳。杀身两停。")
    if gan_shens[1] == '杀' and gan_shens[3] == '杀':
        print("月时天干为七杀：体弱多病")    
    if gan_shens[0] == '杀' and gan_shens[3] == '杀':
        print("七杀年干时干：男头胎麻烦（概率），女婚姻有阻碍。")  
    if gan_shens[3] == '杀':
        print("七杀在时干，通月支：固执有毅力。")       
    if '印' in gan_shens:
        print("身弱杀生印，不少是精明练达的商人。")  
    if '财' in gan_shens or '才' in gan_shens:
        print("财生杀，如果不是身弱有印，不佳。")  
        for zhi_ in zhis: 
            if set((ten_deities[me].inverse['杀'], ten_deities[me].inverse['财'])) in set(zhi5[zhi_]):
                print("杀不喜与财同根透出，这样杀的力量太强。")  


for seq, gan_ in enumerate(gan_shens):
    if gan_ != '杀' and zhi_shens[seq] != '杀':
        continue   
    if gan_ == '杀' and '杀' in zhi_shen3[seq] and seq != 3:
        print("七杀坐七杀，六亲福薄。")
    if get_empty(zhus[2],zhis[seq]) == '空':
        print("七杀坐空亡，女命夫缘薄。")
        
            
if shens2.count('杀') > 2:
    print("杀多者如果无制，性格刚强。打抱不平，不易听人劝。女的喜欢佩服的人。")
if zhi_shens[2]  == '杀' and len(zhi5[zhis[2]]) == 1:
    print("天元坐杀：乙酉，己卯，如无食神，阳刃，性急，聪明，对人不信任。如果七杀还透出月干无制，体弱多病，甚至夭折。如果在时干，晚年不好。")
    
if zhus[2] in (('丁', '卯'), ('丁', '亥'), ('丁', '未')) and zhis.time == '子':
    print("七杀坐桃花，如有刑冲，引感情引祸。忌讳午运。")
     
# 食分析    
if '食' in gan_shens:
    if '食' in zhi_shens:
        print("食神成格的情况下，寿命比较好。食神和偏财格比较长寿。食神厚道，为人不慷慨。食神有口福。成格基础84，喜财忌偏印(只能偏财制)。")
        print("食神无财一生衣食无忧，无大福。有印用比劫通关或财制。")
    if '枭' in gan_shens:
        print("男的食神碰到偏印，身体不好。怕偏印，正印要好一点。四柱透出偏财可解。")
        if '劫' in gan_shens:
            print("食神不宜与劫财、偏印齐出干。体弱多病。")
        if '杀' in gan_shens:
            print("食神不宜与杀、偏印齐成格。体弱多病。")
    if '食' in zhi_shens:
        print("食神天透地藏，女命阳日主适合社会性职业，阴日主适合上班族。")
    if (not '财' in gan_shens) and (not '才' in gan_shens):
        print("食神多，要食伤生财才好，无财难发。")
    if '伤' in gan_shens:
        print("食伤混杂：食神和伤官同透天干：志大才疏。")
    if '杀' in gan_shens:
        print("食神制杀，杀不是主格，施舍后后悔。")



    for seq, gan_ in enumerate(gan_shens):
        if gan_ != '食':
            continue   
        if zhi_shens[seq] =='劫':
            print("食神坐阳刃，辛劳。")
        
            
if shens2.count('食') > 2:
    print("食神四个及以上的为多，做伤官处理。食神多，要食伤生财才好，无财难发。")
    if '劫' in gan_shens or '比' in gan_shens:
        print("食神带比劫，好施舍，乐于做社会服务。")
        
if ('杀', '食') in shen_zhus or ( '食', '杀') in shen_zhus:
    print("食神与七杀同一柱，易怒。食神制杀，最好食在前。有一定概率。")
    
if ('枭', '食') in shen_zhus or ( '食', '枭') in shen_zhus:
    print("女命最怕食神偏印同一柱。不利后代。")
    
if zhi_shens[2]  == '食' and len(zhi5[zhis[2]]) == 1:
    print("日支食神专位容易发胖，有福。只有2日：癸卯，己酉。男命有有助之妻。")
    


# 伤分析    
if '伤' in gan_shens:
    print("伤官有才华，但是清高。要生财，或者印制。")
    if '伤' in zhi_shens:
        print("食神重成伤官，不适合伤官配印。金水、土金、木火命造更高。火土要调候，容易火炎土燥。伤官和七杀的局不适合月支为库。")
        print("成格基础87生财、配印。不考虑调候逆用比顺用好，调候更重要。生正财用偏印，生偏财用正印。\n伤官配印，如果透杀，透财不佳。伤官七杀同时成格，不透财为上好命局。")

    if '印' in gan_shens and ('财' not in gan_shens):
        print("伤官配印，无财，有手艺，但是不善于理财。有一定个性")
    if gan_shens[0] == '伤' and gan_shens[1] == '伤' and (not '伤' in zhi_shens2):
        print("年月天干都浮现伤官，亲属少。")

    if zhi_shens[1]  == '伤' and len(zhi5[zhis[1]]) == 1 and gan_shens[1] == '伤':
        print("月柱：伤官坐专位伤官，夫缘不定。假夫妻。比如老板和小蜜。")


    for seq, gan_ in enumerate(gan_shens):
        if gan_ != '伤':
            continue   
        if zhi_shens[seq] =='劫':
            print("伤官地支坐阳刃，力不从心。背禄逐马，克官劫财。影响15年。伤官坐劫财：只适合纯粹之精明商人或严谨掌握财之人。")       
            
if shens2.count('伤') > 2:
    print("女命伤官多，即使不入伤官格，也缘分浅，多有苦情。")
        
    
if zhi_shens[2]  == '伤' and len(zhi5[zhis[2]]) == 1:
    print("女命婚姻宫伤官：克夫。男的对妻子不利。只有庚子日。")
        

print("\n\n大运")    
print("="*120)  
if options.b:
    print(dayuns) 
else:
    birthday = datetime.date(day.getSolarYear(), day.getSolarMonth(), day.getSolarDay()) 
    count = 0
    

    for i in range(30):    
        #print(birthday)
        day_ = sxtwl.fromSolar(birthday.year, birthday.month, birthday.day)
        #if day_.hasJieQi() and day_.getJieQiJD() % 2 == 1
        if day_.hasJieQi() and day_.getJieQi() % 2 == 1:
                break
            #break        
        birthday += datetime.timedelta(days=direction)
        count += 1

    ages = [(round(count/3 + 10*i), round(int(options.year) + 10*i + count//3)) for i in range(12)]
    
    for (seq, value) in enumerate(ages):
        gan_ = dayuns[seq][0]
        zhi_ = dayuns[seq][1]
        fu = '*' if (gan_, zhi_) in zhus else " "
        zhi5_ = ''
        for gan in zhi5[zhi_]:
            zhi5_ = zhi5_ + "{}{}{}　".format(gan, gan5[gan], ten_deities[me][gan]) 
        
        zhi__ = set() # 大运地支关系
        
        for item in zhis:
        
            for type_ in zhi_atts[zhi_]:
                if item in zhi_atts[zhi_][type_]:
                    zhi__.add(type_ + ":" + item)
        zhi__ = '  '.join(zhi__)
        
        empty = chr(12288)
        if zhi_ in empties[zhus[2]]:
            empty = '空'        
        
        jia = ""
        if gan_ in gans:
            for i in range(4):
                if gan_ == gans[i]:
                    if abs(Zhi.index(zhi_) - Zhi.index(zhis[i])) == 2:
                        jia = jia + "  --夹：" +  Zhi[( Zhi.index(zhi_) + Zhi.index(zhis[i]) )//2]
                    if abs( Zhi.index(zhi_) - Zhi.index(zhis[i]) ) == 10:
                        jia = jia + "  --夹：" +  Zhi[(Zhi.index(zhi_) + Zhi.index(zhis[i]))%12]
                
        out = "{1:<4d}{2:<5s}{3} {15} {14} {13}  {4}:{5}{8}{6:{0}<6s}{12}{7}{8}{9} - {10:{0}<15s} {11}".format(
            chr(12288), int(value[0]), '', dayuns[seq],ten_deities[me][gan_], gan_,check_gan(gan_, gans), 
            zhi_, yinyang(zhi_), ten_deities[me][zhi_], zhi5_, zhi__,empty, fu, nayins[(gan_, zhi_)], ten_deities[me][zhi_]) 
        gan_index = Gan.index(gan_)
        zhi_index = Zhi.index(zhi_)
        out = out + jia + get_shens(gans, zhis, gan_, zhi_)
        
        print(out)
        zhis2 = list(zhis) + [zhi_]
        gans2 = list(gans) + [gan_]
        if value[0] > 100:
            continue
        for i in range(10):
            day2 = sxtwl.fromSolar(value[1] + i, 5, 1)       
            yTG = day2.getYearGZ()
            gan2_ = Gan[yTG.tg]
            zhi2_ = Zhi[yTG.dz]
            fu2 = '*' if (gan2_, zhi2_) in zhus else " "
            #print(fu2, (gan2_, zhi2_),zhus)
            
            zhi6_ = ''
            for gan in zhi5[zhi2_]:
                zhi6_ = zhi6_ + "{}{}{}　".format(gan, gan5[gan], ten_deities[me][gan])        
            
            # 大运地支关系
            zhi__ = set() # 大运地支关系
            for item in zhis2:
            
                for type_ in zhi_atts[zhi2_]:
                    if type_ == '破':
                        continue
                    if item in zhi_atts[zhi2_][type_]:
                        zhi__.add(type_ + ":" + item)
            zhi__ = '  '.join(zhi__)
            
            empty = chr(12288)
            if zhi2_ in empties[zhus[2]]:
                empty = '空'       
            out = "{1:>3d} {2:<5d}{3} {15} {14} {13}  {4}:{5}{8}{6:{0}<6s}{12}{7}{8}{9} - {10:{0}<13s} {11}".format(
                chr(12288), int(value[0]) + i, value[1] + i, gan2_+zhi2_,ten_deities[me][gan2_], gan2_,check_gan(gan2_, gans2), 
                zhi2_, yinyang(zhi2_), ten_deities[me][zhi2_], zhi6_, zhi__,empty, fu2, nayins[(gan2_, zhi2_)], ten_deities[me][zhi2_]) 
            
            jia = ""
            if gan2_ in gans2:
                for i in range(5):
                    if gan2_ == gans2[i]:
                        if abs(Zhi.index(zhi2_) - Zhi.index(zhis2[i])) == 2:
                            # print(2, zhi2_, zhis2[i])
                            jia = jia + "  --夹：" +  Zhi[( Zhi.index(zhi2_) + Zhi.index(zhis2[i]) )//2]
                        if abs( Zhi.index(zhi2_) - Zhi.index(zhis2[i]) ) == 10:
                            # print(10, zhi2_, zhis2[i])
                            jia = jia + "  --夹：" +  Zhi[(Zhi.index(zhi2_) + Zhi.index(zhis2[i]))%12]  
                            
            out = out + jia + get_shens(gans, zhis, gan2_, zhi2_)
            all_zhis = set(zhis2) | set(zhi2_)
            if set('戌亥辰巳').issubset(all_zhis):
                out = out + "  天罗地网：戌亥辰巳"
            if set('寅申巳亥').issubset(all_zhis):
                out = out + "  四生：寅申巳亥"   
            if set('子午卯酉').issubset(all_zhis):
                out = out + "  四败：子午卯酉"  
            if set('辰戌丑未').issubset(all_zhis):
                out = out + "  四库：辰戌丑未"             
            print(out)
            
        
    print(count/3)
    #print(list(zip(ages, dayuns)))
    
    # 计算星宿
    d2 = datetime.date(1, 1, 4)
    print("星宿", xingxius[(birthday - d2).days % 28], end=' ')
    
    # 计算建除
    seq = 12 - Zhi.index(zhis.month)
    print(jianchus[(Zhi.index(zhis.day) + seq)%12])        
    
# 检查三会 三合的拱合
result = ''
#for i in range(2):
    #result += check_gong(zhis, i*2, i*2+1, me, gong_he)
    #result += check_gong(zhis, i*2, i*2+1, me, gong_hui, '三会拱')

result += check_gong(zhis, 1, 2, me, gong_he)
result += check_gong(zhis, 1, 2, me, gong_hui, '三会拱')
    
if result:
    print(result)

print("="*120)   



# 格局分析
ge = ''
if (me, zhis.month) in jianlus:
    print(jianlu_desc)
    print("-"*120)
    print(jianlus[(me, zhis.month)]) 
    print("-"*120 + "\n")
    ge = '建'
#elif (me == '丙' and ('丙','申') in zhus) or (me == '甲' and ('己','巳') in zhus):
    #print("格局：专财. 运行官旺 财神不背,大发财官。忌行伤官、劫财、冲刑、破禄之运。喜身财俱旺")
elif (me, zhis.month) in (('甲','卯'), ('庚','酉'), ('壬','子')):
    ge = '月刃'
else:
    zhi = zhis[1]
    if zhi in wuhangs['土'] or (me, zhis.month) in (('乙','寅'), ('丙','午'),  ('丁','巳'), ('戊','午'), ('己','巳'), ('辛','申'), ('癸','亥')):
        for item in zhi5[zhi]:
            if item in gans[:2] + gans[3:]:
                ge = ten_deities[me][item]
    else:
        d = zhi5[zhi]
        ge = ten_deities[me][max(d, key=d.get)]
print("格局:", ge, '\t', end=' ')

# 天乙贵人
flag = False
for items in tianyis[me]:
    for item in items:
        if item in zhis:
            if not flag:
                print("| 天乙贵人：", end=' ')
                flag = True
            print(item, end=' ')
            
# 玉堂贵人
flag = False
for items in yutangs[me]:
    for item in items:
        if item in zhis:
            if not flag:
                print("| 玉堂贵人：", end=' ')
                flag = True
            print(item, end=' ')            

# 天罗
if  nayins[zhus[0]][-1] == '火':			
    if zhis.day in '戌亥':
        print("| 天罗：{}".format(zhis.day), end=' ') 

# 地网		
if  nayins[zhus[0]][-1] in '水土':			
    if zhis.day in '辰巳':
        print("| 地网：{}".format(zhis.day), end=' ') 		

# 三奇
flag = False
if ['乙','丙', '丁'] == list(gans[:3]) or ['乙','丙', '丁'] == list(gans[1:]):
    flag = True  
    print("三奇　乙丙丁", end=' ')  
if ['甲','戊', '庚'] == list(gans[:3]) or ['甲','戊', '庚'] == list(gans[1:]):
    flag = True   
    print("三奇　甲戊庚", end=' ')  
if ['辛','壬', '癸'] == list(zhis[:3]) or ['辛','壬', '癸'] == list(zhis[1:]):
    flag = True       
    print("三奇　辛壬癸", end=' ')    


# 学堂分析
for seq, item in enumerate(statuses):
    if item == '长':
        print("学堂:", zhis[seq], "\t", end=' ')
        if  nayins[zhus[seq]][-1] == ten_deities[me]['本']:
            print("正学堂:", nayins[zhus[seq]], "\t", end=' ')


#xuetang = xuetangs[ten_deities[me]['本']][1]
#if xuetang in zhis:
    #print("学堂:", xuetang, "\t\t", end=' ')
    #if xuetangs[ten_deities[me]['本']] in zhus:
        #print("正学堂:", xuetangs[ten_deities[me]['本']], "\t\t", end=' ')

# 学堂分析

for seq, item in enumerate(statuses):
    if item == '建':
        print("| 词馆:", zhis[seq], end=' ')
        if  nayins[zhus[seq]][-1] == ten_deities[me]['本']:
            print("- 正词馆:", nayins[zhus[seq]], end=' ')


ku = ten_deities[me]['库'][0]    
if ku in zhis:
    print("库：",ku, end=' ')

    for item in zhus: 
        if ku != zhus[1]:
            continue
        if nayins[item][-1] == ten_deities[me]['克']:
            print("库中有财，其人必丰厚")
        if nayins[item][-1] == ten_deities[me]['被克']:
            print(item, ten_deities[me]['被克'])
            print("绝处无依，其人必滞")    

print()

# 天元分析
for item in zhi5[zhis[2]]:    
    name = ten_deities[me][item]
    print(self_zuo[name])
print("-"*120)


# 出身分析
cai = ten_deities[me].inverse['财']
guan = ten_deities[me].inverse['官']
births = tuple(gans[:2])
if cai in births and guan in births:
    birth = '不错'
#elif cai in births or guan in births:
    #birth = '较好'
else:
    birth = '一般'

print("出身:", birth)    

guan_num = shens.count("官")
sha_num = shens.count("杀")
cai_num = shens.count("财")
piancai_num = shens.count("才")
jie_num = shens.count("劫")
bi_num = shens.count("比")
yin_num = shens.count("印")





# 食神分析
if ge == '食':
    print("\n****食神分析****: 格要日主食神俱生旺，无冲破。有财辅助财有用。  食神可生偏财、克杀")
    print(" 阳日食神暗官星，阴日食神暗正印。食神格人聪明、乐观、优雅、多才多艺。食居先，煞居后，功名显达。")
    print("======================================")  
    print('''
    喜:身旺 宜行财乡 逢食看财  忌:身弱 比 倒食(偏印)  一名进神　　二名爵星　　三名寿星
    月令建禄最佳，时禄次之，更逢贵人运
    ''')

    shi_num = shens.count("食")
    if shi_num > 2:
        print("食神过多:食神重见，变为伤官，令人少子，纵有，或带破拗性. 行印运",end=' ')
    if set(('财','食')) in set(gan_shens[:2] + zhi_shens[:2]):
        print("祖父荫业丰隆", end=' ')
    if set(('财','食')) in set(gan_shens[2:] + zhi_shens[2:]):
        print("妻男获福，怕母子俱衰绝，两皆无成", end=' ')
    if cai_num >1:
        print("财多则不清，富而已", end=' ')

    for seq, item in enumerate(gan_shens):
        if item == '食':
            if ten_deities[gans[seq]][zhis[seq]] == '墓':
                print("食入墓，即是伤官入墓，住寿难延。")  


    for seq, item in enumerate(gan_shens):
        if item == '食' or zhi_shens[seq] == '食':
            if get_empty(zhus[2],zhis[seq]):
                print("大忌空亡，更有官煞显露，为太医师巫术数九流之士，若食神逢克，又遇空亡，则不贵，再行死绝或枭运，则因食上气上生灾，翻胃噎食，缺衣食，忍饥寒而已")                     

    # 倒食分析
    if '枭' in shens and (me not in ['庚', '辛','壬']) and ten_deities[me] != '建':
        flag = True
        for item in zhi5[zhis.day]:
            if ten_deities[me]['合'] == item:
                flag = False
                break
        if flag:
            print("倒食:凡命带倒食，福薄寿夭，若有制合没事，主要为地支为天干的杀;日支或者偏印的坐支为日主的建禄状态。偏印和日支的主要成分天干合")  
            print("凡命有食遇枭，犹尊长之制我，不得自由，作事进退悔懒，有始无终，财源屡成屡败，容貌欹斜，身品琐小，胆怯心虚，凡事无成，克害六亲，幼时克母，长大伤妻子") 
            print("身旺遇此方为福")
    print()
    print("-"*120)

# 伤官分析
if ge == '伤':
    print("\n****伤官分析****: 喜:身旺,财星,印绶,伤尽 忌:身弱,无财,刑冲,入墓枭印　")
    print(" 多材艺，傲物气高，心险无忌惮，多谋少遂，弄巧成拙，常以天下之人不如己，而人亦惮之、恶之。 一名剥官神　　二名羊刃煞")
    print(" 身旺用财，身弱用印。用印不忌讳官煞。用印者须去财方能发福")
    print("官星隐显，伤之不尽，岁运再见官星，官来乘旺，再见刑冲破害，刃煞克身，身弱财旺，必主徒流死亡，五行有救，亦残疾。若四柱无官而遇伤煞重者，运入官乡，岁君又遇，若不目疾，必主灾破。")
    print("娇贵伤不起、谨慎过头了略显胆小，节俭近于吝啬")
    print("======================================")  

    if '财' in shens or '才' in shens:
        print("伤官生财")
    else:
        print("伤官无财，主贫穷")
        
    if '印' in shens or '枭' in shens:
        print('印能制伤，所以为贵，反要伤官旺，身稍弱，始为秀气;印旺极深，不必多见，偏正叠出，反为不秀，故伤轻身重而印绶多见，贫穷之格也。')   
        if '财' in shens or '才' in shens:
            print('财印相克，本不并用，只要干头两清而不相碍；又必生财者，财太旺而带印，佩印者印太重而带财，调停中和，遂为贵格')
    if ('官' in shens) :
        print(shang_guans[ten_deities[me]['本']])   
        print('金水独宜，然要财印为辅，不可伤官并透。若冬金用官，而又化伤为财，则尤为极秀极贵。若孤官无辅，或官伤并透，则发福不大矣。')
    if ('杀' in shens) :
        print("煞因伤而有制，两得其宜，只要无财，便为贵格")   
    if gan_shens[0] == '伤':
        print("年干伤官最重，谓之福基受伤，终身不可除去，若月支更有，甚于伤身七煞")

    for seq, item in enumerate(gan_shens):
        if item == '伤':
            if ten_deities[gans[seq]][zhis[seq]] == '墓':
                print("食入墓，即是伤官入墓，住寿难延。")  


    for seq, item in enumerate(gan_shens):
        if item == '食' or zhi_shens[seq] == '食':
            if get_empty(zhus[2],zhis[seq]):
                print("大忌空亡，更有官煞显露，为太医师巫术数九流之士，若食神逢克，又遇空亡，则不贵，再行死绝或枭运，则因食上气上生灾，翻胃噎食，缺衣食，忍饥寒而已")                     
    print()
    print("-"*120)    

# 劫财分析
if ge == '劫':
    print("\n****劫财(阳刃)分析****：阳刃冲合岁君,勃然祸至。身弱不作凶。")
    print("======================================")  
    if "劫" == gan_shens[3] or "劫" == zhi_shens[3]:
        print("劫财阳刃,切忌时逢,岁运并临,灾殃立至,独阳刃以时言,重于年月日也。")

    shi_num = shens.count("食")
    print("-"*120)

# 财分析

if ge == '财' or ge == '才':
    print("\n****财分析 **** 喜:旺,印,食,官 忌:比 羊刃 空绝 冲合   财星,天马星,催官星,壮志神")
    if gan_shens.count('财') + gan_shens.count('才') > 1:
        print('财喜根深，不宜太露，然透一位以清用，格所最喜，不为之露。即非月令用神，若寅透乙、卯透甲之类，一亦不为过，太多则露矣。')
        print('财旺生官，露亦不忌，盖露不忌，盖露以防劫，生官则劫退，譬如府库钱粮，有官守护，即使露白，谁敢劫之？')
    if '伤' in gan_shens:
        print("有伤官，财不能生官")    
    if '食' in shens:
        print("有财用食生者，身强而不露官，略带一位比劫，益觉有情")     
        if '印' in shens or '枭' in 'shens':
            print("注意印食冲突")  
    if '比' in shens:
        print("比不吉，但是伤官食神可化!")   
    if '杀' in shens:
        print("不论合煞制煞，运喜食伤身旺之方!")          
    
    if "财" == zhi_shens[0]:
        print("岁带正马：月令有财或伤食，不犯刑冲分夺，旺祖业丰厚。同类月令且带比，或遇运行伤劫 贫")
    if "财" == zhi_shens[3]:
        print("时带正马：无冲刑破劫，主招美妻，得外来财物，生子荣贵，财产丰厚，此非父母之财，乃身外之财，招来产业，宜俭不宜奢。")      
    if "财" == zhi_shens[2] and (me not in ('壬','癸')):
        print("天元坐财：喜印食 畏官煞，喜月令旺 ")              
    if ('官' not in shens) and ('伤' not in shens) and ('食' not in shens):
        print("财旺生官:若月令财无损克，亦主登科")


    if cai_num > 2 and ('劫' not in shens) and ('比' not in shens) \
       and ('比' not in shens) and ('印' not in shens):
        print("财　不重叠多见　财多身弱，柱无印助; 若财多身弱，柱无印助不为福。")

    if '印' in shens:
        print("先财后印，反成其福，先印后财，反成其辱是也?")      
    if '官' in gan_shens:
        print("官星显露，别无伤损，或更食生印助日主健旺，富贵双全")          
    if '财' in gan_shens and (('劫' not in shens) and ('比' not in shens)):
        print("财不宜明露")  
    for seq, item in enumerate(gan_shens):
        if item == '财':
            if ten_deities[gans[seq]][zhis[seq]] == '墓':
                print("财星入墓，必定刑妻")  
            if ten_deities[gans[seq]][zhis[seq]] == '长':   
                print("财遇长生，田园万顷")  

    if ('官' not in shens) and (('劫' in shens) or ('比' in shens)):
        print("切忌有姊妹兄弟分夺，柱无官星，祸患百出。")

    if bi_num + jie_num > 1:
        print("兄弟辈出: 纵入官乡，发福必渺.")        

    for seq, item in enumerate(zhi_shens):
        if item == '才' or ten_deities[me][zhis[seq]] == '才':
            if get_empty(zhus[2],zhis[seq]):
                print("空亡 官将不成，财将不住")  

    print("-"*120)         

# 财库分析
if ten_deities[ten_deities[me].inverse["财"]]['库'][-1] in zhis:
    print("财临库墓: 一生财帛丰厚，因财致官, 天干透土更佳")   
if cai_num < 2 and (('劫' in shens) or ('比' in shens)):
    print("财少身强，柱有比劫，不为福")   




# 官分析
if ge == "官":
    print("\n**** 官分析 ****\n 喜:身旺 财印   忌：身弱 偏官 伤官 刑冲 泄气 贪合 入墓")
    print("一曰正官 二曰禄神 最忌刑冲破害、伤官七煞，贪合忘官，劫财比等等，遇到这些情况便成为破格 财印并存要分开")
    print("运：财旺印衰喜印，忌食伤生财；旺印财衰喜财，喜食伤生财；带伤食用印制；")
    print("带煞伤食不碍。劫合煞财运可行，伤食可行，身旺，印绶亦可行；伤官合煞，则伤食与财俱可行，而不宜逢印")
    print("======================================")  
    if guan_num > 1:
        print("官多变杀，以干为准")
    if "财" in shens and "印" in shens and ("伤" not in shens) and ("杀" not in shens):
        print("官星通过天干显露出来，又得到财、印两方面的扶持，四柱中又没有伤煞，行运再引到官乡，是大富大贵的命。")
    if "财" in shens or '才' in shens:
        print("有财辅助")       
    if "印" in shens or "枭" in shens:
        print("有印辅助　正官带伤食而用印制，运喜官旺印旺之乡，财运切忌。若印绶叠出，财运亦无害矣。")   
    if "食" in shens:
        print("又曰凡论官星，略见一位食神坐实，便能损局，有杀则无妨。惟月令隐禄，见食却为三奇之贵。因为食神和官相合。")    
    if "伤" in shens:
        print("伤官需要印或偏印来抑制，　有杀也无妨")         
    if "杀" in shens:
        print("伤官需要印或偏印来抑制。用劫合煞，则财运可行，伤食可行，身旺，印绶亦可行，只不过复露七煞。若命用伤官合煞，则伤食与财俱可行，而不宜逢印矣。")        

    if zhi_shens[2] in ("财","印"):
        print("凡用官，日干自坐财印，终显")           
    if zhi_shens[2] in ("伤","杀"):
        print("自坐伤、煞，终有节病")   



    # 检查天福贵人
    if (guan, ten_deities[guan].inverse['建']) in zhus:
        print("天福贵人:主科名巍峨，官职尊崇，多掌丝纶文翰之美!")

    # 天元坐禄    
    if guan in zhi5[zhis[2]]:
        print("天元作禄: 日主与官星并旺,才是贵命。大多不贵即富,即使是命局中有缺点,行到好的大运时,便能一发如雷。")
        print(tianyuans[ten_deities[me]['本']])         

    # 岁德正官
    if gan_shens[0] == '官' or zhi_shens[0] == '官':
        print("岁德正官: 必生宦族,或荫袭祖父之职,若月居财官分野,运向财官旺地,日主健旺,贵无疑矣。凡年干遇官,福气最重,发达必早。")    

    # 时上正官
    if gan_shens[0] == '官' or zhi_shens[0] == '官':
        print("时上正官: 正官有用不须多，多则伤身少则和，日旺再逢生印绶，定须平步擢高科。")        

    print()
    print("-"*120)  
# 官库分析
if ten_deities[ten_deities[me].inverse["官"]]['库'][-1] in zhis:
    print("官临库墓")   
    if lu_ku_cai[me] in zhis:
        print("官印禄库: 有官库，且库中有财")


# 杀(偏官)分析
if ge == "杀":
    print("\n杀(偏官)分析 **** 喜:身旺  印绶  合煞  食制 羊刃  比  逢煞看印及刃  以食为引   忌：身弱  财星  正官  刑冲  入墓")
    print("一曰偏官 二曰七煞 三曰五鬼 四曰将星 五曰孤极星 原有制伏,煞出为福,原无制伏,煞出为祸   性情如虎，急躁如风,尤其是七杀为丙、丁火时。")
    print("坐长生、临官、帝旺,更多带比同类相扶,则能化鬼为官,化煞为权,行运引至印乡,必发富贵。倘岁运再遇煞地,祸不旋踵。")
    print("七杀喜酒色而偏争好斗、爱轩昂而扶弱欺强")
    print("======================================")  
    if "财" in shens:
        print("逢煞看财,如身强煞弱,有财星则吉,身弱煞强,有财引鬼盗气,非贫则夭;")
    if "比" in shens:
        print("如果比比自己弱，可以先挨杀。")        
    if "食" in shens:
        print("有食神透制,即《经》云:一见制伏,却为贵本")   
        if "财" in shens or "印" in shens or '才' in shens or "枭" in shens:
            print("煞用食制，不要露财透印，以财能转食生煞，而印能去食护煞也。然而财先食后，财生煞而食以制之，或印先食后，食太旺而印制，则格成大贵。")   
    if "劫" in shens:
        print("有阳刃配合,即《经》云:煞无刃不显,逢煞看刃是也。")    
    if "印" in shens:
        print("印: 则煞生印，印生身")           
    if sha_num > 1:
        print("七煞重逢") 
        if weak:
            print("弃命从煞，须要会煞从财.四柱无一点比印绶方论，如遇运扶身旺，与煞为敌，从煞不专，故为祸患")
            print("阴干从地支，煞纯者多贵，以阴柔能从物也。阳干从地支，煞纯者亦贵，但次于阴，以阳不受制也。")
            print("水火金土皆从，惟阳木不能从，死木受斧斤，反遭其伤故也。")
            print("古歌曰：五阳坐日全逢煞，弃命相从寿不坚，如是五阴逢此地，身衰煞旺吉堪言。")            
    if "杀" == zhi_shens[2]:
        print("为人心多性急，阴险怀毒，僭伪谋害，不近人情")      
    if "杀" == zhi_shens[3] or "杀" == gan_shens[3]:
        print(" 时杀：月制干强，其煞反为权印。《经》云：时上偏官身要强，阳刃、冲刑煞敢当，制多要行煞旺运，煞多制少必为殃。")   
        print(" 一位为妙，年、月、日重见，反主辛苦劳碌。若身旺，煞制太过，喜行煞旺运，或三合煞运，如无制伏，要行制伏运方发。但忌身弱，纵得运扶持发福，运过依旧不济。")   
        print("《独步》云：时上一位，贵藏在支中，是日，主要旺强名利，方有气。")   
        print("《古歌》云：时上偏官喜刃冲，身强制伏禄丰隆。正官若也来相混，身弱财多主困穷。") 
        print("时上偏官一位强，日辰自旺喜非常。有财有印多财禄，定是天生作栋梁。") 
        print("煞临子位，必招悖逆之儿。")

    if "杀" == zhi_shens[0]:
        print(" 年上七煞：出身寒微，命有贵子。")   
        print("岁煞一位不宜制，四柱重见却宜制，日主生旺，制伏略多，喜行煞旺地，制伏太过，或煞旺身衰，官煞混杂，岁运如之，碌碌之辈。若制伏不及，运至身衰煞旺乡，必生祸患。")   
        print("《独步》云：时上一位，贵藏在支中，是日，主要旺强名利，方有气。")   
        print("《古歌》云：时上偏官喜刃冲，身强制伏禄丰隆。正官若也来相混，身弱财多主困穷。") 
        print("时上偏官一位强，日辰自旺喜非常。有财有印多财禄，定是天生作栋梁。")         
    if ('官' in shens) :
        print("官煞混杂：身弱多夭贫")

    for seq, item in enumerate(gan_shens):
        if item == '杀':
            if ten_deities[gans[seq]][zhis[seq]] == '长':   
                print("七煞遇长生乙位，女招贵夫。")  
    print()
    print("-"*120)      

# 印分析
if ge == "印":
    print("\n印分析 **** 喜:食神 天月德 七煞 逢印看煞 以官为引   忌： 刑冲 伤官 死墓 辰戊印怕木 丑未印不怕木")
    print("一曰正印 二曰魁星 三曰孙极星")
    print("以印绶多者为上,月最要,日时次之,年干虽重,须归禄月、日、时,方可取用,若年露印,月日时无,亦不济事。")
    print("======================================")  
    if "官" in shens:
        print("官能生印。身旺印强，不愁太过，只要官星清纯")      
    if "杀" in shens:
        print("喜七煞,但煞不可太多,多则伤身。原无七煞,行运遇之则发;原有七煞,行财运,或印绶死绝,或临墓地,皆凶。")    
    if "伤" in shens or "食" in shens:
        print("伤食：身强印旺，恐其太过，泄身以为秀气；若印浅身轻，而用层层伤食，则寒贫之局矣。")     
    if "财" in shens or "才" in shens:
        print("有印多而用财者，印重身强，透财以抑太过，权而用之，只要根深，无防财破。 若印轻财重，又无劫财以救，则为贪财破印，贫贱之局也。")             

    if yin_num > 1:
        print("印绶复遇拱禄、专禄、归禄、鼠贵、夹贵、时贵等格,尤为奇特,但主少子或无子,印绶多者清孤。")  
    if "劫" in shens:
        print("化印为劫；弃之以就财官")              
    print()
    print("-"*120)         
    
# 偏印分析
if ge == "枭":
    print("\n印分析 **** 喜:食神 天月德 七煞 逢印看煞 以官为引   忌： 刑冲 伤官 死墓 辰戊印怕木 丑未印不怕木")
    print("一曰正印 二曰魁星 三曰孙极星")
    print("以印绶多者为上,月最要,日时次之,年干虽重,须归禄月、日、时,方可取用,若年露印,月日时无,亦不济事。")
    print("======================================")  
    if "官" in shens:
        print("官能生印。身旺印强，不愁太过，只要官星清纯")      
    if "杀" in shens:
        print("喜七煞,但煞不可太多,多则伤身。原无七煞,行运遇之则发;原有七煞,行财运,或印绶死绝,或临墓地,皆凶。")    
    if "伤" in shens or "食" in shens:
        print("伤食：身强印旺，恐其太过，泄身以为秀气；若印浅身轻，而用层层伤食，则寒贫之局矣。")     
    if "财" in shens or "才" in shens:
        print("弃印就财。")             

    if yin_num > 1:
        print("印绶复遇拱禄、专禄、归禄、鼠贵、夹贵、时贵等格,尤为奇特,但主少子或无子,印绶多者清孤。")  
    if "劫" in shens:
        print("化印为劫；弃之以就财官")              
    print()
    print("-"*120)         



gan_ = tuple(gans)
for item in Gan:
    if gan_.count(item) == 3:
        print("三字干：", item, "--", gan3[item])
        break

gan_ = tuple(gans)
for item in Gan:
    if gan_.count(item) == 4:
        print("四字干：", item, "--", gan4[item])
        break    

zhi_ = tuple(zhis)
for item in Zhi:
    if zhi_.count(item) > 2:
        print("三字支：", item, "--", zhi3[item])
        break

print("="*120)  
print("你属:", me, "特点：--", gan_desc[me],"\n")
print("年份:", zhis[0], "特点：--", zhi_desc[zhis[0]],"\n")





# 羊刃分析
key = '帝' if Gan.index(me)%2 == 0 else '冠'

if ten_deities[me].inverse[key] in zhis:
    print("\n羊刃:", me, ten_deities[me].inverse[key])  
    print("======================参考：https://www.jianshu.com/p/c503f7b3ed04")  
    if ten_deities[me].inverse['冠']:
        print("羊刃重重又见禄，富贵饶金玉。 官、印相助福相资。")  
    else:
        print("劳累命！")




# 将星分析
me_zhi = zhis[2]
other_zhis = zhis[:2] + zhis[3:]
flag = False
tmp_list = []
if me_zhi in ("申", "子", "辰"):
    if "子" in other_zhis:
        flag = True
        tmp_list.append((me_zhi, '子'))
elif me_zhi in ("丑", "巳", "酉"):
    if "酉" in other_zhis:
        flag = True   
        tmp_list.append((me_zhi, '酉'))
elif me_zhi in ("寅", "午", "戌"):
    if "午" in other_zhis:
        flag = True     
        tmp_list.append((me_zhi, '午'))
elif me_zhi in ("亥", "卯", "未"):
    if "卯" in other_zhis:
        flag = True   
        tmp_list.append((me_zhi, '卯'))

if flag:
    print("\n\n将星: 常欲吉星相扶，贵煞加临乃为吉庆。")  
    print("=========================")   
    print('''理愚歌》云：将星若用亡神临，为国栋梁臣。言吉助之为贵，更夹贵库墓纯粹而
    不杂者，出将入相之格也，带华盖、正印而不夹库，两府之格也；只带库墓而带正印，员郎
    以上，既不带墓又不带正印，止有华盖，常调之禄也；带华印而正建驿马，名曰节印，主旌节
    之贵；若岁干库同库为两重福，主大贵。''')
    print(tmp_list)

# 华盖分析
flag = False
if me_zhi in ("申", "子", "辰"):
    if "辰" in other_zhis:
        flag = True
elif me_zhi in ("丑", "巳", "酉"):
    if "丑" in other_zhis:
        flag = True   
elif me_zhi in ("寅", "午", "戌"):
    if "戌" in other_zhis:
        flag = True     
elif me_zhi in ("亥", "卯", "未"):
    if "未" in other_zhis:
        flag = True   

if flag:
    print("\n\n华盖: 多主孤寡，总贵亦不免孤独，作僧道艺术论。")  
    print("=========================")   
    print('''《理愚歌》云：华盖虽吉亦有妨，或为孽子或孤孀。填房入赘多阙口，炉钳顶笠拔缁黄。
    又云：华盖星辰兄弟寡，天上孤高之宿也；生来若在时与胎，便是过房庶出者。''')    


# 咸池 桃花
flag = False
taohuas = []
year_zhi = zhis[0]
if me_zhi in ("申", "子", "辰") or year_zhi in ("申", "子", "辰"):
    if "酉" in zhis:
        flag = True
        taohuas.append("酉")
elif me_zhi in ("丑", "巳", "酉") or year_zhi in ("丑", "巳", "酉"):
    if "午" in other_zhis:
        flag = True   
        taohuas.append("午")
elif me_zhi in ("寅", "午", "戌") or year_zhi in ("寅", "午", "戌"):
    if "卯" in other_zhis:
        flag = True    
        taohuas.append("卯")
elif me_zhi in ("亥", "卯", "未") or year_zhi in ("亥", "卯", "未"):
    if "子" in other_zhis:
        flag = True   
        taohuas.append("子")

if flag:
    print("\n\n咸池(桃花): 墙里桃花，煞在年月；墙外桃花，煞在日时；")  
    print("=========================")   
    print('''一名败神，一名桃花煞，其神之奸邪淫鄙，如生旺则美容仪，耽酒色，疏财好欢，
    破散家业，唯务贪淫；如死绝，落魄不检，言行狡诈，游荡赌博，忘恩失信，私滥奸淫，
    靡所不为；与元辰并，更临生旺者，多得匪人为妻；与贵人建禄并，多因油盐酒货得生，
    或因妇人暗昧之财起家，平生有水厄、痨瘵之疾，累遭遗失暗昧之灾。此人入命，有破无成，
    非为吉兆，妇人尤忌之。
    咸池非吉煞，日时与水命遇之尤凶。''')  
    print(taohuas, zhis)

# 禄分析
flag = False
for item in zhus:
    if item in lu_types[me]:
        if not flag:
            print("\n\n禄分析:")  
            print("=========================")	    
        print(item,lu_types[me][item])
 

# 文星贵人
if wenxing[me] in zhis:
    print("文星贵人: ", me,  wenxing[me])  

# 天印贵人
if tianyin[me] in zhis:
    print("天印贵人: 此号天印贵，荣达受皇封", me,  tianyin[me])  


short = min(scores, key=scores.get)
print("\n\n五行缺{}的建议参见 http://t.cn/E6zwOMq".format(short))    

sum_index = ''.join([me, '日', *zhus[3]])
if sum_index in summarys:
    print("\n\n命")    
    print("=========================")      
    print(summarys[sum_index])
    
    
print("======================================")  
if '杀' in shens:
    if yinyang(me) == '+':
        print("阳杀:话多,热情外向,异性缘好")
    else:
        print("阴杀:话少,性格柔和")
if '印' in shens and '才' in shens and '官' in shens:
    print("印,偏财,官:三奇 怕正财")
if '才' in shens and '杀' in shens:
    print("男:因女致祸、因色致祸; 女:赔货")
    
if '才' in shens and '枭' in shens:
    print("偏印因偏财而不懒！")    
    
