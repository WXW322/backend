from Fields_info.base_field import base_field

class loc_field(base_field):

    def __init__(self, loc=(None, None), word_type=None, content = None):
        super().__init__(content)
        self.loc = loc
        self.word_type = word_type

    def get_content_count(self):
        return len(self.content)

    def get_wordtype(self):
        return self.word_type

    def get_loc(self):
        return self.loc






