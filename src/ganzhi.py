#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 钉钉或微信pythontesting 钉钉群21734177 技术支持qq群：630011153 144081101
# CreateDate: 2019-2-21
from collections import OrderedDict

import sxtwl

from common.const import HEAVENLY_STEMS, EARTHLY_BRANCHES


def getGZ(gzStr):
    tg = -1
    dz = -1
    for i, v in enumerate(HEAVENLY_STEMS):
        if gzStr[0] == v:
            tg = i
            break

    for i, v in enumerate(EARTHLY_BRANCHES):
        if gzStr[1] == v:
            dz = i
            break
    return sxtwl.GZ(tg, dz)


