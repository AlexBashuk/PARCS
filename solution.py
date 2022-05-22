from Pyro4 import expose
import time

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        start_time = time.time()

        print("Workers %d" % len(self.workers))
        n = self.read_input()
        step = (n - 1) / len(self.workers) + 1

        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(1 + min(n, i * step), 1 + min(n, i * step + step)))

        print("Map finished: ", mapped)

        # reduce
        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))
        print("Job Finished")
        end_time = time.time()

        # output
        self.write_output(reduced, end_time - start_time)

    @staticmethod
    @expose
    def mymap(a, b):
        print (a, b)
        res = 0
        for i in xrange(a, b):
            res += i
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        output = 0
        for x in mapped:
            output += x.value
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, result, t):
        f = open(self.output_file_name, 'w')
        output = ""
        output += "Sum of numbers: " + str(result) + "\n"
        output += "Spent time: " + str(t) + "\n"
        f.write(output)
        f.close()