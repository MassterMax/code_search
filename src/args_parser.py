import copy

# Здесь класс чтобы токенизировать строчку с аргументами

class TerminalArgsParser:
    def __init__(self, args_line):
        self.args_line_ = args_line
        self.current_tocken_ = None
        

    # Get current tocken.
    def get_tocken(self):
        return self.current_tocken_

    # Get next tocken.
    # Examples:
    #   Hello world (str was as "Hello world")
    #   Hello (str was without "")
    #   -p
    # (In case of success) delete a read part from args_line_, subsequent spaces and store new value in current_tocken_
    def next(self):
        if not self.args_line_:
            self.current_tocken_ = None
            return "end"
        result = None
        if self.args_line_[0] == '"':
            close_quote_ind = self.args_line_.find('"', 1)
            if close_quote_ind == -1:
                result = None
            else:
                result = self.args_line_[1: close_quote_ind - 1]
        else:
            end_text_ind = self.args_line_.find(' ')
            if end_text_ind == -1:
                result = self.args_line_
            else:
                result = self.args_line_[:end_text_ind]
        
        if result is None:
            return "Smth wrong with args"
        self.current_tocken_ = copy.copy(result)
        self.args_line_ = self.args_line_[len(result):].lstrip()
        return None