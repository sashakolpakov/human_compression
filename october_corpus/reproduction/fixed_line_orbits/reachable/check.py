"""Independent actual-parent replay; imports neither discovery nor solver."""
import field as f
import tree

def consume(g,v,certificate,target,b):
    raw=tree.parse(certificate,target);points=bytearray(v);seen={v}
    for j in range(1,target):
        parent=raw[3*j]|raw[3*j+1]<<8;label=raw[3*j+2]
        f.need(parent<j and label<3,'earlier parent and actual generator label')
        image=b.image(bytes(points[7*parent:7*(parent+1)]),g[label])
        f.need(image not in seen,'all full seven-byte reached vectors distinct')
        seen.add(image);points.extend(image)
    f.need(len(seen)==target,'whole reachable distinctness coverage')
    return dict(reachable_distinct=target,parent_images_verified=target-1,
                orbit_closure_claimed=False)
