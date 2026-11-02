"""Ten new admission tests; metadata never substitutes for word verification."""
import sys
import runtime as rt
import verify_intersection as api
def tests(b):
    d=dict(schema='F004_PORTABLE_TWO_END_WORD_INTERSECTION_CASE_V1',original_job=[20,4],position=0,original_row_id='synthetic',marks=[],LEFT_word=[],RIGHT_word=[],RIGHT_positive_power=1,expected_middle_order=4,provenance={},external_premises='Untrusted descriptive metadata, not a matrix verdict.')
    names=[]
    def no(name,fn):
        try:fn()
        except ValueError:names.append(name);return
        raise ValueError(name)
    rt.need(api.header(d)is d,'closed header');names.append('closed_header_preserves_untrusted_metadata')
    no('header_alone_not_matrix_verdict',lambda:api.verify_case(d,b))
    rt.need(api.case_path('verify_intersection.py')==api.ROOT/'verify_intersection.py','relative Source path');names.append('relative_local_path_accepted_without_case_authority')
    no('existing_outside_package_case_path_refused',lambda:api.case_path('../fixed_line_orbits/runtime/supervise_validation.py'))
    no('bool_subject_position_refused',lambda:api.header(dict(d,position=True)))
    no('extra_Root_authority_field_refused',lambda:api.header(dict(d,Root_authority=True)))
    no('bool_expected_middle_order_refused',lambda:api.header(dict(d,expected_middle_order=True)))
    no('whole_case_SHA_mismatch_refused',lambda:api.decode_case(rt.encoded(d),'f'*64,b))
    raw=b'{"schema":0,"schema":1}'
    no('duplicate_case_key_refused',lambda:api.decode_case(raw,rt.digest(raw),b))
    raw=b' '*131073
    no('case131073_extent_refused_before_parse',lambda:api.decode_case(raw,rt.digest(raw),b))
    rt.need(len(names)==len(set(names))==10,'all10 new loader designs');return names
def main():
    b,a,pins=api.start(sys.argv,'admission');api.origin(sys.modules[__name__],'intersection_admission.py')
    names=tests(b);api.close(b)
    outputs=api.emit(a.output,dict(status='PASS',admission_count=10,names=names,Original_inputs_loaded=False),dict(Source=pins,counts=b.snapshot()),b)
    sys.stdout.buffer.write(rt.encoded(dict(status='PASS',count=10,outputs=outputs)))
if __name__=='__main__':main()
