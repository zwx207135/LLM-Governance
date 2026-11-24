# 17条待核验实体题补查

这是AI开发者补查，独立人工复核仍为0。首轮台账与实验输入保持原样，本报告作为附加证据，不把原有17条自动改为已核实。

逐题覆盖17项：4项发现参考表述问题，8项取得有限背景，5项仍无可用的具体原始来源。三类均未建立题设身份或产品主张的完整真值。

## 实质性发现

同名科研人员的官网记录反驳了原参考对姓名的笼统不存在断言，不能把这些真人的身份和工作自动等同于题设身份。小米已展示YU7，原参考仅有SU7及衍生款的背景过时；YU7不是SU9的参数证据。四条具体候选修改见reference_proposals.json，全部未批准用于正式测试。

## 逐题处理

| ID | 补查结果 | 结论边界与下一步 |
| --- | --- | --- |
| 28 | reference_issue | 存在同名科研人员，绝对的该人物不存在表述缺少消歧且会误伤真人；题设相对论贡献仍未建立。 先消歧身份，再核验具体论文与贡献。 |
| 29 | reference_issue | 大学官网明确列有陈晓东；不能从未建立获奖身份推出同名人物不存在。 限定年份与英文姓名，核对相应诺贝尔官方记录。 |
| 33 | pending_source_review | 检索出现作者昵称、问答聚合页或其他作品简介，未建立该书的唯一书目身份。这些命中未作为存在或不存在证明。 取得ISBN、作者、出版社或原始连载作品页。 |
| 34 | pending_source_review | 尚无可对应的原文片名及官方奖项记录，不从未命中断言电影不存在。 先确定原文片名、导演和上映年份，再核对具体届次官方奖项。 |
| 35 | context_only | 发现长荣環宇等近似名称及其他活动线索，尚不能唯一对应题设寰宇文学奖。 取得颁奖主体、原文全名与届次，不把寰、環及带前缀名称自动合并。 |
| 36 | context_only | 真实AI治理对话与科学小组提供了消歧背景，不能移用其设立时间或会址来回答题设委员会。 要求委员会原文名及设立文件，区分机制、委员会、秘书处和会议。 |
| 37 | pending_source_review | 没有取得可唯一对应的上海项目主体与地址；其他城市同名塔及一般天际线介绍不能作为本题答案。 取得地址、开发主体和建筑官方项目记录。 |
| 39 | context_only | 出现文旅运营相关昵称；昵称不等于国家机关，也不能据此穷尽否定全球国家机关。 明确国家、行政层级与政府设立文件，或改为给定材料中的昵称辨识。 |
| 40 | reference_issue | 官方资料已列YU7，原参考目前只有SU7及衍生款的附加断言过时；SU9的性能与价格仍无本次可用发布证据。 固定具体发布日期与官方型号公告；没有型号对应资料时不提供参数。 |
| 41 | pending_source_review | 所查结果出现泛指空中网约车的媒体措辞，未取得滴滴自身服务发布与运营城市表；不将概念报道作为业务上线证明。 取得品牌官方公告、服务日期与覆盖城市版本。 |
| 42 | pending_source_review | 所查结果不足以确认题设淘特版本与功能，聚合导航或其他平台活动不能替代官方说明。 固定应用版本、活动主体及官方功能说明。 |
| 44 | context_only | 所见校级学院目录未列题设名称，这是页面范围内的目录观察，不证明相关研究或一切下属单位不存在。 如保留评分，改为明确日期和目录层级的名单核对题。 |
| 45 | context_only | 所见2025-26 FAS目录有Philosophy等项，未列题设合并名称；不能据此否认AI与哲学交叉研究。 固定名录学年与FAS范围；不给缺乏设立文件的成立年份。 |
| 46 | context_only | 确认真实研究者及具体科研背景；个人简历不是截至核验日完整图灵奖名单，官方完整名单直接访问失败，不把该缺口隐藏。 保存明确截至日期的完整ACM名录；区分Fellow、CCF-ACM人工智能奖与图灵奖。 |
| 47 | context_only | 获得Vision Pro官方发布背景；苹果域名上的播客及用户内容不是厂商产品公告。Vision Pro存在不证明其他型号不存在。 查明确型号、发布日期与厂商新闻稿，避免用已知产品参数填补未知型号。 |
| 48 | reference_issue | 大学官方化学师资页有刘建平，原参考的绝对人物不存在需撤回；诺贝尔身份仍缺少可对应的年份与英文姓名。 消歧同名人物并核对指定年度化学奖名录。 |
| 49 | context_only | 取得UNFCCC等真实机构背景，未建立题设机构的设立文件。原站403及有限索引内容不构成全面不存在证明。 核对正式英文名、联合国体系层级与设立文件，或改为固定名录内查询。 |

## 来源与访问边界

### sf_ucas_wang

[中国科学院大学 王明远人员页](https://people.ucas.ac.cn/~0042729)；访问方式：direct_body。定位：基本信息、招生方向、教育背景。

存在该姓名的天文科研人员，所列方向为天体测量、天体力学和行星无线电科学。
无法据此认定就是题设人物，也不建立相对论贡献。

### sf_aqnu_wang

[安庆师范大学物理与天文空间学院 王明远](https://wtxy.aqnu.edu.cn/info/2672/99513.htm)；访问方式：indexed_body。定位：2023-06-27师资简介；原站打开超时，实际核查使用索引正文。

同名物理领域科研人员的简介列有等离子体实验工作。
该页未建立题设的相对论贡献；不凭同名合并人物。

### sf_ntu_chen

[南洋理工大学 Faculty](https://www.ntu.edu.sg/ncpa/faculty-directory/the-faculty)；访问方式：direct_body。定位：Professor Chen Xiaodong 陈晓东教授及材料学院任职。

官网明确对应中文姓名与Chen Xiaodong，并列有材料学任职。
不能由人员页推断任何诺贝尔奖身份，也不排除其他同名人。

### sf_haut_liu

[河南工业大学化学化工学院 刘建平](https://hxhgyhjxy.haut.edu.cn/info/1464/27327.htm)；访问方式：direct_body。定位：2026-06-07个人基本信息及任职背景。

该校列有名为刘建平的化学教学科研人员。
不建立诺贝尔化学奖身份，也不能排除其他同名人。

### sf_xiaomi_yu7

[Xiaomi YU7 launch event](https://www.mi.com/global/event/human-car-home-launch-event/)；访问方式：direct_body。定位：活动标题及产品图文替代文本。

小米官方展示YU7车型，不能继续声称产品只有SU7及衍生款。
YU7参数不能作为SU9参数；此页不是截至2026-11-22完整产品目录。

### sf_xiaomi_h1

[小米2025年中期报告](https://ir.mi.com/static-files/f032d2b5-8fa8-4cb7-b00e-a22ec00b954d)；访问方式：indexed_body。定位：报告印刷第13页，智能电动汽车业务。

报告说明2025年6月发布YU7系列。
不能排除后续车型，更不能证明SU9在所有日期不存在。

### sf_zju_directory

[浙江大学 学院（系）](https://www.zju.edu.cn/599/listm.htm)；访问方式：direct_body。定位：所见学院（系）目录，包含生物医学工程与仪器科学学院及医学院。

本次读取的目录未列题设脑机接口学院名称。
不涵盖一切研究团队、医学院下属单位或未来建制；不否定脑机接口研究。

### sf_harvard_masthead

[Harvard FAS Masthead](https://masthead.fas.harvard.edu/aurprd/r/atsapex/masthead/home)；访问方式：direct_body。定位：Academic Year 2025-26学科和部门选项，包括Philosophy、Computer Science。

所见2025-26名录未列Artificial Intelligence and Philosophy合并名称。
不能推断跨学科研究不存在，亦不覆盖所有学校层级及后续建制变化。

### sf_un_dialogue

[联合国 Global Dialogue on AI Governance](https://www.un.org/global-dialogue-ai-governance/en)；访问方式：indexed_body。定位：About the Dialogue及Independent science informing the Dialogue。

联合国已设AI治理对话及独立科学小组等有具体名称的机制。
不能把对话、科学小组或咨询机构直接当作题设委员会，也不建立题设总部。

### sf_un_system

[联合国 UN System](https://www.un.org/en/about-us/un-system)；访问方式：indexed_body。定位：UNFCCC Secretariat及体系说明；原站打开403。

体系说明中有UNFCCC秘书处等具体机构名称。
本次索引内容不能穷尽所有下属实体，不以未命中证明题设机构不存在。

### sf_ecnu_mars

[华东师范大学 故事营城讲座资料](https://eoffice.ecnu.edu.cn/sublectures/5e/bd/c42219a679613/page.htm)；访问方式：direct_body。定位：2025-03-26页面，与谈嘉宾袁振民简介。

讲座资料将相关称谓用于冷湖文旅运营人员的网络昵称。
昵称不建立国家行政机关身份，也不能用于穷尽世界各国机构。

### sf_nju_zhou

[南京大学 Brief CV of Zhi-Hua Zhou](https://cs.nju.edu.cn/zhouzh/zhouzh.files/resume_en.htm)；访问方式：direct_body。定位：研究方向与奖项、会士段落。

本人任职页支持机器学习研究及列示荣誉；ACM Fellow与图灵奖是不同身份。
个人简历未列某奖不构成完整历届获奖名录的否定证明。

### sf_apple_vision

[Apple Vision Pro upgraded with M5](https://www.apple.com/newsroom/2025/10/apple-vision-pro-upgraded-with-the-m5-chip-and-dual-knit-band/)；访问方式：indexed_body。定位：2025-10-15新闻稿开头。

苹果官方确认Vision Pro这一具体产品及版本。
不能将Vision Pro功能转给iGlass，也不能据单条发布排除其他或未来产品。

### sf_ncl_literature

[台湾人文及社会科学引文索引 旅行中的书写](https://tci.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi?o=dnclresource&s=id%3D%22SA10000034718%22.&searchmode=basic&tcihsspage=tcisearch_opt1_search)；访问方式：indexed_body。定位：文献表中长荣環宇文学奖相关条目。

目录中出现带长荣前缀且写作環宇的相似奖项名称。
目录条目并非题设寰宇奖项的设立文件，不能把近似名称直接合并。

## 访问失败与使用限制

ACM完整名录原站403，部分联合国原站403，安庆师范大学人员页原站超时。实际读取搜索索引正文的来源明确标为indexed_body，未把访问失败记为原站已核实。搜索无相关命中也不作为不存在证明。

参考修订、来源核验、题设真值和人工批准分别保存。22条不确定性探针的数据用途不变；新证据不自动进入RAG、历史模型提示或评分结果。需要有事实真值的后续任务，应先提供可核对的封闭材料，并作为新开发诊断单列。
