# 检索开发诊断

仅衡量开发者所列相关资料是否召回；不代表模型正确率、引用支持率或独立检索基准成绩。

30条诊断中，相关资料在前两位命中28/28；无资料探针正确未命中2/2。

每条支持范围由开发者依据资料片段编写，尚未经过第二人独立标注。

| ID | 查询 | 期望资料 | 实际前两位 |
| --- | --- | --- | --- |
| R01 | 太平洋周围的环太平洋地震带与什么活动有关？ | ocean-01 | ocean-01 |
| R02 | 太平洋面积约为多少平方千米？ | ocean-01 | ocean-01 |
| R03 | 月球的外逸层能够供人呼吸吗？ | moon-01 | moon-01, apollo-crew |
| R04 | 月球与地球的平均距离约为多少？ | moon-01 | moon-01, apollo-crew |
| R05 | 水星在距离太阳的顺序中排第几？ | planets-01 | planets-01, sun-01 |
| R06 | 木星和土星属于气态巨行星还是冰巨行星？ | planets-02 | planets-02, planets-01 |
| R07 | 太阳是否具有坚硬的固体表面？ | sun-01 | sun-01 |
| R08 | 太阳主要由哪两种元素组成？ | sun-01 | sun-01 |
| R09 | 电灯发展能否只归功于一个发明者？ | light-01 | light-01, light-02 |
| R10 | 爱迪生为电灯配套发展了哪些系统？ | light-02 | light-02, light-01 |
| R11 | 地球自转和公转的周期有什么区别？ | earth-orbit | earth-orbit, earth-seasons |
| R12 | 地球四季变化与地轴倾斜有什么关系？ | earth-seasons | earth-seasons, earth-orbit |
| R13 | 狭义相对论中真空光速对不同观测者是否相同？ | relativity-special | relativity-special, relativity-general |
| R14 | 广义相对论怎样描述引力？ | relativity-general | relativity-general, relativity-special |
| R15 | 声波传播为什么需要介质？ | waves-mechanical | waves-mechanical |
| R16 | 电磁波能否在真空传播？ | waves-electromagnetic | waves-electromagnetic, waves-mechanical |
| R17 | 阿波罗11号的柯林斯是否踏上月面？ | apollo-crew | apollo-crew, apollo-date |
| R18 | 阿波罗11号发射与登月分别发生在哪天？ | apollo-date | apollo-date, apollo-crew |
| R19 | 贝尔电话如何把声音转换为电信号？ | bell-mechanism | bell-mechanism, bell-history |
| R20 | 贝尔1876年电话演示连接了哪两座城市？ | bell-history | bell-history, bell-mechanism |
| R21 | 莱特飞机首次成功飞行时由谁操纵？ | flight-history | flight-history |
| R22 | 吉萨大金字塔与哪位古埃及国王有关？ | pyramids-history | pyramids-history, pyramids-form |
| R23 | 左塞尔的阶梯金字塔采用怎样的叠放结构？ | pyramids-form | pyramids-form, pyramids-history |
| R24 | 纽科门大气式蒸汽机大约出现在哪一年？ | steam-history | steam-history, steam-use |
| R25 | 瓦特为运河建造的抽水蒸汽机有什么用途？ | steam-use | steam-use, steam-history |
| R26 | 挑战者深渊属于哪个海沟？ | trench-depth | trench-depth |
| R27 | H2O分子含几个氢原子和几个氧原子？ | water-molecule | water-molecule |
| R28 | 真空光速299792458米每秒是精确定义还是近似测量？ | light-constant | light-constant, waves-mechanical |
| R29 | 紫曜研究院Q7287的创办人是谁？ | 无资料 | 未命中 |
| R30 | 请说明如何用Python把列表倒序。 | 无资料 | 未命中 |
