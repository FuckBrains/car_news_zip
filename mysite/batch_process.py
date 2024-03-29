import requests
import time
import schedule
import re
import regex
import mysql.connector
import os, json
import traceback
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
## 장고 프로젝트를 사용할 수 있도록 환경을 구축
import django
django.setup()

from website.models import TblTotalCarNewsList, TblMemberList, TblNewsKeywordList, TblNewsKeywordMap
from datetime import datetime
from konlpy.tag import Kkma
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

new_car_list = []
used_car_list = []
review_list = []
industry_list = []



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath('./mysite'))
# SECURITY WARNING: keep the secret key used in production secret!
db_info_file = os.path.join(BASE_DIR, 'db_conn.json')
with open(db_info_file) as f :
	db_infos = json.loads(f.read())


# BeautifulSoup
def get_soup(url) :
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
	res = requests.get(url, headers=headers)
	res.raise_for_status()
	res.encoding=None
	soup = BeautifulSoup(res.text, 'lxml')
	return soup

# 셀레니움 (동적 DATA)
def get_soup2(url) :
	options = webdriver.ChromeOptions()
	options.headless = True
	options.add_argument('window-size=1920x1080')
	browser = webdriver.Chrome(r'C:\Users\PC\Documents\simbyungki\git\car_news_zip\chromedriver.exe', options=options)
	browser.maximize_window()
	browser.get(url)
	time.sleep(2)
	soup = BeautifulSoup(browser.page_source, 'lxml')
	return soup

# 기사 DB INSERT
# Custom 쿼리 실행 함수


# 오토뷰
class GetAutoview() :
	# 오토뷰 신차
	def new() :
		url = 'http://www.autoview.co.kr/content/news/news_new_car.asp?page=1&pageshow=1'
				
		soup = get_soup(url)

		h_news_list = soup.find('div', attrs={'class': 'top_article'}).find_all('li')
		news_list = soup.find('div', attrs={'class': 'section newslist'}).find_all('li')

		data_list = []
		return_data_dic = {}

		for h_news in h_news_list :
			link = h_news.find('a')['href']
			img_url = h_news.find('div', attrs={'class', 'thumb'})['style']
			subject = h_news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = h_news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = h_news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)
		
		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('div', attrs={'class', 'thumb'})['style']
			subject = news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['autoview_new'] = data_list
		new_car_list.append(return_data_dic)

	# 오토뷰 자동차 산업
	def industry() :
		url = 'http://www.autoview.co.kr/content/news/news_cominfo.asp'
				
		soup = get_soup(url)

		h_news_list = soup.find('div', attrs={'class': 'top_article'}).find_all('li')
		news_list = soup.find('div', attrs={'class': 'section newslist'}).find_all('li')

		data_list = []
		return_data_dic = {}

		for h_news in h_news_list :
			link = h_news.find('a')['href']
			img_url = h_news.find('div', attrs={'class', 'thumb'})['style']
			subject = h_news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = h_news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = h_news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)
		
		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('div', attrs={'class', 'thumb'})['style']
			subject = news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['autoview_industry'] = data_list
		industry_list.append(return_data_dic)

	# 오토뷰 자동차 시승기
	def review() :
		url = 'http://www.autoview.co.kr/content/buyer_guide/guide_road.asp?page=1&pageshow=1'
				
		soup = get_soup(url)

		h_news_list = soup.find('div', attrs={'class': 'top_article'}).find_all('li')
		news_list = soup.find('div', attrs={'class': 'section newslist'}).find_all('li')

		data_list = []
		return_data_dic = {}

		for h_news in h_news_list :
			link = h_news.find('a')['href']
			img_url = h_news.find('div', attrs={'class', 'thumb'})['style']
			subject = h_news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = h_news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = h_news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)
		
		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('div', attrs={'class', 'thumb'})['style']
			subject = news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['autoview_review'] = data_list
		review_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=300).filter(news_content='')
		print('-'*30)
		print('오토뷰')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.autoview.co.kr/content/article.asp?num_code={newsList.values()[idx].get("news_code")}&news_section=new_car&pageshow=1'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'view_title'}).find('h4').get_text().strip()
					d_content = soup.find('div', attrs={'class': 'article_text'}).get_text().strip()
					
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# IT조선 #
class GetItChosun() :
	# IT조선 신차	
	def new() :
		url = 'http://it.chosun.com/svc/list_in/list.html?catid=32&pn=1'
		soup = get_soup(url)

		h_news = soup.find('div', attrs={'class': 'thumb_big'})
		news_list = soup.select('.add_item_wrap > li')

		data_list = []
		return_data_dic = {}

		# headline
		link = h_news.find('div', attrs={'class': 'txt_wrap'}).find('a')['href']
		img_url = h_news.find('img')['src']
		subject = h_news.find('span', attrs={'class': 'tt'}).get_text().strip()
		summary = h_news.find('span', attrs={'class': 'txt'}).get_text().strip()
		reporter = h_news.find('span', attrs={'class': 'name'}).get_text().strip()
		date = h_news.find('span', attrs={'class': 'date'}).get_text().strip()
		data_group = {}
		data_group['link'] = link
		data_group['img_url'] = img_url
		data_group['subject'] = subject
		data_group['summary'] = summary
		data_group['reporter'] = reporter
		data_group['date'] = date
		data_list.append(data_group)

		# normal
		for news in news_list :
			link = news.find('div', 'txt_wrap').find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('div', attrs={'class': 'txt_dot1'}).get_text().strip()
			summary = news.find('span', attrs={'class': 'txt_dot2'}).get_text().strip()
			reporter = news.find('span', attrs={'class': 'name'}).get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['chosun_new'] = data_list
		new_car_list.append(return_data_dic)

	# IT조선 시승기	
	def review() :
		url = 'http://it.chosun.com/svc/list_in/list.html?catid=33&pn=1'
		soup = get_soup(url)

		h_news = soup.find('div', attrs={'class': 'thumb_big'})
		news_list = soup.select('.add_item_wrap > li')

		data_list = []
		return_data_dic = {}

		# headline
		link = h_news.find('div', attrs={'class': 'txt_wrap'}).find('a')['href']
		img_url = h_news.find('img')['src']
		subject = h_news.find('span', attrs={'class': 'tt'}).get_text().strip()
		summary = h_news.find('span', attrs={'class': 'txt'}).get_text().strip()
		reporter = h_news.find('span', attrs={'class': 'name'}).get_text().strip()
		date = h_news.find('span', attrs={'class': 'date'}).get_text().strip()
		data_group = {}
		data_group['link'] = link
		data_group['img_url'] = img_url
		data_group['subject'] = subject
		data_group['summary'] = summary
		data_group['reporter'] = reporter
		data_group['date'] = date
		data_list.append(data_group)

		# normal
		for news in news_list :
			link = news.find('div', 'txt_wrap').find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('div', attrs={'class': 'txt_dot1'}).get_text().strip()
			summary = news.find('span', attrs={'class': 'txt_dot2'}).get_text().strip()
			reporter = news.find('span', attrs={'class': 'name'}).get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['chosun_new'] = data_list
		review_list.append(return_data_dic)

	# IT조선 자동차업계	
	def industry() :
		url = 'http://it.chosun.com/svc/list_in/list.html?catid=31&pn=1'
		soup = get_soup(url)

		h_news = soup.find('div', attrs={'class': 'thumb_big'})
		news_list = soup.select('.add_item_wrap > li')

		data_list = []
		return_data_dic = {}

		# headline
		link = h_news.find('div', attrs={'class': 'txt_wrap'}).find('a')['href']
		img_url = h_news.find('img')['src']
		subject = h_news.find('span', attrs={'class': 'tt'}).get_text().strip()
		summary = h_news.find('span', attrs={'class': 'txt'}).get_text().strip()
		reporter = h_news.find('span', attrs={'class': 'name'}).get_text().strip()
		date = h_news.find('span', attrs={'class': 'date'}).get_text().strip()
		data_group = {}
		data_group['link'] = link
		data_group['img_url'] = img_url
		data_group['subject'] = subject
		data_group['summary'] = summary
		data_group['reporter'] = reporter
		data_group['date'] = date
		data_list.append(data_group)

		# normal
		for news in news_list :
			link = news.find('div', 'txt_wrap').find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('div', attrs={'class': 'txt_dot1'}).get_text().strip()
			summary = news.find('span', attrs={'class': 'txt_dot2'}).get_text().strip()
			reporter = news.find('span', attrs={'class': 'name'}).get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['chosun_industry'] = data_list
		industry_list.append(return_data_dic)
	
	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=400).filter(news_content='')
		print('-'*30)
		print('IT조선')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://it.chosun.com/site/data/html_dir/{newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('h1', attrs={'id': 'news_title_text_id'}).get_text().strip()
					d_content = soup.find('div', attrs={'id': 'news_body_id'}).get_text().strip()
					
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 오토헤럴드
class GetAutoH() :
	def new() :
		url = 'http://autotimes.hankyung.com/apps/news.sub_list?popup=0&nid=02&c1=02&c2=04&c3=&newscate=&isslide=&page=1'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.newest_list > dl')

		# normal
		for idx, news in enumerate(news_list) :
			link = news.find('dt').find('a')['href']
			subject = news.find('dt').find('a').get_text().strip()
			summary = news.find('dd', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('dd', attrs={'class': 'date'}).get_text().strip()
			if news.find('dd', attrs={'class', 'thum'}) :
				img_url = news.find('dd', attrs={'class', 'thum'}).find('img')['src']
			else :
				img_url = ''

			data_group = {}
			data_group['link'] = link
			if img_url != '' :
				data_group['img_url'] = 'http://autotimes.hankyung.com' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[0:-6]

			data_list.append(data_group)

			# 상위 15개만 가져오기
			if idx == 14 :
				break
			
		return_data_dic['autoh_new'] = data_list
		new_car_list.append(return_data_dic)


	# 오토헤럴드 중고차 (21.01.28 페이지 없어짐)
	def used() : 
		url = 'http://autotimes.hankyung.com/apps/news.sub_list?popup=0&nid=05&c1=05&c2=02&c3=&newscate=&isslide=&page=1'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.newest_list > dl')

		# normal
		for idx, news in enumerate(news_list) :
			link = news.find('dt').find('a')['href']
			subject = news.find('dt').find('a').get_text().strip()
			summary = news.find('dd', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('dd', attrs={'class': 'date'}).get_text().strip()
			if news.find('dd', attrs={'class', 'thum'}) :
				img_url = news.find('dd', attrs={'class', 'thum'}).find('img')['src']
			else :
				img_url = ''

			data_group = {}
			data_group['link'] = link
			if img_url != '' :
				data_group['img_url'] = 'http://autotimes.hankyung.com' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[0:-6]

			data_list.append(data_group)

			# 상위 15개만 가져오기
			if idx == 14 :
				break

		return_data_dic['autoh_used'] = data_list
		used_car_list.append(return_data_dic)

	# 오토헤럴드 시승기
	def review() :
		url = 'http://autotimes.hankyung.com/apps/news.sub_list?popup=0&nid=02&c1=02&c2=05&c3=&newscate=&isslide=&page=1'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.newest_list > dl')

		# normal
		for idx, news in enumerate(news_list) :
			link = news.find('dt').find('a')['href']
			subject = news.find('dt').find('a').get_text().strip()
			summary = news.find('dd', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('dd', attrs={'class': 'date'}).get_text().strip()
			if news.find('dd', attrs={'class', 'thum'}) :
				img_url = news.find('dd', attrs={'class', 'thum'}).find('img')['src']
			else :
				img_url = ''

			data_group = {}
			data_group['link'] = link
			if img_url != '' :
				data_group['img_url'] = 'http://autotimes.hankyung.com' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[0:-6]

			data_list.append(data_group)

			# 상위 15개만 가져오기
			if idx == 14 :
				break

		return_data_dic['autoh_review'] = data_list
		review_list.append(return_data_dic)

	# 오토헤럴드 자동차 업계
	def industry() :
		url = 'http://autotimes.hankyung.com/apps/news.sub_list?popup=0&nid=03&c1=03&c2=&c3=&newscate=&isslide=&page=1'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.newest_list > dl')

		# normal
		for idx, news in enumerate(news_list) :
			link = news.find('dt').find('a')['href']
			subject = news.find('dt').find('a').get_text().strip()
			summary = news.find('dd', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('dd', attrs={'class': 'date'}).get_text().strip()
			if news.find('dd', attrs={'class', 'thum'}) :
				img_url = news.find('dd', attrs={'class', 'thum'}).find('img')['src']
			else :
				img_url = ''

			data_group = {}
			data_group['link'] = link
			if img_url != '' :
				data_group['img_url'] = 'http://autotimes.hankyung.com' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[0:-6]

			data_list.append(data_group)

			# 상위 15개만 가져오기
			if idx == 14 :
				break

		return_data_dic['autoh_industry'] = data_list
		industry_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=100).filter(news_content='')
		print('-'*30)
		print('오토헤럴드')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = 'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=05&c1=05&c2=02&c3=&nkey=' + newsList.values()[idx].get('news_code')
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'view-title'}).find('h2').get_text().strip()
					d_content = soup.find('div', attrs={'class': 'view_report'}).get_text().strip()
					
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 데일리카 #
class GetDailyCar() :
	# 데일리카 중고차
	def used() :
		url = 'http://www.dailycar.co.kr/content/news.html?type=list&sub=sell&maker=used'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.nwslistwrap > .nwslist')

		# normal
		for idx, news in enumerate(news_list) :
			# 광고 제외
			if 'ad nwslist' not in str(news) :
				link = news.find('section', attrs={'class': 'nwslist_title'}).find('a')['href']
				subject = news.find('section', attrs={'class': 'nwslist_title'}).find('a').get_text().strip()
				summary = news.find('section', attrs={'class': 'nwslist_summary'}).get_text().strip()
				date = news.find('date').get_text().strip()
				img_url = news.find('div', attrs={'class', 'fixedratio'}).find('img')['src']
				# /data/news_xml_img/Id0000000216/ns107631.jpg
				# /data_thumb/gallery/Id0000000198/98680_240.jpg

				data_group = {}
				data_group['link'] = 'http://www.dailycar.co.kr'+ link
				data_group['img_url'] = 'http://www.dailycar.co.kr'+ img_url
				data_group['subject'] = subject
				data_group['summary'] = summary
				data_group['date'] = date[:10]

				data_list.append(data_group)

				# 상위 15개만 가져오기
				# if idx == 14 :
				# 	break

		return_data_dic['daily_used'] = data_list
		used_car_list.append(return_data_dic)

	# 데일리카 시승기
	def review() :
		url = 'http://www.dailycar.co.kr/content/news.html?gu=12'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.nwslistwrap > .nwslist')

		# normal
		for idx, news in enumerate(news_list) :
			# 광고 제외
			if 'ad nwslist' not in str(news) :
				link = news.find('section', attrs={'class': 'nwslist_title'}).find('a')['href']
				subject = news.find('section', attrs={'class': 'nwslist_title'}).find('a').get_text().strip()
				summary = news.find('section', attrs={'class': 'nwslist_summary'}).get_text().strip()
				date = news.find('date').get_text().strip()
				img_url = news.find('div', attrs={'class', 'fixedratio'}).find('img')['src']
				# /data/news_xml_img/Id0000000216/ns107631.jpg
				# /data_thumb/gallery/Id0000000198/98680_240.jpg

				data_group = {}
				data_group['link'] = 'http://www.dailycar.co.kr'+ link
				data_group['img_url'] = 'http://www.dailycar.co.kr'+ img_url
				data_group['subject'] = subject
				data_group['summary'] = summary
				data_group['date'] = date[:10]

				data_list.append(data_group)

				# 상위 15개만 가져오기
				# if idx == 14 :
				# 	break

		return_data_dic['daily_review'] = data_list
		review_list.append(return_data_dic)

	# 데일리카 자동차 업계
	def industry() :
		url = 'http://www.dailycar.co.kr/content/news.html?sub=news2'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.nwslistwrap > .nwslist')

		# normal
		for idx, news in enumerate(news_list) :
			# 광고 제외
			if 'ad nwslist' not in str(news) :
				link = news.find('section', attrs={'class': 'nwslist_title'}).find('a')['href']
				subject = news.find('section', attrs={'class': 'nwslist_title'}).find('a').get_text().strip()
				summary = news.find('section', attrs={'class': 'nwslist_summary'}).get_text().strip()
				date = news.find('date').get_text().strip()
				img_url = news.find('div', attrs={'class', 'fixedratio'}).find('img')['src']
				# /data/news_xml_img/Id0000000216/ns107631.jpg
				# /data_thumb/gallery/Id0000000198/98680_240.jpg

				data_group = {}
				data_group['link'] = 'http://www.dailycar.co.kr'+ link
				data_group['img_url'] = 'http://www.dailycar.co.kr'+ img_url
				data_group['subject'] = subject
				data_group['summary'] = summary
				data_group['date'] = date[:10]

				data_list.append(data_group)

				# 상위 15개만 가져오기
				# if idx == 14 :
				# 	break

		return_data_dic['daily_industry'] = data_list
		industry_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=200).filter(news_content='')
		print('-'*30)
		print('데일리카')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.dailycar.co.kr/content/news.html?type=view&autoId={newsList.values()[idx].get("news_code")}&from=%2Fcontent%2Fnews.html%3Ftype%3Dlist%26sub%3Dsell%26maker%3Dused'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('span', attrs={'id': 'content_titleonly'}).get_text().strip()
					d_content = soup.find('span', attrs={'id': 'content_bodyonly'}).get_text().strip()
					soup.select_one('span#content_bodyonly').figure.decompose()
					d_reporter = soup.select_one('span#content_bodyonly').get_text().strip()[6:12]
					
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}", REPORTER_NAME = "{d_reporter}" 
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 오토모닝 # 
class GetAutoMorning() :
	# 오토모닝 신차
	def new() :
		url = 'http://www.automorning.com/news/section_list_all.html?sec_no=84'
		soup = get_soup(url)

		news_list = soup.select('.ara_001 > .art_list_all > li')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('h2', attrs={'class': 'clamp c2'}).get_text().strip()
			summary = news.find('p', attrs={'class': 'ffd clamp c2'}).get_text().strip()
			reporter = summary[6:12]
			date = news.find('li', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['automoring_new'] = data_list
		new_car_list.append(return_data_dic)

	# 오토모닝 중고차
	def used() :
		url = 'http://www.automorning.com/news/section_list_all.html?sec_no=85'
		soup = get_soup(url)

		news_list = soup.select('.ara_001 > .art_list_all > li')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('h2', attrs={'class': 'clamp c2'}).get_text().strip()
			summary = news.find('p', attrs={'class': 'ffd clamp c2'}).get_text().strip()
			reporter = summary[6:12]
			date = news.find('li', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['automoring_used'] = data_list
		used_car_list.append(return_data_dic)

	# 오토모닝 시승기
	def review() :
		url = 'http://www.automorning.com/news/section_list_all.html?sec_no=87'
		soup = get_soup(url)

		news_list = soup.select('.ara_001 > .art_list_all > li')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('h2', attrs={'class': 'clamp c2'}).get_text().strip()
			summary = news.find('p', attrs={'class': 'ffd clamp c2'}).get_text().strip()
			reporter = summary[6:12]
			date = news.find('li', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['automoring_review'] = data_list
		review_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=500).filter(news_content='')
		print('-'*30)
		print('오토모닝')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.automorning.com/news/article.html?no={newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'art_top'}).find('h2').get_text().strip()
					d_content = soup.find('div', attrs={'id': 'news_body_area'}).get_text().strip()
					
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 오토다이어리 #
class GetAutoDiary() :
	# 오토다이어리 신차
	def new() :
		url = 'http://www.autodiary.kr/category/news/new-car/'
		soup = get_soup(url)

		news_list = soup.select('#posts-container > div')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('h2', attrs={'class': 'entry-title'}).get_text().strip()
			summary = ''
			date = news.find('span', attrs={'class': 'updated'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['autodiary_new'] = data_list
		new_car_list.append(return_data_dic)

	# 오토다이어리 자동차 업계
	def industry() :
		url = 'http://www.autodiary.kr/category/news/car-business/'
		soup = get_soup(url)

		news_list = soup.select('#posts-container > div')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			if news.find('img') :  
				img_url = news.find('img')['src']
			else :
				img_url = ''
			subject = news.find('h2', attrs={'class': 'entry-title'}).get_text().strip()
			summary = ''
			date = news.find('span', attrs={'class': 'updated'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['autodiary_industry'] = data_list
		industry_list.append(return_data_dic)

	# 오토다이어리 시승기
	def review() :
		url = 'http://www.autodiary.kr/category/impression/'
		soup = get_soup(url)

		news_list = soup.select('#posts-container > div')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('h2', attrs={'class': 'entry-title'}).get_text().strip()
			summary = ''
			date = news.find('span', attrs={'class': 'updated'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['autodiary_review'] = data_list
		review_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=600).filter(news_content='')
		print('-'*30)
		print('오토다이어리')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.autodiary.kr{newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('h2', attrs={'class': 'entry-title'}).get_text().strip()
					d_content = soup.find('div', attrs={'class': 'post-content'}).get_text().strip()
					d_content_tree = soup.find('div', attrs={'class': 'post-content'}).find_all('p')
					reporter = d_content_tree[len(d_content_tree) -1].get_text()[0:4]
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}", REPORTER_NAME = "{reporter}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 카가이 #
class GetCarguy() :
	# 카가이 자동차 업계
	def industry() :
		url = 'http://www.carguy.kr/news/articleList.html?page=1&total=3201&sc_section_code=S1N1&view_type=sm'
		soup = get_soup(url)

		news_list = soup.select('.article-list-content > .list-block')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-titles'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style']
			subject = news.find('div', attrs={'class': 'list-titles'}).get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).get_text().strip()
			info = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.carguy.kr' + link
			data_group['img_url'] = 'http://www.carguy.kr/news' + img_url[22:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = info[5:12]
			data_group['date'] = info[-16:-6]

			data_list.append(data_group)

		return_data_dic['carguy_industry'] = data_list
		industry_list.append(return_data_dic)

	# 카가이 시승기
	def review() :
		url = 'http://www.carguy.kr/news/articleList.html?page=1&total=1477&sc_section_code=S1N3&view_type=sm'
		soup = get_soup(url)

		news_list = soup.select('.article-list-content > .list-block')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-titles'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style']
			subject = news.find('div', attrs={'class': 'list-titles'}).get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).get_text().strip()
			info = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.carguy.kr' + link
			data_group['img_url'] = 'http://www.carguy.kr/news' + img_url[22:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = info[5:12]
			data_group['date'] = info[-16:-6]

			data_list.append(data_group)

		return_data_dic['carguy_review'] = data_list
		review_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=700).filter(news_content='')
		print('-'*30)
		print('카가이')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.carguy.kr/news/articleView.html?idxno={newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'article-head-title'}).get_text().strip()
					d_content = soup.find('div', attrs={'id': 'article-view-content-div'}).get_text().strip()
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 더드라이브 #
class GetTheDrive() :
	# 더드라이브 자동차 업계
	def industry() :
		url = 'http://www.thedrive.co.kr/news/newsList.php?tid=181930993&pagenum=0'
		soup = get_soup(url)

		news_list = soup.select('#listWrap > .listPhoto')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('p', attrs={'class': 'img'}).find('a')['href']
			img_url = news.find('p', attrs={'class': 'img'}).find('img')['src']
			subject = news.find('dt').get_text().strip()
			summary = news.find('dd', attrs={'class': 'conts'}).get_text().strip()
			reporter = news.find('dd', attrs={'class': 'winfo'}).find('a').get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.thedrive.co.kr' + link
			data_group['img_url'] = 'http://www.thedrive.co.kr' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['drive_industry'] = data_list
		industry_list.append(return_data_dic)

	# 더드라이브 시승기
	def review() :
		url = 'http://www.thedrive.co.kr/news/newsList.php?tid=181930911&pagenum=0'
		soup = get_soup(url)

		news_list = soup.select('#listWrap > .listPhoto')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('p', attrs={'class': 'img'}).find('a')['href']
			img_url = news.find('p', attrs={'class': 'img'}).find('img')['src']
			subject = news.find('dt').get_text().strip()
			summary = news.find('dd', attrs={'class': 'conts'}).get_text().strip()
			reporter = news.find('dd', attrs={'class': 'winfo'}).find('a').get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.thedrive.co.kr' + link
			data_group['img_url'] = 'http://www.thedrive.co.kr' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['drive_review'] = data_list
		review_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=800).filter(news_content='')
		print('-'*30)
		print('더드라이브')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.thedrive.co.kr/news/newsview.php?ncode={newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'viewTitle'}).find('h3').get_text().strip()
					d_content = soup.find('div', attrs={'id': 'viewConts'}).get_text().strip()
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 모터그래프
class GetMotorGraph() :
	# 신차
	def new() :
		url = 'https://www.motorgraph.com/news/articleList.html?page=1&total=1103&sc_section_code=&sc_sub_section_code=S2N2&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=E&view_type=sm'
		soup = get_soup(url)

		news_list = soup.find('section', attrs={'class': 'article-list-content'}).findAll('div', attrs={'class': 'list-block'})
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-image'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style'][22:-1]
			subject = news.find('div', attrs={'class': 'list-titles'}).find('strong').get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).find('a').get_text().strip()
			reporter = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			reporter = re.search(r'\|(.*?)\|', reporter).group(1).strip()
			date = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()[-16:-6]
			data_group = {}
			data_group['link'] = 'https://www.motorgraph.com' + link
			data_group['img_url'] = 'https://www.motorgraph.com/news/' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['motorgraph_new'] = data_list
		new_car_list.append(return_data_dic)

	# 시승기 (국산)
	def review_k() :
		url = 'https://www.motorgraph.com/news/articleList.html?page=1&total=142&sc_section_code=&sc_sub_section_code=S2N4&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=E&view_type=sm'
		soup = get_soup(url)

		news_list = soup.find('section', attrs={'class': 'article-list-content'}).findAll('div', attrs={'class': 'list-block'})
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-image'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style'][22:-1]
			subject = news.find('div', attrs={'class': 'list-titles'}).find('strong').get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).find('a').get_text().strip()
			reporter = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			reporter = re.search(r'\|(.*?)\|', reporter).group(1).strip()
			date = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()[-16:-6]
			data_group = {}
			data_group['link'] = 'https://www.motorgraph.com' + link
			data_group['img_url'] = 'https://www.motorgraph.com/news/' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['motorgraph_review_k'] = data_list
		review_list.append(return_data_dic)

	# 시승기 (수입)
	def review_g() :
		url = 'https://www.motorgraph.com/news/articleList.html?page=1&total=344&sc_section_code=&sc_sub_section_code=S2N5&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=E&view_type=sm'
		soup = get_soup(url)

		news_list = soup.find('section', attrs={'class': 'article-list-content'}).findAll('div', attrs={'class': 'list-block'})
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-image'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style'][22:-1]
			subject = news.find('div', attrs={'class': 'list-titles'}).find('strong').get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).find('a').get_text().strip()
			reporter = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			reporter = re.search(r'\|(.*?)\|', reporter).group(1).strip()
			date = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()[-16:-6]
			data_group = {}
			data_group['link'] = 'https://www.motorgraph.com' + link
			data_group['img_url'] = 'https://www.motorgraph.com/news/' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)
			
		return_data_dic['motorgraph_review_g'] = data_list
		review_list.append(return_data_dic)

	# 자동차 업계
	def industry() :
		url = 'https://www.motorgraph.com/news/articleList.html?page=1&total=1280&sc_section_code=&sc_sub_section_code=S2N15&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=E&view_type=sm'
		soup = get_soup(url)

		news_list = soup.find('section', attrs={'class': 'article-list-content'}).findAll('div', attrs={'class': 'list-block'})
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-image'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style'][22:-1]
			subject = news.find('div', attrs={'class': 'list-titles'}).find('strong').get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).find('a').get_text().strip()
			reporter = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			reporter = re.search(r'\|(.*?)\|', reporter).group(1).strip()
			date = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()[-16:-6]
			data_group = {}
			data_group['link'] = 'https://www.motorgraph.com' + link
			data_group['img_url'] = 'https://www.motorgraph.com/news/' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)
			
		return_data_dic['motorgraph_industry'] = data_list
		industry_list.append(return_data_dic)

		# 본문 수집
	
	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=900).filter(news_content='')
		print('-'*30)
		print('모터그래프')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'https://www.motorgraph.com/news/articleView.html?idxno={newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'article-head-title'}).get_text().strip()
					d_content = soup.find('div', attrs={'id': 'articleBody'}).get_text().strip()
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass


# 중고차 뉴스 모음
def get_used_car() :
	# GetAutoH.used()
	GetDailyCar.used()
	GetAutoMorning.used()

	return used_car_list

# 신차 뉴스 모음
def get_new_car() :
	GetAutoH.new()
	GetAutoview.new()
	GetItChosun.new()
	GetAutoMorning.new()
	# GetAutoDiary.new()
	GetMotorGraph.new()

	return new_car_list

# 시승기 모음
def get_review() :
	GetAutoH.review()
	GetDailyCar.review()
	GetAutoview.review()
	GetItChosun.review()
	GetAutoMorning.review()
	# GetAutoDiary.review()
	GetCarguy.review()
	GetTheDrive.review()
	GetMotorGraph.review_k()
	GetMotorGraph.review_g()

	return review_list

# 자동차 업계 뉴스 모음
def get_industry() :
	GetAutoH.industry()
	GetDailyCar.industry()
	GetAutoview.industry()
	GetItChosun.industry()
	# GetAutoDiary.industry()
	GetCarguy.industry()
	GetTheDrive.industry()
	GetMotorGraph.industry()

	return industry_list


# 중고차 뉴스 INSERT
def insert_used_db(dbconn, cursor) :
	try :
		print('**** 중고차 관련 기사 수집 시작!')
		
		media_code = 0
		media_name = ''
		news_code = 0
		for idx, news_list in enumerate(get_used_car()) :
			if idx == 0 :
				# # 오토헤럴드 (21.01.28 페이지 없어짐)
				# media_code = 100
				# media_name = '오토헤럴드'
				# 데일리카
				media_code = 200
				media_name = '데일리카'
			elif idx == 1 :
				# 오토모닝
				media_code = 500
				media_name = '오토모닝'
			for news_dict in news_list.values() :
				for news in news_dict : 
					if idx == 0 :
						# # 오토헤럴드 (21.01.28 페이지 없어짐)
						# news_code = news.get('link')[-15:]
						# url = f'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=05&c1=05&c2=02&c3=&nkey={news_code}'
						# 데일리카
						news_code = news.get('link')[61:66]
						url = f'http://www.dailycar.co.kr/content/news.html?type=view&autoId={news_code}&from=%2Fcontent%2Fnews.html%3Ftype%3Dlist%26sub%3Dsell%26maker%3Dused'
					elif idx == 1 :
						# 오토모닝
						news_code = news.get('link')[-5:]
						url = f'http://www.automorning.com/news/article.html?no={news_code}'

					subject = re.sub('[-=.#/?:$}\"\']', '', news.get('subject'))
					summary = re.sub('[-=.#/?:$}\"\']', '', news.get('summary'))
					reporter = news.get('reporter')
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')

					cursor.execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, REPORTER_NAME,
							NEWS_IMG_URL, NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 1, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "", "{reporter}",
							"{img_url}", "{url}", "{date}", 
							NOW(), 1
						) 
					""")
	except Exception as e :
		print(f'***** + error! >> {e}')	
		pass
	finally : 
		print('**** 중고차 관련 기사 수집 및 DB저장 완료!')
		print('ㅡ'*50)

# 신차 뉴스 INSERT
def insert_new_db(dbconn, cursor) :
	try :
		print('**** 신차 관련 기사 수집 시작!')
		media_code = 0
		media_name = ''
		news_code = 0
		for idx, news_list in enumerate(get_new_car()) :
			if idx == 0 :
				# 오토헤럴드
				media_code = 100
				media_name = '오토헤럴드'
			elif idx == 1 :
				# 오토뷰
				media_code = 300
				media_name = '오토뷰'
			elif idx == 2 :
				# IT조선
				media_code = 400
				media_name = 'IT조선'
			elif idx == 3 :
				# 오토모닝
				media_code = 500
				media_name = '오토모닝'
			# elif idx == 4 :
			# 	# 오토다이어리
			# 	media_code = 600
			# 	media_name = '오토다이어리'
			elif idx == 4 :
				# 모터그래프
				media_code = 900
				media_name = '모터그래프'

			for news_dict in news_list.values() :
				for news in news_dict : 
					if idx == 0 :
						# 오토헤럴드
						news_code = news.get('link')[-15:]
						url = f'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=05&c1=05&c2=02&c3=&nkey={news_code}'
					elif idx == 1 :
						# 오토뷰
						news_code = news.get('link')[55:60]
						url = f'http://www.autoview.co.kr/content/article.asp?num_code={news_code}&news_section=new_car&pageshow=1'
					elif idx == 2 :
						# IT조선
						news_code = news.get('link')[39:]
						url = f'http://it.chosun.com/site/data/html_dir{news_code}'
					elif idx == 3 :
						# 오토모닝
						news_code = news.get('link')[-5:]
						url = f'http://www.automorning.com/news/article.html?no={news_code}'
					# elif idx == 5 :
					# 	# 오토다이어리
					# 	news_code = news.get('link')[-17:]
					# 	url = f'http://www.autodiary.kr{news_code}'
					elif idx == 4 : 
						# 모터그래프
						news_code = news.get('link')[-5:]
						url = f'https://www.motorgraph.com/news/articleView.html?idxno={news_code}'

					subject = re.sub('[-=.#/?:$}\"\']', '', news.get('subject'))
					summary = re.sub('[-=.#/?:$}\"\']', '', news.get('summary'))
					reporter = news.get('reporter')
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')

					cursor.execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, REPORTER_NAME,
							NEWS_IMG_URL, NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 3, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "", "{reporter}",
							"{img_url}", "{url}", "{date}", 
							NOW(), 1
						) 
					""")

	except Exception as e :
		print(f'***** + error! >> {e}')	
	finally : 
		print('**** 신차 관련 기사 수집 및 DB저장 완료!')
		print('ㅡ'*50)
	
# 시승기 INSERT
def insert_review_db(dbconn, cursor) :
	try :
		print('**** 시승기 수집 시작!')
		media_code = 0
		media_name = ''
		news_code = 0
		for idx, news_list in enumerate(get_review()) :
			if idx == 0 :
				# 오토헤럴드
				media_code = 100
				media_name = '오토헤럴드'
			elif idx == 1 :
				# 데일리카
				media_code = 200
				media_name = '데일리카'
			elif idx == 2 :
				# 오토뷰
				media_code = 300
				media_name = '오토뷰'
			elif idx == 3 :
				# IT조선
				media_code = 400
				media_name = 'IT조선'
			elif idx == 4 :
				# 오토모닝
				media_code = 500
				media_name = '오토모닝'
			# elif idx == 5 :
			# 	# 오토다이어리
			# 	media_code = 600
			# 	media_name = '오토다이어리'
			elif idx == 5 :
				# 카가이
				media_code = 700
				media_name = '카가이'
			elif idx == 6 :
				# 더드라이브
				media_code = 800
				media_name = '더드라이브'
			elif idx == 7 or idx == 8 :
				# 모터그래프
				media_code = 900
				media_name = '모터그래프'

			for news_dict in news_list.values() :
				for news in news_dict : 
					if idx == 0 :
						# 오토헤럴드
						news_code = news.get('link')[-15:]
						url = f'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=06&c1=06&c2=&c3=&nkey={news_code}'
					elif idx == 1 :
						# 데일리카
						news_code = news.get('link')[61:66]
						url = f'http://www.dailycar.co.kr/content/news.html?type=view&autoId={news_code}&from=%2Fcontent%2Fnews.html'
					elif idx == 2 :
						# 오토뷰
						news_code = news.get('link')[78:83]
						url = f'http://www.autoview.co.kr/content/buyer_guide/guide_road_article.asp?num_code={news_code}&news_section=car_ride&pageshow=3'
					elif idx == 3 :
						# IT조선
						news_code = news.get('link')[39:]
						url = f'http://it.chosun.com/site/data/html_dir{news_code}'
					elif idx == 4 :
						# 오토모닝
						news_code = news.get('link')[-5:]
						url = f'http://www.automorning.com/news/article.html?no={news_code}'
					# elif idx == 5 :
					# 	# 오토다이어리
					# 	news_code = news.get('link')[-17:]
					# 	url = f'http://www.autodiary.kr{news_code}'
					elif idx == 5 :
						# 카가이
						news_code = news.get('link')[-5:]
						url = f'http://www.carguy.kr/news/articleView.html?idxno={news_code}'
					elif idx == 6 :
						# 더드라이브
						news_code = news.get('link')[-16:]
						url = f'http://www.thedrive.co.kr/news/newsview.php?ncode={news_code}'
					elif idx == 7 or idx == 8 :
						news_code = news.get('link')[-5:]
						url = f'https://www.motorgraph.com/news/articleView.html?idxno={news_code}'
					
					subject = re.sub('[-=.#/?:$}\"\']', '', news.get('subject'))
					summary = re.sub('[-=.#/?:$}\"\']', '', news.get('summary'))
					reporter = news.get('reporter')
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')

					cursor.execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, REPORTER_NAME,
							NEWS_IMG_URL, NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 5, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "", "{reporter}",
							"{img_url}", "{url}", "{date}", 
							NOW(), 1
						) 
					""")
		
	except Exception as e :
		print(f'***** + error! >> {e}')	
	finally : 
		print('**** 시승기 수집 및 DB저장 완료!')
		print('ㅡ'*50)

# 자동차 업계 뉴스 INSERT
def insert_industry_db(dbconn, cursor) :
	try :
		print('**** 자동차 업계 뉴스 수집 시작!')
		media_code = 0
		media_name = ''
		news_code = 0
		for idx, news_list in enumerate(get_industry()) :
			if idx == 0 :
				# 오토헤럴드
				media_code = 100
				media_name = '오토헤럴드'
			elif idx == 1 :
				# 데일리카
				media_code = 200
				media_name = '데일리카'
			elif idx == 2 :
				# 오토뷰
				media_code = 300
				media_name = '오토뷰'
			elif idx == 3 :
				# IT조선
				media_code = 400
				media_name = 'IT조선'
			# elif idx == 4 :
			# 	# 오토다이어리
			# 	media_code = 600
			# 	media_name = '오토다이어리'
			elif idx == 4 :
				# 카가이
				media_code = 700
				media_name = '카가이'
			elif idx == 5 :
				# 더드라이브
				media_code = 800
				media_name = '더드라이브'
			elif idx == 6 :
				# 모터그래프
				media_code = 900
				media_name = '모터그래프'

			for news_dict in news_list.values() :
				for news in news_dict : 
					if idx == 0 :
						# 오토헤럴드
						news_code = news.get('link')[-15:]
						url = f'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=06&c1=06&c2=&c3=&nkey={news_code}'
					elif idx == 1 :
						# 데일리카
						news_code = news.get('link')[61:66]
						url = f'http://www.dailycar.co.kr/content/news.html?type=view&autoId={news_code}&from=%2Fcontent%2Fnews.html'
					elif idx == 2 :
						# 오토뷰
						news_code = news.get('link')[78:83]
						url = f'http://www.autoview.co.kr/content/buyer_guide/guide_road_article.asp?num_code={news_code}&news_section=car_ride&pageshow=3'
					elif idx == 3 :
						# IT조선
						news_code = news.get('link')[39:]
						url = f'http://it.chosun.com/site/data/html_dir{news_code}'
					# elif idx == 4 :
					# 	# 오토다이어리
					# 	news_code = news.get('link')[-17:]
					# 	url = f'http://www.autodiary.kr{news_code}'
					elif idx == 4 :
						# 카가이
						news_code = news.get('link')[-5:]
						url = f'http://www.carguy.kr/news/articleView.html?idxno={news_code}'
					elif idx == 5 :
						# 더드라이브
						news_code = news.get('link')[-16:]
						url = f'http://www.thedrive.co.kr/news/newsview.php?ncode={news_code}'
					elif idx == 6 :
						# 모터그래프
						news_code = news.get('link')[-5:]
						url = f'https://www.motorgraph.com/news/articleView.html?idxno={news_code}'

					subject = re.sub('[-=.#/?:$}\"\']', '', news.get('subject'))
					summary = re.sub('[-=.#/?:$}\"\']', '', news.get('summary'))
					reporter = news.get('reporter')
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')

					cursor.execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, REPORTER_NAME,
							NEWS_IMG_URL, NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 7, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "", "{reporter}",
							"{img_url}", "{url}", "{date}", 
							NOW(), 1
						) 
					""")
		
	except Exception as e :
		print(f'***** + error! >> {e}')	
	finally : 
		print('**** 자동차 업계 뉴스 수집 및 DB저장 완료!')
		print('ㅡ'*50)


# 뉴스 목록 새로 수집
def reload_list_data() :
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	print('뉴스 받아오기 시작!')

	insert_used_db(dbconn, cursor)
	print(f'중고차 처리건수 >> [{len(used_car_list)}]')
	insert_new_db(dbconn, cursor)
	print(f'신차 처리건수 >> [{len(new_car_list)}]')
	insert_review_db(dbconn, cursor)
	print(f'시승기 처리건수 >> [{len(review_list)}]')
	insert_industry_db(dbconn, cursor)
	print(f'자동차 산업 처리건수 >> [{len(industry_list)}]')
	dbconn.commit()
	dbconn.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('뉴스 받아오기 DB Commit/Close 완료!')
	print('뉴스 받아오기 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('뉴스 받아오기 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))

# 뉴스 본문 수집
def load_detail_data() :
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	now = time.localtime()
	print('뉴스 상세 내용 가져오기 시작!')

	GetAutoH.detail(dbconn, cursor)
	GetDailyCar.detail(dbconn, cursor)
	GetAutoview.detail(dbconn, cursor)
	GetItChosun.detail(dbconn, cursor)
	GetAutoMorning.detail(dbconn, cursor)
	# GetAutoDiary.detail(dbconn, cursor)
	GetCarguy.detail(dbconn, cursor)
	GetTheDrive.detail(dbconn, cursor)
	GetMotorGraph.detail(dbconn, cursor)
	
	print('뉴스 상세 내용 가져오기 완료!')
	dbconn.commit()
	dbconn.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('뉴스 상세 내용 가져오기 DB Commit/Close 완료!')
	print('뉴스 상세 내용 가져오기 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('뉴스 상세 내용 가져오기 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))
	

# 뉴스 분석
mining_result_data = []
def text_mining(cont_type, dbconn, cursor) :
	kkma = Kkma()
	car_news_list = TblTotalCarNewsList.objects.all().filter(mining_status = 1).exclude(news_content = '')
	except_word_list = []
	except_keyword_list = []
	origin_sentence_list = []
	news_no = 0
	# user_id = request.session.get('user')
	# if user_id :
	# 	memb_name = TblMemberList.objects.filter(memb_id=user_id).values()[0].get('memb_name')
	# 	context['user'] = memb_name
	# else : 
	# 	context['user'] = None

	# print(car_news_list[0].news_summary)

	print('형태소 분석')

	# step00. 긍정, 부정 단어 사전 load
	positive_keywords = []
	negative_keywords = []
	va_keywords = []
	p_keywords_list = TblNewsKeywordList.objects.all().filter(positive_yn='y')
	n_keywords_list = TblNewsKeywordList.objects.all().filter(negative_yn='y')
	va_keywords_list = TblNewsKeywordList.objects.all().filter(word_class='VA')
	for idx in range(len(p_keywords_list)) :
		positive_keywords.append(p_keywords_list[idx].word_morpheme)
	for idx in range(len(n_keywords_list)) :
		negative_keywords.append(n_keywords_list[idx].word_morpheme)
	for idx in range(len(va_keywords_list)) :
		va_keywords.append(va_keywords_list[idx].word_morpheme)

	# 뉴스 본문 분석
	if cont_type == 'news' : 
		# step01. 형태소 분석 (데이터 가공)
		for idx in range(len(car_news_list)) :
		# for idx in range(10) :
			re_content = regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}]+', f'{car_news_list[idx].news_content}')
			# print(f'[{idx}] >> {len(re_content)}')
			origin_sentence_list.append(car_news_list[idx].news_summary)
			# print(re_summary)
			# print('-'*50)
			in_result_data = []
		# in_result_data[0] 각종 카운트 사전
			count_dic = {}
			# 형태소 단어 총 개수
			count_dic['morpheme_count'] = len(re_content)
			# 형용사 개수
			va_count = 0
			count_dic['va_count'] = va_count
			# 긍정단어 개수
			p_count = 0
			count_dic['positive_count'] = p_count
			# 부정단어 개수
			n_count = 0
			count_dic['negative_count'] = n_count
			
			in_result_data.append(count_dic)
		# in_result_data[1] 뉴스 번호
			in_result_data.append(car_news_list[idx].news_no)
			for word in re_content :
				in_result_word = []	
				group = []
				if (word not in except_word_list) :
					word_g = []
					word_g.append(word)
					group.append(word_g)
					# print(word)
					# print('-'*50)
					for keyword in kkma.pos(word) :
						if (keyword not in except_keyword_list) :
							# print(keyword)
							# print('-'*50)
							in_result_word.append(keyword)
					group.append(in_result_word)
				
				if (word in positive_keywords) :
					p_count += 1
				if (word in negative_keywords) :
					n_count += 1
				if (word in va_keywords) :
					va_count += 1

				in_result_data.append(group)
			in_result_data[0]['positive_count'] = p_count
			in_result_data[0]['negative_count'] = n_count
			in_result_data[0]['va_count'] = va_count
			mining_result_data.append(in_result_data)

		# step02. DB Insert
		print('DB Insert')
		try : 
			for out_idx, data_list in enumerate(mining_result_data) :
				print('DB Insert 2')
				for idx, data in enumerate(data_list) :
					try : 
						if idx == 0 :
							news_info = data_list[0]
						elif idx == 1 :	
							news_no = data_list[1]
						else : 
							pass
							origin_word = re.sub('[-=.#/?:$}\"\']', '', str(data[0])).replace('[','').replace(']','')
							print(f'*** : [{out_idx}/{len(mining_result_data) -1}][{news_no}][{idx}/{len(data_list)}][{origin_word}]')
							# data[1] 형태소 분석 (세트) >> ex) [('신', 'NNG'), ('차', 'NNG')]
							for in_idx, word in enumerate(data[1]):
								# INSERT
								cursor.execute(f"""
									INSERT IGNORE INTO TBL_NEWS_KEYWORD_LIST 
									(
										WORD_MORPHEME, WORD_CLASS, UPDATE_DATE
									) 
									VALUES (
										"{word[0]}", "{word[1]}", NOW()
									)
								""")
								cursor.execute(f"""
									INSERT IGNORE INTO TBL_NEWS_KEYWORD_MAP 
									(
										WORD_ORIGIN, WORD_MORPHEME,
										NEWS_NO, WORD_COUNT
									) 
									VALUES (
										"{origin_word}", "{word[0]}",
										"{news_no}", 1
									)
								""")
								print(f'**** : [{out_idx}/{len(mining_result_data) -1}][{news_no}][{idx}/{len(data_list) - 1}][{origin_word}][{in_idx}/{len(data[1]) -1}] >> {word[0]} / {word[1]} / KEYWORD 추가 및 뉴스 매핑 완료!')
								cursor.execute(f"""
									UPDATE TBL_TOTAL_CAR_NEWS_LIST
									SET MINING_STATUS = 3, MINING_DATE = NOW(), 
										POSITIVE_COUNT = {news_info["positive_count"]}, NEGATIVE_COUNT = {news_info["negative_count"]},
										VA_COUNT = {news_info["va_count"]}, MORPHEME_COUNT = {news_info["morpheme_count"]}
									WHERE NEWS_NO = {news_no}
								""")
								# time.sleep(0.1)
					except Exception as e :
						print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 안쪽 오류!')
						pass
					finally : 
						print('-'*50)
						print(f'***** : [{out_idx}/{len(mining_result_data) -1}][{idx}/{len(data_list) - 1}][{news_no}] >> 분석 / INSERT 완료')
		except Exception as e :
			print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 바깥쪽 오류!')
			pass
		finally : 
			pass
			print('바깥쪽 종료')

	# # 유튜브 댓글 분석
	elif cont_type == 'youtube_comments' : 
		reviews = pd.read_excel('../data/youtube_comments/기아자동차레이_review_comments_youtube.xlsx')
		df_list = reviews.values.tolist()
		in_result_data = []

		# # step01. 형태소 분석 (데이터 가공)
		for idx in range(len(df_list)) :
			re_content = regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}]+', f'{df_list[idx][2]}')
			origin_sentence_list.append(df_list[idx][2])
			# print(re_summary)
			# print('-'*50)
			in_result_data = []
			in_result_data.append('idx')
			for word in re_content :
				in_result_word = []	
				group = []
				if (word not in except_word_list) :
					word_g = []
					word_g.append(word)
					group.append(word_g)
					# print(word)
					# print('-'*50)
					for keyword in kkma.pos(word) :
						if (keyword not in except_keyword_list) :
							# print(keyword)
							# print('-'*50)
							in_result_word.append(keyword)
					group.append(in_result_word)
				in_result_data.append(group)
			mining_result_data.append(in_result_data)
	
		# step02. DB Insert
		print(f'{len(mining_result_data)} > DB Insert')
		try : 
			for out_idx, data_list in enumerate(mining_result_data) :
				for idx, data in enumerate(data_list) :
					try : 
						origin_word = re.sub('[-=.#/?:$}\"\']', '', str(data[0])).replace('[','').replace(']','')
						print(f'*** : [{out_idx}/{len(mining_result_data) -1}][{idx}/{len(data_list) - 1}][{origin_word}]')
						for in_idx, word in enumerate(data[1]) :
							# print(f'[{word[0]}], [{word[1]}]')
							# INSERT
							cursor.execute(f"""
								INSERT IGNORE INTO TBL_NEWS_KEYWORD_LIST 
								(
									WORD_MORPHEME, WORD_CLASS, UPDATE_DATE
								) 
								VALUES (
									"{word[0]}", "{word[1]}", NOW()
								)
							""")
							print(f'**** : [{out_idx}/{len(mining_result_data) -1}][{idx}/{len(data_list) - 1}][{origin_word}][{in_idx}/{len(data[1]) -1}] >> {word[0]} / {word[1]} / KEYWORD 추가 완료!')
						time.sleep(0.1)
					except Exception as e :
						print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 안쪽 오류!')
						pass
					finally : 
						print('-'*50)
						print(f'***** : [{out_idx}/{len(mining_result_data) -1}][{idx}/{len(data_list) - 1}] >> 분석 / INSERT 완료')

		except Exception as e :
			print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 바깥쪽 오류!')
			pass
		finally : 
			print('바깥쪽 종료')
					
					
def run_text_mining() :
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	text_mining('news', dbconn, cursor)
	# text_mining('youtube_comments', dbconn, cursor)

	dbconn.commit()
	dbconn.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('뉴스 상세 내용 분석 DB Commit/Close 완료!')
	print('뉴스 상세 내용 분석 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('뉴스 상세 내용 분석 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))


# SQL 실행
def get_conn_cursor() :
	try:
		dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
		cursor = dbconn.cursor(dictionary=True)
		cursor.execute('SELECT NOW();')
		return dbconn, cursor
	except Exception:
		traceback.print_stack()
		print('재시도')
		return get_conn_cursor()


if __name__ == '__main__' : 
	# print(db_infos)
	# reload_list_data()
	# load_detail_data()
	# run_text_mining()

	print('스케쥴 작업 시작!')
	run_text_mining()

	# Schedule Work
	# 매일 4회 (오전 9시 / 오후 12시 / 오후 3시 / 오후 7시) 뉴스 데이터 수집
	# schedule.every().days.at('09:00').do(reload_list_data)
	# schedule.every().days.at('12:00').do(reload_list_data)
	# schedule.every().days.at('15:00').do(reload_list_data)
	# schedule.every().days.at('19:00').do(reload_list_data)

	# # 매일 1회 (오전 01시) 뉴스 본문 데이터 수집
	# schedule.every().days.at('01:00').do(load_detail_data)

	# # 매일 1회 (오전 05시) 뉴스 본문 데이터 분석
	# schedule.every().days.at('06:00').do(run_text_mining)
	# while True :
	# 	schedule.run_pending()
	# 	time.sleep(1)