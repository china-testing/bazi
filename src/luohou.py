#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 钉钉或微信pythontesting 钉钉群21734177 技术支持qq群：630011153 144081101
# 代码地址 https://github.com/china-testing/python-api-tesing/blob/master/bazi/luohou.py
# 鸣谢 https://github.com/yuangu/sxtwl_cpp/tree/master/python
# CreateDate: 2019-2-21

import argparse
import collections
import datetime

import sxtwl

from common.const import (
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
    JI_HOUR_DATA,
    JIS,
    RMCS,
    SHI_HOUR_DATA,
    YEAR_HOUR_DATA,
    YMCS,
    YUE_HOUR_DATA,
    ZHI_TIME_DATA,
)

description = """
# 年罗猴日
$ python luohou.py -d "2019 6 16"

"""

parser = argparse.ArgumentParser(
    description=description, formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("-d", action="store", help="year", default="")
parser.add_argument("-n", action="store", help="year", default=32, type=int)
parser.add_argument("--version", action="version", version="%(prog)s 0.1 Rongzhong xu 2019 05 05")
options = parser.parse_args()

GANS = collections.namedtuple("Gans", "year month day")
ZHIS = collections.namedtuple("Zhis", "year month day")

if options.d:
    year, month, day = options.d.split()
    d = datetime.date(int(year), int(month), int(day))
else:
    d = datetime.datetime.now()


def get_hou(d):
    lunar = sxtwl.Lunar()
    cal_day = lunar.getDayBySolar(d.year, d.month, d.day)

    # 　计算甲干相合
    gans = GANS(
        year=HEAVENLY_STEMS[cal_day.Lyear2.tg],
        month=HEAVENLY_STEMS[cal_day.Lmonth2.tg],
        day=HEAVENLY_STEMS[cal_day.Lday2.tg],
    )
    zhis = ZHIS(
        year=EARTHLY_BRANCHES[cal_day.Lyear2.dz],
        month=EARTHLY_BRANCHES[cal_day.Lmonth2.dz],
        day=EARTHLY_BRANCHES[cal_day.Lday2.dz],
    )

    print("公历:", end="")
    print(f"{cal_day.y}年{cal_day.m}月{cal_day.d}日", end="")

    Lleap = "闰" if cal_day.Lleap else ""
    print("\t农历:", end="")
    print(f"{cal_day.Lyear0 + 1984}年{Lleap}{YMCS[cal_day.Lmc]}月{RMCS[cal_day.Ldi]}日  ", end="")

    print(" \t", end="")
    print("-".join(["".join(item) for item in zip(gans, zhis)]), end="")

    print("\t杀师时:", end="")
    for item in SHI_HOUR_DATA[zhis[2]]:
        print(item + ZHI_TIME_DATA[item], end="")

    day_ganzhi = gans[2] + zhis[2]

    if day_ganzhi == YEAR_HOUR_DATA[zhis[0]]:
        print(" \t年猴:{}年{}日".format(zhis[0], day_ganzhi), end=" ")

    if zhis[2] == YUE_HOUR_DATA[YMCS[cal_day.Lmc]]:
        print(" \t月罗:{}日".format(zhis[2]), end=" ")

    if day_ganzhi in tuple(JI_HOUR_DATA.values()):
        birthday = d
        for _ in range(30):
            day_ = sxtwl.Lunar().getDayBySolar(birthday.year, birthday.month, birthday.day)
            if day_.qk != -1:
                ji = JIS[(day_.qk + 3) // 6]
                break
            birthday += datetime.timedelta(days=-1)

        if day_ganzhi == JI_HOUR_DATA[ji]:
            print(" \t季猴:{}季{}日".format(ji, JI_HOUR_DATA[ji]), end=" ")
    print()


get_hou(d)

for i in range(1, options.n):
    d_ = d + datetime.timedelta(days=i)
    get_hou(d_)
