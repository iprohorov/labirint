from threading import Thread

class Intelect(Thread):
    def __init__(self, map, inputData_q, outData_q):
        Thread.__init__(self)
        self.inputData_q = inputData_q
        self.outData_q = outData_q
        self.map = map
    def run(self):
        pass