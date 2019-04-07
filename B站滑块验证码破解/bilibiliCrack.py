
import os
import re
import time
import Tracks
import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


'''获取图像块正确的位置'''
def getRightPositions(gt_cut_bg_slice, gt_cut_fullbg_slice):
	gap_image_loc_list = []
	full_image_loc_list = []
	for each in gt_cut_bg_slice:
		x, y = [int(i) for i in re.findall(r'background-position:\s(.*?)px\s(.*?)px;', each.get('style'))[0]]
		gap_image_loc_list.append([x, y])
	for each in gt_cut_fullbg_slice:
		x, y = [int(i) for i in re.findall(r'background-position:\s(.*?)px\s(.*?)px;', each.get('style'))[0]]
		full_image_loc_list.append([x, y])
	return gap_image_loc_list, full_image_loc_list


'''图像重组'''
def reorganImage(image, positions):
	uppers = []
	downs = []
	for pos in positions:
		if pos[-1] == -58:
			uppers.append(image.crop((abs(pos[0]), 58, abs(pos[0])+12, 116)))
		else:
			downs.append(image.crop((abs(pos[0]), 0, abs(pos[0])+12, 58)))
	image_new = Image.new('RGB', image.size)
	offset = 0
	for each in uppers:
		image_new.paste(each, (offset, 0))
		offset += 10
	offset = 0
	for each in downs:
		image_new.paste(each, (offset, 58))
		offset += 10
	return image_new


'''获得缺口偏移量'''
def getGapOffset(image, source_img, thresh=150):
	print(image.size)
	for i in range(60, image.size[0]):
		for j in range(image.size[1]):
			#获取RGB的值
			#方法一
			# pixel1 = image.getpixel((i, j))
			# pixel2 = source_img.getpixel((i, j))
			#方法二
			pixel1=image.load()[i,j]
			pixel2=source_img.load()[i,j]
			#对比RGB
			if abs(pixel1[0]-pixel2[0]) + abs(pixel1[1]-pixel2[1]) + abs(pixel1[2]-pixel2[2]) >= thresh:
				return i



def moveToGap(browser, slider, tracks):
	ActionChains(browser).click_and_hold(slider).perform()
	for track in tracks:
		ActionChains(browser).move_by_offset(xoffset=track, yoffset=0).perform()
		time.sleep(0.01)
	ActionChains(browser).pause(0.5).release().perform()


'''主函数'''
def main(url):

	browser=webdriver.Chrome()
	# 访问登录页面
	browser.get(url)
	# 等待滑块出现
	slider = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#gc-box > div > div.gt_slider > div.gt_slider_knob.gt_show")))
	# 随便填个账号密码
	username = browser.find_element_by_id("login-username")
	username.send_keys('1234567')
	password = browser.find_element_by_id("login-passwd")
	password.send_keys('7654321')
	# 找验证码图片
	soup = BeautifulSoup(browser.page_source, 'lxml')
	gt_cut_bg_slice = soup.find_all(class_='gt_cut_bg_slice')
	gt_cut_fullbg_slice = soup.find_all(class_='gt_cut_fullbg_slice')
	
	gap_image_url = re.findall(r'background-image:\surl\("(.*?)"\)', gt_cut_bg_slice[0].get('style'))[0].replace('webp', 'jpg')
	full_image_url = re.findall(r'background-image:\surl\("(.*?)"\)', gt_cut_fullbg_slice[0].get('style'))[0].replace('webp', 'jpg')
	print(gt_cut_bg_slice)
	print(gt_cut_fullbg_slice)
	print(gap_image_url)
	print(full_image_url)

	# --带残缺块的
	gap_image = Image.open(BytesIO(requests.get(gap_image_url).content))
	# --完整的
	full_image = Image.open(BytesIO(requests.get(full_image_url).content))
	# 获取图像块正确的位置
	gap_image_loc_list, full_image_loc_list = getRightPositions(gt_cut_bg_slice, gt_cut_fullbg_slice)
	# 根据位置重新拼接
	gap_image = reorganImage(gap_image, gap_image_loc_list)
	full_image = reorganImage(full_image, full_image_loc_list)
	gap_image.save('1.jpg')
	full_image.save('2.jpg')

	# 计算偏移量
	distance = getGapOffset(gap_image, full_image)
	# 获取轨迹
	tracks = Tracks.getTracks(int(distance*0.95), 12, 3)
	print(tracks)
	# 模拟滑动
	moveToGap(browser, slider, tracks)
	time.sleep(2)


if __name__ == '__main__':
	url = 'https://passport.bilibili.com/login'
	main(url)