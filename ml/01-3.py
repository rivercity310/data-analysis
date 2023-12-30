import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

# Machine Learning: 스스로 기준을 찾아서 일을 진행
# 모델: ML 알고리즘을 구현한 프로그램 또는 구체화하여 표현한 것

# [ K-최근접 이웃 알고리즘(K-Nearest Neighbors) / 모델 ]
# - 어떤 데이터에 대한 답을 구할 때 주위의 다른 데이터를 보고 다수를 차지하는 것을 정답으로 판단
# - KNeighborsClassifier() 생성자
#       1. n_neighbors: 이웃의 개수 (기본값 5)
#       2. p: 거리를 재는 방법 (1: 맨해튼 거리, 2: 유클리디안 거리, 기본값 2)
#       3. n_jobs: 사용할 CPU 코어 (-1: 모든 코어 사용, 기본값 1), fit() 메서드에는 영향 없고 거리 계산 속도만 향상
# - 단점
#       1. 데이터가 많을 경우 메모리 사용이 크고 시간이 오래 걸림
#       2. kn._fit_X, kn._y 속성에 전달한 data를 다 들고있음
# - 즉, 전달한 데이터를 모두 들고 있다가 새로운 데이터가 등장하면 이웃 거리를 계산하여 정답 예측

bream_length = [25.4, 26.3, 26.5, 29.0, 29.0, 29.7, 29.7, 30.0, 30.0, 30.7, 31.0, 31.0,
                31.5, 32.0, 32.0, 32.0, 33.0, 33.0, 33.5, 33.5, 34.0, 34.0, 34.5, 35.0,
                35.0, 35.0, 35.0, 36.0, 36.0, 37.0, 38.5, 38.5, 39.5, 41.0, 41.0]

bream_weight = [242.0, 290.0, 340.0, 363.0, 430.0, 450.0, 500.0, 390.0, 450.0, 500.0, 475.0, 500.0,
                500.0, 340.0, 600.0, 600.0, 700.0, 700.0, 610.0, 650.0, 575.0, 685.0, 620.0, 680.0,
                700.0, 725.0, 720.0, 714.0, 850.0, 1000.0, 920.0, 955.0, 925.0, 975.0, 950.0]

smelt_length = [9.8, 10.5, 10.6, 11.0, 11.2, 11.3,
                11.8, 11.8, 12.0, 12.2, 12.4, 13.0, 14.3, 15.0]

smelt_weight = [6.7, 7.5, 7.0, 9.7, 9.8, 8.7, 10.0,
                9.9, 9.8, 12.2, 13.4, 12.2, 19.7, 19.9]

length = bream_length + smelt_length
weight = bream_weight + smelt_weight

fish_data = [[l, w] for l, w in zip(length, weight)]
fish_target = [1] * 35 + [0] * 14


# 1. 주어진 데이터에 대해 matplotlib을 이용하여 산점도 그리기
def ex1():
    global bream_length, bream_weight

    # 길이에 따른 무게 산점도 그리기
    plt.scatter(bream_length, bream_weight)
    plt.scatter(smelt_length, smelt_weight)
    plt.xlabel("length")
    plt.ylabel("weight")

    plt.savefig("scatter_grp.png", dpi=800)
    plt.show()


def ex2():
    # kn 객체에 fish_data와 fish_target을 전달하여 기준을 학습(training)시킴
    kn = KNeighborsClassifier()
    kn.fit(fish_data, fish_target)                 # fit(): 주어진 데이터로 알고리즘을 훈련
    print(kn.score(fish_data, fish_target))        # score(): 모델을 평가 (정확도 = (맞힌 갯수) / (전체 개수))
    print(kn.predict([[30, 600]]))                 # predict(): 새로운 데이터의 정답을 예측

    # 전달한(학습시킨) 데이터를 내부적으로 들고있기 때문에 메모리 사용량이 크다는 단점
    print(kn._fit_X)
    print(kn._y)


def ex3():
    kn = KNeighborsClassifier(n_neighbors=49, n_jobs=-1, p=1)
    kn.fit(fish_data, fish_target)

    print(kn.score(fish_data, fish_target))         # 정확도: 35/49 = 0.714..
    print(kn.predict([[30, 600]]))


def ex4():
    kn = KNeighborsClassifier()
    kn.fit(fish_data, fish_target)

    for n in range(5, 50):
        kn.n_neighbors = n
        score = kn.score(fish_data, fish_target)

        if score < 1:
            print(n, score)


if __name__ == "__main__":
    ex4()
