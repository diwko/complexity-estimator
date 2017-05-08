class CodeReader:
    def __init__(self, mark_variable="#N#"):
        self.code = ""
        self.mark = mark_variable

    def read_from_file(self, path):
        try:
            with open(path, "r") as file:
                code = file.readlines()
            for line in code:
                self.code += line
        except FileNotFoundError:
            print("Nie znaleziono pliku: %s" % path)

    def read_from_string(self, text):
        self.code = text

    def get_function(self, scope={}):
        code = self.code
        mark = self.mark

        def fun(problem_size):
            exec(('%s = %d' % (mark, problem_size)), scope)
            exec(code, scope)
        return fun
