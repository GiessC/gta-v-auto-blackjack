from typing import List


class Observable[TObserver]:
    observers: List[TObserver]

    def __init__(self):
        self.observers = []

    def attach(self, observer: TObserver):
        self.observers.append(observer)

    def detach(self, observer: TObserver):
        self.observers.remove(observer)
