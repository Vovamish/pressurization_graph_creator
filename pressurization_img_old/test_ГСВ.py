from MyLibs import pressurization_img as p_i
'''
P_I = p_i.Pressurization()
P_I.ideal_fill(obj_name = 'труба и', working_pressure=0.6, test_pressure=None, speed_percentage=5, double_pressurization=False)
p_i.Graf_Bilder(P_I).create_pressurization_graph().write('идеальный график нагружения.svg', encoding='utf-8')
#print(*P_I.T_Points['raw'])
#print(*P_I.P_Points['raw'])

P_R = p_i.Pressurization()
P_R.real_fill(obj_name = 'труба р', unit_time ='с', working_pressure=0.6, points=((0, 5), (57, 5), (110, 10), (710, 10), (760, 15), (1360, 15), (1395, 18), (1600, 18), (1620, 0), (3907, 0), (4040, 18), (4625, 18), (4670, 24), (4940, 24), (5000, 18), (5240, 18), (5400, 24), (5700, 24)))
p_i.Graf_Bilder(P_R).create_pressurization_graph().write('реальный график нагружения.svg', encoding='utf-8')
'''
GSV_GSN1_Near = p_i.Pressurization()
GSV_GSN1_Near.real_fill(obj_name = 'ГСВ_ГСН1 ближний манометр', unit_time ='с', unit_pressure='кг', working_pressure=6, points=((0, 0), (1090, 1.8), (3170, 2.2), (3545, 3), (3619, 3.5), (4707, 4.5), (4900, 4.8), (6284, 6), (7061, 6), (7285, 6.2), (7653, 6), (8336, 6), (10037, 6.7), (11406, 7), (13191, 7.6), (15355, 6), (16158, 3)))
p_i.Graf_Bilder(GSV_GSN1_Near, unit_time = 'мин', unit_pressure = 'МПа').create_pressurization_graph().write('ГСВ_ГСН1 ближний манометр.svg', encoding='utf-8')
with open('ГСВ_ГСН1 ближний манометр.nag', 'w', encoding='utf-16 LE') as nag_file:
    nag_file.write(GSV_GSN1_Near.create_nag_text())

GSV_GSN1_distant = p_i.Pressurization()
GSV_GSN1_distant.real_fill(obj_name = 'ГСВ_ГСН1 дальний манометр', unit_time ='с', unit_pressure='кг', working_pressure=6, points=((0, 0), (1219, 1.4), (3170, 1.8), (3545, 2.6), (3619, 3.1), (4707, 4.5), (4900, 5.2), (6214, 5.6), (7061, 6), (7285, 6), (7653, 6), (8336, 6), (11406, 7), (13191, 7.6), (15355, 6), (16158, 3)))
p_i.Graf_Bilder(GSV_GSN1_distant, unit_time = 'мин', unit_pressure = 'МПа').create_pressurization_graph().write('ГСВ_ГСН1 дальний манометр.svg', encoding='utf-8')
with open('ГСВ_ГСН1 дальний манометр.nag', 'w', encoding='utf-16 LE') as nag_file:
    nag_file.write(GSV_GSN1_Near.create_nag_text())

#print(P_R.create_nag_text())

