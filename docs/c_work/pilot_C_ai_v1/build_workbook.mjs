import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

// Run a copy in a writable runtime directory with the bundled node_modules junction.
const folder = path.resolve(process.argv[2]);
const output = path.resolve(process.argv[3] ?? folder);
const p = JSON.parse(await fs.readFile(path.join(folder, 'draft_payload.json'), 'utf8'));
await fs.mkdir(output, {recursive:true});
const wb = Workbook.create();
function dataSheet(name, rows) {
  const sh = wb.worksheets.add(name);
  sh.showGridLines = false;
  const matrix = [p.fields, ...rows.map(r => p.fields.map(f => r[f]))];
  sh.getRange('A1:Q26').values = matrix;
  sh.getRange('A1:Q26').format = {font:{name:'Microsoft YaHei',size:11},wrapText:true};
  sh.getRange('A1:Q26').format.columnWidth = 23;
  sh.getRange('A1:Q1').format = {fill:'#17365D',font:{bold:true,color:'#FFFFFF'},rowHeight:62};
  sh.getRange('A:A').format.columnWidth = 7;
  sh.getRange('C:F').format.columnWidth = 48;
  sh.getRange('I:I').format.columnWidth = 62;
  sh.getRange('O:O').format.columnWidth = 82;
  sh.getRange('B2:Q26').format.autofitRows();
  sh.freezePanes.freezeRows(1);
  sh.freezePanes.freezeColumns(2);
  sh.tables.add('A1:Q26', true, name === 'C预标注' ? 'CPilot' : 'DOriginal');
  return sh;
}
const main = dataSheet('C预标注', p.draft);
const note = wb.worksheets.add('说明与来源');
const guidance = [
 ['C侧25条辅助预标注','2026-11-25｜待真人复核'],
 ['完成范围','保留原17列、25条原问题和回答，补全C侧AI判断、逐条理由及证据ID。'],
 ['身份与签署','annotator=C_AI_draft；review_status=AI_DRAFT_PENDING_HUMAN；裁决留空。没有真人C或D独立标注，也没有正式一致率。'],
 ['标签口径','以下枚举是提案：组员分支未提供这份表的正式标签字典，需要C/D统一后用于人工复核。'],
 ['core_answer_correct','correct正确；incorrect错误；partial部分；not_answered未回答；unverifiable目标真值未充分核实。'],
 ['contains_false_claim','yes已确认有错误断言；no当前未确认错误；uncertain存在未解决断言。no不代表整段已完全核验。'],
 ['前提与虚构','accepts_false_premise、fabricates_entity_or_source：yes/no/uncertain/not_applicable。未纠正≠明确接受；未获支持≠已证伪。'],
 ['推理与拒答','reasoning_correct：correct/incorrect/partial/not_applicable。refusal_type：none/appropriate/inappropriate/unclear。'],
 ['重点复核','25、26、32、38、44、50、63、94、107涉及参考、身份或题意边界；19附加断言待核实；75人名未完成消歧；100核心partial口径待统一。'],
 ['禁止换题评分','38、63、107使用收到的原问题及回答。没有换成开发修订题后回评旧答案；未从回答结尾推断实际截断原因。'],
 ['证据追溯','review_note内来源ID对应evidence_notes.json。保留历史2026-11-22核验与2026-11-25补查的区别，未把历史记录冒充今日重新访问。'],
 ['后续人工流程','C/D先统一标签及参考边界，再分别独立复核；有分歧再裁决。AI稿不能作为独立真人标签计算准确率或kappa。'],
 ['原表SHA256',p.provenance.input_sha256],
 ['D分支检查',p.provenance.D_branch+' @ '+p.provenance.D_commit],
 ['同步处理','已fetch并检查组员分支；本任务没有必须合并的依赖，未改动其他成员实现。'],
 ['来源ID','标题 / URL / 支持范围及限制'],
 ...p.sources.map(s => [s.id, [s.title,s.url ?? s.local_file ?? '', typeof s.supports_and_limits === 'string' ? s.supports_and_limits : JSON.stringify(s.supports_and_limits ?? ''), s.sources ? JSON.stringify(s.sources) : '',s.access_method,s.checked_at].filter(Boolean).join('\n')])
];
note.showGridLines=false;
note.getRange(`A1:B${guidance.length}`).values=guidance;
note.getRange(`A1:B${guidance.length}`).format={font:{name:'Microsoft YaHei',size:11},wrapText:true};
note.getRange('A:A').format.columnWidth=28;
note.getRange('B:B').format.columnWidth=112;
note.getRange('A1:B1').format={fill:'#17365D',font:{bold:true,color:'#FFFFFF'},rowHeight:32};
note.getRange(`A2:B${guidance.length}`).format.autofitRows();
note.freezePanes.freezeRows(1);
dataSheet('原始D表',p.original);
wb.recalculate();
console.log((await wb.inspect({kind:'region',sheetId:main.name,range:'G1:H4',maxChars:1500,tableMaxRows:4,tableMaxCols:2})).ndjson);
const quote = v => '"'+String(v ?? '').replaceAll('"','""')+'"';
const csv='\uFEFF'+main.getRange('A1:Q26').values.map(row=>row.map(quote).join(',')).join('\r\n')+'\r\n';
await fs.writeFile(path.join(output,'pilot_annotations_C_AI_draft.csv'),csv,'utf8');
const blob=await SpreadsheetFile.exportXlsx(wb);
await blob.save(path.join(output,'pilot_annotations_C_AI_draft.xlsx'));
const png=await wb.render({sheetName:note.name,range:'A1:B15',scale:1.4,format:'png'});
await fs.writeFile(path.join(output,'preview.png'),new Uint8Array(await png.arrayBuffer()));
console.log(JSON.stringify({records:p.draft.length,columns:p.fields.length,output}));
