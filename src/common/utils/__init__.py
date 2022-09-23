from common.const import TEN_DEITIES, HEAVENLY_STEMS, EARTHLY_BRANCHES, EMPTIES, ZHI_5_DATA, GAN_5


def check_gan(gan, gans):
    result = ""
    if TEN_DEITIES[gan]["合"] in gans:
        result += "合" + TEN_DEITIES[gan]["合"]
    if TEN_DEITIES[gan]["冲"] in gans:
        result += "冲" + TEN_DEITIES[gan]["冲"]
    return result


def yinyang(item):
    if item in HEAVENLY_STEMS:
        return "＋" if HEAVENLY_STEMS.index(item) % 2 == 0 else "－"
    else:
        return "＋" if EARTHLY_BRANCHES.index(item) % 2 == 0 else "－"


def get_empty(zhu, zhi):
    empty = EMPTIES[zhu]
    if zhi in empty:
        return "空"
    return ""


def get_zhi_detail(zhi, me, multi=1):
    out = ""
    for gan in ZHI_5_DATA[zhi]:
        out = f"{out}{gan}{GAN_5[gan]}{ZHI_5_DATA[zhi][gan] * multi}{TEN_DEITIES[me][gan]} "
    return out


def check_gong(zhis, n1, n2, me, hes, desc="三合拱"):
    result = ""
    if zhis[n1] + zhis[n2] in hes:
        gong = hes[zhis[n1] + zhis[n2]]
        if gong not in zhis:
            result += "\t{}：{}{}-{}[{}]".format(
                desc, zhis[n1], zhis[n2], gong, get_zhi_detail(gong, me)
            )
    return result
