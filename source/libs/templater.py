#!/usr/bin/env python3
# Templater by Infected

from jinja2 import Environment
# from .libs.rainbow import msg

class Templater():
    """Templater"""
    def __init__(self, template):
        self.env = Environment()
        self.gen_filters()
        self.template = self.env.from_string(template)
        self._id = 0
        self._data_table = {}

    def gen_filters(self):
        self.env.filters['button'] = self.button
        self.env.filters['input'] = self.input
        self.env.filters['form'] = self.form

    def untemplate(self):
        return self.template.render().replace('\n', '<br>')

    def get_id(self):
        current_id = self._id
        self._id += 1
        return current_id

    def button(self, label):
        text = "<button type='button' id='{}'>{}</button>".format(
            self.get_id(),
            label
            )
        return text

    def input(self, label):
        text = "<input id='{}' type='text' name='{}' value='default'></input>".format(
            self.get_id(),
            label
            )
        return text

    def form(self, label, fields):
        return None
