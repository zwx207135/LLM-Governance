import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';

const root=path.resolve(process.argv[2]);
const work=path.resolve(process.argv[3]);
const finalPath=path.resolve(process.argv[4]);
const skill='C:/Users/ASUS/.codex/plugins/cache/openai-primary-runtime/presentations/26.1123.11515/skills/presentations';
const runtimePython='C:/Users/ASUS/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Users/ASUS/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const folder=path.join(root,'docs/c_work/closeout_supplement_20261125_v1');
const data=JSON.parse(await fs.readFile(path.join(folder,'slide_data.json'),'utf8'));
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
await fs.mkdir(work,{recursive:true});
await fs.mkdir(path.dirname(finalPath),{recursive:true});
const p=Presentation.create({slideSize:{width:1280,height:720}});
const FONT='Microsoft YaHei';
const NAVY='#153B50', INK='#172936', MUTED='#526875', WHITE='#FFFFFF', TEAL='#197F82';
function text(slide,value,left,top,width,height,size=23,bold=false,color=INK){
  const box=slide.shapes.add({geometry:'textbox',position:{left,top,width,height},fill:'none',line:{fill:'none',width:0}});
  box.text=value;
  box.text.style={typeface:FONT,fontSize:`${size}pt`,bold,color,insets:0,autoFit:'none',wrap:'square'};
  return box;
}
function slide(title,sub,notes){
  const s=p.slides.add(); s.background.fill=WHITE;
  text(s,title,64,46,1152,68,34,true,NAVY);
  if(sub)text(s,sub,66,126,1148,56,19,false,MUTED);
  s.speakerNotes.text=notes;
  return s;
}
function table(s,values,left,top,width,height,widths){
  const t=s.tables.add({rows:values.length,columns:values[0].length,left,top,width,height,columnWidths:widths,values});
  t.borders.assign({fill:'#DBE4E9',width:1,style:'solid'});
  for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){
    const cell=t.getCell(r,c); cell.fill=r===0?NAVY:(r%2===0?'#F3F7F9':WHITE);
    cell.text.style={typeface:FONT,fontSize:'19pt',bold:r===0,color:r===0?WHITE:INK,verticalAlignment:'middle',insets:12};
  }
  return t;
}
let s=slide('幻觉数据与证据边界','C负责数据核验、知识检索与抗幻组件；当前结论限定在开发阶段',
  '讲述约45秒。来源：docs/c_work/data_audit.json；data_usage.json；pending_repairs_v2/report.md；knowledge/corpus_v4.json。原始125题保留，22条是开发不确定性探针，不等同22道原题均已被证伪；5个原始目标仍未核实。来源台账和入库材料分开，未把参考答案导入检索内容。');
table(s,[['交付对象','当前证据','适用边界'],
 ['原始幻觉题集','125题，五类各25题','保留原题和修订记录'],
 ['不确定性探针','22条移除未确认真值','未找到资料不等于不存在'],
 ['开发知识库','21个来源，31个片段','主题覆盖有限，正式冻结待确认']],64,210,1152,292,[295,350,507]);
text(s,'仍待核实的原始目标：33、34、37、41、42',68,551,1140,44,24,true,TEAL);
text(s,'数据修订、未知边界和来源记录可追溯；尚未形成全部批准的正式题集',68,613,1140,43,19,false,MUTED);

s=slide('检索与回答约束','BM25词面排序与主题过滤；证据注入采用固定提示词',
  '讲述约50秒。方法参考：Robertson & Zaragoza (2009), DOI 10.1561/1500000019，第3.4—3.5节；Lewis et al. (2020), https://arxiv.org/abs/2005.11401。实现来源：src/governance/retrieval.py、anti_hallucination.py、configs/c_component_profile.json。当前k1=1.5、b=0.75，平滑IDF；主题锚点、消歧及年份别名为本项目规则。未联合训练检索器与生成器，不复现原论文RAG-Sequence/RAG-Token；论文提升幅度不作为本项目实测结果。');
table(s,[['开发条件','外部检索','回答约束'],['baseline','关闭','关闭'],['constraint','关闭','开启'],['retrieval','开启','关闭'],['combined','开启','开启']],64,206,680,338,[290,195,195]);
text(s,'实际参数',810,214,370,48,26,true,NAVY);
text(s,'top_k = 2\nmin_score = 1.5',810,285,370,108,25,false,INK);
text(s,'数学题绕过无关检索\n无命中如实记录',810,425,370,104,22,false,TEAL);
text(s,'每条保留实际证据、来源与版本；检索相关不等于支持完整回答',66,594,1140,64,22,false,MUTED);

s=slide('30条检索支持分析','30个不同开发问题，逐条保存证据与判断理由',
  '讲述约45秒。数据来源：docs/c_work/retrieval_support_30_v1.json。类别与样本数来自原JSON：supports_core16、supports_core_with_scope1、supports_premise_correction_only2、topic_only_insufficient2、no_retrieved_evidence8、retrieval_miss_with_available_evidence1。总计30。全部为AI开发诊断，独立真人评分0；图展示证据支持范围，不是事实正确率或治理提升幅度。');
const counts=data.retrieval_support_counts;
const chart=s.charts.add('bar',{
  position:{left:62,top:205,width:1148,height:348},
  categories:['核心支持','需组合与范围','仅纠正前提','主题相关不足','无检索资料','库内有资料但漏检'],
  series:[{name:'问题数',values:[counts.supports_core,counts.supports_core_with_scope,counts.supports_premise_correction_only,counts.topic_only_insufficient,counts.no_retrieved_evidence,counts.retrieval_miss_with_available_evidence],fill:TEAL}],
  barOptions:{direction:'bar',grouping:'clustered',gapWidth:55},hasLegend:false,
  xAxis:{min:0,max:18,majorUnit:3,numberFormatCode:'0',textStyle:{typeface:FONT,fontSize:'17pt'}},
  yAxis:{textStyle:{typeface:FONT,fontSize:'17pt'}},
  dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0',textStyle:{typeface:FONT,fontSize:'18pt'}},
  chartFill:WHITE,plotAreaFill:WHITE
});
applyPresentationChartFont(chart,{fontFamily:FONT});
text(s,'AI开发诊断，独立人工评分为0；这些数量不能当作正式正确率',68,592,1142,63,22,true,NAVY);

s=slide('检索改善与生成失败','保留正反结果，区分召回问题、证据不足和生成错用',
  '讲述约50秒。来源：docs/c_work/C_FAILURE_EVIDENCE.md、failure_evidence_ledger_v1.json、anchor_diagnostics_summary.json、C_EVIDENCE_USE.md、closeout_supplement_20261125_v1/temporal_cases.json。125题回归中15题去掉贝尔误召回，其余110题不变，这不是15题全部答对。第76题有相对论资料却仍将贡献归给牛顿；第94题只给来源而未完成任务。时间专项明确区分旧任人物与其他日期/主体错误；不能反推原生成时间或训练截止。');
table(s,[['现象','实际观察','解释'],
 ['词项碰撞修复','125题中15题减少误召回','检索改善，非答案全对'],
 ['主体归因错配','有资料仍把相对论归给牛顿','生成未遵循证据'],
 ['只给来源不作答','真实链接仍未回答原问题','引用有效与任务完成分开'],
 ['当前身份与日期错误','时间专项绑定原文与截至日','不一律归因为知识过时']],64,204,1152,350,[260,460,432]);
text(s,'不稳定候选保留为负面结果；默认方案没有因局部改善而整体替换',68,601,1144,58,22,false,TEAL);

s=slide('知识更新与结论范围','以版本、来源日期与哈希保留旧结果的复现路径',
  '讲述约50秒。来源：knowledge/build_manifest_v4.json、docs/c_work/c_work_inventory.json、C_COMPONENT_HANDOFF.md、closeout_supplement_20261125_v1/SOURCE_DATES.md、A_HANDOFF.md、REPRODUCTION.md。开发运行16个目录1316条输出，其中1311次模型调用、5条程序拒答，跨轮有重复，不是独立样本量。A的12条开发输入与36条正常任务目前48条全部无命中；导出是真实覆盖结果，不证明联合治理有效。正式评分、B/C交叉检查与共同冻结仍待完成。');
text(s,'旧结果',67,219,255,55,28,true,NAVY);
text(s,'旧数据＋旧语料＋旧源码＋旧模型哈希\n保存原回答，重放实际证据',335,219,830,110,23,false,INK);
text(s,'新知识',67,365,255,55,28,true,NAVY);
text(s,'新建语料和配置版本，另建运行目录\n更新日期、发表日期、采集日期分别记录',335,365,830,110,23,false,INK);
text(s,`${data.inventory.outputs}条开发输出含重复；正式正确率及独立人工一致率尚未产生`,68,538,1144,56,21,false,MUTED);
text(s,'当前A输入48条均无命中；跨模块覆盖范围与正式接入仍需共同确认',68,611,1144,46,21,true,TEAL);

await fs.writeFile(path.join(work,'slides.inspect.ndjson'),(await p.inspect({select:'$.slides[*].elements[*]',include:['id','text','position','style']})).ndjson ?? '');
for(let i=0;i<p.slides.items.length;i++){
  const png=await p.export({slide:p.slides.items[i],format:'png',scale:1});
  await fs.writeFile(path.join(work,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
const candidatePath=path.join(work,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidatePath);
const result=await finalizePresentation({workspaceDir:root,candidatePath,finalPath,
  pythonExecutable:runtimePython,
  integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...([1,2,4].flatMap(n=>['--require-native-table-slide',String(n)]))],
  explicitTotalSlideCount:5,requiredNativeTableOwnerSlides:[1,2,4],requiredNativeChartOwnerSlides:[3],
  materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,
  receiptPath:path.join(work,'validation.json')});
console.log(JSON.stringify({slides:5,finalPath,validation:result}));
