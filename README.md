# 简介

- bazi.py 八字排盘，能比常用的排盘更清晰地显示冲、合、刑等关系，计算五行分数，附加《三命通会》等命理评判
- luohou.py 计算罗喉日时,用于提示风水师何时慎用罗盘。
- shengxiao.py 用户生肖合婚等。

交流钉钉群21734177

软件部署定制技术支持及批八字学八字：微信或钉钉pythontesting

风水远程查看收费888起，实地1888(仅限湖南邵阳、广东深圳东莞等，其他地方需要加差旅费用）起。

# 命理书籍(访问密码: 2274) 点击“普通下载”下面的“立即下载”可浏览器下载

- [三命通会.pdf 文字版本](https://url97.ctfile.com/f/18113597-649595228-10f29e?p=2274) 
- [图解三命通会 第3部论命精要 - 2009.pdf](https://url97.ctfile.com/f/18113597-649699807-d4cd2a?p=2274)
- [图解三命通会 第2部吉凶推断 - 2009.pdf](https://url97.ctfile.com/f/18113597-649699779-b87c3c?p=2274)
- [图解三命通会 第1部 八字神煞 2009 -扫描.pdf](https://url97.ctfile.com/f/18113597-649699750-44b525?p=2274)
- [千里命稿.pdf 古籍图片版本](https://url97.ctfile.com/f/18113597-612723542-319345?p=2274)
- [千里命稿.pdf 文字版本](https://url97.ctfile.com/f/18113597-612723571-e22c74?p=2274)
- [千里命稿.pdf 古籍图片版本](https://url97.ctfile.com/f/18113597-612723542-319345?p=2274)
- [千里命稿.pdf 文字版本](https://url97.ctfile.com/f/18113597-612723571-e22c74?p=2274)
- [朱鹊桥 -鹊桥命理【一】.pdf](https://url97.ctfile.com/f/18113597-723734086-4b23bf?p=2274)
- [朱鹊桥 -鹊桥命理【四】.pdf](https://url97.ctfile.com/f/18113597-723734085-b3d415?p=2274)
- [命运的求索 中国命理学简史及推演方法 (陆致极.pdf ](https://url97.ctfile.com/f/18113597-756319536-0f0ae7?p=2274)
- [中国命理学史论 (陆致极).pdf ](https://url97.ctfile.com/f/18113597-756319535-ef2812?p=2274)
- [八字命理动态分析教程 (陆致极).pdf ](https://url97.ctfile.com/f/18113597-756319531-48e4d9?p=2274)
- [又一种“基因”的探索 (陆致极).pdf ](https://url97.ctfile.com/f/18113597-756319530-dd8028?p=2274)
- [八字命理學進階教程 (陆致极).pdf ](https://url97.ctfile.com/f/18113597-756319525-a897c1?p=2274)
- [梁湘润-星相书简法卷宇册.pdf ](https://url97.ctfile.com/f/18113597-756715812-4ca590?p=2274)
- [梁湘润-星相书简法卷 天册.pdf](https://url97.ctfile.com/f/18113597-756715812-4ca590?p=2274)
- [梁湘润 - 星相书简法卷 黄册.pdf ](https://url97.ctfile.com/f/18113597-756715796-203c11?p=2274)
- [梁湘润 星相书简法卷地册.pdf](https://url97.ctfile.com/f/18113597-756715783-34e1f8?p=2274)

# 安装
- 安裝依赖库

```python
pip install sxtwl bidict lunar_python
```

Windows下如果安装sxtwl报错，安装 [BuildTools_Full.exe](https://url97.ctfile.com/f/18113597-800958828-d3b94d?p=2274) 点击普通下载，不用注册，访问密码: 2274
注意：sxtwl可能不支持python3.11。 Linux下的兼容性会好很多。

- linux打开终端或windows打开cmd或git的bash或powercmd等工具

进入到代码所在目录。


# 使用

- 生肖合婚

```python
$ python shengxiao.py 虎
你的生肖是： 虎
你的年支是： 寅
================================================================================
合生肖是合八字的一小部分，有一定参考意义，但是不是全部。
合婚请以八字为准，技术支持：钉钉或微信pythontesting
以下为相合的生肖：
================================================================================

与你三合的生肖：马狗
与你六合的生肖：猪
与你三会的生肖：兔龙
================================================================================
以下为不合的生肖：
================================================================================

与你相冲的生肖：猴
你刑的生肖：蛇
被你刑的生肖：猴
与你相害的生肖：蛇
与你相破的生肖：猪
================================================================================
如果生肖同时在你的合与不合中，则做加减即可。
比如猪对于虎，有一个相破，有一六合，抵消就为平性。

```


- 计算罗喉日时

```python
$ python luohou.py 
公历:2021年3月23日	农历:2021年二月十一日   	辛丑-辛卯-庚午	杀师时:卯5-7申15-17
公历:2021年3月24日	农历:2021年二月十二日   	辛丑-辛卯-辛未	杀师时:午11-13辰7-9
公历:2021年3月25日	农历:2021年二月十三日   	辛丑-辛卯-壬申	杀师时:戌19-21丑1-3
公历:2021年3月26日	农历:2021年二月十四日   	辛丑-辛卯-癸酉	杀师时:子23-1午11-13
公历:2021年3月27日	农历:2021年二月十五日   	辛丑-辛卯-甲戌	杀师时:卯5-7午11-13 	年猴:丑年甲戌日 
...
```


- 八字排盘

```python

$ python bazi.py -h
usage: bazi.py [-h] [-b] [-g] [-r] [-n] [--version] year month day time

positional arguments:
  year        year
  month       month
  day         day
  time        time

optional arguments:
  -h, --help  show this help message and exit
  -b          直接输入八字
  -g          是否采用公历
  -r          是否为闰月，仅仅使用于农历
  -n          是否为女，默认为男
  --version   show program's version number and exit


# 八字示例

> python .\bazi.py 1977 8 11 19 -n

女命
======================================
公历:   1977年9月23日
lunar_python: 丁巳 己酉 癸未 壬戌
农历:   1977年8月11日 穿=害 上运时间：
------------------------------------------------------------------------------------------------------------------------
墓库： {辰: 水土, 戌: 火土, 丑: 金, 未: 木} 解读:钉ding或v信pythontesting 丁巳 己酉 癸未 壬戌
甲己-中正土  乙庚-仁义金  丙辛-威制水  丁壬-淫慝木  戊癸-无情火   三会: {亥子丑: 水, 寅卯辰: 木, 巳午未: 火, 申酉戌: 金}
========================================================================================================================
丁 己 癸 壬       才 杀 -- 劫       申子辰:水 寅  巳酉丑:金 亥  寅午戌:火 申  亥卯未:木 巳
巳 酉 未 戌       财 枭 杀 官       生：寅申巳亥 败：子午卯酉　库：辰戌丑未    子丑土 寅亥木 卯戌火 酉辰金 申巳水 未午土
------------------------------------------------------------------------------------------------------------------------
　　　　【年】4:5午　　　　　　　【月】-4:-3午　　　　　　　【日】-6:3　　　　　　　【时】-5:4亥|　　　
------------------------------------------------------------------------------------------------------------------------
丁－火【才】合壬冲癸　　　　　己－土【杀】　　　　　　　　　癸－水冲丁　　　　　　　　　　壬＋水【劫】合丁　　　　　　　
巳－胎【帝】　　　　　　　　　酉－病【长】空　　　　　　　　未－墓　　　　　　　　　　　　戌＋衰【冠】　　　　　　　　　
丙火财　戊土官　庚金印　　　　辛金枭　　　　　　　　　　　　己土杀　丁火才　乙木食　　　　戊土官　辛金枭　丁火才　　　　
合：酉　　　　　　　　　　　　合：巳　　　　　　　　　　　　被刑：戌　　　　　　　　　　　　　　　　　　　　　　　　　　
会：未　　　　　　　　　　　　会：戌　害：戌　　　　　　　　会：巳　　　　　　　　　　　　会：酉　害：酉　　　　　　　　
=砂中土　　　　　　　　　　　 ↓大驿土　　　　　　　　　　　 ←杨柳木　　　　　　　　　　　 ←大海水　　　　　　　　　　　
驿马　天乙　　　　　　　　　　 　　　　　　　　　　　　　　　 　　　　　　　　　　　　　　 大耗　　　　　　　　　　　　
------------------------------------------------------------------------------------------------------------------------
调候： 1辛2_丙  ##金不换大运： 调候：喜丙辛 忌癸  大运：喜申未巳午  忌亥子
金不换大运：说明： 丑寅午戌亥有损寿运；子丑辰巳午未亥调候待改进！
格局选用： 食伤生财：    财格：     印格；无用          杀印相生：   官杀：          伤官配印：最佳
月日时支没有财或偏财的禄旺。
月日时支没有官的禄旺。
驿马 : 多迁移、水准与命格相关。女驿马合贵人，终沦落风尘。
大耗 : 意外破损，单独没关系。与桃花或驿马之类同柱则危险。
天乙 : 后天解难、女命不适合多
#################### 女命
------------------------------------------------------------------------------------------------------------------------
甲:伤 儿子-病 胎 墓 养  乙:食 女儿-沐 绝 养 墓  丙:财 父亲-建 死 衰 墓  丁:才 婆婆-帝 长 冠 养  戊:官 丈夫-建 死 衰 墓
己:杀 情夫-帝 长 冠 养  庚:印 女婿-长 帝 冠 衰  辛:枭 母亲-死 建 衰 冠  壬:劫 兄弟-绝 沐 养 冠  癸:比 姐妹-胎 病 墓 衰

五行分数 {'金': 19, '木': 1, '水': 10, '火': 13, '土': 17}   八字强弱： 29 通常>29为强，需要参考月份、坐支等 weak: True
湿度分数 -5 正为暖燥，负为寒湿，正常区间[-6,6] 拱： []
甲[伤]-0   乙[食]-1   丙[财]-5   丁[才]-8   戊[官]-7   己[杀]-10   庚[印]-1   辛[枭]-18   壬[劫]-5   癸[比]-5
------------------------------------------------------------------------------------------------------------------------
劫财扶助，无微不至。劫财多者谦虚之中带有傲气。凡事先理情，而后情理。先细节后全局。性刚强、精明干练、女命不适合干透支藏。
务实，不喜欢抽象性的空谈。不容易认错，比较倔。有理想，但是不够灵活。不怕闲言闲语干扰。不顾及别人面子。
合作事业有始无终。太重细节。做小领导还是可以的。有志向，自信。杀或食透干可解所有负面。女命忌讳比劫和合官杀，多为任性引发困难之事。
时柱劫：只要不是去经济大权还好。
偏印在月：有慧少福，能舍己为人。
偏印专位在月支：比较适合音乐，艺术，宗教等。子午卯酉。22-30之间职业定型。基56：壬午 癸卯 丁丑 丁未
印或枭在月支，有压制丈夫的心态。
偏财明现天干，不论是否有根:财富外人可见;实际财力不及外观一半。没钱别人都不相信;协助他人常超过自己的能力
偏财出天干，又与天月德贵人同一天干者。在年月有声明远扬的父亲，月时有聪慧的红颜知己。喜奉承。
偏财透天干，四柱没有刑冲，长寿。女子为孝顺女，主要针对年月。时柱表示中年以后有自己的事业，善于理财。
财格基础80:比劫用食伤通关或官杀制；身弱有比劫仍然用食伤通关。如果时柱坐实比劫，晚年破产。
偏财透天干，讲究原则，不拘小节。喜奉承，善于享受。财格基础80
偏财和七杀并位，地支又有根，父子外合心不合。因为偏财生杀攻身。偏财七杀在日时，则为有难伺候的女朋友。 基62壬午 甲辰 戊寅 癸亥
偏财坐空亡，财官难求。
偏财多的人慷慨，得失看淡。花钱一般不会后悔。偏乐观，甚至是浮夸。生活习惯颠倒。适应能力强。有团队精神。得女性欢心。小事很少失信。
乐善好施，有团队精神，女命偏财，听父亲的话。时柱偏财女，善于理财，中年以后有事业。
七杀是非多。但是对男人有时是贵格。比如毛主席等。成格基础85可杀生印或食制印、身杀两停、阳刃驾杀。
杀格：喜食神制，要食在前，杀在后。阳刃驾杀：杀在前，刃在后。身杀两停：比如甲寅日庚申月。杀印相生，忌食同成格。
杀格透比或劫：性急但还有分寸。
杀格透官：精明琐屑，不怕脏。
财生杀，如果不是身弱有印，不佳。
七杀坐空亡，女命夫缘薄。 基68 壬申 庚戌 甲子 丙寅
七杀坐刑或对冲，夫妻不和。
杀格透比或劫：性急但还有分寸。
杀格透官：精明琐屑，不怕脏。
自坐食伤库：总觉得钱不够花。
局 [] 格 ['才', '杀']


命
=========================

    六癸日生日壬戌，支内正官生财库；月兼有救贵多成，倚托若无终不富。
    癸日壬戌时，水火既济，癸用丙丁为财，戊土为官，戊与癸合旺，为人智谋，通月气有倚托者贵；不通，平常；通火土月气，富贵双全；运气通，亦吉。
    1-158 中年心灰意冷。

    天乙壬癸戌时排，库内财官等钥开；不遇刑冲空锁闭，少年难发更生灾。
    癸日时逢壬戌，就中仓库盈余，将星天德两相扶，辰戌钥匙开助。土旺长流水局，六亲恩处成疏，不遇空亡有增余，中末荣华享福。

    癸丑日壬戌时,刑,亥月,土厚地方上贵。辰申年月,南方运,状元。五月,南运,都宪。若春秋生,南方运,八九品。

    癸卯日壬戌时,日贵格,寅巳年月,干透戊丁财官而旺, 大贵有权。卯辰丑午子等年月,文贵。酉戌,金土运,五六品。

    癸巳日壬戌时,财官双美,春平,夏秋冬贵。辰丑未寅酉年月,风宪。

    癸未日壬戌时,刑。巳月生,三四品。子庚年月,近侍贵。

    癸酉日壬戌时,亥子月,才智高贵,妻贤子孝。春平常。夏财官,秋印绶,俱吉。辰丑,刑冲戌库,贵富两全。戌月, 东南运,武贵。

    癸亥日壬戌时,春生,伤官见官,夏财旺,秋、冬吉,名利有成。戌辰月,行亥子运,贵。子月,行西南运,金紫。



大运
========================================================================================================================
5        庚戌 衰 钗钏金    印:庚＋　　　　　　　戌＋衰 - 戊土官　辛金枭　丁火才　　　　 害:酉  会:酉  刑:未  破:未  神:大耗 月德
  5 1982 壬戌 衰 大海水 *  劫:壬＋合丁　　　　　戌＋衰 - 戊土官　辛金枭　丁火才　　 害:酉  会:酉  刑:未  神:大耗
  6 1983 癸亥 帝 大海水    比:癸－冲丁　　　　　亥－帝 - 壬水劫　甲木伤　　　　　　 冲:巳  合:未
  7 1984 甲子 建 海中金    伤:甲＋合己冲庚　　　子＋建 - 癸水比　　　　　　　　　　 害:未  神:大耗 桃花
  8 1985 乙丑 冠 海中金    食:乙－合庚　　　　　丑－冠 - 己土杀　癸水比　辛金枭　　 冲:未  刑:戌  合:酉  合:巳  被刑:未  神:文昌
  9 1986 丙寅 沐 炉中火    财:丙＋冲壬　　　　　寅＋沐 - 甲木伤　丙火财　戊土官　　 刑:巳  合:戌  害:巳  神:天德 亡神
 10 1987 丁卯 长 炉中火    才:丁－合壬冲癸　　　卯－长 - 乙木食　　　　　　　　　　 合:未  六:戌  冲:酉  --夹：辰  神:将星 天乙
 11 1988 戊辰 养 大林木    官:戊＋合癸　　　　　辰＋养 - 戊土官　乙木食　癸水比　　 六:酉  冲:戌  神:寡宿
 12 1989 己巳 胎 大林木    杀:己－　　　　　　　巳－胎 - 丙火财　戊土官　庚金印　　 合:酉  会:未  神:驿马 天乙
 13 1990 庚午 绝 路旁土    印:庚＋　　　　　　　午＋绝 - 丁火才　己土杀　　　　　　 六:未  合:戌  会:巳  会:未  神:月德
 14 1991 辛未 墓 路旁土    枭:辛－　　　　　　　未－墓 - 己土杀　丁火才　乙木食　　 会:巳  被刑:戌  神:华盖
15       辛亥 帝 钗钏金    枭:辛－　　　　　　　亥－帝 - 壬水劫　甲木伤　　　　　　　　 冲:巳  合:未
 15 1992 壬申 死 剑锋金    劫:壬＋合丁　　　　空申＋死 - 庚金印　壬水劫　戊土官　　 会:酉  会:戌  六:巳  被刑:巳  害:亥  --夹：酉  神:孤辰 劫煞 红艳
 16 1993 癸酉 病 剑锋金    比:癸－冲丁　　　　空酉－病 - 辛金枭　　　　　　　　　　 会:戌  害:戌  被刑:酉  合:巳  刑:酉  --夹：申
 17 1994 甲戌 衰 山头火    伤:甲＋合己　　　　　戌＋衰 - 戊土官　辛金枭　丁火才　　 害:酉  会:酉  刑:未  神:大耗
 18 1995 乙亥 帝 山头火    食:乙－冲辛　　　　　亥－帝 - 壬水劫　甲木伤　　　　　　 冲:巳  合:未  刑:亥  被刑:亥
 19 1996 丙子 建 涧下水    财:丙＋合辛冲壬　　　子＋建 - 癸水比　　　　　　　　　　 害:未  会:亥  神:大耗 桃花
 20 1997 丁丑 冠 涧下水    才:丁－合壬冲癸　　　丑－冠 - 己土杀　癸水比　辛金枭　　 冲:未  刑:戌  会:亥  合:酉  合:巳  被刑:未  神:文昌
 21 1998 戊寅 沐 城头土    官:戊＋合癸　　　　　寅＋沐 - 甲木伤　丙火财　戊土官　　 刑:巳  六:亥  合:戌  害:巳  神:天德 亡神
 22 1999 己卯 长 城头土    杀:己－　　　　　　　卯－长 - 乙木食　　　　　　　　　　 合:未  六:戌  合:亥  冲:酉  神:将星 天乙
 23 2000 庚辰 养 白蜡金    印:庚＋　　　　　　　辰＋养 - 戊土官　乙木食　癸水比　　 六:酉  冲:戌  神:寡宿 月德  天罗地网：戌亥辰巳
 24 2001 辛巳 胎 白蜡金    枭:辛－　　　　　　　巳－胎 - 丙火财　戊土官　庚金印　　 冲:亥  合:酉  会:未  神:驿马 天乙
25       壬子 建 桑柘木    劫:壬＋合丁　　　　　子＋建 - 癸水比　　　　　　　　　　　　 害:未  破:酉  --夹：戌  神:大耗 桃花
 25 2002 壬午 绝 杨柳木    劫:壬＋合丁　　　　　午＋绝 - 丁火才　己土杀　　　　　　 六:未  冲:子  合:戌  会:未  会:巳
 26 2003 癸未 墓 杨柳木 *  比:癸－冲丁　　　　　未－墓 - 己土杀　丁火才　乙木食　　 害:子  会:巳  被刑:戌  神:华盖
 27 2004 甲申 死 井泉水    伤:甲＋合己　　　　空申＋死 - 庚金印　壬水劫　戊土官　　 会:酉  会:戌  六:巳  被刑:巳  合:子  神:孤辰 劫煞 红艳
 28 2005 乙酉 病 井泉水    食:乙－　　　　　　空酉－病 - 辛金枭　　　　　　　　　　 会:戌  害:戌  被刑:酉  合:巳  刑:酉
 29 2006 丙戌 衰 屋上土    财:丙＋冲壬　　　　　戌＋衰 - 戊土官　辛金枭　丁火才　　 害:酉  会:酉  刑:未  神:大耗
 30 2007 丁亥 帝 屋上土    才:丁－合壬冲癸　　　亥－帝 - 壬水劫　甲木伤　　　　　　 冲:巳  合:未  会:子
 31 2008 戊子 建 霹雳火    官:戊＋合癸　　　　　子＋建 - 癸水比　　　　　　　　　　 害:未  神:大耗 桃花
 32 2009 己丑 冠 霹雳火    杀:己－　　　　　　　丑－冠 - 己土杀　癸水比　辛金枭　　 冲:未  六:子  刑:戌  会:子  合:酉  合:巳  被刑:未  神:文昌
 33 2010 庚寅 沐 松柏木    印:庚＋　　　　　　　寅＋沐 - 甲木伤　丙火财　戊土官　　 刑:巳  合:戌  害:巳  神:天德 月德 亡神
 34 2011 辛卯 长 松柏木    枭:辛－　　　　　　　卯－长 - 乙木食　　　　　　　　　　 合:未  被刑:子  刑:子  六:戌  冲:酉  神:将星 天乙
35       癸丑 冠 桑柘木    比:癸－冲丁　　　　　丑－冠 - 己土杀　癸水比　辛金枭　　　　 冲:未  刑:戌  合:酉  合:巳  被刑:未  神:文昌
 35 2012 壬辰 养 长流水    劫:壬＋合丁　　　　　辰＋养 - 戊土官　乙木食　癸水比　　 六:酉  冲:戌  神:寡宿  四库：辰戌丑未
 36 2013 癸巳 胎 长流水    比:癸－冲丁　　　　　巳－胎 - 丙火财　戊土官　庚金印　　 合:丑  合:酉  会:未  --夹：午  神:驿马 天乙
 37 2014 甲午 绝 砂中金    伤:甲＋合己　　　　　午＋绝 - 丁火才　己土杀　　　　　　 六:未  合:戌  害:丑  会:未  会:巳
 38 2015 乙未 墓 砂中金    食:乙－　　　　　　　未－墓 - 己土杀　丁火才　乙木食　　 刑:丑  会:巳  被刑:戌  冲:丑  神:华盖
 39 2016 丙申 死 山下火    财:丙＋冲壬　　　　空申＋死 - 庚金印　壬水劫　戊土官　　 被刑:巳  会:酉  会:戌  六:巳  神:孤辰 劫煞 红艳
 40 2017 丁酉 病 山下火    才:丁－合壬冲癸　　空酉－病 - 辛金枭　　　　　　　　　　 会:戌  合:丑  害:戌  被刑:酉  合:巳  刑:酉
 41 2018 戊戌 衰 平地木    官:戊＋合癸　　　　　戌＋衰 - 戊土官　辛金枭　丁火才　　 害:酉  会:酉  刑:未  被刑:丑  神:大耗
 42 2019 己亥 帝 平地木    杀:己－　　　　　　　亥－帝 - 壬水劫　甲木伤　　　　　　 冲:巳  合:未  会:丑  --夹：戌
 43 2020 庚子 建 壁上土    印:庚＋　　　　　　　子＋建 - 癸水比　　　　　　　　　　 害:未  会:丑  六:丑  神:大耗 月德 桃花
 44 2021 辛丑 冠 壁上土    枭:辛－　　　　　　　丑－冠 - 己土杀　癸水比　辛金枭　　 冲:未  刑:戌  合:酉  合:巳  被刑:未  神:文昌
45       甲寅 沐 大溪水    伤:甲＋合己　　　　　寅＋沐 - 甲木伤　丙火财　戊土官　　　　 刑:巳  合:戌  害:巳  神:天德 亡神
 45 2022 壬寅 沐 金泊金    劫:壬＋合丁　　　　　寅＋沐 - 甲木伤　丙火财　戊土官　　 刑:巳  合:戌  害:巳  神:天德 亡神
 46 2023 癸卯 长 金泊金    比:癸－冲丁　　　　　卯－长 - 乙木食　　　　　　　　　　 合:未  六:戌  会:寅  冲:酉  神:将星 天乙
 47 2024 甲辰 养 覆灯火    伤:甲＋合己　　　　　辰＋养 - 戊土官　乙木食　癸水比　　 六:酉  冲:戌  会:寅  --夹：卯  神:寡宿
 48 2025 乙巳 胎 覆灯火    食:乙－　　　　　　　巳－胎 - 丙火财　戊土官　庚金印　　 害:寅  被刑:寅  合:酉  会:未  神:驿马 天乙
 49 2026 丙午 绝 天河水    财:丙＋冲壬　　　　　午＋绝 - 丁火才　己土杀　　　　　　 六:未  合:戌  会:未  合:寅  会:巳
 50 2027 丁未 墓 天河水    才:丁－合壬冲癸　　　未－墓 - 己土杀　丁火才　乙木食　　 会:巳  被刑:戌  --夹：午  神:华盖
 51 2028 戊申 死 大驿土    官:戊＋合癸　　　　空申＋死 - 庚金印　壬水劫　戊土官　　 会:酉  会:戌  六:巳  被刑:巳  冲:寅  刑:寅  神:孤辰 劫煞 红艳
 52 2029 己酉 病 大驿土 *  杀:己－合甲　　　　空酉－病 - 辛金枭　　　　　　　　　　 会:戌  害:戌  被刑:酉  合:巳  刑:酉
 53 2030 庚戌 衰 钗钏金    印:庚＋冲甲　　　　　戌＋衰 - 戊土官　辛金枭　丁火才　　 害:酉  会:酉  合:寅  刑:未  神:大耗 月德
 54 2031 辛亥 帝 钗钏金    枭:辛－　　　　　　　亥－帝 - 壬水劫　甲木伤　　　　　　 冲:巳  合:未  六:寅
55       乙卯 长 大溪水    食:乙－　　　　　　　卯－长 - 乙木食　　　　　　　　　　　　 合:未  六:戌  冲:酉  神:将星 天乙
 55 2032 壬子 建 桑柘木    劫:壬＋合丁　　　　　子＋建 - 癸水比　　　　　　　　　　 害:未  刑:卯  被刑:卯  --夹：戌  神:大耗 桃花
 56 2033 癸丑 冠 桑柘木    比:癸－冲丁　　　　　丑－冠 - 己土杀　癸水比　辛金枭　　 冲:未  刑:戌  合:酉  合:巳  被刑:未  神:文昌
 57 2034 甲寅 沐 大溪水    伤:甲＋合己　　　　　寅＋沐 - 甲木伤　丙火财　戊土官　　 刑:巳  会:卯  合:戌  害:巳  神:天德 亡神
 58 2035 乙卯 长 大溪水    食:乙－　　　　　　　卯－长 - 乙木食　　　　　　　　　　 合:未  六:戌  冲:酉  神:将星 天乙
 59 2036 丙辰 养 砂中土    财:丙＋冲壬　　　　　辰＋养 - 戊土官　乙木食　癸水比　　 会:卯  六:酉  冲:戌  害:卯  神:寡宿
 60 2037 丁巳 胎 砂中土 *  才:丁－合壬冲癸　　　巳－胎 - 丙火财　戊土官　庚金印　　 合:酉  会:未  神:驿马 天乙
 61 2038 戊午 绝 天上火    官:戊＋合癸　　　　　午＋绝 - 丁火才　己土杀　　　　　　 六:未  合:戌  会:巳  会:未
 62 2039 己未 墓 天上火    杀:己－　　　　　　　未－墓 - 己土杀　丁火才　乙木食　　 合:卯  会:巳  被刑:戌  --夹：申  神:华盖
 63 2040 庚申 死 石榴木    印:庚＋合乙　　　　空申＋死 - 庚金印　壬水劫　戊土官　　 会:酉  会:戌  六:巳  被刑:巳  暗:卯  神:孤辰 月德 劫煞 红艳
 64 2041 辛酉 病 石榴木    枭:辛－冲乙　　　　空酉－病 - 辛金枭　　　　　　　　　　 会:戌  害:戌  被刑:酉  合:巳  冲:卯  刑:酉
65       丙辰 养 砂中土    财:丙＋冲壬　　　　　辰＋养 - 戊土官　乙木食　癸水比　　　　 六:酉  冲:戌  神:寡宿
 65 2042 壬戌 衰 大海水 *  劫:壬＋合丁冲丙　　　戌＋衰 - 戊土官　辛金枭　丁火才　　 害:酉  会:酉  刑:未  冲:辰  神:大耗
 66 2043 癸亥 帝 大海水    比:癸－冲丁　　　　　亥－帝 - 壬水劫　甲木伤　　　　　　 冲:巳  合:未  天罗地网：戌亥辰巳
 67 2044 甲子 建 海中金    伤:甲＋合己　　　　　子＋建 - 癸水比　　　　　　　　　　 害:未  合:辰  神:大耗 桃花
 68 2045 乙丑 冠 海中金    食:乙－　　　　　　　丑－冠 - 己土杀　癸水比　辛金枭　　 冲:未  刑:戌  合:酉  合:巳  被刑:未  神:文昌  四库：辰戌丑未
 69 2046 丙寅 沐 炉中火    财:丙＋冲壬　　　　　寅＋沐 - 甲木伤　丙火财　戊土官　　 刑:巳  合:戌  会:辰  害:巳  --夹：卯  神:天德 亡神
 70 2047 丁卯 长 炉中火    才:丁－合壬冲癸　　　卯－长 - 乙木食　　　　　　　　　　 合:未  害:辰  六:戌  会:辰  冲:酉  --夹：辰  神:将星 天乙
 71 2048 戊辰 养 大林木    官:戊＋合癸　　　　　辰＋养 - 戊土官　乙木食　癸水比　　 被刑:辰  刑:辰  六:酉  冲:戌  神:寡宿
 72 2049 己巳 胎 大林木    杀:己－　　　　　　　巳－胎 - 丙火财　戊土官　庚金印　　 合:酉  会:未  神:驿马 天乙
 73 2050 庚午 绝 路旁土    印:庚＋　　　　　　　午＋绝 - 丁火才　己土杀　　　　　　 六:未  合:戌  会:巳  会:未  神:月德
 74 2051 辛未 墓 路旁土    枭:辛－合丙　　　　　未－墓 - 己土杀　丁火才　乙木食　　 会:巳  被刑:戌  神:华盖
75       丁巳 胎 砂中土 *  才:丁－合壬冲癸　　　巳－胎 - 丙火财　戊土官　庚金印　　　　 合:酉  会:未  神:驿马 天乙
 75 2052 壬申 死 剑锋金    劫:壬＋合丁　　　　空申＋死 - 庚金印　壬水劫　戊土官　　 被刑:巳  会:酉  会:戌  六:巳  --夹：酉  神:孤辰 劫煞 红艳
 76 2053 癸酉 病 剑锋金    比:癸－冲丁　　　　空酉－病 - 辛金枭　　　　　　　　　　 会:戌  害:戌  被刑:酉  合:巳  刑:酉  --夹：申
 77 2054 甲戌 衰 山头火    伤:甲＋合己　　　　　戌＋衰 - 戊土官　辛金枭　丁火才　　 害:酉  会:酉  刑:未  神:大耗
 78 2055 乙亥 帝 山头火    食:乙－　　　　　　　亥－帝 - 壬水劫　甲木伤　　　　　　 冲:巳  合:未
 79 2056 丙子 建 涧下水    财:丙＋冲壬　　　　　子＋建 - 癸水比　　　　　　　　　　 害:未  神:大耗 桃花
 80 2057 丁丑 冠 涧下水    才:丁－合壬冲癸　　　丑－冠 - 己土杀　癸水比　辛金枭　　 冲:未  刑:戌  合:酉  合:巳  被刑:未  神:文昌
 81 2058 戊寅 沐 城头土    官:戊＋合癸　　　　　寅＋沐 - 甲木伤　丙火财　戊土官　　 刑:巳  合:戌  害:巳  神:天德 亡神
 82 2059 己卯 长 城头土    杀:己－　　　　　　　卯－长 - 乙木食　　　　　　　　　　 合:未  六:戌  冲:酉  神:将星 天乙
 83 2060 庚辰 养 白蜡金    印:庚＋　　　　　　　辰＋养 - 戊土官　乙木食　癸水比　　 六:酉  冲:戌  神:寡宿 月德
 84 2061 辛巳 胎 白蜡金    枭:辛－　　　　　　　巳－胎 - 丙火财　戊土官　庚金印　　 合:酉  会:未  神:驿马 天乙
85       戊午 绝 天上火    官:戊＋合癸　　　　　午＋绝 - 丁火才　己土杀　　　　　　　　 六:未  合:戌  会:巳  会:未
 85 2062 壬午 绝 杨柳木    劫:壬＋合丁　　　　　午＋绝 - 丁火才　己土杀　　　　　　 六:未  刑:午  合:戌  被刑:午  会:未  会:巳
 86 2063 癸未 墓 杨柳木 *  比:癸－合戊冲丁　　　未－墓 - 己土杀　丁火才　乙木食　　 六:午  会:巳  被刑:戌  会:午  神:华盖
 87 2064 甲申 死 井泉水    伤:甲＋合己　　　　空申＋死 - 庚金印　壬水劫　戊土官　　 被刑:巳  会:酉  会:戌  六:巳  神:孤辰 劫煞 红艳
 88 2065 乙酉 病 井泉水    食:乙－　　　　　　空酉－病 - 辛金枭　　　　　　　　　　 会:戌  害:戌  被刑:酉  合:巳  刑:酉
 89 2066 丙戌 衰 屋上土    财:丙＋冲壬　　　　　戌＋衰 - 戊土官　辛金枭　丁火才　　 害:酉  会:酉  合:午  刑:未  神:大耗
 90 2067 丁亥 帝 屋上土    才:丁－合壬冲癸　　　亥－帝 - 壬水劫　甲木伤　　　　　　 冲:巳  合:未  暗:午
 91 2068 戊子 建 霹雳火    官:戊＋合癸　　　　　子＋建 - 癸水比　　　　　　　　　　 害:未  冲:午  神:大耗 桃花
 92 2069 己丑 冠 霹雳火    杀:己－　　　　　　　丑－冠 - 己土杀　癸水比　辛金枭　　 冲:未  刑:戌  害:午  合:酉  合:巳  被刑:未  神:文昌
 93 2070 庚寅 沐 松柏木    印:庚＋　　　　　　　寅＋沐 - 甲木伤　丙火财　戊土官　　 刑:巳  合:戌  害:巳  合:午  神:天德 月德 亡神
 94 2071 辛卯 长 松柏木    枭:辛－　　　　　　　卯－长 - 乙木食　　　　　　　　　　 合:未  六:戌  冲:酉  神:将星 天乙
95       己未 墓 天上火    杀:己－　　　　　　　未－墓 - 己土杀　丁火才　乙木食　　　　 破:戌  会:巳  被刑:戌  --夹：申  神:华盖
 95 2072 壬辰 养 长流水    劫:壬＋合丁　　　　　辰＋养 - 戊土官　乙木食　癸水比　　 六:酉  冲:戌  神:寡宿
 96 2073 癸巳 胎 长流水    比:癸－冲丁　　　　　巳－胎 - 丙火财　戊土官　庚金印　　 合:酉  会:未  --夹：午  神:驿马 天乙
 97 2074 甲午 绝 砂中金    伤:甲＋合己　　　　　午＋绝 - 丁火才　己土杀　　　　　　 六:未  合:戌  会:巳  会:未
 98 2075 乙未 墓 砂中金    食:乙－　　　　　　　未－墓 - 己土杀　丁火才　乙木食　　 会:巳  被刑:戌  神:华盖
 99 2076 丙申 死 山下火    财:丙＋冲壬　　　　空申＋死 - 庚金印　壬水劫　戊土官　　 被刑:巳  会:酉  会:戌  六:巳  神:孤辰 劫煞 红艳
100 2077 丁酉 病 山下火    才:丁－合壬冲癸　　空酉－病 - 辛金枭　　　　　　　　　　 会:戌  害:戌  被刑:酉  合:巳  刑:酉
101 2078 戊戌 衰 平地木    官:戊＋合癸　　　　　戌＋衰 - 戊土官　辛金枭　丁火才　　 害:酉  会:酉  刑:未  神:大耗
102 2079 己亥 帝 平地木    杀:己－　　　　　　　亥－帝 - 壬水劫　甲木伤　　　　　　 冲:巳  合:未  --夹：戌
103 2080 庚子 建 壁上土    印:庚＋　　　　　　　子＋建 - 癸水比　　　　　　　　　　 害:未  神:大耗 月德 桃花
104 2081 辛丑 冠 壁上土    枭:辛－　　　　　　　丑－冠 - 己土杀　癸水比　辛金枭　　 冲:未  刑:戌  合:酉  合:巳  被刑:未  神:文昌
105      庚申 死 石榴木    印:庚＋　　　　　　空申＋死 - 庚金印　壬水劫　戊土官　　　　 会:酉  会:戌  六:巳  被刑:巳  破:巳  神:孤辰 月德 劫煞 红艳
115      辛酉 病 石榴木    枭:辛－　　　　　　空酉－病 - 辛金枭　　　　　　　　　　　　 会:戌  害:戌  被刑:酉  合:巳  刑:酉
5.0
星宿 ('胃', '') ('开', '重新开展的好日子。 宜：祭祀、祈福、开光、入宅、嫁娶、上任、修造、动土、开市、安床、交易、出行、竖柱。 忌：诉讼、安葬。')
========================================================================================================================

```

### 更多书籍 (访问密码: 2274) 点击“普通下载”下面的“立即下载”可浏览器下载

- [生活智慧掌中宝37_解密家装1家庭风水一学就会.pdf](https://url97.ctfile.com/f/18113597-810840303-8cd789?p=2274)

- [书籍: 图解易经中的数学梅花易数 - 2007.pdf 故宫珍藏善本：梅花易数 - 2012.pdf](https://url97.ctfile.com/f/18113597-810842961-4b58ce?p=2274)

易经.pdf

古代文化集粹丛书（套装共9册） 《中国起名宝典》、《算命不求人》、《手相面相测人生》、《四柱预测学》、《周公解梦》、《十二生肖与运程》、《中国风水宝典》、《血型与属相》、《万事不求人》 下载

绍金解易经-八字揭秘.pdf

道家与性文化.pdf

安星法及推断实例-2013.pdf

紫微斗数讲义-2013.pdf

万年历- 2013.pdf

中华万年历全书(超值版) (家庭珍藏经典畅销书系)-2012.pdf

中华民俗万年历-2007.pdf

新编实用万年历(1901-2100年)(第2版) - 2011.pdf

中国罗盘详解 - 2014.pdf

中国罗盘通俗解读 - 2011.pdf

-- 鸣谢：本程序的日历使用库　https://pypi.org/project/sxtwl/。
