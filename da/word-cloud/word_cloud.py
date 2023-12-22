import wikipedia                               # 위키백과의 내용을 가져오는 모듈 (pip install wikipedia)
import matplotlib.pyplot as plt                # matplotlib: 시각화/차트 라이브러리
from wordcloud import WordCloud, STOPWORDS     # 워드 클라우드 이미지 생성 모듈 (pip install wordcloud)


# 화면에 이미지를 그려주는 함수 (matplotlib)
def _drawing_image(wc):
    plt.figure(figsize=(40, 30))
    plt.imshow(wc)
    plt.show()


def _get_word_cloud(keyword: str, stop_words: set[str]):
    # Word Cloud: 각 단어의 빈도나 중요성을 크기를 통해 시각화
    # - 즉, 텍스트 데이터를 시각적으로 제공할 때 유용
    # - 주로 SNS나 웹 사이트의 텍스트 데이터를 분석하는 데 널리 사용
    # - matplotlib, pandas, wordcloud 모듈 이용
    page = wikipedia.page(keyword)                                            # 위키백과 사전으로부터 컨텐츠 추출
    return WordCloud(width=2000, height=1500, stopwords=stop_words).generate(page.content)     # 워드클라우드 생성


# 중지어(stop word): one, using, two 등 자연어 처리에 있어서 특별한 의미를 갖지 않는 단어
# wordcloud 모듈의 STOPWORDS: 집합 자료구조로 중지어들을 모아둠
# 중지어를 추가하고자 싶으면 새 집합을 정의한 뒤 합집합을 구해서 사용
if __name__ == "__main__":
    keyword = input("검색 키워드 입력: ")
    stop_words = STOPWORDS | {"one", "first", "using", "two", "make", "use"}        # 또는 .union 메서드
    word_cloud = _get_word_cloud(keyword, stop_words)
    _drawing_image(word_cloud)


