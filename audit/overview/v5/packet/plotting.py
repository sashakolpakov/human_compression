from pathlib import Path
import csv,io,json,os,textwrap
SHORT={'Representation':'Represent.','ChiralEnumeration':'Chiral','Operations':'Operations'}
def csv_text(r):
    ans={};f=io.StringIO(newline='');w=csv.writer(f,lineterminator='\n');w.writerow(['topic','title','originals','representation','sources','common','applications','written','written_factor','printed_programs','printed_factor','raw_programs','raw_factor','numerical_status'])
    for t in r['topics']:w.writerow([t['topic'],t['title'],t['source_count'],t['representation'],t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'],t['written']['decimal'],t['printed_program_cost'],None if t['including_printed_programs'] is None else t['including_printed_programs']['decimal'],t['raw_program_alternative'],None if t['including_raw_programs'] is None else t['including_raw_programs']['decimal'],t.get('numerical_status','unchanged_admitted')])
    ans['topics.csv']=f.getvalue();f=io.StringIO(newline='');w=csv.writer(f,lineterminator='\n');w.writerow(['topic','title','source','application','source_cost','application_cost','conditional_exact','conditional_factor','full_common_prepaid','full_program_or_software_prepaid','acquisition_representation','source_representation'])
    for t in r['topics']:
        for q in t['pairs']:w.writerow([t['topic'],t['title'],q['source'],q['application'],q['source_cost'],q['application_cost'],q['conditional']['exact_fraction'],q['conditional']['decimal'],t['common_theory'],t['raw_program_alternative'] if t['topic']=='Operations' else t['printed_program_cost'],'whole_raw_software_and_external_data' if t['topic']=='Operations' else 'whole_printed_programs',q['source_representation']])
    ans['applications.csv']=f.getvalue();return ans

def plot_spec(r,kind):
    rows=[]
    if kind=='whole_topics':
        for t in r['topics']:
            segments=[{'id':'common-'+k,'cost':v,'role':'common'} for k,v in t['common_components'].items()]
            segments += [{'id':q['application']+'-'+name,'cost':cost,'role':'application'} for q in t['pairs'] for name,cost in t.get('application_components',{}).get(q['application'],{q['application']:q['application_cost']}).items()]
            rows.append({'id':t['topic'],'label':SHORT.get(t['topic'],t['topic'])+': '+t['title'],'source':t['source_sum'],'segments':segments,'factor':t['written']['decimal']})
    else:
        pairs=[(t,q) for t in r['topics'] for q in t['pairs']]
        if kind=='conditional_1':pairs=pairs[:17]
        elif kind=='conditional_2':pairs=pairs[17:]
        for t,q in pairs:rows.append({'id':t['topic']+'-'+q['source'],'label':q['source']+' / '+q['application'],'topic':t['topic'],'title':t['title'],'source':q['source_cost'],'segments':[{'id':q['application']+'-'+name,'cost':cost,'role':'application'} for name,cost in t.get('application_components',{}).get(q['application'],{q['application']:q['application_cost']}).items()],'factor':q['conditional']['decimal']})
    return {'kind':kind,'rows':rows,'unit':'NFC characters without whitespace','bar_scale':'one common linear scale per chart; identical for source and replacement','candidate_scope':'All 36 candidate originals; numerical inputs are accepted and consolidated overview review remains pending'}

def draw(spec,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'overview36-operations','pdf.fonttype':42})
    rows=spec['rows'];whole=spec['kind']=='whole_topics';fig,ax=plt.subplots(figsize=(10.2,8.0 if whole else 8.6))
    fig.subplots_adjust(left=.37 if whole else .34,right=.91,top=.94,bottom=.08)
    ymax=max(max(q['source'],sum(x['cost'] for x in q['segments'])) for q in rows); ax.set_xlim(0,ymax*1.13)
    for i,row in enumerate(rows):
        b=ax.barh(i-.16,row['source'],height=.25,color='#344354');b[0].set_gid('bar-'+row['id']+'-source')
        start=0
        for j,s in enumerate(row['segments']):
            color='#286e99' if s['role']=='common' else ['#81bdb0','#61a294'][j%2]
            b=ax.barh(i+.16,s['cost'],left=start,height=.25,color=color,edgecolor='white',linewidth=.4);b[0].set_gid('bar-'+row['id']+'-'+s['id']);start+=s['cost']
        ax.text(ymax*1.14,i,f"{float(row['factor']):.3f}×",va='center',fontsize=10,clip_on=False)
    labels=['\n'.join(textwrap.wrap(q['label'] if whole else SHORT.get(q['topic'],q['topic'])+' · '+q['label'],35 if whole else 30)) for q in rows]
    ax.set_yticks(range(len(rows)),labels);ax.invert_yaxis();ax.tick_params(axis='y',length=0,pad=9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{int(x):,}'));ax.grid(axis='x',alpha=.22);ax.set_axisbelow(True)
    for spine in ['top','right','left']:ax.spines[spine].set_visible(False)
    ax.set_xlabel('NFC characters without whitespace')
    from matplotlib.patches import Patch
    handles=[Patch(color='#344354',label='Full original(s)')]
    if whole:handles.append(Patch(color='#286e99',label='Full common theory'))
    handles.append(Patch(color='#81bdb0',label='Complete application(s)'))
    fig.legend(handles=handles,loc='upper center',ncol=len(handles),frameon=False,fontsize=10)
    meta={'Creator':'Human Compression numerical candidate overview','CreationDate':None,'ModDate':None}
    fig.savefig(out/(spec['kind']+'.pdf'),metadata=meta);fig.savefig(out/(spec['kind']+'.svg'),metadata={'Date':None});plt.close(fig)

