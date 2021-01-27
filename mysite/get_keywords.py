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
from bs4 import BeautifulSoup

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath('./mysite'))
# SECURITY WARNING: keep the secret key used in production secret!
db_info_file = os.path.join(BASE_DIR, 'db_conn.json')
with open(db_info_file) as f :
	db_infos = json.loads(f.read())

# 뉴스 분석
mining_result_data = []
def text_mining(cont_type, dbconn, cursor) :
	kkma = Kkma()
	car_news_list = TblTotalCarNewsList.objects.all().filter(mining_status=1).exclude(news_content = '')
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

	# 뉴스 본문 분석
	if cont_type == 'news' : 

		# step01. 형태소 분석 (데이터 가공)
		for idx in range(len(car_news_list)) :
		# for idx in range(10) :
			re_content = regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}]+', f'{car_news_list[idx].news_content}')
			origin_sentence_list.append(car_news_list[idx].news_summary)
			# print(re_summary)
			# print('-'*50)
			in_result_data = []
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
				in_result_data.append(group)
			mining_result_data.append(in_result_data)

		# step02. DB Insert
		print('DB Insert')
		try : 
			for out_idx, data_list in enumerate(mining_result_data) :
				print('DB Insert 2')
				for idx, data in enumerate(data_list) :
					try : 
						if idx == 0 :	
							news_no = data_list[0]
						else : 
							origin_word = re.sub('[-=.#/?:$}\"\']', '', str(data[0])).replace('[','').replace(']','')
							print(f'*** : [{out_idx}/{len(mining_result_data) -1}][{news_no}][{idx}/{len(data_list)}][{origin_word}]')

							for in_idx, word in enumerate(data[1]) :
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
									SET MINING_STATUS = 3, MINING_DATE = NOW() 
									WHERE NEWS_NO = {news_no}
								""")
								time.sleep(0.1)
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
			print('바깥쪽 종료')

	# 유튜브 댓글 분석
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


if __name__ == '__main__' : 
	run_text_mining()