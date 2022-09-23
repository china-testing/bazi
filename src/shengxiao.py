#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 钉钉或微信pythontesting 钉钉群21734177 技术支持qq群：630011153 144081101
# CreateDate: 2019-2-21

import argparse
import logging

from common.const import SHENG_XIAO_DATA, ZHI_ATT_DATA

logger = logging.getLogger(__name__)


def output(des, key):
    logger.info()
    logger.info(des, end="")
    for item in ZHI_ATT_DATA[zhi][key]:
        logger.info(SHENG_XIAO_DATA[item], end="")


description = """
"""
parser = argparse.ArgumentParser(
    description=description, formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("shengxiao", action="store", help="生肖")
parser.add_argument(
    "--version", action="version", version="%(prog)s 0.1 Rongzhong xu 2019 03 06 钉钉或微信pythontesting"
)
options = parser.parse_args()

if options.shengxiao not in SHENG_XIAO_DATA.inverse:
    logger.info("请输入正确的生肖：")
    logger.info(SHENG_XIAO_DATA.inverse.keys())
else:
    logger.info("你的生肖是：", options.shengxiao)
    zhi = SHENG_XIAO_DATA.inverse[options.shengxiao]
    logger.info("你的年支是：", zhi)
    logger.info("=" * 80)
    logger.info("合生肖是合八字的一小部分，有一定参考意义，但是不是全部。")
    logger.info("合婚请以八字为准，技术支持：钉钉或微信pythontesting")
    logger.info("以下为相合的生肖：")
    logger.info("=" * 80)
    output("与你三合的生肖：", "合")
    output("与你六合的生肖：", "六")
    output("与你三会的生肖：", "会")
    logger.info()
    logger.info("=" * 80)
    logger.info("以下为不合的生肖：")
    logger.info("=" * 80)
    output("与你相冲的生肖：", "冲")
    output("你刑的生肖：", "刑")
    output("被你刑的生肖：", "被刑")
    output("与你相害的生肖：", "害")
    output("与你相破的生肖：", "破")
    logger.info()
    logger.info("=" * 80)
    logger.info("如果生肖同时在你的合与不合中，则做加减即可。")
    logger.info("比如猪对于虎，有一个相破，有一六合，抵消就为平性。")
