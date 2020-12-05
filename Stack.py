class Stack:
    def __init__(self, height_limit=None):
        self.contents = []
        self.height_limit = height_limit

    def push(self, item):
        if self.height_limit:
            if (self.height() + 1) > self.height_limit:
                msg = "This Stack has a height_limit set to: {}".format(
                    self.height_limit
                )
                raise ValueError(msg)
        self.contents.append(item)

    def pop(self):
        return self.contents.pop()

    def peek(self):
        return self.contents[-1]

    def isEmpty(self):
        return self.height() == 0

    def height(self):
        return len(self.contents)
