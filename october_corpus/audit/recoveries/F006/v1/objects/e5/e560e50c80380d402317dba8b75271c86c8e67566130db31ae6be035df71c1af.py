from pathlib import Path
import shutil
W=Path(__file__).resolve().parent;S=W.parent
for model in ['E6','E7']:
    src=S/f'corpus106_F006_exceptional_work/{model}_model.g'
    (W/f'{model}_model.g').write_text(src.read_text()+'\nA:=G;;\n')
for model in ['Test','E8']:
    src=S/f'corpus106_F006_twist_work/{model}_model.g'
    setup=(S/'corpus106_F006_twist_work/enumerate_twist.g').read_text()
    setup=setup[setup.index('oldG:=G;;'):setup.index('fullAutOrder:=')]
    (W/f'{model}_model.g').write_text(src.read_text()+'\n'+setup)
(W/'Co3_model.g').write_text('G:=PrimitiveGroup(276,3);;A:=G;;expectedOrder:=495766656000;;modelName:="Co3";;\n')

