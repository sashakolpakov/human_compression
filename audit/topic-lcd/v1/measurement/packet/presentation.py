"""Whole-document graphs and complete-file disclosure; no theorem-count ratios."""
import csv,json,os,tempfile
from decimal import Decimal,localcontext
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'lcd-numeric-mpl'))
os.environ.setdefault('XDG_CACHE_HOME',str(Path(tempfile.gettempdir())/'lcd-numeric-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch
from calculate import DOCS,ROLES,UNITS,COMPARE,FORMS
COLORS=dict(zip(DOCS+ROLES,['#355c7d','#4d8eaa','#aa6b39','#568574','#86b4a0','#8d537b','#a47d9a','#bf913f','#d1ad70','#8292bb','#7c8996','#627166','#8fa894']))
LABELS={'L050':'L050','F017':'F017','U_LCD':'Whole U','A_L050':'A(L050)','A_F017':'A(F017)'}
ROLE_LABELS=['Required programs','Derived certificates','Mandatory data','Finite records','Optional validation','Operational drivers','Partial Lean files','Partial scope files']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','svg.hashsalt':'LCD-whole-manuscripts-v1'})
def display(q,places=6):
 with localcontext()as c:
  c.prec=50;return f"{Decimal(q['numerator'])/Decimal(q['denominator']):.{places}f}"
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def records(r):
 return [[x['variant'],x['normalization'],x['unit'],kind,k,v]for x in r['coordinates']for kind,m in [('PDF',x['costs']),('raw-role',x['raw_costs'])]for k,v in m.items()]
def fraction_records(r):
 return [[x['variant'],x['normalization'],x['unit'],k]+list(x['comparisons'][k].values())+[x['interpretation'][k]]for x in r['coordinates']for k in COMPARE]
def raw_records(r):
 return [[x['path'],x['role'],x['mathematical_premise'],x['bytes'],x['sha256'],len(x['occurrences']),f,u,x['metrics'][f][u]]for x in r['raw_file_inventory']['files']for f in FORMS for u in UNITS]
def occurrence_records(r):
 return [[x['path'],x['sha256'],x['bytes'],x['role'],x['mathematical_premise'],x['original_role'],x['application_occurrence']]for x in r['raw_file_inventory']['occurrence_bindings']]
def bars(r,name):
 c=r['primary']['costs'];q=r['primary']['raw_costs'];rows=[]
 if name=='costs':
  H=315;W=792;base=70;s=.0016
  for col,parts in [(0,['L050','F017']),(1,['U_LCD','A_L050','A_F017'])]:
   y=base
   for k in parts:rows.append(dict(id=f'cost-whole-{k}',key=k,value=c[k],x=55+col*130,y=y,w=75,h=c[k]*s));y+=c[k]*s
  for j,k in enumerate(['L050','A_L050','F017','A_F017']):rows.append(dict(id='cost-local-'+k,key=k,value=c[k],x=390+j*88,y=base,w=50,h=c[k]*.004))
 else:
  H=255;W=792;base=60
  for j,k in enumerate(ROLES):rows.append(dict(id='cost-inventory-'+k,key=k,value=q[k],x=30+j*95,y=base,w=55,h=q[k]*.0012))
 return W,H,rows

def canvas(W,H):
 fig=plt.figure(figsize=(W/72,H/72),dpi=72);ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,W);ax.set_ylim(0,H);ax.axis('off');return fig,ax

def chart(root,r,name):
 W,H,rs=bars(r,name);fig,ax=canvas(W,H)
 for b in rs:
  rect=Rectangle((b['x'],b['y']),b['w'],b['h'],facecolor=COLORS[b['key']],edgecolor='none');rect.set_gid(b['id']);ax.add_patch(rect)
  if name=='costs'and b['id'].startswith('cost-whole'):
   ax.text(b['x']+b['w']/2,b['y']+b['h']/2,LABELS[b['key']]+'\n'+f"{b['value']:,}",ha='center',va='center',fontsize=10,color='white'if b['key']!='A_F017'else'#172821')
  else:ax.text(b['x']+b['w']/2,b['y']+b['h']+6,f"{b['value']:,}",ha='center',va='bottom',fontsize=10)
 if name=='costs':
  ax.text(158,294,'Complete manuscripts',ha='center',weight='bold');ax.text(548,294,'After acquiring U and required premises',ha='center',weight='bold',fontsize=9)
  for x,label,total in [(92.5,'Both sources',r['primary']['totals']['source']),(222.5,'Whole U + both apps',r['primary']['totals']['written'])]:
   ax.text(x,49,label,ha='center',fontsize=10);ax.text(x,33,f'Total {total:,}',ha='center',fontsize=10)
  for j,k in enumerate(['L050','A_L050','F017','A_F017']):ax.text(415+j*88,49,LABELS[k],ha='center')
  ax.plot([39,278],[70,70],color='#425466',lw=.5);ax.plot([370,743],[70,70],color='#425466',lw=.5)
  ax.text(33,69,'0',ha='right',va='center',fontsize=9);ax.text(364,69,'0',ha='right',va='center',fontsize=9)
  ax.text(396,10,'NFC nonspace characters, calibrated selected text. Both panels start at zero; their scales differ.',ha='center',fontsize=10)
 else:
  ax.text(W/2,H-17,'Complete raw files by role — inventory only, no software-inclusive ratio',ha='center',weight='bold')
  labels=['Required\nprograms','Derived\ncertificates','Mandatory\ndata','Finite\nrecords','Optional\nvalidation','Operational\ndrivers','Partial Lean\nfiles','Partial scope\nfiles']
  for b,label in zip(rs,labels):ax.text(b['x']+b['w']/2,43,label,ha='center',va='top',fontsize=10)
  ax.plot([20,760],[60,60],color='#425466',lw=.5);ax.text(17,59,'0',ha='right',va='center',fontsize=9)
  ax.text(W/2,7,'Same NFC nonspace unit; raw files are not added to manuscript denominators.',ha='center',fontsize=10)
 for ext in ['svg','pdf']:fig.savefig(root/(name+'.'+ext),format=ext,metadata={'Date':None}if ext=='svg'else{'CreationDate':None,'ModDate':None})
 plt.close(fig)

def graph(r):
 c=r['primary']['costs'];a=r['acquisition'];q=r['primary']['raw_costs']
 nodes=[dict(id=k,label=LABELS[k]+'\n'+f'{c[k]:,}',kind='source'if k in DOCS[:2]else'written',cost=c[k])for k in DOCS]
 nodes += [dict(id='required',label=f"{a['required_whole_files']} required whole files\n{sum(q[k]for k in ROLES[:4]):,} raw chars",kind='conservative_preacquisition',cost=sum(q[k]for k in ROLES[:4])),dict(id='retained',label='Retained mathematical inputs\nfull proof costs unknown',kind='retained',cost=None),dict(id='optional',label='3 optional validation files\nnot proof premises',kind='optional',cost=q['optional_validation'])]
 edges=[dict(source=a,target=b,kind=k)for a,b,k in [('L050','A_L050','correspondence'),('F017','A_F017','correspondence'),('U_LCD','A_L050','common'),('U_LCD','A_F017','common'),('required','U_LCD','declared_preacquisition'),('retained','U_LCD','retained_acquisition'),('optional','U_LCD','optional_check')]]
 return dict(title='Whole-document acquisition and declared premises',not_a_theorem_DAG=True,node_counts_are_not_ratios=True,not_a_minimal_scientific_dependency_graph=True,nodes=nodes,edges=edges,initial_acquisition=['whole U_LCD','complete declared required file union','actual retained mathematical premises'],optional_checks_required=False,no_sibling_application_dependency=True,raw_and_manuscript_units_not_added=True)
POSITIONS={'L050':(102,155),'F017':(690,155),'U_LCD':(396,210),'A_L050':(250,45),'A_F017':(542,45),'retained':(120,315),'required':(396,315),'optional':(672,315)}
def graph_render(root,r):
 g=graph(r);dump(root/'document_graph.json',g);fig,ax=canvas(792,390)
 for n in g['nodes']:
  x,y=POSITIONS[n['id']];box=Rectangle((x-91,y-24),182,48,facecolor='#f3f4f5',edgecolor='#465566',lw=.8);box.set_gid('node-'+n['id']);ax.add_patch(box);ax.text(x,y,n['label'],ha='center',va='center',fontsize=10)
 for e in g['edges']:
  a=POSITIONS[e['source']];b=POSITIONS[e['target']];delta=(b[0]-a[0],b[1]-a[1]);t=min(91/abs(delta[0])if delta[0]else 100,24/abs(delta[1])if delta[1]else 100)
  start=(a[0]+t*delta[0],a[1]+t*delta[1]);end=(b[0]-t*delta[0],b[1]-t*delta[1]);dashed=e['kind']in ['correspondence','optional_check']
  edge=FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=9,lw=.8,linestyle='--'if dashed else'-',color='#526272');edge.set_gid('edge-'+e['source']+'-'+e['target']);ax.add_patch(edge)
 ax.text(396,374,'Full common theory and declared premises acquired before either local comparison',ha='center',fontsize=11,weight='bold')
 ax.text(396,356,'Dashed: source correspondence or optional checks. Solid: declared acquisition; not a minimal proof DAG.',ha='center',fontsize=10)
 for ext in ['svg','pdf']:fig.savefig(root/('document_graph.'+ext),format=ext,metadata={'Date':None}if ext=='svg'else{'CreationDate':None,'ModDate':None})
 plt.close(fig)
def texint(n):return f'{n:,}'.replace(',',r'\,')
def writecsv(root,name,header,rows):
 with(root/name).open('w',newline='')as f:w=csv.writer(f);w.writerow(header);w.writerows(rows)
def write(root,r):
 dump(root/'results.json',r);dump(root/'acquisition.json',r['acquisition']);dump(root/'plot_data.json',{name:bars(r,name)[2]for name in ['costs','inventory']})
 writecsv(root,'costs.csv',['variant','normalization','unit','representation','key','cost'],records(r))
 writecsv(root,'fractions.csv',['variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal','interpretation'],fraction_records(r))
 writecsv(root,'raw_files.csv',['file','role','mathematical_premise','whole_bytes','sha256','occurrences','normalization','unit','cost'],raw_records(r))
 writecsv(root,'raw_occurrences.csv',['path','sha256','whole_bytes','role','mathematical_premise','original_role','application_occurrence'],occurrence_records(r))
 writecsv(root,'acquisition.csv',['variant','normalization','unit','stage','complete_manuscript_cost'],[[x['variant'],x['normalization'],x['unit'],stage,cost]for x in r['coordinates']for stage,cost in zip(['whole_common','common_and_L050','common_and_both_apps'],x['acquisition']['common_then_L050_then_F017'])])
 for name in ['costs','inventory']:chart(root,r,name)
 graph_render(root,r)
 p=r['primary'];c=p['costs'];sub={'@WRITTEN@':display(p['comparisons']['written']),'@L050@':display(p['comparisons']['conditional_L050']),'@F017@':display(p['comparisons']['conditional_F017'])}
 for k,v in c.items():sub['@C_'+k+'@']=texint(v)
 for k,v in p['totals'].items():sub['@TOTAL_'+k.upper()+'@']=texint(v)
 sub['@DOCROWS@']='\n'.join(LABELS[k].replace('Whole U',r'Whole $U$')+' & '+str(r['physical_pages'][k])+' & '+texint(c[k])+r' \\'for k in DOCS)
 sub['@RAWROWS@']='\n'.join(label+' & '+str(row['whole_files'])+' & '+texint(row['whole_bytes'])+' & '+texint(p['raw_costs'][row['role']])+r' \\'for label,row in zip(ROLE_LABELS,r['raw_role_inventory']))
 sub['@REQUIRED_BYTES@']=texint(r['acquisition']['required_whole_bytes']);sub['@RAW_TOTAL@']=texint(r['raw_file_inventory']['whole_bytes']);sub['@RAW_CHARS@']=texint(sum(p['raw_costs'].values()))
 labels=['Whitespace tokens','Alphanumeric units','Nonspace characters','Collapsed characters','Collapsed UTF-8 bytes']
 sub['@SENSITIVITY@']='\n'.join(label+' & '+' & '.join(display(x['comparisons'][k])for k in COMPARE)+r' \\'for label,u in zip(labels,UNITS)for x in r['coordinates']if[x['variant'],x['normalization'],x['unit']]==['calibrated_selected','NFC',u])
 sub['@VARIANTROWS@']='\n'.join(v.replace('_',' ')+', '+f+' & '+' & '.join(display(x['comparisons'][k])for k in COMPARE)+r' \\'for v in ['raw_untrimmed','raw_selected','calibrated_selected']for f in FORMS for x in r['coordinates']if[x['variant'],x['normalization'],x['unit']]==[v,f,UNITS[2]])
 sub['@STAGES@']='; '.join(texint(x)for x in r['acquisition']['complete_written_stages'])
 template=(root/'reader_template.tex').read_text()
 for a,b in sub.items():template=template.replace(a,b)
 if '@'in template:raise ValueError('unresolved reader substitution')
 (root/'reader.tex').write_text(template)
