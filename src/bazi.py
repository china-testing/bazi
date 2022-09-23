#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 钉钉、抖音或微信pythontesting 钉钉群21734177
# CreateDate: 2019-2-21
import argparse
import collections
import datetime

import sxtwl
from bidict import bidict

from common.const import (
    TEN_DEITIES,
    ZHI_5_DATA,
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
    GAN_5,
    KUS_DATA,
    ZHI_3_HE_DATA,
    ZHI_6_HE_DATA,
    TEMP_DATA,
    ZHI_ATT_DATA,
    NAYINS,
    WANG_DATA,
    JIE_SHA_DATA,
    EMPTIES,
    INDEX_CONSTELLATION_TUPLE,
    INDEX_JIAN_CHU_TUPLE,
    GONG_HE_DATA,
    GONG_HUI_DATA,
    JIAN_LU_DATA,
    JIANLU_DESC_DATA,
    WU_HANG_DATA,
    TIAN_YI_DATA,
    YU_TANG_DATA,
    TIAN_DE_DATA,
    YUE_DE_DATA,
    MAS_DATA,
    MA_ZHU_DATA,
    SELF_ZUO_DATA,
    SHANG_GUAN_DATA,
    TIAN_YUAN_DATA,
    LU_KU_CAI_DATA,
    GAN_3,
    GAN_4,
    ZHI_3,
    GAN_DESC_DATA,
    ZHI_DESC_DATA,
    LU_TYPES,
    WEN_CHANG,
    WEN_XING,
    TIAN_YIN,
    SUMMARY_DATA,
    ZHI_HUI_DATA,
)
from common.utils import yinyang, check_gan, get_empty, check_gong
from ganzhi import getGZ


def gan_zhi_he(zhu):
    gan, zhi = zhu
    if TEN_DEITIES[gan]["合"] in ZHI_5_DATA[zhi]:
        return "|"
    return ""


def get_gong_kus(zhis):
    result = []
    for i in range(3):
        zhi1 = zhis[i]
        zhi2 = zhis[i + 1]
        if abs(EARTHLY_BRANCHES.index(zhi1) - EARTHLY_BRANCHES.index(zhi2)) == 2:
            value = EARTHLY_BRANCHES[(EARTHLY_BRANCHES.index(zhi1) + EARTHLY_BRANCHES.index(zhi2)) // 2]
            if value in ("丑", "辰", "未", "戌"):
                result.append(value)
    return result


description = """

"""

parser = argparse.ArgumentParser(
    description=description, formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("year", action="store", help="year")
parser.add_argument("month", action="store", help="month")
parser.add_argument("day", action="store", help="day")
parser.add_argument("time", action="store", help="time")
parser.add_argument("--start", help="start year", type=int, default=1850)
parser.add_argument("--end", help="end year", default="2030")
parser.add_argument("-b", action="store_true", default=False, help="直接输入八字")
parser.add_argument("-g", action="store_true", default=False, help="是否采用公历")
parser.add_argument("-r", action="store_true", default=False, help="是否为闰月，仅仅使用于农历")
parser.add_argument("-n", action="store_true", default=False, help="是否为女，默认为男")
parser.add_argument("--version", action="version", version="%(prog)s 1.0 Rongzhong xu 2022 06 15")
options = parser.parse_args()

GANS = collections.namedtuple("Gans", "year month day time")
ZHIS = collections.namedtuple("Zhis", "year month day time")

if options.b:
    gans = GANS(
        year=options.year[0], month=options.month[0], day=options.day[0], time=options.time[0]
    )
    zhis = GANS(
        year=options.year[1], month=options.month[1], day=options.day[1], time=options.time[1]
    )
    jds = sxtwl.siZhu2Year(
        getGZ(options.year),
        getGZ(options.month),
        getGZ(options.day),
        getGZ(options.time),
        options.start,
        int(options.end),
    )
    for jd in jds:
        t = sxtwl.JD2DD(jd)
        print(
            "可能出生时间: python bazi.py -g %d %d %d %d :%d:%d" % (t.Y, t.M, t.D, t.h, t.m, round(t.s))
        )

else:

    if options.g:
        day = sxtwl.fromSolar(int(options.year), int(options.month), int(options.day))
    else:
        day = sxtwl.fromLunar(int(options.year), int(options.month), int(options.day), options.r)

    gz = day.getHourGZ(int(options.time))
    yTG = day.getYearGZ()
    mTG = day.getMonthGZ()
    dTG = day.getDayGZ()

    # 　计算甲干相合
    gans = GANS(year=HEAVENLY_STEMS[yTG.tg], month=HEAVENLY_STEMS[mTG.tg], day=HEAVENLY_STEMS[dTG.tg], time=HEAVENLY_STEMS[gz.tg])
    zhis = ZHIS(year=EARTHLY_BRANCHES[yTG.dz], month=EARTHLY_BRANCHES[mTG.dz], day=EARTHLY_BRANCHES[dTG.dz], time=EARTHLY_BRANCHES[gz.dz])


me = gans.day
month = zhis.month
alls = list(gans) + list(zhis)
zhus = [item for item in zip(gans, zhis)]

gan_shens = []
for seq, item in enumerate(gans):
    if seq == 2:
        gan_shens.append("--")
    else:
        gan_shens.append(TEN_DEITIES[me][item])
# print(gan_shens)

zhi_shens = []
for item in zhis:
    d = ZHI_5_DATA[item]
    zhi_shens.append(TEN_DEITIES[me][max(d, key=d.get)])
# print(zhi_shens)
shens = gan_shens + zhi_shens


# 计算五行分数 http://www.131.com.tw/word/b3_2_14.htm

scores = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
gan_scores = {"甲": 0, "乙": 0, "丙": 0, "丁": 0, "戊": 0, "己": 0, "庚": 0, "辛": 0, "壬": 0, "癸": 0}

for item in gans:
    scores[GAN_5[item]] += 5
    gan_scores[item] += 5


for item in list(zhis) + [zhis.month]:
    for gan in ZHI_5_DATA[item]:
        scores[GAN_5[gan]] += ZHI_5_DATA[item][gan]
        gan_scores[gan] += ZHI_5_DATA[item][gan]


# 计算八字强弱
# 子平真诠的计算
weak = True
me_status = []
for item in zhis:
    me_status.append(TEN_DEITIES[me][item])
    if TEN_DEITIES[me][item] in ("长", "帝", "建"):
        weak = False


if weak:
    if shens.count("比") + me_status.count("库") > 2:
        weak = False

# 计算大运
seq = HEAVENLY_STEMS.index(gans.year)
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
gan_seq = HEAVENLY_STEMS.index(gans.month)
zhi_seq = EARTHLY_BRANCHES.index(zhis.month)
for i in range(12):
    gan_seq += direction
    zhi_seq += direction
    dayuns.append(HEAVENLY_STEMS[gan_seq % 10] + EARTHLY_BRANCHES[zhi_seq % 12])

# 网上的计算
me_attrs_ = TEN_DEITIES[me].inverse
strong = (
    gan_scores[me_attrs_["比"]]
    + gan_scores[me_attrs_["劫"]]
    + gan_scores[me_attrs_["枭"]]
    + gan_scores[me_attrs_["印"]]
)

if not options.b:
    # print("direction",direction)
    sex = "女" if options.n else "男"
    print("\n{}命".format(sex))
    print("======================================")
    print("公历:", end="")
    print("\t{}年{}月{}日".format(day.getSolarYear(), day.getSolarMonth(), day.getSolarDay()))

    Lleap = "闰" if day.isLunarLeap() else ""
    print("农历:", end="")
    print(
        "\t{}年{}{}月{}日 穿=害".format(
            day.getLunarYear(), Lleap, day.getLunarMonth(), day.getLunarDay()
        )
    )
print("-" * 120)
print("墓库：", str(KUS_DATA).replace("'", ""), "解读:钉ding或v信pythontesting", end=" ")
for item in zhus:
    print("".join(item), end=" ")
print()
print("甲己-中正土  乙庚-仁义金  丙辛-威制水  丁壬-淫慝木  戊癸-无情火", "  三会:", str(ZHI_HUI_DATA).replace("'", ""))
print("=" * 120)

# print(ZHI_3_HE_DATA, "生：寅申巳亥 败：子午卯酉　库：辰戌丑未")
# print("地支六合:", ZHI_6_HE_DATA)
out = ""
for item in ZHI_3_HE_DATA:
    out = out + "{}:{}  ".format(item, ZHI_3_HE_DATA[item])
print(
    "\033[1;36;40m" + " ".join(list(gans)),
    " " * 5,
    " ".join(list(gan_shens)) + "\033[0m",
    " " * 5,
    out,
)
out = ""
for item in ZHI_6_HE_DATA:
    out = out + "{}{} ".format(item, ZHI_6_HE_DATA[item])
print(
    "\033[1;36;40m" + " ".join(list(zhis)),
    " " * 5,
    " ".join(list(zhi_shens)) + "\033[0m",
    " " * 5,
    "生：寅申巳亥 败：子午卯酉　库：辰戌丑未",
    " " * 2,
    out,
)
print("-" * 120)
print(
    "{1:{0}^15s}{2:{0}^15s}{3:{0}^15s}{4:{0}^15s}".format(
        chr(12288),
        "【年】{}:{}{}{}".format(
            TEMP_DATA[gans.year],
            TEMP_DATA[zhis.year],
            TEN_DEITIES[gans.year].inverse["建"],
            gan_zhi_he(zhus[0]),
        ),
        "【月】{}:{}{}{}".format(
            TEMP_DATA[gans.month],
            TEMP_DATA[zhis.month],
            TEN_DEITIES[gans.month].inverse["建"],
            gan_zhi_he(zhus[1]),
        ),
        "【日】{}:{}{}".format(TEMP_DATA[me], TEMP_DATA[zhis.day], gan_zhi_he(zhus[2])),
        "【时】{}:{}{}{}".format(
            TEMP_DATA[gans.time],
            TEMP_DATA[zhis.time],
            TEN_DEITIES[gans.time].inverse["建"],
            gan_zhi_he(zhus[3]),
        ),
    )
)
print("-" * 120)


print(
    "\033[1;36;40m{1:{0}<15s}{2:{0}<15s}{3:{0}<15s}{4:{0}<15s}\033[0m".format(
        chr(12288),
        "{}{}{}【{}】{}".format(
            gans.year,
            yinyang(gans.year),
            GAN_5[gans.year],
            TEN_DEITIES[me][gans.year],
            check_gan(gans.year, gans),
        ),
        "{}{}{}【{}】{}".format(
            gans.month,
            yinyang(gans.month),
            GAN_5[gans.month],
            TEN_DEITIES[me][gans.month],
            check_gan(gans.month, gans),
        ),
        "{}{}{}{}".format(me, yinyang(me), GAN_5[me], check_gan(me, gans)),
        "{}{}{}【{}】{}".format(
            gans.time,
            yinyang(gans.time),
            GAN_5[gans.time],
            TEN_DEITIES[me][gans.time],
            check_gan(gans.time, gans),
        ),
    )
)

print(
    "\033[1;36;40m{1:{0}<15s}{2:{0}<15s}{3:{0}<15s}{4:{0}<15s}\033[0m".format(
        chr(12288),
        "{}{}{}【{}】{}".format(
            zhis.year,
            yinyang(zhis.year),
            TEN_DEITIES[me][zhis.year],
            TEN_DEITIES[gans.year][zhis.year],
            get_empty(zhus[2], zhis.year),
        ),
        "{}{}{}【{}】{}".format(
            zhis.month,
            yinyang(zhis.month),
            TEN_DEITIES[me][zhis.month],
            TEN_DEITIES[gans.month][zhis.month],
            get_empty(zhus[2], zhis.month),
        ),
        "{}{}{}".format(zhis.day, yinyang(zhis.day), TEN_DEITIES[me][zhis.day]),
        "{}{}{}【{}】{}".format(
            zhis.time,
            yinyang(zhis.time),
            TEN_DEITIES[me][zhis.time],
            TEN_DEITIES[gans.time][zhis.time],
            get_empty(zhus[2], zhis.time),
        ),
    )
)

statuses = [TEN_DEITIES[me][item] for item in zhis]


for seq, item in enumerate(zhis):
    out = ""
    multi = 2 if item == zhis.month and seq == 1 else 1

    for gan in ZHI_5_DATA[item]:
        out = out + "{}{}{}　".format(gan, GAN_5[gan], TEN_DEITIES[me][gan])
    print("\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), out.rstrip("　")), end="")

print()
# 输出地支关系
for seq, item in enumerate(zhis):

    output = ""
    others = zhis[:seq] + zhis[seq + 1 :]
    for type_ in ZHI_ATT_DATA[item]:
        flag = False
        if type_ in ("害", "破", "会", "刑"):
            continue
        for zhi in ZHI_ATT_DATA[item][type_]:
            if zhi in others:
                if not flag:
                    output = (
                        output + "　" + type_ + "："
                        if type_ not in ("冲", "暗")
                        else output + "　" + type_
                    )
                    flag = True
                if type_ not in ("冲", "暗"):
                    output += zhi
        output = output.lstrip("　")
    print("\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), output), end="")

print()

# 输出地支minor关系
for seq, item in enumerate(zhis):

    output = ""
    others = zhis[:seq] + zhis[seq + 1 :]
    for type_ in ZHI_ATT_DATA[item]:
        flag = False
        if type_ not in ("害", "会"):
            continue
        for zhi in ZHI_ATT_DATA[item][type_]:
            if zhi in others:
                if not flag:
                    output = output + "　" + type_ + "："
                    flag = True
                output += zhi
    output = output.lstrip("　")
    print("\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), output), end="")

print()
for seq, item in enumerate(zhus):
    # 检查空亡
    result = "{}－{}".format(NAYINS[item], "亡") if zhis[seq] == WANG_DATA[zhis[0]] else NAYINS[item]
    # 检查劫杀
    result = "{}－{}".format(result, "劫杀") if zhis[seq] == JIE_SHA_DATA[zhis[0]] else result
    # 检查元辰
    result = (
        "{}－{}".format(result, "元辰")
        if zhis[seq] == EARTHLY_BRANCHES[(EARTHLY_BRANCHES.index(zhis[0]) + direction * -1 * 5) % 12]
        else result
    )
    print("{1:{0}<15s}".format(chr(12288), result), end="")

print()
print("-" * 120)


children = ["食", "伤"] if options.n else ["官", "杀"]

liuqins = bidict(
    {
        "才": "婆婆" if options.n else "父亲",
        "财": "父亲" if options.n else "妻子",
        "印": "女婿" if options.n else "母亲",
        "枭": "母亲" if options.n else "祖父",
        "官": "丈夫" if options.n else "女儿",
        "杀": "情夫" if options.n else "儿子",
        "劫": "兄弟" if options.n else "姐妹",
        "比": "姐妹" if options.n else "兄弟",
        "食": "女儿" if options.n else "下属",
        "伤": "儿子" if options.n else "孙女",
    }
)

# 六亲分析
for item in HEAVENLY_STEMS:
    print(
        "{}:{} {}-{} {} {} {}".format(
            item,
            TEN_DEITIES[me][item],
            liuqins[TEN_DEITIES[me][item]],
            TEN_DEITIES[item][zhis[0]],
            TEN_DEITIES[item][zhis[1]],
            TEN_DEITIES[item][zhis[2]],
            TEN_DEITIES[item][zhis[3]],
        ),
        end="  ",
    )
    if HEAVENLY_STEMS.index(item) == 4:
        print()

print()
print()

# 计算上运时间，有年份时才适用

temps_scores = (
    TEMP_DATA[gans.year]
    + TEMP_DATA[gans.month]
    + TEMP_DATA[me]
    + TEMP_DATA[gans.time]
    + TEMP_DATA[zhis.year]
    + TEMP_DATA[zhis.month] * 2
    + TEMP_DATA[zhis.day]
    + TEMP_DATA[zhis.time]
)
print("\033[1;36;40m五行分数", scores, "  八字强弱：", strong, "通常>29为强，需要参考月份、坐支等", "weak:", weak)


print("湿度分数", temps_scores, "正为暖燥，负为寒湿，正常区间[-6,6] 拱库气：", get_gong_kus(zhis), "\033[0m")
for item in gan_scores:
    print("{}[{}]-{} ".format(item, TEN_DEITIES[me][item], gan_scores[item]), end="  ")
print()
print("-" * 120)

print("\n\n大运")
print("=" * 120)
if options.b:
    print(dayuns)
else:
    birthday = datetime.date(day.getSolarYear(), day.getSolarMonth(), day.getSolarDay())
    count = 0

    for i in range(30):
        # print(birthday)
        day_ = sxtwl.fromSolar(birthday.year, birthday.month, birthday.day)
        # if day_.hasJieQi() and day_.getJieQiJD() % 2 == 1
        if day_.hasJieQi() and day_.getJieQi() % 2 == 1:
            break
        # break
        birthday += datetime.timedelta(days=direction)
        count += 1

    ages = [
        (round(count / 3 + 10 * i), round(int(options.year) + 10 * i + count // 3))
        for i in range(12)
    ]

    for (seq, value) in enumerate(ages):
        gan_ = dayuns[seq][0]
        zhi_ = dayuns[seq][1]
        fu = "*" if (gan_, zhi_) in zhus else " "
        zhi5_ = ""
        for gan in ZHI_5_DATA[zhi_]:
            zhi5_ = zhi5_ + "{}{}{}　".format(gan, GAN_5[gan], TEN_DEITIES[me][gan])

        zhi__ = set()  # 大运地支关系

        for item in zhis:

            for type_ in ZHI_ATT_DATA[zhi_]:
                if item in ZHI_ATT_DATA[zhi_][type_]:
                    zhi__.add(type_ + ":" + item)
        zhi__ = "  ".join(zhi__)

        empty = chr(12288)
        if zhi_ in EMPTIES[zhus[2]]:
            empty = "空"

        out = "{1:<4d}{2:<5s}{3} {14} {13}\t{4}:{5}{8}{6:{0}<6s}{12}{7}{8}{9} - {10:{0}<15s} {11}".format(
            chr(12288),
            int(value[0]),
            "",
            dayuns[seq],
            TEN_DEITIES[me][gan_],
            gan_,
            check_gan(gan_, gans),
            zhi_,
            yinyang(zhi_),
            TEN_DEITIES[me][zhi_],
            zhi5_,
            zhi__,
            empty,
            fu,
            NAYINS[(gan_, zhi_)],
        )
        gan_index = HEAVENLY_STEMS.index(gan_)
        zhi_index = EARTHLY_BRANCHES.index(zhi_)
        print(out)
        zhis2 = list(zhis) + [zhi_]
        gans2 = list(gans) + [gan_]
        if value[0] > 100:
            continue
        for i in range(10):
            day2 = sxtwl.fromSolar(value[1] + i, 5, 1)
            yTG = day2.getYearGZ()
            gan2_ = HEAVENLY_STEMS[yTG.tg]
            zhi2_ = EARTHLY_BRANCHES[yTG.dz]
            fu2 = "*" if (gan2_, zhi2_) in zhus else " "
            # print(fu2, (gan2_, zhi2_),zhus)

            zhi6_ = ""
            for gan in ZHI_5_DATA[zhi2_]:
                zhi6_ = zhi6_ + "{}{}{}　".format(gan, GAN_5[gan], TEN_DEITIES[me][gan])

            # 大运地支关系
            zhi__ = set()  # 大运地支关系
            for item in zhis2:

                for type_ in ZHI_ATT_DATA[zhi2_]:
                    if type_ == "破":
                        continue
                    if item in ZHI_ATT_DATA[zhi2_][type_]:
                        zhi__.add(type_ + ":" + item)
            zhi__ = "  ".join(zhi__)

            empty = chr(12288)
            if zhi2_ in EMPTIES[zhus[2]]:
                empty = "空"
            out = "{1:>3d} {2:<5d}{3} {14} {13}\t{4}:{5}{8}{6:{0}<6s}{12}{7}{8}{9} - {10:{0}<15s} {11}".format(
                chr(12288),
                int(value[0]) + i,
                value[1] + i,
                gan2_ + zhi2_,
                TEN_DEITIES[me][gan2_],
                gan2_,
                check_gan(gan2_, gans2),
                zhi2_,
                yinyang(zhi2_),
                TEN_DEITIES[me][zhi2_],
                zhi6_,
                zhi__,
                empty,
                fu2,
                NAYINS[(gan2_, zhi2_)],
            )
            print(out)

    print(count / 3)
    # print(list(zip(ages, dayuns)))

    # 计算星宿
    d2 = datetime.date(1, 1, 4)
    print("星宿", INDEX_CONSTELLATION_TUPLE[(birthday - d2).days % 28], end=" ")

    # 计算建除
    seq = 12 - EARTHLY_BRANCHES.index(zhis.month)
    print(INDEX_JIAN_CHU_TUPLE[(EARTHLY_BRANCHES.index(zhis.day) + seq) % 12])

# 检查三会 三合的拱合
result = ""
# for i in range(2):
# result += check_gong(zhis, i*2, i*2+1, me, GONG_HE_DATA)
# result += check_gong(zhis, i*2, i*2+1, me, GONG_HUI_DATA, '三会拱')

result += check_gong(zhis, 1, 2, me, GONG_HE_DATA)
result += check_gong(zhis, 1, 2, me, GONG_HUI_DATA, "三会拱")

if result:
    print(result)

print("=" * 120)


# 格局分析
ge = ""
if (me, zhis.month) in JIAN_LU_DATA:
    print(JIANLU_DESC_DATA)
    print("-" * 120)
    print(JIAN_LU_DATA[(me, zhis.month)])
    print("-" * 120 + "\n")
    ge = "建"
# elif (me == '丙' and ('丙','申') in zhus) or (me == '甲' and ('己','巳') in zhus):
# print("格局：专财. 运行官旺 财神不背,大发财官。忌行伤官、劫财、冲刑、破禄之运。喜身财俱旺")
elif (me, zhis.month) in (("甲", "卯"), ("庚", "酉"), ("壬", "子")):
    ge = "月刃"
else:
    zhi = zhis[1]
    if zhi in WU_HANG_DATA["土"] or (me, zhis.month) in (
        ("乙", "寅"),
        ("丙", "午"),
        ("丁", "巳"),
        ("戊", "午"),
        ("己", "巳"),
        ("辛", "申"),
        ("癸", "亥"),
    ):
        for item in ZHI_5_DATA[zhi]:
            if item in gans[:2] + gans[3:]:
                ge = TEN_DEITIES[me][item]
    else:
        d = ZHI_5_DATA[zhi]
        ge = TEN_DEITIES[me][max(d, key=d.get)]
print("格局:", ge, "\t", end=" ")

# 天乙贵人
flag = False
for items in TIAN_YI_DATA[me]:
    for item in items:
        if item in zhis:
            if not flag:
                print("| 天乙贵人：", end=" ")
                flag = True
            print(item, end=" ")

# 玉堂贵人
flag = False
for items in YU_TANG_DATA[me]:
    for item in items:
        if item in zhis:
            if not flag:
                print("| 玉堂贵人：", end=" ")
                flag = True
            print(item, end=" ")

# 天德贵人
if TIAN_DE_DATA[month] in alls:
    print("| 天德贵人：{}".format(TIAN_DE_DATA[month]), end=" ")

# 月德贵人
if YUE_DE_DATA[month] in zhis:
    print("| 月德贵人：{}".format(YUE_DE_DATA[month]), end=" ")

# 驿马
if MAS_DATA[zhis.day] in zhis:
    for seq, item in enumerate(zhis):
        if item == MAS_DATA[zhis.day]:
            print(MA_ZHU_DATA[zhus[seq]], zhus[seq])

# 天罗
if NAYINS[zhus[0]][-1] == "火":
    if zhis.day in "戌亥":
        print("| 天罗：{}".format(zhis.day), end=" ")

# 地网
if NAYINS[zhus[0]][-1] in "水土":
    if zhis.day in "辰巳":
        print("| 地网：{}".format(zhis.day), end=" ")

# 三奇
flag = False
if ["乙", "丙", "丁"] == list(gans[:3]) or ["乙", "丙", "丁"] == list(gans[1:]):
    flag = True
    print("三奇　乙丙丁", end=" ")
if ["甲", "戊", "庚"] == list(gans[:3]) or ["甲", "戊", "庚"] == list(gans[1:]):
    flag = True
    print("三奇　甲戊庚", end=" ")
if ["辛", "壬", "癸"] == list(zhis[:3]) or ["辛", "壬", "癸"] == list(zhis[1:]):
    flag = True
    print("三奇　辛壬癸", end=" ")


# 学堂分析
for seq, item in enumerate(statuses):
    if item == "长":
        print("学堂:", zhis[seq], "\t", end=" ")
        if NAYINS[zhus[seq]][-1] == TEN_DEITIES[me]["本"]:
            print("正学堂:", NAYINS[zhus[seq]], "\t", end=" ")


# xuetang = XUE_TANG_DATA[TEN_DEITIES[me]['本']][1]
# if xuetang in zhis:
# print("学堂:", xuetang, "\t\t", end=' ')
# if XUE_TANG_DATA[TEN_DEITIES[me]['本']] in zhus:
# print("正学堂:", XUE_TANG_DATA[TEN_DEITIES[me]['本']], "\t\t", end=' ')

# 学堂分析

for seq, item in enumerate(statuses):
    if item == "建":
        print("| 词馆:", zhis[seq], end=" ")
        if NAYINS[zhus[seq]][-1] == TEN_DEITIES[me]["本"]:
            print("- 正词馆:", NAYINS[zhus[seq]], end=" ")


ku = TEN_DEITIES[me]["库"][0]
if ku in zhis:
    print("库：", ku, end=" ")

    for item in zhus:
        if ku != zhus[1]:
            continue
        if NAYINS[item][-1] == TEN_DEITIES[me]["克"]:
            print("库中有财，其人必丰厚")
        if NAYINS[item][-1] == TEN_DEITIES[me]["被克"]:
            print(item, TEN_DEITIES[me]["被克"])
            print("绝处无依，其人必滞")

print()

# 天元分析
for item in ZHI_5_DATA[zhis[2]]:
    name = TEN_DEITIES[me][item]
    print(SELF_ZUO_DATA[name])
print("-" * 120)


# 出身分析
cai = TEN_DEITIES[me].inverse["财"]
guan = TEN_DEITIES[me].inverse["官"]
births = tuple(gans[:2])
if cai in births and guan in births:
    birth = "不错"
# elif cai in births or guan in births:
# birth = '较好'
else:
    birth = "一般"

print("出身:", birth)

guan_num = shens.count("官")
sha_num = shens.count("杀")
cai_num = shens.count("财")
piancai_num = shens.count("才")
jie_num = shens.count("劫")
bi_num = shens.count("比")
yin_num = shens.count("印")


# 食神分析
if ge == "食":
    print("\n****食神分析****: 格要日主食神俱生旺，无冲破。有财辅助财有用。  食神可生偏财、克杀")
    print(" 阳日食神暗官星，阴日食神暗正印。食神格人聪明、乐观、优雅、多才多艺。食居先，煞居后，功名显达。")
    print("======================================")
    print(
        """
    喜:身旺 宜行财乡 逢食看财  忌:身弱 比 倒食(偏印)  一名进神　　二名爵星　　三名寿星
    月令建禄最佳，时禄次之，更逢贵人运
    """
    )

    shi_num = shens.count("食")
    if shi_num > 2:
        print("食神过多:食神重见，变为伤官，令人少子，纵有，或带破拗性. 行印运", end=" ")
    if set(("财", "食")) in set(gan_shens[:2] + zhi_shens[:2]):
        print("祖父荫业丰隆", end=" ")
    if set(("财", "食")) in set(gan_shens[2:] + zhi_shens[2:]):
        print("妻男获福，怕母子俱衰绝，两皆无成", end=" ")
    if cai_num > 1:
        print("财多则不清，富而已", end=" ")

    for seq, item in enumerate(gan_shens):
        if item == "食":
            if TEN_DEITIES[gans[seq]][zhis[seq]] == "墓":
                print("食入墓，即是伤官入墓，住寿难延。")

    for seq, item in enumerate(gan_shens):
        if item == "食" or zhi_shens[seq] == "食":
            if get_empty(zhus[2], zhis[seq]):
                print("大忌空亡，更有官煞显露，为太医师巫术数九流之士，若食神逢克，又遇空亡，则不贵，再行死绝或枭运，则因食上气上生灾，翻胃噎食，缺衣食，忍饥寒而已")

    # 倒食分析
    if "枭" in shens and (me not in ["庚", "辛", "壬"]) and TEN_DEITIES[me] != "建":
        flag = True
        for item in ZHI_5_DATA[zhis.day]:
            if TEN_DEITIES[me]["合"] == item:
                flag = False
                break
        if flag:
            print("倒食:凡命带倒食，福薄寿夭，若有制合没事，主要为地支为天干的杀;日支或者偏印的坐支为日主的建禄状态。偏印和日支的主要成分天干合")
            print("凡命有食遇枭，犹尊长之制我，不得自由，作事进退悔懒，有始无终，财源屡成屡败，容貌欹斜，身品琐小，胆怯心虚，凡事无成，克害六亲，幼时克母，长大伤妻子")
            print("身旺遇此方为福")
    print()
    print("-" * 120)

# 伤官分析
if ge == "伤":
    print("\n****伤官分析****: 喜:身旺,财星,印绶,伤尽 忌:身弱,无财,刑冲,入墓枭印　")
    print(" 多材艺，傲物气高，心险无忌惮，多谋少遂，弄巧成拙，常以天下之人不如己，而人亦惮之、恶之。 一名剥官神　　二名羊刃煞")
    print(" 身旺用财，身弱用印。用印不忌讳官煞。用印者须去财方能发福")
    print("官星隐显，伤之不尽，岁运再见官星，官来乘旺，再见刑冲破害，刃煞克身，身弱财旺，必主徒流死亡，五行有救，亦残疾。若四柱无官而遇伤煞重者，运入官乡，岁君又遇，若不目疾，必主灾破。")
    print("娇贵伤不起、谨慎过头了略显胆小，节俭近于吝啬")
    print("======================================")

    if "财" in shens or "才" in shens:
        print("伤官生财")
    else:
        print("伤官无财，主贫穷")

    if "印" in shens or "枭" in shens:
        print("印能制伤，所以为贵，反要伤官旺，身稍弱，始为秀气;印旺极深，不必多见，偏正叠出，反为不秀，故伤轻身重而印绶多见，贫穷之格也。")
        if "财" in shens or "才" in shens:
            print("财印相克，本不并用，只要干头两清而不相碍；又必生财者，财太旺而带印，佩印者印太重而带财，调停中和，遂为贵格")
    if "官" in shens:
        print(SHANG_GUAN_DATA[TEN_DEITIES[me]["本"]])
        print("金水独宜，然要财印为辅，不可伤官并透。若冬金用官，而又化伤为财，则尤为极秀极贵。若孤官无辅，或官伤并透，则发福不大矣。")
    if "杀" in shens:
        print("煞因伤而有制，两得其宜，只要无财，便为贵格")
    if gan_shens[0] == "伤":
        print("年干伤官最重，谓之福基受伤，终身不可除去，若月支更有，甚于伤身七煞")

    for seq, item in enumerate(gan_shens):
        if item == "伤":
            if TEN_DEITIES[gans[seq]][zhis[seq]] == "墓":
                print("食入墓，即是伤官入墓，住寿难延。")

    for seq, item in enumerate(gan_shens):
        if item == "食" or zhi_shens[seq] == "食":
            if get_empty(zhus[2], zhis[seq]):
                print("大忌空亡，更有官煞显露，为太医师巫术数九流之士，若食神逢克，又遇空亡，则不贵，再行死绝或枭运，则因食上气上生灾，翻胃噎食，缺衣食，忍饥寒而已")
    print()
    print("-" * 120)

# 劫财分析
if ge == "劫":
    print("\n****劫财(阳刃)分析****：阳刃冲合岁君,勃然祸至。身弱不作凶。")
    print("======================================")
    if "劫" == gan_shens[3] or "劫" == zhi_shens[3]:
        print("劫财阳刃,切忌时逢,岁运并临,灾殃立至,独阳刃以时言,重于年月日也。")

    shi_num = shens.count("食")
    print("-" * 120)

# 财分析

if ge == "财" or ge == "才":
    print("\n****财分析 **** 喜:旺,印,食,官 忌:比 羊刃 空绝 冲合   财星,天马星,催官星,壮志神")
    if gan_shens.count("财") + gan_shens.count("才") > 1:
        print("财喜根深，不宜太露，然透一位以清用，格所最喜，不为之露。即非月令用神，若寅透乙、卯透甲之类，一亦不为过，太多则露矣。")
        print("财旺生官，露亦不忌，盖露不忌，盖露以防劫，生官则劫退，譬如府库钱粮，有官守护，即使露白，谁敢劫之？")
    if "伤" in gan_shens:
        print("有伤官，财不能生官")
    if "食" in shens:
        print("有财用食生者，身强而不露官，略带一位比劫，益觉有情")
        if "印" in shens or "枭" in "shens":
            print("注意印食冲突")
    if "比" in shens:
        print("比不吉，但是伤官食神可化!")
    if "杀" in shens:
        print("不论合煞制煞，运喜食伤身旺之方!")

    if "财" == zhi_shens[0]:
        print("岁带正马：月令有财或伤食，不犯刑冲分夺，旺祖业丰厚。同类月令且带比，或遇运行伤劫 贫")
    if "财" == zhi_shens[3]:
        print("时带正马：无冲刑破劫，主招美妻，得外来财物，生子荣贵，财产丰厚，此非父母之财，乃身外之财，招来产业，宜俭不宜奢。")
    if "财" == zhi_shens[2] and (me not in ("壬", "癸")):
        print("天元坐财：喜印食 畏官煞，喜月令旺 ")
    if ("官" not in shens) and ("伤" not in shens) and ("食" not in shens):
        print("财旺生官:若月令财无损克，亦主登科")

    if (
        cai_num > 2
        and ("劫" not in shens)
        and ("比" not in shens)
        and ("比" not in shens)
        and ("印" not in shens)
    ):
        print("财　不重叠多见　财多身弱，柱无印助; 若财多身弱，柱无印助不为福。")

    if "印" in shens:
        print("先财后印，反成其福，先印后财，反成其辱是也?")
    if "官" in gan_shens:
        print("官星显露，别无伤损，或更食生印助日主健旺，富贵双全")
    if "财" in gan_shens and (("劫" not in shens) and ("比" not in shens)):
        print("财不宜明露")
    for seq, item in enumerate(gan_shens):
        if item == "财":
            if TEN_DEITIES[gans[seq]][zhis[seq]] == "墓":
                print("财星入墓，必定刑妻")
            if TEN_DEITIES[gans[seq]][zhis[seq]] == "长":
                print("财遇长生，田园万顷")

    if ("官" not in shens) and (("劫" in shens) or ("比" in shens)):
        print("切忌有姊妹兄弟分夺，柱无官星，祸患百出。")

    if bi_num + jie_num > 1:
        print("兄弟辈出: 纵入官乡，发福必渺.")

    for seq, item in enumerate(zhi_shens):
        if item == "才" or TEN_DEITIES[me][zhis[seq]] == "才":
            if get_empty(zhus[2], zhis[seq]):
                print("空亡 官将不成，财将不住")

    print("-" * 120)

# 财库分析
if TEN_DEITIES[TEN_DEITIES[me].inverse["财"]]["库"][-1] in zhis:
    print("财临库墓: 一生财帛丰厚，因财致官, 天干透土更佳")
if cai_num < 2 and (("劫" in shens) or ("比" in shens)):
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
    if "财" in shens or "才" in shens:
        print("有财辅助")
    if "印" in shens or "枭" in shens:
        print("有印辅助　正官带伤食而用印制，运喜官旺印旺之乡，财运切忌。若印绶叠出，财运亦无害矣。")
    if "食" in shens:
        print("又曰凡论官星，略见一位食神坐实，便能损局，有杀则无妨。惟月令隐禄，见食却为三奇之贵。因为食神和官相合。")
    if "伤" in shens:
        print("伤官需要印或偏印来抑制，　有杀也无妨")
    if "杀" in shens:
        print("伤官需要印或偏印来抑制。用劫合煞，则财运可行，伤食可行，身旺，印绶亦可行，只不过复露七煞。若命用伤官合煞，则伤食与财俱可行，而不宜逢印矣。")

    if zhi_shens[2] in ("财", "印"):
        print("凡用官，日干自坐财印，终显")
    if zhi_shens[2] in ("伤", "杀"):
        print("自坐伤、煞，终有节病")

    # 检查天福贵人
    if (guan, TEN_DEITIES[guan].inverse["建"]) in zhus:
        print("天福贵人:主科名巍峨，官职尊崇，多掌丝纶文翰之美!")

    # 天元坐禄
    if guan in ZHI_5_DATA[zhis[2]]:
        print("天元作禄: 日主与官星并旺,才是贵命。大多不贵即富,即使是命局中有缺点,行到好的大运时,便能一发如雷。")
        print(TIAN_YUAN_DATA[TEN_DEITIES[me]["本"]])

    # 岁德正官
    if gan_shens[0] == "官" or zhi_shens[0] == "官":
        print("岁德正官: 必生宦族,或荫袭祖父之职,若月居财官分野,运向财官旺地,日主健旺,贵无疑矣。凡年干遇官,福气最重,发达必早。")

    # 时上正官
    if gan_shens[0] == "官" or zhi_shens[0] == "官":
        print("时上正官: 正官有用不须多，多则伤身少则和，日旺再逢生印绶，定须平步擢高科。")

    print()
    print("-" * 120)
# 官库分析
if TEN_DEITIES[TEN_DEITIES[me].inverse["官"]]["库"][-1] in zhis:
    print("官临库墓")
    if LU_KU_CAI_DATA[me] in zhis:
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
        if "财" in shens or "印" in shens or "才" in shens or "枭" in shens:
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
    if "官" in shens:
        print("官煞混杂：身弱多夭贫")

    for seq, item in enumerate(gan_shens):
        if item == "杀":
            if TEN_DEITIES[gans[seq]][zhis[seq]] == "长":
                print("七煞遇长生乙位，女招贵夫。")
    print()
    print("-" * 120)

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
    print("-" * 120)

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
    print("-" * 120)


gan_ = tuple(gans)
for item in HEAVENLY_STEMS:
    if gan_.count(item) == 3:
        print("三字干：", item, "--", GAN_3[item])
        break

gan_ = tuple(gans)
for item in HEAVENLY_STEMS:
    if gan_.count(item) == 4:
        print("四字干：", item, "--", GAN_4[item])
        break

zhi_ = tuple(zhis)
for item in EARTHLY_BRANCHES:
    if zhi_.count(item) > 2:
        print("三字支：", item, "--", ZHI_3[item])
        break

print("=" * 120)
print("你属:", me, "特点：--", GAN_DESC_DATA[me], "\n")
print("年份:", zhis[0], "特点：--", ZHI_DESC_DATA[zhis[0]], "\n")


# 羊刃分析
key = "帝" if HEAVENLY_STEMS.index(me) % 2 == 0 else "冠"

if TEN_DEITIES[me].inverse[key] in zhis:
    print("\n羊刃:", me, TEN_DEITIES[me].inverse[key])
    print("======================参考：https://www.jianshu.com/p/c503f7b3ed04")
    if TEN_DEITIES[me].inverse["冠"]:
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
        tmp_list.append((me_zhi, "子"))
elif me_zhi in ("丑", "巳", "酉"):
    if "酉" in other_zhis:
        flag = True
        tmp_list.append((me_zhi, "酉"))
elif me_zhi in ("寅", "午", "戌"):
    if "午" in other_zhis:
        flag = True
        tmp_list.append((me_zhi, "午"))
elif me_zhi in ("亥", "卯", "未"):
    if "卯" in other_zhis:
        flag = True
        tmp_list.append((me_zhi, "卯"))

if flag:
    print("\n\n将星: 常欲吉星相扶，贵煞加临乃为吉庆。")
    print("=========================")
    print(
        """理愚歌》云：将星若用亡神临，为国栋梁臣。言吉助之为贵，更夹贵库墓纯粹而
    不杂者，出将入相之格也，带华盖、正印而不夹库，两府之格也；只带库墓而带正印，员郎
    以上，既不带墓又不带正印，止有华盖，常调之禄也；带华印而正建驿马，名曰节印，主旌节
    之贵；若岁干库同库为两重福，主大贵。"""
    )
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
    print(
        """《理愚歌》云：华盖虽吉亦有妨，或为孽子或孤孀。填房入赘多阙口，炉钳顶笠拔缁黄。
    又云：华盖星辰兄弟寡，天上孤高之宿也；生来若在时与胎，便是过房庶出者。"""
    )


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
    print(
        """一名败神，一名桃花煞，其神之奸邪淫鄙，如生旺则美容仪，耽酒色，疏财好欢，
    破散家业，唯务贪淫；如死绝，落魄不检，言行狡诈，游荡赌博，忘恩失信，私滥奸淫，
    靡所不为；与元辰并，更临生旺者，多得匪人为妻；与贵人建禄并，多因油盐酒货得生，
    或因妇人暗昧之财起家，平生有水厄、痨瘵之疾，累遭遗失暗昧之灾。此人入命，有破无成，
    非为吉兆，妇人尤忌之。
    咸池非吉煞，日时与水命遇之尤凶。"""
    )
    print(taohuas, zhis)

# 禄分析
flag = False
for item in zhus:
    if item in LU_TYPES[me]:
        if not flag:
            print("\n\n禄分析:")
            print("=========================")
        print(item, LU_TYPES[me][item])


# 文昌贵人
if WEN_CHANG[me] in zhis:
    print("文昌贵人: ", me, WEN_CHANG[me])

# 文星贵人
if WEN_XING[me] in zhis:
    print("文星贵人: ", me, WEN_XING[me])

# 天印贵人
if TIAN_YIN[me] in zhis:
    print("天印贵人: 此号天印贵，荣达受皇封", me, TIAN_YIN[me])


short = min(scores, key=scores.get)
print("\n\n五行缺{}的建议参见 http://t.cn/E6zwOMq".format(short))

sum_index = "".join([me, "日", *zhus[3]])
if sum_index in SUMMARY_DATA:
    print("\n\n命")
    print("=========================")
    print(SUMMARY_DATA[sum_index])


print("======================================")
if "杀" in shens:
    if yinyang(me) == "+":
        print("阳杀:话多,热情外向,异性缘好")
    else:
        print("阴杀:话少,性格柔和")
if "印" in shens and "才" in shens and "官" in shens:
    print("印,偏财,官:三奇 怕正财")
if "才" in shens and "杀" in shens:
    print("男:因女致祸、因色致祸; 女:赔货")

if "才" in shens and "枭" in shens:
    print("偏印因偏财而不懒！")
