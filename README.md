# 카뉴스.zip 🙈 (car_news.zip)
### 9개 자동차 관련 언론사에서 뉴스 스크래핑 및 분석
#### 중고차/신차/자동차업계 뉴스 및 시승기
![가장 편한 자동차 정보 - 카뉴스집](http://carnewszip.com/static/images/common/img_share.png "가장 편한 자동차 정보 - 카뉴스집")  

### 정보
- 접속 URL : <a href="http://carnewszip.com">http://carnewszip.com</a>
- 테이블 명세서 : <a href="https://docs.google.com/spreadsheets/d/1TOZSDXpLZaXQhyP-K11WmGR_dQ1tswQc181uI90sgF4/edit#gid=0">https://docs.google.com/spreadsheets/d/1TOZSDXpLZaXQhyP-K11WmGR_dQ1tswQc181uI90sgF4/edit#gid=0</a>
- 9개 자동차 언론사 : 모터그래프, 오토헤럴드, 데일리카, 오토뷰, IT조선, 오토모닝, 오토다이어리, 카가이, 더드라이브
- 수집 분야 : 중고차/신차/자동차업계 뉴스 및 시승기

---

### 추가해야할 기능
- 카뉴스집 소개 구성 (간단하게)
- 좋아요(스크랩) 기능 (좋아요 테이블 추가)
  - 좋아요 한 페이지 별도 구성
- 유튜브 자동차 관련 영상 수집 테스트
- 네이버 자동차 블로그 수집 / 분석 테스트
- 네이버 자동차 댓글 수집 / 분석 테스트

- <del>유튜브 영상 댓글 수집 >> 2021.01.14</del>
- <del>뉴스 수집(본문) / 분석 Batch 작업 >> 2020.12.31</del>
- <del>뉴스 목록 타입 (스타일) 선택 제공 >> 2020.12.31</del>
- <del>코드 리팩토링 >> 2020.12.30</del>
  - <del>view 정리 (기능별 분리)</del>
  - <del>Template 공통 코드 처리 (Extends)</del>
- <del>기자 이름 함께 수집 >> 2020.12.29</del>
- <del>뉴스 검색 >> 2020.12.28</del>
- <del>뉴스 분석 (Konlpy, Kkma) >> 2020.12.27</del>
  - <del>뉴스 본문 어절 분리 (regex)</del>
  - <del>뉴스 본문 형태소 분석</del>
- <del>뉴스 클릭 수 카운팅 (표시) >> 2020.12.15</del>
- <del>뉴스 목록 페이징 처리 (스크롤 로드 방식) >> 2020.12.15</del>
- <del>메뉴 기능 추가 (각 카테고리별 언론사 보기, 언론사별 뉴스 모아보기) >> 2020.12.14</del>
- <del>회원(회원가입) >> 2020.12.08</del>
- <del>회원(로그인) >> 2020.12.07</del>
- <del>테마 (light모드, dark모드) >> 2020.12.01</del>
- <del>get_data.py 코드 리팩토링 >> 2020.12.01</del>

---

### History
#### 2021.01.18 (월)
- 형태소 분석 된 단어 라벨링 (긍/부정)
  - 문장 긍/부정 테스트

#### 2021.01.17 (일)
- 차종별 여론 확인 화면 UI구성
  - Mobile 대응
- 형태소 분석 된 단어 라벨링 (긍/부정)

#### 2021.01.14 (목)
> 차종별 여론을 확인할 수 있는 메뉴를 추가하기로 결정했다. 여론은 네이버 카 토크와 유튜브 차종별 시승기 영상 댓글에서 수집하여 뿌려주기로 했다.  
다만 유튜브 시승기 영상에는 영상 자체에 대한 댓글도 많아 이부분 필터링에 대한 고민도 필요해보인다.
- 유튜브 영상 검색 결과 영상들에 대한 댓글 수집 테스트
- 차종별 여론 확인 화면 UI구성 및 기능 구현
  - 수집 > xlsx파일 저장 > xlsx파일 로드하여 front 화면 노출

#### 2021.01.13 (수)
- 유튜브 영상별 댓글 수집 테스트

#### 2021.01.12 (화)
- 유튜브 영상 검색 결과 가져오기 테스트

#### 2021.01.11 (월)
- 형태소 분석 된 단어 라벨링 (긍/부정)
  - 일반 부사, 부사격 조사, 어근, 일반 관형사

#### 2021.01.08 (금)
- 형태소 분석 된 단어 라벨링 (긍/부정)
  - 형용사, 보조사, 동사

#### 2021.01.07 (목)
- 뉴스 목록 > View Count 오류 수정

#### 2021.01.06 (수)
- 자동차 여론 확인 콘텐츠 추가
  - 네이버 자동차토크 댓글 수집 > CSV파일 저장

#### 2021.01.05 (화)
- 자동차 여론 확인 콘텐츠 추가
  - 네이버 자동차토크 댓글 수집 

#### 2021.01.04 (월)
> 최초 계획은 자동차 뉴스 본문을 분석하여 특정 브랜드나 차종의 평가 데이터 등을 얻어내는게 목적이었으나, 자동차 뉴스기사는 대부분 브랜드에서  
내놓은 자료를 편집하여 그대로 전달하는 역할을 하고 있어 쉽지 않아 보였다. 그러던 중 네이버 자동차에서 모델별로 댓글이 있는 것을 확인할 수 있었고  
꽤나 활성화 되어있었다. 이곳에서 댓글을 수집하여 모델별 여론 반응 데이터를 만들어보려고 한다. 
- 자동차 여론 확인 콘텐츠 추가
  - 네이버 자동차토크 댓글 수집 
- 뉴스 수집 / 분석 Schedule daemon 실행
  - 실행방법 및 log 확인방법 확인
  - 모니터링 및 이슈 조치

#### 2021.01.02 (토)
> 언론사 1개를 추가하면서 데이터를 검수 중 뭔가 꼬이는 부분이 발견되어 수집 및 삭제를 직접 쿼리문으로 조작하다가.. (데이터가 꼬였던 이유는 언론사 추가할때 뉴스 카테고리 변수를 잘못 부여..) 약 300여개의 뉴스 데이터를 날렸다.  하하.. 순간 머리가 하얘졌다. 마음과 머릿속은 너무 복잡한데 주말이라 내 시간만 챙길 순 없는 법.. 흑ㅜㅜ
- 뉴스 언론사 추가 (모터그래프)

#### 2021.01.01 (금)
> 서버에 올려 Schedule작동을 확인하는데 몇번은 잘 작동되는 듯 싶더니 형태소 분석 단계에서 또 처음보는 에러를 접했다. ```broken pipe``` 에러였다.  검색해보니 잦은 입출력 호출로 발생된다고 했다. 그래서 아래와 같이 신규 뉴스 수집 횟수는 늘리고 뉴스 본문 데이터 수집 및 분석은 새벽시간에 하는 것으로 변경하니 일단 첫날은 이상없이 잘 작동했다.  

---
#### 2021 새해 원하는 것 다 이루자!! 🐮
---

#### 2020.12.31 (목)
> Schedule작동은 좀 더 지켜봐야겠지만(DB서버에서 튕겨냄 증상 빈번), 일단 하루 Local에서 테스트 해본 결과는 이슈가 없었다.  이제 서버에 올려서 확인해봐야겠다. Schedule 작업을 끝으로 2020년의 마지막 기능추가가 끝났다. 회원별 좋아요(스크랩) 기능은 현재 시점에서는 크게 필요가 없을 것 같아 (비활성화된 서비스) 일단 보류하고 다른 기능을 먼저 구현할 생각이다. 2020년 작업은 여기서 마무리하고 새해부터 시작할 예정. 
- 뉴스 수집(본문) / 분석 Schedule 작업
  - 서버에서 Schedule 작업 진행 / 테스트
- 뉴스 목록 타입 (스타일) 선택 UI 구성 및 기능 구현

#### 2020.12.30 (수)
> 이제 뉴스 수집 및 분석 로직은 views.py에서 분리할때가 됐다.  그 후 서버에서 Schedule 작업 테스트를 진행 예정이다.
- 뉴스 수집(본문) / 분석 Schedule 작업
  - 데이터 수집, 분석, DB 삽입 코드는 별도 파일로 분리
  - 분리 후 서버에서 Schedule 작업 진행 / 테스트  
  ![배치정보 - 카뉴스집](http://carnewszip.com/static/images/common/img_batch.png "배치정보 - 카뉴스집")  

#### 2020.12.29 (화)
> 계속해서 많은량의 데이터를 DB에 넣으면 서버에서 접근을 막아버린다. 이렇게 되면 주기적으로  뉴스 수집 및 분석 Schedule 작업을 서버에서 돌릴 수 없다. (현재는 로컬에서 수동으로 실행 중)  오늘은 주로 로직을 수정해가면서 테스트를 진행했다. db connect를 close()하면서 문제가 생기는 것 같은데.. 솔직히 모르겠다.ㅠㅠ 사수가 필요하다..
- SNS 공유용 이미지 (og tag)
- 뉴스 작성 기자 정보 수집
- 분석 완료시점 기록
- 분석 로그 확인 및 수정 필요

#### 2020.12.28 (월)
- 분석 완료된 기사 체크할 때 분석 완료된 시점도 기록
  - TBL_TOTAL_CAR_NEWS_LIST 테이블 > MINING_DATE COLUMN 추가
- 뉴스 수집 시 기자 이름도 포함하여 수집
  - TBL_TOTAL_CAR_NEWS_LIST 테이블 > REPOTER_NAME COLUMN 추가

#### 2020.12.24 (목)
> 뉴스 목록 API에 검색기능까지 추가해서 검색결과까지 기존 뉴스 목록에 보여주려다보니 (그렇게 하려고 계획했던 것은 아니었지만 하다보니..)  결과 데이터로 뉴스목록 뿐만 아니라 검색결과 개수까지도 넘겨줘야 하는데 그 과정에서 데이터타입에 문제가 생겼다. 뉴스목록만 넘겨줄땐  
ORM Filter로 목록만 serialize해서 넘기면 됐는데 검색결과의 총 갯수를 같이 넘겨주려고 검색결과 뉴스 목록과 총 개수를 dict형태로   넘겨줫으나 templates에서 받을땐 string으로 계속 변환이 됐다. views에서 json.dumps를 해줘도 마찬가지..  
여기서 꽤 오랜시간을 허비했는데 그냥 templates에서 데이터를 사용할때 JSON.parse(data) 해주면 되는 문제였다.  
사실 이렇게 문제 해결하는게 옳은건지는 모르겠지만 어쨋든 원하는대로 검색 기능은 잘 작동된다.
- 뉴스 검색 기능 구현

#### 2020.12.23 (수) 
- 뉴스 검색 UI 수정 (모바일 최적화)
- 뉴스 검색 기능 구현
- 뉴스 본문 분석 DB INSERT(추가 34건) 및 데이터 검수 > 총 215건

#### 2020.12.22 (화)
> 오늘은.. ```MySQL Connection not available``` 에러.. ..ㅋㅋ
- 뉴스 검색 UI 추가
- 뉴스 검색 기능 구현
- 뉴스 본문 분석 DB INSERT(추가 51건) 및 데이터 검수 > 총 181건

#### 2020.12.21 (월)
> 오늘도 분석/INSERT 중 새로운 에러를 접했다. ```system error: 32 Broken pipe``` ㅠㅠ 계속 처음보는 에러와의 싸움.. 근 5일동안 DB와 씨름을 하고 있으니 슬슬 루즈해진다.  내일은 간만에 UI작업을 진행해야겠다.
- 뉴스 본문 분석 DB INSERT(추가 45건) 및 데이터 검수 > 총 127건

#### 2020.12.20 (일)
> (밤) 구글링을 하며 이것저것 계속 시도하다가 /etc/my.cnf 파일에 ```innodb_buffer_pool_dump_at_shutdown = 1```, ```innodb_buffer_pool_load_at_startup = 1``` 속성을 추가하니 DB서버는 다시 시작이 됐다. 하지만 다시 데이터를 수집해보려 했으나 "10038 소켓 이외의 개체에 작업을 시도했습니다".. 또다시 분노.. 근데 정말 오랜 구글링 끝에 의외의 곳에서 단서를 찾아서 해결했다. db connect close 메소드의 실행 위치 문제였다.. 계속 리팩토링 하면서 이것저것 옮기다가 그랬나보다. 어쨋든 서비스는 다시 살아났다. 

> (오전) 오늘 새벽까지 계속 DB에 INSERT를 해서인가..? 갑자기 오전부터 DB서버가 죽었다.  
재시작 하려고 해도 ```Job for mariadb.service failed because the control process exited with error code.``` 란 메세지와 함께 DB서버가 실행도 되지 않는다..  하.. 서버쪽에서 문제가 생길때가 가장 난감하다. 결국 이 문제는 밤까지 해결하지 못했다. 어차피 방문자는 없었겠지만 하루동안 서비스가 죽은 꼴이다. 빨리 조치해보자..

#### 2020.12.19 (토)
> 약 25건씩 실행문을 걸어놓고 수시로 확인을 하는데  
10건을 채우지 못하고 계속 DB서버 연결 종료를 이유로 프로그램이 종료가 된다.  
결국 오전부터 자기전까지 하루 종일 중간중간 신경쓰면서 수집한 데이터는 58건.. 일단 최초 누적된 데이터를 처리할때까지는 별다른 대책없이 이렇게 고생을 해야만 하는건가..
- 뉴스 본문 분석 DB INSERT(추가 58건) 및 데이터 검수 > 총 82건

#### 2020.12.18 (금)
> 예상했던대로(?) 많은 데이터를 분석하며 형태소 단어 단위로 쪼개어  테이블에 넣다보니 서버에서 ```Lost connection to MySQL server at 'server ip', system error: 10054``` 에러를 내며 튕겨내며 프로그램이 종료가 됐다. 역시 쉬운일이 없다.  오늘도 계속 찾아보자.  
- 뉴스 본문 분석 DB INSERT(추가 24건) 및 데이터 검수 > 총 29건
- 서버 MariaDB 설정 변경 ```max_allowed_packet=256M```

#### 2020.12.17 (목)
> 뉴스 기사를 분석 결과를 담을 테이블은 만들었으나,  
테이블에 INSERT하려면 데이터를 구조화 해야한다.  
이런 경험이 많지 않다보니 쉽지 않고, 테스트 코드를 실행하는 환경이  
임의로 만든 페이지를 호출해서 결과를 확인하고 있어 시간도 오래걸리고 있다. 분명히 훨씬 효율적인 방법이 있을텐데 ㅠㅠ..  
- 뉴스 기사 분석을 위한 데이터 구조화
- DB INSERT 테스트(추가 5건) 및 데이터 검수

#### 2020.12.16 (수)
> 테이블 추가 및 컬럼 변경으로 인한 DB정리  ,
inspectdb > local, server migration 완료..  
(작업 환경마다 꼬여있어서 migrations 못하고 있었음..) 
DB수정할때마다 잊지말고 inspectdb!
- DB정리 (local,server migrations)
- 뉴스 기사 분석을 위한 테이블 설계/생성
- 뉴스 본문 어절 분리
- 형태소 분석 테스트 (Konlpy, Kkma)

#### 2020.12.15 (화)
- 뉴스 목록 페이징 처리 (infinity scroll data load 방식)
  - 기능 구현
- 네이버 서치어드바이저, 구글 서치콘솔 사이트 등록
- 뉴스 카운트 기능 추가 (기사별 클릭 횟수)
- 뉴스 list Template 개선 
- 뉴스 본문 어절 분리
- 형태소 분석 테스트 (Konlpy, Kkma)

#### 2020.12.14 (월)
> 현재 각 언론사 목록 페이지에서 뉴스 제목, 요약내용만 가져오고 있는 상황(기사별 2~3줄)  
데이터 분석을 위한 각 상세페이지에 접근하여 기사 전체 내용 스크랩 필요

- 테이블 생성,수정,삭제
  - 테이블 명세서 히스토리 참조
- 뉴스 상세 데이터(제목, 내용) 스크랩, DB INSERT 로직 추가
- 뉴스 목록 페이징 처리 (스크롤 로드 방식)
  - 기능 구현

#### 2020.12.13 (일)
- 뉴스 클릭 수 카운팅 기능
  - UI 구성
  - models에 column추가 했으나 migrations되지 않는 문제로 기능 구현은 하지 못함
- 뉴스 목록 페이징 처리 (스크롤 로드 방식)
  - 효율적인 뉴스 목록 로드를 위한 구상 (param) 

#### 2020.12.12 (토)
- 뉴스 list 로드 방식 수정
  - ajax 호출 방식 (카테고리 클릭 시 해당 목록만 호출하여 노출)
- GNB 메뉴 추가 (UI, 기능)
  - 모바일 최적화
  - param에 따른 데이터 및 화면 구성 
    - 메뉴 클릭 시 마다 통신을 해야하니 이게 최선의 방법인지는 고민 필요,,

#### 2020.12.11 (금)
- 뉴스 list 로드 방식 수정
  - ajax 호출 방식 (카테고리 클릭 시 해당 목록만 호출하여 노출)
- GNB 메뉴 추가 (UI, 기능)
  - UI 구성
  - 뉴스 목록 urls, view 재정의 (카테고리, 언론사 별로 load를 위한 param 정의)

#### 2020.12.10 (목)
- 뉴스 TABLE 재설계(통합)
  - 뉴스 카테고리별로 테이블 구분 불필요 판단 > 통합뉴스 테이블에서 뉴스 카테고리 column을 생성
  - view(뉴스 수집 로직) 수정
- 뉴스 list 로드 방식 수정
  - ajax 호출 방식 (카테고리 클릭 시 해당 목록만 호출하여 노출)

#### 2020.12.09 (수)
- 로그인, 회원가입, 로그아웃 기능 구현
- SECRET_KEY, DB정보 분리 배포
 - 도메인 구입, 연결 (고대디 > <a href="http://www.carnewszip.com">http://www.carnewszip.com</a>)

#### 2020.12.08 (화)
- 로그인, 회원가입, 로그아웃 기능 구현
- Template 개선 (모바일 최적화)

#### 2020.12.07 (월)
- 로그인, 회원가입 Template 작업

#### 2020.12.04 (금)
- CentOS8 서버 셋팅
  - Python, Django
  - MariaDB

#### 2020.12.02 (수)
- 호스팅 서버 임대 (Conoha.jp)
- CentOS8 서버 셋팅
  - Python, Django
  - MariaDB

#### 2020.12.01 (화)
- 뉴스 가져오기 기능 웹 버튼으로 구현
- Skin기능 구현 (light, dark모드)

#### 2020.11.24 (화)
- 배포 (github, pythonanyway)

#### 2020.11.23 (월)
- 오토모닝 썸네일 비노출 이슈 확인 (URL변경되는 이슈?) > data 다시 수집 > 해결
- 뉴스 기사 좋아요 기능을 위한 column 추가 (LIKE_CNT)
- 배포 (github, pythonanyway)
  - settings.py파일은 ignore

#### 2020.11.19 (목)
- Django > 웹 구현 (뉴스 목록)
- list > today tag 추가 (오늘날짜 뉴스에 tag 표시)
- 시승기 카테고리 추가 (추가 언론사)
- 업계뉴스 카테고리 추가 (추가 언론사)

#### 2020.11.18 (수)
- Django > 웹 구현 (뉴스 목록)
- 시승기 카테고리 추가
- 업계뉴스 카테고리 추가
- 뉴데일리 중고차 이미지 URL 수정 
  - 이미지 스크랩 방어 코드로 되어 있어 분기처리로 대체 ('이미지를 불러올 수 없습니다')

#### 2020.11.17 (화)
- 불필요한 TABLE 정리
- Django > 웹 구현 (뉴스 목록)

#### 2020.11.11 (수)
- 뉴스 기사 형태소 분석
 - keyword 넣을 TABLE생성

#### 2020.11.10 (화)
- python에서 mariaDB연결
  - (ATC TEST DB)
- TABLE생성, 스크래핑한 뉴스 data INSERT

#### 2020.11.09 (월)
- 자동차 뉴스 사이트 4개 > 신차 뉴스, 중고차 뉴스 데이터 스크래핑
  - (오토헤럴드, 데일리카, 오토뷰, IT조선)
- python에서 mariaDB연결
  - (ATC TEST DB)