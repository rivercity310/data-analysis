import sys

sys.path.append(r"C:\Users\seungsu\Desktop\projects\unittest\ml")

from sample import Sample


# 결정 트리

class DecisionTreeEx:
    def __init__(self):
        sample = Sample()
        self.wine_data, self.wine_target = sample.read_remote_wine_data()


if __name__ == "__main__":
    dt = DecisionTreeEx()