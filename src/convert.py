#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 钉钉或微信pythontesting 钉钉群21734177 技术支持qq群：630011153 144081101
# CreateDate: 2019-2-21

import argparse
import logging
import subprocess

logger = logging.getLogger(__name__)


description = """
"""
parser = argparse.ArgumentParser(
    description=description, formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("gans", action="store", help="天干")
parser.add_argument("zhis", action="store", help="地支")
parser.add_argument(
    "--version", action="version", version="%(prog)s 0.1 Rongzhong xu 2019 4 12 钉钉或微信pythontesting"
)
options = parser.parse_args()

result = ""
for item in zip(options.gans, options.zhis):
    result = result + "".join(item) + " "

# subprocess.call("cls", shell=True)
logger.info(result)
logger.info(subprocess.check_output(f"python bazi.py -b {result}", shell=True).decode("gbk"))
