"""UNRUN strict9241 supplier from a freshly verified order19 fixed seed."""
import sys
import runtime as rt
import field as f
import common,prime_seed,tree,search

def main(argv):
    mp,msha,jp,jsha,out=rt.arguments(argv);b,job,pins=rt.startup(mp,msha,jp,jsha)
    rt.origins(pins,__file__,f,common,prime_seed,tree,search)
    rt.need(set(job)=={'schema','end_id','end_marks','word','seed','context_refs'}and
            job['schema']=='F004_ORDER19_REACHABILITY_SUPPLIER_V1','exact supplier job')
    context=rt.provenance(job,b);name=common.end_id(job,b);certificate=None;coverage={}
    try:
        g=common.marks(job['end_marks'],b);v=prime_seed.begin(g,job['seed'],job['word'],b)
        certificate=search.supply(g,v,9241,b,coverage)
        status='SUPPLIED_9241_REACHABILITY_UNADOPTED'if certificate else 'INCONCLUSIVE_UNPAID'
    except rt.Limit as stop:
        status='INCONCLUSIVE_UNPAID';coverage['resource_stop']=str(stop)
    proof=dict(schema='F004_ORDER19_REACHABILITY_SUPPLIER_PROOF_V1',end_id=name,
               input_pins=pins,context=context,certificate=certificate,coverage=coverage,
               Root_authority=False,original_case_credit=0)
    rt.close_inputs(b)
    result=dict(schema='F004_ORDER19_REACHABILITY_SUPPLIER_RESULT_V1',status=status,
                counts=b.snapshot(),Root_authority=False,original_case_credit=0)
    outputs=rt.emit(out,result,proof,b);print(rt.encoded(dict(status=status,outputs=outputs)).decode(),end='')

if __name__=='__main__':main(sys.argv)
