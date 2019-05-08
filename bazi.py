#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 钉钉或微信pythontesting 钉钉群21734177 技术支持qq群：630011153 144081101
# 鸣谢 https://github.com/yuangu/sxtwl_cpp/tree/master/python
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


description = '''

'''

parser = argparse.ArgumentParser(description=description,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('year', action="store", help=u'year')
parser.add_argument('month', action="store", help=u'month')
parser.add_argument('day', action="store", help=u'day')
parser.add_argument('time', action="store", help=u'time')    
parser.add_argument('-b', action="store_true", default=False, help=u'直接输入八字')
parser.add_argument('-g', action="store_true", default=False, help=u'是否采用公历')
parser.add_argument('-r', action="store_true", default=False, help=u'是否为闰月，仅仅使用于农历')
parser.add_argument('-n', action="store_true", default=False, help=u'是否为女，默认为男')
parser.add_argument('--version', action='version',
                    version='%(prog)s 0.1 Rongzhong xu 2019 02 21')
options = parser.parse_args()

Gans = collections.namedtuple("Gans", "year month day time")
Zhis = collections.namedtuple("Zhis", "year month day time")

if options.b:
    gans = Gans(year=options.year[0], month=options.month[0], 
                day=options.day[0],  time=options.time[0])
    zhis = Gans(year=options.year[1], month=options.month[1], 
                day=options.day[1],  time=options.time[1])
else:

    lunar = sxtwl.Lunar();
    if options.g:
        day = lunar.getDayBySolar(
            int(options.year), int(options.month), int(options.day))
    else:
        day = lunar.getDayByLunar(
            int(options.year), int(options.month), int(options.day), options.r)

    gz = lunar.getShiGz(day.Lday2.tg, int(options.time))

    #　计算甲干相合    
    gans = Gans(year=Gan[day.Lyear2.tg], month=Gan[day.Lmonth2.tg], 
                day=Gan[day.Lday2.tg], time=Gan[gz.tg])
    zhis = Zhis(year=Zhi[day.Lyear2.dz], month=Zhi[day.Lmonth2.dz], 
                day=Zhi[day.Lday2.dz], time=Zhi[gz.dz])


me = gans.day
month = zhis.month
alls = list(gans) + list(zhis)
zhus = [item for item in zip(gans, zhis)]

gan_shens = []
for seq, item in enumerate(gans):    
    if seq == 2:
        gan_shens.append('自己')
    else:
        gan_shens.append(ten_deities[me][item])
#print(gan_shens)

zhi_shens = []
for item in zhis:
    d = zhi5[item]
    zhi_shens.append(ten_deities[me][max(d, key=d.get)])
#print(zhi_shens)
shens = gan_shens + zhi_shens


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

# 计算八字强弱
# 子平真诠的计算
weak = True
me_status = []
for item in zhis:
    me_status.append(ten_deities[me][item])
    if ten_deities[me][item] in ('长生', '帝旺', '建'):
        weak = False
        

if weak:
    if shens.count('比肩') + me_status.count('库') >2:
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
strong = gan_scores[me_attrs_['比肩']] + gan_scores[me_attrs_['劫']] \
    + gan_scores[me_attrs_['偏印']] + gan_scores[me_attrs_['印']]

if not options.b:
    print("\n日期:")
    print("======================================")  
    print("公历:", end='')
    print("\t{}年{}月{}日".format(day.y, day.m, day.d))

    Lleap = "闰" if day.Lleap else ""
    print("农历:", end='')
    print("\t{}年{}{}月{}日".format(day.Lyear0 + 1984, Lleap, ymc[day.Lmc], rmc[day.Ldi]))
print("-"*140)
print("排盘源码: http://t.cn/E6zzQYj \t\t解读:钉钉或微信pythontesting","\t\t墓库：", kus)
print("甲己-中正土  乙庚-仁义金  丙辛-威制水  丁壬-淫慝木  戊癸-无情火", "  三会:", zhi_huis)
print("="*140)    
print("{:^28s}{:^28s}{:^28s}{:^28s}".format('年【父-根】', "月【兄弟僚友-苗】", "日【自己配偶-花】", "时【子孙-实】"))
print("-"*140)


print("{:^29s}{:^29s}{:^30s}{:^30s}".format(
    '{}{}{}5 [{}] {}'.format(
        gans.year, yinyang(gans.year), gan5[gans.year], ten_deities[me][gans.year], check_gan(gans.year, gans)),
    '{}{}{}5 [{}] {}'.format(
        gans.month, yinyang(gans.month), gan5[gans.month], ten_deities[me][gans.month], check_gan(gans.month, gans)),
    '{}{}{}5 [{}] {}'.format(me, yinyang(me),gan5[me], '天', check_gan(me, gans)), 
    '{}{}{}5 [{}] {}'.format(gans.time, yinyang(gans.time), gan5[gans.time], ten_deities[me][gans.time], check_gan(gans.time, gans)),
))

print("{:^30s}{:^29s}{:^29s}{:^30s}".format(
    "{}{}{} [{}] {}".format(
        zhis.year, yinyang(zhis.year), ten_deities[me][zhis.year],
        ten_deities[gans.year][zhis.year], get_empty(zhus[2],zhis.year)),
    "{}{}{} [{}] {}【命】地".format(
        zhis.month, yinyang(zhis.month), ten_deities[me][zhis.month],
        ten_deities[gans.month][zhis.month], get_empty(zhus[2],zhis.month)),  
    "{}{}{} 地".format(zhis.day, yinyang(zhis.day), ten_deities[me][zhis.day]),   
    "{}{}{} [{}] {}".format(
        zhis.time, yinyang(zhis.time), ten_deities[me][zhis.time], 
        ten_deities[gans.time][zhis.time], get_empty(zhus[2],zhis.time)),
))

statuses = [ten_deities[me][item] for item in zhis]


for seq, item in enumerate(zhis):
    out = ''
    multi = 2 if item == zhis.month and seq == 1 else 1

    for gan in zhi5[item]:
        out = out + "{}{}{}{} ".format(gan, gan5[gan], zhi5[item][gan]*multi,  
                                       ten_deities[me][gan])
    print("{:^27s}".format(out), end=' ')

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
                    output = output + " " + type_ + ":" if type_ not in ('冲','暗合') else output + " " + type_
                    flag = True
                if type_ not in ('冲','暗合'):
                    output += zhi
    print("{:^30s}".format(output), end=' ')

print()

# 输出地支minor关系
for seq, item in enumerate(zhis):

    output = ''
    others = zhis[:seq] + zhis[seq+1:] 
    for type_ in zhi_atts[item]:
        flag = False
        if type_ not in ('害',"破","会"):
            continue
        for zhi in zhi_atts[item][type_]:
            if zhi in others:
                if not flag:
                    output = output + " " + type_ + ":"
                    flag = True
                output += zhi
    print("{:^32s}".format(output), end=' ')

print()
for seq, item in enumerate(zhus):
    # 检查空亡 
    result = "{}-{}".format(nayins[item], '亡') if zhis[seq] == wangs[zhis[0]] else nayins[item]
    # 检查劫杀 
    result = "{}-{}".format(result, '劫杀') if zhis[seq] == jieshas[zhis[0]] else result
    # 检查元辰
    result = "{}-{}".format(result, '元辰') if zhis[seq] == Zhi[(Zhi.index(zhis[0]) + direction*-1*5)%12] else result    
    print("{:^30s}".format(result), end=' ')


print()  
# 检查三会 三合的拱合
result = ''
#for i in range(2):
    #result += check_gong(zhis, i*2, i*2+1, me, gong_he)
    #result += check_gong(zhis, i*2, i*2+1, me, gong_hui, '三会拱')

result += check_gong(zhis, 1, 2, me, gong_he)
result += check_gong(zhis, 1, 2, me, gong_hui, '三会拱')
    
if result:
    print(result)

print("="*140)   
print(gan_shens, zhi_3hes, " 生：寅申巳亥 败：子午卯酉　库：辰戌丑未")
print(zhi_shens, "　　地支六合:", zhi_6hes)


# 格局分析
ge = ''
if (me, zhis.month) in jianlus:
    print(jianlu_desc)
    print("-"*140)
    print(jianlus[(me, zhis.month)]) 
    print("-"*140 + "\n")
    ge = '建'
#elif (me == '丙' and ('丙','申') in zhus) or (me == '甲' and ('己','巳') in zhus):
    #print("格局：专财. 运行官旺 财神不背,大发财官。忌行伤官、劫财、冲刑、破禄之运。喜身财俱旺")
else:
    zhi = zhis[1]
    if zhi in wuhangs['土']:
        for item in zhi5[zhi]:
            if item in gans[:2] + gans[3:]:
                ge = ten_deities[me][item]

        print("格局：杂气-", ge, end=' ')
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

# 天德贵人
if tiandes[month] in alls:
    print("| 天德贵人：{}".format(tiandes[month]), end=' ') 

# 月德贵人
if yuedes[month] in zhis:
    print("| 月德贵人：{}".format(yuedes[month]), end=' ') 

# 驿马
if mas[zhis.day] in zhis:
    for seq, item in enumerate(zhis):
        if item == mas[zhis.day]:
            print(ma_zhus[zhus[seq]], zhus[seq])     

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
    if item == '长生':
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
print("-"*140)
print("五行分数", scores, '  八字强弱：', strong, "通常>29为强，需要参考月份、坐支等", "weak:", weak)
for item in gan_scores:  
    print("{}[{}]-{} ".format(
        item, ten_deities[me][item], gan_scores[item]),  end='  ')    
print()
print("-"*140)
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
piancai_num = shens.count("财")
jie_num = shens.count("劫")
bi_num = shens.count("比肩")
yin_num = shens.count("印")




# 食神分析
if ge == '食':
    print("\n****食神分析****: 格要日主食神俱生旺，无冲破。有财辅助财有用。  食神可生偏财、克杀")
    print(" 阳日食神暗合官星，阴日食神暗合正印。食神格人聪明、乐观、优雅、多才多艺。食居先，煞居后，功名显达。")
    print("======================================")  
    print('''
    喜:身旺 宜行财乡 逢食看财  忌:身弱 比肩 倒食(偏印)  一名进神　　二名爵星　　三名寿星
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
    if '偏印' in shens and (me not in ['庚', '辛','壬']) and ten_deities[me] != '建':
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
    print("-"*140)

# 伤官分析
if ge == '伤':
    print("\n****伤官分析****: 喜:身旺,财星,印绶,伤尽 忌:身弱,无财,刑冲,入墓枭印　")
    print(" 多材艺，傲物气高，心险无忌惮，多谋少遂，弄巧成拙，常以天下之人不如己，而人亦惮之、恶之。 一名剥官神　　二名羊刃煞")
    print(" 身旺用财，身弱用印。用印不忌讳官煞。用印者须去财方能发福")
    print("官星隐显，伤之不尽，岁运再见官星，官来乘旺，再见刑冲破害，刃煞克身，身弱财旺，必主徒流死亡，五行有救，亦残疾。若四柱无官而遇伤煞重者，运入官乡，岁君又遇，若不目疾，必主灾破。")
    print("娇贵伤不起、谨慎过头了略显胆小，节俭近于吝啬")
    print("======================================")  

    if '财' in shens or '偏财' in shens:
        print("伤官生财")
    else:
        print("伤官无财，主贫穷")
        
    if '印' in shens or '偏印' in shens:
        print('印能制伤，所以为贵，反要伤官旺，身稍弱，始为秀气;印旺极深，不必多见，偏正叠出，反为不秀，故伤轻身重而印绶多见，贫穷之格也。')   
        if '财' in shens or '偏财' in shens:
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
    print("-"*140)    

# 劫财分析
if ge == '劫':
    print("\n****劫财(阳刃)分析****：阳刃冲合岁君,勃然祸至。身弱不作凶。")
    print("======================================")  
    if "劫" == gan_shens[3] or "劫" == zhi_shens[3]:
        print("劫财阳刃,切忌时逢,岁运并临,灾殃立至,独阳刃以时言,重于年月日也。")

    shi_num = shens.count("食")
    print("-"*140)

# 财分析

if ge == '财' or ge == '偏财':
    print("\n****财分析 **** 喜:旺,印,食,官 忌:比 羊刃 空绝 冲合   财星,天马星,催官星,壮志神")
    if gan_shens.count('财') + gan_shens.count('偏财') > 1:
        print('财喜根深，不宜太露，然透一位以清用，格所最喜，不为之露。即非月令用神，若寅透乙、卯透甲之类，一亦不为过，太多则露矣。')
        print('财旺生官，露亦不忌，盖露不忌，盖露以防劫，生官则劫退，譬如府库钱粮，有官守护，即使露白，谁敢劫之？')
    if '伤' in gan_shens:
        print("有伤官，财不能生官")    
    if '食' in shens:
        print("有财用食生者，身强而不露官，略带一位比劫，益觉有情")     
        if '印' in shens or '偏印' in 'shens':
            print("注意印食冲突")  
    if '比肩' in shens:
        print("比肩不吉，但是伤官食神可化!")   
    if '杀' in shens:
        print("不论合煞制煞，运喜食伤身旺之方!")          
    
    if "财" == zhi_shens[0]:
        print("岁带正马：月令有财或伤食，不犯刑冲分夺，旺祖业丰厚。同类月令且带比肩，或遇运行伤劫 贫")
    if "财" == zhi_shens[3]:
        print("时带正马：无冲刑破劫，主招美妻，得外来财物，生子荣贵，财产丰厚，此非父母之财，乃身外之财，招来产业，宜俭不宜奢。")      
    if "财" == zhi_shens[2] and (me not in ('壬','癸')):
        print("天元坐财：喜印食 畏官煞，喜月令旺 ")              
    if ('官' not in shens) and ('伤' not in shens) and ('食' not in shens):
        print("财旺生官:若月令财无损克，亦主登科")


    if cai_num > 2 and ('劫' not in shens) and ('比肩' not in shens) \
       and ('比肩' not in shens) and ('印' not in shens):
        print("财　不重叠多见　财多身弱，柱无印助; 若财多身弱，柱无印助不为福。")

    if '印' in shens:
        print("先财后印，反成其福，先印后财，反成其辱是也?")      
    if '官' in gan_shens:
        print("官星显露，别无伤损，或更食生印助日主健旺，富贵双全")          
    if '财' in gan_shens and (('劫' not in shens) and ('比肩' not in shens)):
        print("财不宜明露")  
    for seq, item in enumerate(gan_shens):
        if item == '财':
            if ten_deities[gans[seq]][zhis[seq]] == '墓':
                print("财星入墓，必定刑妻")  
            if ten_deities[gans[seq]][zhis[seq]] == '长生':   
                print("财遇长生，田园万顷")  

    if ('官' not in shens) and (('劫' in shens) or ('比肩' in shens)):
        print("切忌有姊妹兄弟分夺，柱无官星，祸患百出。")

    if bi_num + jie_num > 1:
        print("兄弟辈出: 纵入官乡，发福必渺.")        

    for seq, item in enumerate(zhi_shens):
        if item == '偏财' or ten_deities[me][zhis[seq]] == '偏财':
            if get_empty(zhus[2],zhis[seq]):
                print("空亡 官将不成，财将不住")  

    print("-"*140)         

# 财库分析
if ten_deities[ten_deities[me].inverse["财"]]['库'][-1] in zhis:
    print("财临库墓: 一生财帛丰厚，因财致官, 天干透土更佳")   
if cai_num < 2 and (('劫' in shens) or ('比肩' in shens)):
    print("财少身强，柱有比劫，不为福")   




# 官分析
if ge == "官":
    print("\n**** 官分析 ****\n 喜:身旺 财印   忌：身弱 偏官 伤官 刑冲 泄气 贪合 入墓")
    print("一曰正官 二曰禄神 最忌刑冲破害、伤官七煞，贪合忘官，劫财比肩等等，遇到这些情况便成为破格 财印并存要分开")
    print("运：财旺印衰喜印，忌食伤生财；旺印财衰喜财，喜食伤生财；带伤食用印制；")
    print("带煞伤食不碍。劫合煞财运可行，伤食可行，身旺，印绶亦可行；伤官合煞，则伤食与财俱可行，而不宜逢印")
    print("======================================")  
    if guan_num > 1:
        print("官多变杀，以干为准")
    if "财" in shens and "印" in shens and ("伤" not in shens) and ("杀" not in shens):
        print("官星通过天干显露出来，又得到财、印两方面的扶持，四柱中又没有伤煞，行运再引到官乡，是大富大贵的命。")
    if "财" in shens or "偏财" in shens:
        print("有财辅助")       
    if "印" in shens or "偏印" in shens:
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
    print("-"*140)  
# 官库分析
if ten_deities[ten_deities[me].inverse["官"]]['库'][-1] in zhis:
    print("官临库墓")   
    if lu_ku_cai[me] in zhis:
        print("官印禄库: 有官库，且库中有财")


# 杀(偏官)分析
if ge == "杀":
    print("\n杀(偏官)分析 **** 喜:身旺  印绶  合煞  食制 羊刃  比肩  逢煞看印及刃  以食为引   忌：身弱  财星  正官  刑冲  入墓")
    print("一曰偏官 二曰七煞 三曰五鬼 四曰将星 五曰孤极星 原有制伏,煞出为福,原无制伏,煞出为祸   性情如虎，急躁如风,尤其是七杀为丙、丁火时。")
    print("坐长生、临官、帝旺,更多带比肩同类相扶,则能化鬼为官,化煞为权,行运引至印乡,必发富贵。倘岁运再遇煞地,祸不旋踵。")
    print("七杀喜酒色而偏争好斗、爱轩昂而扶弱欺强")
    print("======================================")  
    if "财" in shens:
        print("逢煞看财,如身强煞弱,有财星则吉,身弱煞强,有财引鬼盗气,非贫则夭;")
    if "比肩" in shens:
        print("如果比肩比自己弱，可以先挨杀。")        
    if "食" in shens:
        print("有食神透制,即《经》云:一见制伏,却为贵本")   
        if "财" in shens or "印" in shens or "偏财" in shens or "偏印" in shens:
            print("煞用食制，不要露财透印，以财能转食生煞，而印能去食护煞也。然而财先食后，财生煞而食以制之，或印先食后，食太旺而印制，则格成大贵。")   
    if "劫" in shens:
        print("有阳刃配合,即《经》云:煞无刃不显,逢煞看刃是也。")    
    if "印" in shens:
        print("印: 则煞生印，印生身")           
    if sha_num > 1:
        print("七煞重逢") 
        if weak:
            print("弃命从煞，须要会煞从财.四柱无一点比肩印绶方论，如遇运扶身旺，与煞为敌，从煞不专，故为祸患")
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
            if ten_deities[gans[seq]][zhis[seq]] == '长生':   
                print("七煞遇长生乙位，女招贵夫。")  
    print()
    print("-"*140)      

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
    if "财" in shens or "偏财" in shens:
        print("有印多而用财者，印重身强，透财以抑太过，权而用之，只要根深，无防财破。 若印轻财重，又无劫财以救，则为贪财破印，贫贱之局也。")             

    if yin_num > 1:
        print("印绶复遇拱禄、专禄、归禄、鼠贵、夹贵、时贵等格,尤为奇特,但主少子或无子,印绶多者清孤。")  
    if "劫" in shens:
        print("化印为劫；弃之以就财官")              
    print()
    print("-"*140)         
    
# 偏印分析
if ge == "偏印":
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
    if "财" in shens or "偏财" in shens:
        print("弃印就财。")             

    if yin_num > 1:
        print("印绶复遇拱禄、专禄、归禄、鼠贵、夹贵、时贵等格,尤为奇特,但主少子或无子,印绶多者清孤。")  
    if "劫" in shens:
        print("化印为劫；弃之以就财官")              
    print()
    print("-"*140)         

# 子女分析
boy = ten_deities[me].inverse['食'] if options.n else ten_deities[me].inverse['杀']
girl = ten_deities[me].inverse['伤'] if options.n else ten_deities[me].inverse['官']
children = ['食','伤'] if options.n else ['官','杀'] 
boy_state = "子：{} -- {} {} {} [{}]".format(
    boy, ten_deities[boy][zhis[0]], ten_deities[boy][zhis[1]], 
    ten_deities[boy][zhis[2]], ten_deities[boy][zhis[3]] )
girl_state = "女：{} -- {} {} {} [{}]".format(
    girl, ten_deities[girl][zhis[0]], ten_deities[girl][zhis[1]], 
    ten_deities[girl][zhis[2]], ten_deities[girl][zhis[3]] )


# 对象状态
mate = ten_deities[me].inverse['官'] if options.n else ten_deities[me].inverse['财']
lover = ten_deities[me].inverse['杀'] if options.n else ten_deities[me].inverse['偏财'] 
mate_state = "对象：{} -- {} [{}] {} {}".format(
    mate, ten_deities[mate][zhis[0]], ten_deities[mate][zhis[1]], 
    ten_deities[mate][zhis[2]], ten_deities[mate][zhis[3]] )
lover_state = "情人：{} -- {} [{}] {} {}".format(
    lover, ten_deities[lover][zhis[0]], ten_deities[lover][zhis[1]], 
    ten_deities[lover][zhis[2]], ten_deities[lover][zhis[3]] )
print("{:<25s}  {:<25s}  {:<25}  {:<25s}".format(
    boy_state, girl_state, mate_state, lover_state))

# 父母状态
father = ten_deities[me].inverse['偏财'] 
mother = ten_deities[me].inverse['印'] 
father_state = "父：{} -- {} [{}] {} {}".format(
    father, ten_deities[father][zhis[0]], ten_deities[father][zhis[1]], 
    ten_deities[father][zhis[2]], ten_deities[father][zhis[3]] )
mother_state = "母：{} -- {} [{}] {} {}".format(
    mother, ten_deities[mother][zhis[0]], ten_deities[mother][zhis[1]], 
    ten_deities[mother][zhis[2]], ten_deities[mother][zhis[3]] )

# 兄弟姐妹状态
brother = ten_deities[me].inverse['劫'] if options.n else ten_deities[me].inverse['比肩']
sister = ten_deities[me].inverse['比肩'] if options.n else ten_deities[me].inverse['劫'] 
brother_state = "兄弟：{} -- {} [{}] {} {}".format(
    brother, ten_deities[brother][zhis[0]], ten_deities[brother][zhis[1]], 
    ten_deities[brother][zhis[2]], ten_deities[brother][zhis[3]] )
sister_state = "姐妹：{} -- {} [{}] {} {}".format(
    sister, ten_deities[sister][zhis[0]], ten_deities[sister][zhis[1]], 
    ten_deities[sister][zhis[2]], ten_deities[sister][zhis[3]] )
print("{:<25s}  {:<25s}  {:<25}  {:<25s}".format(
    father_state, mother_state, brother_state, sister_state))

print("-"*140)    






# 计算上运时间，有年份时才适用
print("\n\n大运")    
print("=========================")  
if options.b:
    print(dayuns) 
else:
    birthday = datetime.date(day.y, day.m, day.d) 
    count = 0

    for i in range(30):    
        day_ = sxtwl.Lunar().getDayBySolar(birthday.year, birthday.month, birthday.day)
        if day_.qk != -1 and day_.qk % 2 == 1:
            break        
        birthday += datetime.timedelta(days=direction)
        count += 1

    ages = [(round(count/3 + 10*i, 2), int(options.year) + 10*i + count//3) for i in range(12)]
    print(list(zip(ages, dayuns)))


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

print("="*140)  
print("你属:", me, "特点：--", gan_desc[me],"\n")
print("年份:", zhis[0], "特点：--", zhi_desc[zhis[0]],"\n")





# 羊刃分析
key = '帝旺' if Gan.index(me)%2 == 0 else '冠带'

if ten_deities[me].inverse[key] in zhis:
    print("\n羊刃:", me, ten_deities[me].inverse[key])  
    print("======================参考：https://www.jianshu.com/p/c503f7b3ed04")  
    if ten_deities[me].inverse['冠带']:
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


# 文昌贵人
if wenchang[me] in zhis:
    print("文昌贵人: ", me,  wenchang[me])  

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
if '印' in shens and '偏财' in shens and '官' in shens:
    print("印,偏财,官:三奇 怕正财")
if '偏财' in shens and '杀' in shens:
    print("男:因女致祸、因色致祸; 女:赔货")
    
if '偏财' in shens and '偏印' in shens:
    print("偏印因偏财而不懒！")    
    
