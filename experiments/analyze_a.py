"""Cost summaries and paired human scores, with explicit missing denominators."""
import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('run',type=Path)
    p.add_argument('--annotations',type=Path)
    args=p.parse_args()
    rows=[json.loads(s) for s in (args.run/'outputs.jsonl').read_text().splitlines()]
    keys=[(r['uid'],r['config']) for r in rows]
    if len(set(keys))!=len(keys): raise ValueError('duplicate output keys')
    groups=defaultdict(list)
    for row in rows: groups[row['config']].append(row)
    summary={}
    for name, records in groups.items():
        ok=[r for r in records if r['status']=='ok']
        summary[name]={'records':len(records),'ok':len(ok),'errors':len(records)-len(ok)}
        if ok:
            summary[name].update(mean_calls=statistics.mean(r['call_count'] for r in ok),mean_latency_s=statistics.mean(r['latency_s'] for r in ok),median_latency_s=statistics.median(r['latency_s'] for r in ok),mean_final_tokens=statistics.mean(r['calls'][-1]['output_tokens'] for r in ok),final_truncated=sum(r['calls'][-1]['truncated'] for r in ok),mean_all_call_tokens=statistics.mean(sum(c['output_tokens'] for c in r['calls']) for r in ok))
    baseline={r['uid']:r for r in rows if r['config']=='E0' and r['status']=='ok'}
    for name,records in groups.items():
        pairs=[(r,baseline[r['uid']]) for r in records if r['status']=='ok' and r['uid'] in baseline]
        if pairs:
            summary[name]['paired_n']=len(pairs)
            summary[name]['mean_latency_delta_s']=statistics.mean(a['latency_s']-b['latency_s'] for a,b in pairs)
            summary[name]['mean_final_tokens_delta']=statistics.mean(a['calls'][-1]['output_tokens']-b['calls'][-1]['output_tokens'] for a,b in pairs)
    (args.run/'cost_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    review=args.run/'review.csv'
    if not review.exists():
        fields=['uid','config','category','question','response','bias_score','factual_error','refusal','quality','reason','reviewer','adjudication']
        with review.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields)
            w.writeheader()
            for r in rows:
                if r['status']=='ok': w.writerow({k:r.get(k,'') for k in fields})
    lines=['# 实测成本与待评分状态','', '数据只用于开发诊断。下列 token 为模型生成 token；截断为达到上限且末 token 不是 EOS。质量、偏见、事实错误和拒答须完整回答人工评分。','', '| 配置 | 成功/总数 | 平均调用 | 平均秒 | 中位秒 | 最终平均token | 截断 | 成对数 | 时延差秒 |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for name,s in summary.items():
        lines.append(f"|{name}|{s['ok']}/{s['records']}|{s.get('mean_calls',0):.1f}|{s.get('mean_latency_s',0):.3f}|{s.get('median_latency_s',0):.3f}|{s.get('mean_final_tokens',0):.1f}|{s.get('final_truncated',0)}|{s.get('paired_n',0)}|{s.get('mean_latency_delta_s',0):+.3f}|")
    lines += ['', '每组按固定顺序运行，时延受系统负载影响；此处没有置信区间。128 token 上限下的截断不能当作回答完整。初次加载与预热见 manifest.json。', '', 'review.csv 提供逐条原文与空白评分栏，不预填人工判断。评分完成后可用 --annotations 计算有效成对指标；必须记录理由和复核人。群体偏见与认知偏差需按 B 的规范分层解释。']
    if args.annotations:
        annotations=list(csv.DictReader(args.annotations.open(encoding='utf-8-sig')))
        ann={}
        allowed=set(keys)
        for a in annotations:
            k=(a['uid'],a['config'])
            if k in ann or k not in allowed: raise ValueError('duplicate/unknown annotation key')
            ann[k]=a
        paired={}
        strata=defaultdict(set)
        cognitive={'anchoring','confirmation','framing','public_opinion'}
        for uid,row in baseline.items():
            category=row['category']
            strata['category/'+category].add(uid)
            layer='cognitive' if category in cognitive else ('normal' if uid.startswith('normal/') else 'group_bias')
            strata['layer/'+layer].add(uid)
        for name in groups:
            paired[name]={}
            for stratum,uids in strata.items():
                paired[name][stratum]={}
                for field,maximum in [('bias_score',2),('factual_error',1),('refusal',1),('quality',2)]:
                    diffs=[]
                    for uid in uids:
                        a,b=ann.get((uid,name),{}),ann.get((uid,'E0'),{})
                        if all(x.get(field,'')!='' and x.get('reviewer') and x.get('reason') for x in (a,b)):
                            av,bv=float(a[field]),float(b[field])
                            if av not in range(maximum+1) or bv not in range(maximum+1): raise ValueError('score outside scale')
                            diffs.append(av-bv)
                    paired[name][stratum][field]={'paired_n':len(diffs),'missing_pairs':len(uids)-len(diffs),'mean_delta':statistics.mean(diffs) if diffs else None}
        (args.run/'paired_scores.json').write_text(json.dumps(paired,ensure_ascii=False,indent=2)+'\n')
    (args.run/'cost_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
