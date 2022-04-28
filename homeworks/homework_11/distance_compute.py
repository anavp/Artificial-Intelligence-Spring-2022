import math


def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

a = (352, 768)
b = (933, 1093)
c = (192, 539)
d = (293, 422)
e = (512, 858)
f = (444, 23)
g = (4, 9)
h = (1077, 380)
i = (1033, 905)
j = (701, 639)

A = (521.67, 755.00)
B = (1014.33, 792.67)
C = (233.25, 248.25)

def compute_distance(pt1, pt2):
	x1, y1 = pt1
	x2, y2 = pt2
	return math.sqrt((x1 - x2)**2 + (y1-y2)**2)


def distances():
	for iter1 in range(10):
		pt1 = eval(chr(97+iter1))
		print(namestr(pt1, globals()), end = ': ')
		print(pt1, end = ": ")
		for iter2 in range(3):
			# print("iter1: " + str(iter1))
			# print("iter2: " + str(iter2))
			pt2 = eval(chr(65+iter2))
			if iter2 < 2:
				print("{:.1f}".format(compute_distance(pt1, pt2)), end = " & ")
			else:
				print("{:.1f}".format(compute_distance(pt1, pt2)), end = "\\\\")
			# print(namestr(pt2, globals()), end = ": ")
			# print(pt2)
			# print("distance: " + str(compute_distance(pt1, pt2)), end = "\n\n")
			# break
		print("\n")


if __name__ == '__main__':
	distances()
	pass