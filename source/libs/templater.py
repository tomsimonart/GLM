#!/usr/bin/env python3
# Templater by Infected


class Templater():
    """Templater"""
    def __init__(self, template):
        self.template = template # Template as string
        self.pre_render = []
        self.id_table = {}
        self.stags = ('{{', '{%', '{#', '\n')
        self.etags = ('}}', '%}', '#}', '')
        self.elements = {
            'button':self.add_button,
            'input':self.add_input,
            'html':self.add_html
            }

    def render(self):
        html = ''
        for id in self.pre_render:
            html += self.elements[self.id_table[id][0]](self.id_table[id])
        return html

    def parse(self):
        html_id = 0

        def get_tag_end(start_tag, tag_type):
            tag_closing = self.etags[self.stags.index(tag_type)]
            end_position = self.template[start_tag:].find(tag_closing)
            print(end_position)
            if end_position == 0: # if not found or no closing
                end_position = start_tag + len(tag_type)
            cursor = end_position + len(tag_closing)
            return end_position, cursor

        def get_next_tag(position):
            start_tag = None
            for tag in self.stags:
                position = self.template[position:].find(tag)
                if start_tag:
                    if position < start_tag:
                        start_tag = position + len(tag)
                        tag_type = tag
                else:
                    start_tag = position + len(tag)
                    tag_type = tag
            end_tag, cursor = get_tag_end(start_tag, tag_type)
            return tag_type, start_tag, end_tag, cursor

        def get_html_id(html_id):
            return html_id + 1, 'html_' + str(html_id)

        def parse_tag(tag_type, tag):
            if tag_type == self.stags[0]:
                print(tag)
                parsed_tag = tag.split(';')
                self.id_table[parsed_tag[1]] = [parsed_tag[0]]
                if len(parsed_tag) >= 3:
                    self.id_table[parsed_tag[1]].extend(parsed_tag[2:])
                self.pre_render.append(parsed_tag[1])
            elif tag_type == self.stags[1]:
                html_id, id = get_html_id(html_id)
                parsed_tag = ['html', tag]
                self.id_table[id] = parsed_tag
                self.pre_render.append(id)
            elif tag_type == self.stags[2]:
                pass

        cursor = 0 # Parsing position

        while cursor < len(self.template):
            # tag_meta = type, start, end, cursor end
            tag_meta = get_next_tag(self.template[cursor:])
            tag = self.template[tag_meta[1]:tag_meta[2]].strip()
            parse_tag(tag_meta[0], tag)
            cursor = tag_meta[3]


    def add_button(self, data):
        if len(data) >= 2:
            id = data[0]
            label = data[1]

    def add_input(self, data):
        if len(data) >= 2:
            id = data[0]
            value = data[1]

    def add_html(self, html):
        return html
