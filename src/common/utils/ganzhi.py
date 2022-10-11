#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 钉钉或微信pythontesting 钉钉群21734177 技术支持qq群：630011153 144081101
# CreateDate: 2019-2-21

import sxtwl

from common.const import GAN, ZHI


def get_gan_zhi(gz_str: str) -> sxtwl.GZ:
    tg = next((i for i, v in enumerate(GAN) if gz_str[0] == v), -1)
    dz = next((i for i, v in enumerate(ZHI) if gz_str[1] == v), -1)
    return sxtwl.GZ(tg, dz)
