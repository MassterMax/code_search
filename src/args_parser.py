import copy


# Класс чтобы токенизировать строчку с аргументами

class TerminalArgsParser:
    def __init__(self, args_line):
        self.args_line_ = args_line
        self.current_token_ = None

    # Get current token.
    def get_token(self):
        return self.current_token_
    def is_end(self):
        return self.current_token_ is None

    # Get next token.
    # Examples:
    #   Hello world (str was as "Hello world")
    #   Hello (str was without "")
    #   -p
    # (In case of success) delete a read part from args_line_, subsequent spaces and store new value in current_token_
    def next(self):
        if not self.args_line_:
            self.current_token_ = None
            return
        result = None
        read_length = 0
        if self.args_line_[0] == '"':
            close_quote_ind = self.args_line_.find('"', 1)
            if close_quote_ind == -1:
                result = None
            else:
                result = self.args_line_[1: close_quote_ind]
            read_length = len(result) + 2
        else:
            end_text_ind = self.args_line_.find(' ')
            if end_text_ind == -1:
                result = self.args_line_
            else:
                result = self.args_line_[:end_text_ind]
            read_length = len(result)

        if result is None:
            return "Smth wrong with args"
        self.current_token_ = copy.copy(result)
        self.args_line_ = self.args_line_[read_length:].lstrip()
        return None
