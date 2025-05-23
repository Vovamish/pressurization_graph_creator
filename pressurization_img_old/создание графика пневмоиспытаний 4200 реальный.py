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
if __name__ == "__main__":
    GSV_GSN1_distant = p_i.Pressurization()
    GSV_GSN1_distant.real_fill(obj_name = 'пневмоиспытания_4200_25', unit_time ='мин', unit_pressure='кг', working_pressure=6, points=(((0, 0), (65, 10), (137, 17), (180, 25), (198, 30), (217, 35), (240, 38), (305, 50), (410, 50), (435, 55), (508, 69), (551, 77), (611, 88), (658, 98), (694, 99), (885, 107.6), (914, 113), (937, 117), (945, 120), (969, 125), (987, 128.6), (1000, 130), (1031, 138), (1051, 138))))
    p_i.Graf_Bilder(GSV_GSN1_distant, unit_time = 'мин', unit_pressure = 'кг').create_pressurization_graph().write('пневмоиспытания_4200_25.svg', encoding='utf-8')

#print(P_R.create_nag_text())

