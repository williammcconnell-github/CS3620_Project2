class MadLibString:
    def __init__(self, text, is_input):
        self.text = text
        self.is_input = is_input

    def get_text(self):
        return str(self.text)

    def is_input(self):
        return self.is_input
