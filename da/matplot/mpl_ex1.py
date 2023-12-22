import matplotlib.pyplot as plt
import math


def ex1():
    # 연도별 GDP 변화 그래프 그리기
    years = list(range(1950, 2011, 10))
    gdp = [67.0, 80.0, 257.0, 1686.0, 6505.0, 11865.3, 22105.3]

    # plot(): 선형 차트 만들기
    plt.plot(years, gdp, color='green', marker='o', linestyle='solid')

    plt.title("GDP per capita")     # 차트 제목 설정
    plt.ylabel("dollars")           # y축 레이블
    plt.xlabel("years")             # x축 레이블

    plt.savefig("gdp_per_capita.png", dpi=600)      # 파일로 저장, dot per inch 값 지정
    plt.show()      # 화면에 차트 표시


def ex2():
    # y = 2x 그래프 그려보기
    x = [i for i in range(-10, 10)]
    y = [2 * t for t in x]

    plt.plot(x, y, color='red', marker='o')
    plt.axis([-20, 20, -20, 20])        # 그래프를 그릴 영역 지정
    plt.show()


def ex3():
    # 하나의 차트에 여러 개의 데이터를 중첩하여 그리기
    # y = 2x, y = x^2 + 5, y = x^2 - 5
    x = [x for x in range(-20, 20)]
    y1 = [2 * t for t in x]
    y2 = [t ** 2 + 5 for t in x]
    y3 = [t ** 2 - 5 for t in x]

    # 포맷 지정명령을 통해 선의 형태 제어 가능
    # r, g, b -> 색상 지정
    # --(점선), -(실선), :(짧은 점선)
    # ^(세모), *(별표) 표식
    plt.plot(x, y1, "r--", label="y = 2x")
    plt.plot(x, y2, "g^-", label="y = x^2 + 5")
    plt.plot(x, y3, "b*:", label="y = x^2 - 5")
    plt.axis([-30, 30, -30, 30])

    plt.xlabel("x label")
    plt.ylabel("y label")
    plt.title("functions")

    plt.legend()    # 디폴트 위치에 범례 표시하기
    plt.savefig("functions.png", dpi=800)
    plt.show()


def ex4():
    # sin 그래프 그려보기
    # math module의 sin(), cos() 함수는 radian을 사용
    # 따라서 각을 라디안으로 변환해야 함
    # math.radians(angle)을 통해 변환 가능

    x = []
    y = []

    for angle in range(360):
        x.append(angle)
        y.append(math.sin(math.radians(angle)))

    plt.plot(x, y)
    plt.title("Sine Wave")
    plt.savefig("sine_wave.png", dpi=800)
    plt.show()


if __name__ == "__main__":
    ex4()
