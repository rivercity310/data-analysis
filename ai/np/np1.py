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
    print(ages[ages >= 20])     # 20 이상인 원소를 추출하여 반환


if __name__ == "__main__":
    ex1()
