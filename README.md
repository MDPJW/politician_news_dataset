## 한국 정치인 뉴스 데이터셋

이 데이터셋은 네이버 뉴스에서 2013. 1. 1 부터 2019. 3. 10 까지 생성된 뉴스를 수집한 데이터입니다. 총 20 개의 카테고리로 이뤄져 있으며, 각 카테고리는 아래의 질의어로 검색된 뉴스로 구성되어 있습니다.

```
category 0: 김무성
category 1: 김영삼
category 2: 나경원
category 3: 노무현
category 4: 노회찬
category 5: 문재인
category 6: 박근혜
category 7: 박원순
category 8: 박지원
category 9: 반기문
category 10: 심상정
category 11: 안철수
category 12: 안희정
category 13: 오세훈
category 14: 유승민
category 15: 유시민
category 16: 이명박
category 17: 이재명
category 18: 홍준표
category 19: 황교안
```

Git repository 에는 데이터를 다운로드 받고 이를 로딩하기 위한 파이썬 코드만 제공하며, 실제 데이터는 `fetch` 함수를 이용하여 다운로드 받아야 합니다. 이는 한 번만 다운로드 하시면 됩니다. 다운로드의 설치법은 아래에 있습니다.

각 카테고리의 데이터는 [`lovit_textmining_dataset`](https://github.com/lovit/textmining_dataset) 의 뉴스 데이터와 같은 형식으로 이뤄져 있습니다. 데이터는 `data` 디렉토리에 저장되어 있으며, 각 카테고리 별 압축 파일은 `zips` 디렉토리에 저장됩니다. 패키지의 디렉토리 구조는 아래와 같습니다. `txt` 에는 뉴스 본문이, `index` 에는 각 뉴스에 대한 메타 데이터 (언론사, 기사 아이디, 작성 시간, 카테고리, 타이틀) 가 저장되어 있습니다.

```
|-- politician_news_dataset
|-- data
    |-- 0
        |-- news
            |-- 2013-01-01_politician.txt
            |-- 2013-01-01_politician.index
            |-- ...
    |-- 1
        |-- news
            |-- 2013-01-01_politician.txt
            |-- 2013-01-01-politician.index
            |-- ...
    |-- 19
        |-- news
            |-- ...
|-- zips
    |-- news
        |-- 0.zip
        |-- 1.zip
        ...
        |-- 19.zip
```


## Usage

이 repository 를 복사한 뒤, `fetch` 함수를 한 번 실행해야 합니다. `fetch` 함수는 한 번만 실행하면 됩니다. `

```
git clone https://github.com/lovit/politician_news_dataset.git
```

`category` 를 입력하지 않으면 20 개의 모든 카테고리의 데이터가 다운로드 및 설치 됩니다.

```python
from politician_news_dataset import fetch

fetch()
```

특정 카테고리의 데이터만 설치하고 싶을 때에는 `category` 에 int 형식의 번호를 입력합니다. `remove_zip=False` 를 설정하면 다운로드 받은 압축 파일도 삭제하지 않습니다. 기본값은 `remove_zip=True` 입니다.

```python
from politician_news_dataset import fetch

fetch(category=0, remove_zip=False)
```

이 repository 에서는 설치된 뉴스 기사를 손쉽게 이용할 수 있는 파이썬 클래스를 함께 제공합니다. `News` 클래스는 특정한 기간의 뉴스 기사와 각 기사에 대한 인덱스를 손쉽게 로딩할 수 있도록 도와줍니다. `News` 는 각 카테고리 별로 이용 가능합니다. `begin_date`, `end_date` 를 설정하지 않으면 설치된 기간의 모든 뉴스 기사가 검색됩니다.

```pytohn
from politician_news_dataset import News

news = News(category=0)
```

특정 기간의 기사만 이용할 경우에는 다음처럼 class instance 를 만들 수도 있습니다. 기간의 형식은 `yyyy-mm-dd` 형식의 str 입니다. `begin_date` 와 `end_date` 의 한가지 값만 입력할 경우 데이터에 존재하는 가장 최근의 날짜 혹은 가장 빠른 날짜를 자동으로 설정합니다.

```pytohn
from politician_news_dataset import News

news = News(category=0, begin_date='2013-01-01', end_date='2015-01-01')
news = News(category=0, begin_date='2013-01-01') # unbounded end date
news = News(category=0, end_date='2015-01-01')   # unbounded begin date
```

News class instance 는 해당 기간 내의 날짜 별 뉴스 기사의 개수를 `num_docs` attribute 에 저장하고 있습니다.

```python
news.num_docs
```

`num_docs` 의 형식은 (date, num doc) 로 이뤄진 list of tuple 입니다.

```
 ...
 ('2018-11-30', 21),
 ('2018-12-01', 8),
 ('2018-12-02', 23),
 ('2018-12-03', 14),
 ('2018-12-04', 43),
 ('2018-12-05', 94),
 ('2018-12-06', 64),
 ('2018-12-07', 58),
 ('2018-12-08', 5),
 ('2018-12-09', 17),
 ('2018-12-10', 24),
 ('2018-12-11', 38),
 ('2018-12-12', 34),
 ('2018-12-13', 14),
 ('2018-12-14', 9),
 ...
```

News class instance 는 특정 기간의 뉴스 기사와 인덱스를 로딩하는 기능을 제공합니다. 각 뉴스 기사는 한 줄의 텍스트로 제공되며, 뉴스 기사 내 줄바꿈은 두 칸 띄어쓰기로 구분됩니다. 이는 `soynlp` 의 DoublespaceLineCorpus 의 형식입니다.

```python
for doc in news.get_text():
    # do something
    # double space line corpus format
    sents = doc.split('  ')
```

News class instance 를 만들 때의 기간 내의 특정 기간의 뉴스만 다시 한 번 선택할 수도 있습니다. 이 역시 `begin_date`, `end_date` 중 하나만 설정할 경우, 다른 한 쪽은 class instance 의 최초 혹은 최근 값으로 설정됩니다.

```python
for doc in news.get_text(begin_date='2018-12-01', end_date='2018-12-10'):
    # do something
    # double space line corpus format
    sents = doc.split('  ')
```

각 뉴스에 대한 인덱스 역시 제공됩니다. 이 역시 `begin_date`, `end_date` 에 의하여 기간을 특정할 수 있습니다.

```python
for index in news.get_index(begin_date='2017-01-01', end_date='2017-01-10'):
    # do something
    # namedtuple format
```

인덱스는 namedtuple 형식입니다. 언론사, 기사 아이디, 뉴스 카테고리의 코드, 작성 날짜와 시간, 그리고 뉴스 기사가 제공됩니다.

```
Index(
    press_id='021',
    article_id='0002301296',
    category='100',
    date='2017-01-10',
    time='2017-01-10 12:12',
    title='黨윤리위 재건 나선 印… 親朴핵심 압박 가속화'
)
```

`get_text` 와 `get_index` 는 list of str 과 list of namedtuple 형식의 데이터를 return 합니다. 기간이 길 경우 모든 데이터를 메모리에 올리게 됩니다. 이를 방지하기 위하여 `iter_text` 와 `iter_index` 함수를 제공합니다. 이들은 각 뉴스 기사 별로 기사와 인덱스를 yield 합니다. 이 역시 기간을 특정할 수 있습니다.

```python
for doc in news.iter_text(begin_date='2017-01-01', end_date='2017-01-10'):
    # do something
    # namedtuple format

for index in news.iter_index(begin_date='2017-01-01', end_date='2017-01-10'):
    # do something
    # namedtuple format
```

뉴스 기사와 인덱스를 함께 이용하기 위해서는 아래처럼 zip 함수를 이용할 수도 있습니다.

```python
begin_date='2017-01-01'
end_date='2017-01-01'

for doc, index in zip(news.iter_news(begin_date, end_date), news.iter_index(begin_date, end_date)):
    print(index.title, len(doc))
    # or do some other things
```
