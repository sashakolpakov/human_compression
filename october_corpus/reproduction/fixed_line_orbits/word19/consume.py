"""UNRUN independent full carrier verification; no BFS or solver import."""
import sys
import runtime as rt
import field as f
import common,check19

def main(argv):
    mp,msha,jp,jsha,out=rt.arguments(argv);b,job,pins=rt.startup(mp,msha,jp,jsha)
    rt.origins(pins,__file__,f,common,check19,check19.verify)
    rt.need(set(job)=={'schema','end_id','end_marks','certificate','context_refs'}and
            job['schema']=='F004_ORDER19_FIXED_SEED_CONSUMER_V1','exact independent consumer job')
    context=rt.provenance(job,b);name=common.end_id(job,b);complete=False
    try:
        g=common.marks(job['end_marks'],b);answer=check19.consume(g,job['certificate'],b);complete=True
    except rt.Limit as stop:
        answer=dict(status='INCONCLUSIVE_UNPAID',resource_stop=str(stop),original_case_credit=0)
    proof=dict(schema='F004_ORDER19_FIXED_SEED_CONSUMER_PROOF_V1',end_id=name,input_pins=pins,context=context,
               certificate=job['certificate']if complete else None,Root_authority=False,
               supplier_or_solver_imported=False,original_case_credit=0)
    rt.close_inputs(b)
    result=dict(schema='F004_ORDER19_FIXED_SEED_CONSUMER_RESULT_V1',answer=answer,end_id=name,
                counts=b.snapshot(),Root_authority=False,original_case_credit=0)
    outputs=rt.emit(out,result,proof,b);print(rt.encoded(dict(status=answer['status'],outputs=outputs)).decode(),end='')

if __name__=='__main__':main(sys.argv)
