"""Reachability supplier only: stop at target, no orbit closure certificate."""
import field as f
import tree

def supply(g,v,target,b,coverage):
    f.need(type(target)is int and 1<=target<=tree.TARGET,'reviewed finite target')
    points=bytearray(v);seen={v:0};parents=bytearray(b'\xff\xff\xff');head=0
    coverage.update(reachable_distinct=1,generator_images_completed=0,
                    threshold=target,threshold_reached=False,orbit_closure_claimed=False)
    if target==1:
        coverage['threshold_reached']=True;return tree.encode(parents,1)
    while head<len(seen):
        for label,gen in enumerate(g):
            image=b.image(bytes(points[7*head:7*(head+1)]),gen)
            coverage['generator_images_completed']+=1
            if image not in seen:
                seen[image]=len(seen);points.extend(image);tree.put(parents,head,label)
                coverage['reachable_distinct']=len(seen)
                if len(seen)==target:
                    coverage['threshold_reached']=True
                    return tree.encode(parents,target)
        head+=1
    coverage['stop']='NO_THRESHOLD_CARRIER';return None
