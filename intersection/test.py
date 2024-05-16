
from intersection import Intersection
from intersection_1_1 import Intersection11
from intersection_1_2 import Intersection12
from intersection_2_2 import Intersection22

'''
TO-DO
Class Intersection() o method "get_number_from_point(point)" 
Ver sempre o ponto final do carro em cada line e fazer "get_number_from_point(point)" e atualizar o estado
'''

points1 = [(20, 64), (25.5, 64), (31, 58.5), (31, 53), (25.5, 48), (20, 48), (15, 53), (15, 58.5)]
points2 = [(109.5, 140), (115, 140), (121, 134), (121, 128.5), (121, 123), (121, 117.5), (115, 111), (109.5, 111), (104, 122.5), (104, 128)]
points3 = [(178, 140), (183.5, 140), (189, 140), (194.5, 140), (200.5, 134), (200.5, 128.5), (200.5, 123), (200.5, 117.5), (194.5, 111), (189, 111), (183.5, 111), (178, 111), (172, 117.5), (172, 123), (172, 128.5), (172, 134)]

intersection1 = Intersection11(points1)
intersection2 = Intersection12(points2)
intersection3 = Intersection22(points3)

print(intersection1.points_dict)
print(intersection1.limits)

print(intersection1.get_point_from_number(1))