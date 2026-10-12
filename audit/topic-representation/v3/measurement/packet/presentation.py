"""Readable numerical tables and whole-document acquisition; no theorem DAG."""
import csv,json,os,tempfile
from decimal import Decimal,localcontext
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'representation-numeric-mpl'))
os.environ.setdefault('XDG_CACHE_HOME',str(Path(tempfile.gettempdir())/'representation-numeric-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch
from calculate import DOCS,ROLES,UNITS,COMPARE
COLORS={'F010':'#355c7d','L126':'#4d8eaa','U_R':'#aa6b39','R1':'#70a288','R2':'#9ac2b0','CODE':'#665a8e','required_finite_certificate':'#8d537b','required_graph_data':'#cc9d53','optional_validation':'#8a91ba','current_orchestration_driver':'#7c8996','partial_formal_evidence':'#627166'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','svg.hashsalt':'Representation-L126-v2'})
def display(q):
 with localcontext()as c:
  c.prec=50;return f"{Decimal(q['numerator'])/Decimal(q['denominator']):.6f}"
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def records(r):
 rows=[]
 for x in r['coordinates']:
  for k,v in x['costs'].items():rows.append([x['variant'],x['normalization'],x['unit'],'PDF',k,v])
  for k,v in x['raw_costs'].items():rows.append([x['variant'],x['normalization'],x['unit'],'raw-role',k,v])
 return rows

def bars(r,name):
 c=r['primary']['costs'];q=r['primary']['raw_costs'];rows=[]
 if name=='costs':
  H=300;W=792;base=70;s=.002
  for col,parts in [(0,['F010','L126']),(1,['U_R','R1','R2'])]:
   y=base
   for k in parts:rows.append(dict(id=f'cost-whole-{k}',key=k,value=c[k],x=65+col*115,y=y,w=60,h=c[k]*s));y+=c[k]*s
  for j,k in enumerate(['F010','R1','L126','R2']):rows.append(dict(id='cost-local-'+k,key=k,value=c[k],x=390+j*80,y=base,w=46,h=c[k]*.0045))
 else:
  H=265;W=792;base=65
  for j,k in enumerate(['CODE']+ROLES):
   v=c['CODE']if k=='CODE'else q[k]
   rows.append(dict(id='cost-inventory-'+k,key=k,value=v,x=52+j*125,y=base,w=62,h=v*.0044))
 return W,H,rows

def canvas(W,H):
 fig=plt.figure(figsize=(W/72,H/72),dpi=72);ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,W);ax.set_ylim(0,H);ax.axis('off');return fig,ax

def chart(root,r,name):
 W,H,rs=bars(r,name);fig,ax=canvas(W,H)
 for b in rs:
  rect=Rectangle((b['x'],b['y']),b['w'],b['h'],facecolor=COLORS[b['key']],edgecolor='none');rect.set_gid(b['id']);ax.add_patch(rect)
  if name=='costs'and b['id'].startswith('cost-whole'):
   ax.text(b['x']+b['w']/2,b['y']+b['h']/2,b['key']+'\n'+f"{b['value']:,}",ha='center',va='center',fontsize=8,color='white')
  else:ax.text(b['x']+b['w']/2,b['y']+b['h']+6,f"{b['value']:,}",ha='center',va='bottom',fontsize=8)
 if name=='costs':
  ax.text(145,280,'Complete manuscripts',ha='center',weight='bold');ax.text(535,280,'Local applications after acquiring U and premises',ha='center',weight='bold',fontsize=9)
  for x,label,total in [(95,'Both sources',r['primary']['totals']['source']),(210,'Whole U + R1 + R2',r['primary']['totals']['written'])]:
   ax.text(x,49,label,ha='center',fontsize=8);ax.text(x,32,f'Total {total:,}',ha='center',fontsize=8)
  for j,k in enumerate(['F010','R1','L126','R2']):ax.text(413+j*80,49,k,ha='center')
  ax.text(396,9,'NFC characters excluding whitespace, calibrated selected text. Separate panels use separate scales.',ha='center',fontsize=8)
 else:
  ax.text(W/2,H-18,'Complete software / data inventory — no software-inclusive factors',ha='center',weight='bold')
  labels=['Printed code\n(all 10 files)','Required\ncertificate (raw)','Required\ngraph JSON','Optional\n9 checks (raw)','2 orchestration\nhelpers (raw)','4 partial Lean\nfiles (raw)']
  for b,label in zip(rs,labels):ax.text(b['x']+b['w']/2,47,label,ha='center',va='top',fontsize=8)
  ax.text(W/2,8,'Printed code and the 10 raw programs are alternative representations. JSON is additional required data.',ha='center',fontsize=8)
 for ext in ['svg','pdf']:fig.savefig(root/(name+'.'+ext),format=ext,metadata={'Date':None}if ext=='svg'else{'CreationDate':None,'ModDate':None})
 plt.close(fig)

def graph(r):
 c=r['primary']['costs'];q=r['primary']['raw_costs']
 nodes=[dict(id=k,label=k+'\n'+f'{c[k]:,}',kind='source'if k in DOCS[:2]else'written',cost=c[k])for k in DOCS[:5]]
 nodes += [dict(id='certificate',label='Required certificate\n6,070 raw chars',kind='required',cost=q['required_finite_certificate']),dict(id='data',label='Whole graph JSON\n19,315 raw chars',kind='required',cost=q['required_graph_data']),dict(id='optional',label='9 optional checks\n28,753 raw chars',kind='optional',cost=q['optional_validation']),dict(id='external',label='Retained classical inputs\nfull costs unknown',kind='retained',cost=None)]
 edges=[dict(source=a,target=b,kind=k)for a,b,k in [('F010','R1','correspondence'),('L126','R2','correspondence'),('U_R','R1','common'),('U_R','R2','common'),('data','certificate','required_input'),('certificate','R2','required_input'),('optional','R1','optional_check'),('optional','R2','optional_check'),('external','U_R','retained_input'),('external','R1','retained_input'),('external','R2','retained_input')]]
 return dict(title='Whole-document acquisition and evidence association',not_a_theorem_DAG=True,node_counts_are_not_ratios=True,nodes=nodes,edges=edges,initial_acquisition=['U_R','actual retained classical premises'],additional_L126_required=['certificate','data'],optional_checks_required=False,no_sibling_application_dependency=True)

POSITIONS={'F010':(90,265),'L126':(702,265),'U_R':(396,265),'R1':(220,145),'R2':(565,145),'external':(396,375),'data':(696,28),'certificate':(535,28),'optional':(135,28)}
def graph_render(root,r):
 g=graph(r);dump(root/'document_graph.json',g);fig,ax=canvas(792,440);boxes={}
 for n in g['nodes']:
  x,y=POSITIONS[n['id']];box=Rectangle((x-77,y-23),154,46,facecolor='#f3f4f5',edgecolor='#465566',lw=.8);box.set_gid('node-'+n['id']);ax.add_patch(box);boxes[n['id']]=box;ax.text(x,y,n['label'],ha='center',va='center',fontsize=8)
 for e in g['edges']:
  a=POSITIONS[e['source']];b=POSITIONS[e['target']];delta=(b[0]-a[0],b[1]-a[1]);t=min(77/abs(delta[0])if delta[0]else 100,23/abs(delta[1])if delta[1]else 100)
  start=(a[0]+t*delta[0],a[1]+t*delta[1]);end=(b[0]-t*delta[0],b[1]-t*delta[1]);dashed=e['kind']in ['correspondence','optional_check']
  edge=FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=9,lw=.8,linestyle='--'if dashed else'-',color='#526272',connectionstyle='arc3,rad=0');edge.set_gid('edge-'+e['source']+'-'+e['target']);ax.add_patch(edge)
 ax.text(396,428,'Whole-document acquisition; solid arrows are prerequisites',ha='center',fontsize=10,weight='bold');ax.text(396,410,'Dashed arrows identify source correspondence or optional checks. This is not a theorem dependency DAG.',ha='center',fontsize=8)
 for ext in ['svg','pdf']:fig.savefig(root/('document_graph.'+ext),format=ext,metadata={'Date':None}if ext=='svg'else{'CreationDate':None,'ModDate':None})
 plt.close(fig)

def write(root,r):
 dump(root/'results.json',r);dump(root/'acquisition.json',r['acquisition']);dump(root/'plot_data.json',{name:bars(r,name)[2]for name in ['costs','inventory']})
 with(root/'costs.csv').open('w',newline='')as f:
  w=csv.writer(f);w.writerow(['variant','normalization','unit','representation','key','cost']);w.writerows(records(r))
 with(root/'fractions.csv').open('w',newline='')as f:
  w=csv.writer(f);w.writerow(['variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal'])
  for x in r['coordinates']:
   for k in COMPARE:w.writerow([x['variant'],x['normalization'],x['unit'],k]+list(x['comparisons'][k].values()))
 # Raw files are represented once per actual normalization/unit, not repeated for PDF variants.
 a=json.loads((root/'inputs/input_author_counts.json').read_text())
 with(root/'raw_files.csv').open('w',newline='')as f:
  w=csv.writer(f);w.writerow(['file','role','whole_bytes','sha256','normalization','unit','cost'])
  for row in r['raw_file_inventory']['files']:
   for form in ['NFC','NFKC']:
    for unit in UNITS:w.writerow([row['key'],row['role'],row['bytes'],row['sha256'],form,unit,a['raw_files'][row['key']]['metrics'][form][unit]])
 for name in ['costs','inventory']:chart(root,r,name)
 graph_render(root,r)
 template=(root/'reader_template.tex').read_text();p=r['primary'];c=p['costs']
 substitutions={'@WRITTEN@':display(p['comparisons']['written']),'@F010@':display(p['comparisons']['conditional_F010']),'@L126@':display(p['comparisons']['conditional_L126'])}
 rows=[]
 labels={'whitespace_tokens':'Whitespace tokens','alphanumeric_units':'Alphanumeric units','characters_without_whitespace':'Nonspace characters','characters_with_collapsed_whitespace':'Collapsed characters','utf8_bytes_with_collapsed_whitespace':'Collapsed UTF-8 bytes'}
 for u in UNITS:
  x=next(x for x in r['coordinates']if x['variant']=='calibrated_selected'and x['normalization']=='NFC'and x['unit']==u)
  rows.append(labels[u]+' & '+' & '.join(display(x['comparisons'][k])for k in COMPARE)+r' \\')
 substitutions['@SENSITIVITY@']='\n'.join(rows)
 raw=next(x for x in r['coordinates']if x['variant']=='raw_untrimmed'and x['normalization']=='NFC'and x['unit']=='characters_without_whitespace')
 substitutions['@RAW@']=display(raw['comparisons']['written'])
 for a,b in substitutions.items():template=template.replace(a,b)
 (root/'reader.tex').write_text(template)
