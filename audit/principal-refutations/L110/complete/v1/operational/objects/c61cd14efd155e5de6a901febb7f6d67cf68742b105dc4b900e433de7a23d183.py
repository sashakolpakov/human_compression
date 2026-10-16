"""Check the retained rank-three witness, without repeating its discovery."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Use ordinary Python')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'retained'))
from phase5_suzuki_check import Field,ID,W

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--certificate',type=Path,default=P/'retained'/'certificate.json')
    args=ap.parse_args()
    need(not args.out.exists(),'Fresh output')
    certificate=json.loads(args.certificate.read_text());row=certificate['rank3']
    need(row['q']==32768 and row['field_modulus']==32771,'Fixed field')
    F=Field(15,32771)
    M=(1,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0)
    r=F.U(1,0);ri=F.mpow(r,3)
    need(list(M)==certificate['F2_order15_algebra_generator'],'Fixed binary algebra')
    need(list(r)==certificate['F2_order4_normalizer'],'Fixed normalizer')
    need(not any(x^y^z for x,y,z in zip(F.mpow(M,4),M,ID)),'Polynomial relation')
    need(F.mpow(M,15)==ID and F.mpow(M,3)!=ID and F.mpow(M,5)!=ID,'Order15')
    need(F.mpow(r,4)==ID and F.mpow(r,2)!=ID,'Order4')
    need(F.mm(F.mm(ri,M),r)==F.mpow(M,2),'Binary algebra action')
    generators=[];records=[]
    for d,order,lam,params in [(3,13,5682,(893,0,5682,893,893)),
                              (5,41,624,(5992,4671,1131,5992,1831))]:
        need(lam==row[f'order{order}_scalar'],'Fixed scalar')
        need(F.power(lam,1<<d)==lam,'Scalar subfield')
        shift=tuple(x^(lam if i//4==i%4 else 0) for i,x in enumerate(M))
        a=F.mpow(shift,((1<<(4*d))-1)//order)
        need(list(a)==row[f'order{order}_matrix'],'Retained matrix identity')
        u,v,t,x,y=params
        product=F.mm(F.mm(F.mm(F.U(u,v),F.h(t)),W),F.U(x,y))
        need(product==a,'Literal Bruhat product')
        need(all(F.power(z,1<<d)==z for z in params),'Bruhat parameter subfield')
        need(F.mpow(a,order)==ID and a!=ID,'Exact prime order')
        generators.append(a)
        records.append(dict(field_degree=d,order=order,scalar=lam,
                            exponent=((1<<(4*d))-1)//order,bruhat=list(params)))
    a,b=generators;c=F.mm(a,b)
    need(F.mm(a,b)==F.mm(b,a),'Commuting polynomials')
    need(F.mpow(c,533)==ID and all(F.mpow(c,i)!=ID for i in [13,41]),'Order533')
    need(row['action_exponent']==278 and F.mm(F.mm(ri,c),r)==F.mpow(c,278),'Action278')
    need(pow(278,2,533)==532 and pow(278,4,533)==1,'Action order4')
    size=lambda q:q*q*(q*q+1)*(q-1)
    need(size(8)==29120 and size(32)==32537600,'Subfield group orders')
    need(size(8)%41!=0 and size(32)%13!=0,'Coprime exclusions')
    need(52*164//4==2132 and [20//4,52//4,164//4]==[5,13,41],'Factorization and panels')
    need(7*31*151==32767,'Composite q minus one')
    report=dict(status='PASS_FIXED_L114_WITNESS',field_nonzero_classes=32767,
                records=records,binary_orders=[15,4],torus_order=533,
                action_exponent=278,subfield_group_orders=[29120,32537600],
                intersection_orders=[20,52,164,4],panel_sizes=[5,13,41],
                old_search_repeated=False,group_elements_enumerated=0,
                rank_four_extension_used=False)
    args.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
