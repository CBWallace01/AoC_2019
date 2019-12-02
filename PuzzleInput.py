from urllib import request


class ReadInput:
    data = ""

    def __init__(self, day):
        try:
            f = open("input/day%s.txt" % (day))
            self.data = f.read().split("\n")
            f.close()
            print("Reading File")
        except IOError:
            link = "https://adventofcode.com/2019/day/%s/input" % day
            req = request.Request(link)
            req.add_header('Cookie', 'session=53616c7465645f5f5fd5983dbe5e3f1af2e4ba4828bed4482c300c055065bf646490dac542a8d0e218d849a86e50ff58')
            f = request.urlopen(req)
            self.data = f.read().decode('utf-8').split("\n")
            f.close()
            f = open("input/day%s.txt" % (day), "w+")
            for line in self.data:
                f.write("%s\n" % line)
            f.close()
            print("Reading URL")
