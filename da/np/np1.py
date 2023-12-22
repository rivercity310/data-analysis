import numpy as np

# numpy
# - 데이터 과학에서 사용, 리스트에 비해 처리 속도가 매우 빠름
# - 리스트 간 다양한 연산 기능 제공
# - pandas(데이터 분석 패키지), Scikit-learn, TensorFlow(ML 패키지) 등이 넘파이 위에서 작동


def ex1():
    # ndarray
    # - C언어 기반 n차원 배열: 메모리를 적게 차지하고 속도가 빠름
    # - 배열 간 벡터 연산 지원
    # - 동일 자료형 저장 (만약 서로 다른 문자열을 전달하면 모두 str로 바꿈)
    #   - 모든 원소가 동일 자료형이면 각 데이터 항목에 필요한 저장공간이 일정
    #   - 따라서 원하는 위치에 바로 접근 가능(임의 접근, Random Access)
    mid_scores = np.array([10, 20, 30])
    final_scores = np.array([40, 50, 60])

    # 벡터 연산
    print(mid_scores + final_scores)
    print(mid_scores - final_scores)
    print(mid_scores * final_scores)
    print(mid_scores / final_scores)

    print("-" * 100)

    # 속성값
    a = np.array([10, 20, 30])
    print(a.shape)      # 형태
    print(a.ndim)       # 차원
    print(a.dtype)      # 데이터 타입
    print(a.itemsize)   # 내부 자료 1개의 메모리(byte) 크기
    print(a.size)       # 전체 항목 수
    print(a.size * a.itemsize)      # a 객체 전체의 메모리 크기

    # 배열에 스칼라 값을 더하는 연산도 가능
    print(a + 100)      # 각 원소가 100씩 증가
    print(a - 10)
    print(a * 5)
    print(a / 2)

    # 인덱싱과 슬라이싱 가능
    b = np.array(range(1, 102, 10))
    print(b)
    print(b[-1])
    print(b[3:-2])

    c = np.array([[10, 20, 30], [40, 50, 60]])
    print(c[1, 2])      # numpy 스타일 인덱싱 (= c[1][2])
    print(c[0:2, 0:2])  # numpy 스타일 슬라이싱

    # 논리 인덱싱 (Logical Indexing)
    ages = np.array([15, 19, 21, 25, 30])
    print(ages >= 20)           # 조건을 만족하는 1차원 bool 배열 반환
    print(ages[ages >= 20])     # 해당 bool 배열을 인덱스로 넣어서 바로 20 이상인 원소를 추출할 수도 있음


def ex2():
    # np.arange = np.array(range)
    print(np.arange(5))
    print(np.arange(1, 6))
    print(np.arange(1, 10, 2))

    # np.linspace(start, stop, num)
    # [start, stop] 범위에서 num개만큼 균일한 간격의 수를 갖는 배열 생성 (included)
    print(np.linspace(0, 10, 50))

    # np.logspace(x, y, n)
    # [10^x, 10^y] 범위에서 n개까지 균일한 간격의 로그 스케일 수를 갖는 배열 생성
    print(np.logspace(0, 5, 10))

    # np.reshape()
    # 데이터의 개수는 유지한 채로 배열의 차원과 형태를 변경
    # -1 전달시 데이터의 개수에 맞춰서 자동으로 배열 형태 결정
    y = np.arange(12)
    print(y.reshape(3, 4))      # 3행 4열
    print(y.reshape(6, -1))     # 열 자동으로 결정 (2열)

    # np.flatten()
    # 2차원 이상의 고차원 배열을 1차원 배열로 평탄화
    y = np.array([[1, 2, 3], [4, 5, 6]])
    print(y.flatten())


def ex3():
    # 난수 생성하기 (균등 확률 분포)
    # 규칙성이 전혀 없는 난수 생성 -> 컴퓨터로 불가능
    # 의사 난수: seed를 주어 해시함수를 통해 난수 생성 (0.0 ~ 1.0)
    # 같은 seed값은 같은 난수를 발생시킴
    np.random.seed(100)
    print(np.random.rand(5))            # 난수 5개로 이루어진 1차원 배열
    print(np.random.rand(5, 3))         # 난수 5x3으로 이루어진 2차원 배열
    print(np.random.rand(2, 3, 4))      # 난수 2x3x4로 이루어진 3차원 배열

    # 정수 난수 배열
    print(np.random.randint(1, 7, size=10))
    print(np.random.randint(1, 11, size=(4, 7)))

    # 정규 분포를 따르는 난수 생성
    print(np.random.randn(5))         # 평균 0, 표준편차 1인 표준정규분포를 따르는 난수 5개 배열
    print(np.random.randn(5, 4))    # 5x4 표준정규분포를 따르는 난수 배열

    # 만약 다른 평균, 표준편차를 지정하고 싶으면
    mu = 10     # 평균
    sigma = 2   # 표준편차
    print(mu + (sigma * np.random.randn(5, 4)))

    # 평균이 175, 표준편차가 10인 정규분포를 따르는 데이터 10000개 분석
    mu = 175
    sigma = 10
    heights = mu + (sigma * np.random.randn(10000))     # 난수 데이터 생성
    print(np.mean(heights))     # 평균값
    print(np.median(heights))   # 중앙값


def ex4():
    # corrcoeff(x, y): 두 배열의 상관관계 계산하기
    # [[Cxx, Cxy], [Cyx, Cyy]]
    # - 피어슨 상관 계수 (두 변량의 공분산을 각각의 표준편차를 서로 곱한 값으로 나눈 것)
    # - 자기 자신과의 상관관계는 1이므로 행렬의 대각선은 언제나 1
    # - 또한 (x, y)와 (y, x)는 대칭이므로 대칭행렬을 이룸

    # x의 값과 y의 값이 모두 증가하는 방향이므로 둘 사이의 상관관계가 매우 높게 나옴
    x = [i for i in range(100)]
    y = [i**2 for i in range(100)]
    print(np.corrcoef(x, y))

    # 여러 배열의 상관관계 계산하기: 배열로 묶어서 전달
    # [[Cxx, Cxy, Cxz], [Cyx, Cyy, Cyz], [Czx, Czy, Czz]]
    z = [100 * np.sin(3.14 * i / 100) for i in range(100)]
    print(np.corrcoef([x, y, z]))


if __name__ == "__main__":
    ex4()
