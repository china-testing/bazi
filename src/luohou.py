#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 钉钉或微信pythontesting 钉钉群21734177 技术支持qq群：630011153 144081101
# 代码地址 https://github.com/china-testing/python-api-tesing/blob/master/bazi/luohou.py
# 鸣谢 https://github.com/yuangu/sxtwl_cpp/tree/master/python
# CreateDate: 2019-2-21

import argparse
import datetime

import sxtwl

from common.const import (
    GAN,
    GAN_S_YEAR_MONTH_DAY,
    JI_HOUR_DATA,
    JIS,
    RMCS,
    SHI_HOUR_DATA,
    YEAR_HOUR_DATA,
    YMCS,
    YUE_DATAS,
    YUE_HOUR_DATA,
    ZHI,
    ZHI_S_YEAR_MONTH_DAY,
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


if options.d:
    year, month, day = options.d.split()
    date = datetime.date(int(year), int(month), int(day))
else:
    date = datetime.datetime.now()


def get_hou(datetime_date: datetime.date) -> None:
    cal_day = sxtwl.fromSolar(datetime_date.year, datetime_date.month, datetime_date.day)
    # 以立春为界的天干地支
    y_tg = cal_day.getYearGZ()
    m_tg = cal_day.getMonthGZ()
    d_tg = cal_day.getDayGZ()
    solar_month = YUE_DATAS[cal_day.getLunarMonth() - 1]

    # 　计算甲干相合
    gans = GAN_S_YEAR_MONTH_DAY(
        year=GAN[y_tg.tg],
        month=GAN[m_tg.tg],
        day=GAN[d_tg.tg],
    )
    zhis = ZHI_S_YEAR_MONTH_DAY(
        year=ZHI[y_tg.dz],
        month=ZHI[m_tg.dz],
        day=ZHI[d_tg.dz],
    )
    print(f"公历:{cal_day.getSolarYear()}年{cal_day.getSolarMonth()}月{cal_day.getSolarDay()}日", end="")
    print(
        f"\t农历:{cal_day.getLunarYear(False)}年{'闰' if cal_day.isLunarLeap() else ''}{solar_month}月{RMCS[cal_day.getLunarDay()-1]}日",
        end="",
    )
    print(" \t", end="")
    print("-".join(["".join(item) for item in zip(gans, zhis)]), end="")

    print("\t杀师时:", end="")
    for item in SHI_HOUR_DATA[zhis[2]]:
        print(item + ZHI_TIME_DATA[item], end="")

    day_ganzhi = gans[2] + zhis[2]

    if day_ganzhi == YEAR_HOUR_DATA[zhis[0]]:
        print(" \t年猴:{}年{}日".format(zhis[0], day_ganzhi), end=" ")

    if zhis[2] == YUE_HOUR_DATA[solar_month]:
        print(" \t月罗:{}日".format(zhis[2]), end=" ")

    if day_ganzhi in tuple(JI_HOUR_DATA.values()):
        birthday = date
        ji = None
        for _ in range(30):
            day_ = sxtwl.fromSolar(birthday.year, birthday.month, birthday.day)
            if day_.hasJieQi():
                ji = JIS[(day_.getJieQi() + 3) // 6]
                break
            birthday += datetime.timedelta(days=-1)

        if ji and day_ganzhi == JI_HOUR_DATA[ji]:
            print(" \t季猴:{}季{}日".format(ji, JI_HOUR_DATA[ji]), end=" ")
    print()


get_hou(date)

for i in range(1, options.n):
    d_ = date + datetime.timedelta(days=i)
    get_hou(d_)
