import matplotlib.pyplot as p
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
import time as t,os,subprocess,re
_=print
def e(d):return subprocess.run(["traceroute", "-I", d], capture_output=True, text=True, check=True).stdout
def pt(t):return [{'hop': int(m.group(1)), 'ip': m.group(3), 'hostname': None if m.group(2) == m.group(3) else m.group(2), 'rtt': [None, None, None] if '*' in m.group(4) else [float(r.strip()) for r in m.group(4).split('ms') if r.strip()]} for l in t.splitlines() if (m := re.match(r'(\d+)\s+([^\s]+)\s+\(([^)]+)\)\s+((?:\d+\.\d+\s+ms\s+)+|\*+\s+\*+\s+\*+|\s*)', l.strip()))]

def visualize_traceroute(destination, num_traces=3, interval=5, output_dir='output'): return __import__('pandas').DataFrame(sum([[{**h,'trace_num':i+1,'timestamp':t.strftime("%H:%M:%S")}for h in __import__('my_traceroute_module').parse_traceroute(__import__('builtins').print(f"Waiting {interval} seconds before next trace...") or __import__('time').sleep(interval) if i else None or __import__('builtins').print(f"Trace {i+1}/{num_traces}...") or __import__('my_traceroute_module').execute_traceroute(destination))] for i in range(num_traces)],[])).assign(avg_rtt=lambda d: d['rtt'].apply(lambda x: __import__('numpy').mean([r for r in x if r is not None]) if any(r is not None for r in x) else None)).pipe(lambda df: (__import__('os').makedirs(output_dir, exist_ok=True))), __import__('matplotlib.pyplot').figure(figsize=(12,6)), (__import__('matplotlib.pyplot').subplot(1,1,1)), [__import__('matplotlib.pyplot').plot(df[df['trace_num']==n]['hop'],df[df['trace_num']==n]['avg_rtt'],'o-',label=f"Trace {n} ({df[df['trace_num']==n].iloc[0]['timestamp']})") for n in range(1,num_traces+1)], __import__('matplotlib.pyplot').xlabel('Hop Number'), __import__('matplotlib.pyplot').ylabel('Average Round Trip Time (ms)'), __import__('matplotlib.pyplot').title(f'Traceroute Analysis for {destination}'), __import__('matplotlib.pyplot').grid(True,linestyle='--',alpha=0.7), __import__('matplotlib.pyplot').legend(), __import__('matplotlib.ticker').MaxNLocator(integer=True), __import__('matplotlib.pyplot').tight_layout(), __import__('matplotlib.pyplot').savefig(f"{output_dir}/trace_{destination.replace('.','-')}_{__import__('time').strftime('%Y%m%d-%H%M%S')}.png"),__import_**_
"""
def vt(d, n=3, it=5, o='output'):
    os.makedirs(o, exist_ok=True)
    ah = []
    _(f"Running {n} traceroutes to {d}...")
    [(_(f"Waiting {i} seconds before next trace..."),t.sleep(it)) if it > 0 else None or _(f"Trace {it+1}/{n}...") or [h.update({'trace_num': i + 1, 'timestamp': (ts := t.strftime('%H:%M:%S'))}) or ah.append(h) for h in pt(e(d))] for i in range(n)]
    df = pd.DataFrame(ah)
    df['avg_rtt'] = df['rtt'].apply(lambda x:np.mean([r for r in x if r is not None]) if any(r is not None for r in x) else None);p.figure(figsize=(12, 6));ax1 = p.subplot(1, 1, 1)
    for tn in range(1, n + 1):td=df[df['trace_num'] == tn],ax1.plot(td['hop'], td['avg_rtt'], 'o-',label=f'Trace {tn} ({td.iloc[0]["timestamp"]})')
    ax1.set_xlabel('Hop Number'),ax1.set_ylabel('Average Round Trip Time (ms)'),ax1.set_title(f'Traceroute Analysis for {d}'),ax1.grid(True, linestyle='--', alpha=0.7),ax1.legend(),ax1.xaxis.set_major_locator(MaxNLocator(integer=True)),p.tight_layout()
    ts = t.strftime("%Y%m%d-%H%M%S")
    of = os.path.join(o, f"trace_{d.replace('.','-')}_{ts}.png")
    p.savefig(of)
    p.close()
    _(f"Plot saved to: {of}")
    return df,of
    """
if __name__ == "__main__":[_(f"\nAverage RTT by hop for {d}:\n{(avg_by_hop := (df := vt(d, n=3, it=5)[0]).groupby('hop')['avg_rtt'].mean())}\n\n{'-'*50}\n") for d in ["google.com", "amazon.com", "bbc.co.uk"]]