
import math
import numpy as np


'''用于模拟的一些函数'''
def func(x, kind):
	if kind == 0:
		return x * x
	elif kind == 1:
		return 1 - (1 - x) * (1 - x)
	elif kind == 2:
		return 1 - pow(1 - x, 4)
	elif kind == 3:
		return 1 if x == 1 else 1 - pow(2, -10 * x)
	elif kind == 4:
		n = 7.5625
		d = 2.75
		if x < 1 / d:
			return n * x * x
		elif x < 2 / d:
			x -= 1.5 / d
			return n * x * x + 0.75
		elif x < 2.5 / d:
			x -= 2.25 / d
			return n * x * x + 0.9375
		else:
			x -= 2.625 / d
			return n * x * x + 0.984375
	elif kind == 5:
		if x == 0 or x == 1:
			return x
		else:
			c = (2 * math.pi) / 3
			return pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c) + 1
	else:
		print('[Warning]: kind = {} unsupported...'.format(kind))
		print('[INFO]: Switch to the mode that kind = None...')
		return None



def getTracks(distance, t_len=None, func_kind=None):
	if func_kind is not None:
		if func(0.0, func_kind) is None or t_len is None:
			func_kind = None
	# 先均加速后均减速模拟
	if func_kind is None:
		tracks = []
		offset = 0
		turn_dis = distance * 4 / 5
		t = 0.2
		v = 0
		while offset < distance:
			if offset < turn_dis:
				a = 2
			else:
				a = -3
			v0 = v
			v = v0 + a * t
			move_dis = v0 * t + 1 / 2 * a * t * t
			offset += move_dis
			tracks.append(round(move_dis))
	# 利用一些函数模拟
	else:
		tracks = []
		offset_prev = 0
		for t in np.arange(0.0, t_len, 0.1):
			offset_now = round(func(t/t_len, func_kind) * distance)
			tracks.append(offset_now - offset_prev)
			offset_prev = offset_now
	return tracks