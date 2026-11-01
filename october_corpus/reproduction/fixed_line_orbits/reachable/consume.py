"""UNRUN strict9241 replay and prime19 lower bound, not a full-G2 verdict."""
import sys
import runtime as rt
import field as f
import common,prime_seed,tree,check

def main(argv):
    mp,msha,jp,jsha,out=rt.arguments(argv);b,job,pins=rt.startup(mp,msha,jp,jsha)
    rt.origins(pins,__file__,f,common,prime_seed,tree,check)
    rt.need(set(job)=={'schema','end_id','end_marks','word','seed','certificate','context_refs'}and
            job['schema']=='F004_ORDER19_REACHABILITY_CONSUMER_V1','exact strict9241 consumer job')
    context=rt.provenance(job,b);name=common.end_id(job,b);complete=False
    try:
        g=common.marks(job['end_marks'],b);v=prime_seed.begin(g,job['seed'],job['word'],b)
        answer=check.consume(g,v,job['certificate'],9241,b);complete=True
        answer.update(status='VERIFIED_9241_REACHABLE_AND_ORDER19_STABILIZER_ONLY',
                      concrete_end_order_lower_bound=175579,full_G2_or_IP_authority=False)
    except rt.Limit as stop:
        answer=dict(status='INCONCLUSIVE_UNPAID',resource_stop=str(stop))
    proof=dict(schema='F004_ORDER19_REACHABILITY_CONSUMER_PROOF_V1',end_id=name,
               input_pins=pins,context=context,certificate=job['certificate']if complete else None,
               Root_authority=False,supplier_discovery_or_solver_imported=False,original_case_credit=0)
    rt.close_inputs(b)
    result=dict(schema='F004_ORDER19_REACHABILITY_CONSUMER_RESULT_V1',answer=answer,
                counts=b.snapshot(),Root_authority=False,original_case_credit=0)
    outputs=rt.emit(out,result,proof,b);print(rt.encoded(dict(status=answer['status'],outputs=outputs)).decode(),end='')

if __name__=='__main__':main(sys.argv)
