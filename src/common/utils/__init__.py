from common.const import EARTHLY_BRANCHES, EMPTIES, GAN_5, HEAVENLY_STEMS, TEN_DEITIES, ZHI_5_DATA


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
            value = EARTHLY_BRANCHES[
                (EARTHLY_BRANCHES.index(zhi1) + EARTHLY_BRANCHES.index(zhi2)) // 2
            ]
            if value in ("丑", "辰", "未", "戌"):
                result.append(value)
    return result
