#!/usr/bin/env python3
# Templater by Infected

from ..libs.rainbow import msg

class Templater():
    """Templater"""
    def __init__(self, template):
        self.template = template # Template as string
        self.pre_render = []
        self.id_table = {'\n':'\n'}
        self.stags = ('{{', '{%', '{#', '\n')
        self.etags = ('}}', '%}', '#}', '')
        self.elements = {
            'label': self.add_label,
            'button': self.add_button,
            'input': self.add_input,
            'html': self.add_html,
            '\n': self.add_line
            }

    def render(self):
        html = """<script type="text/javascript">function send_event(e){console.log('sent_event'+e.id);$.post('/plugin/event/',{id:e.id,value:e.value});};</script>
        """ # AJAX sender
        for id_ in self.pre_render:
            html += self.elements[self.id_table[id_][0]](self.id_table[id_], id_)
        msg(html, 0, 'render', level=4, slevel='html')
        return html

    def get_onclick(self):
        return "onclick='send_event(this);'"

    def get_onchange(self):
        return "onchange='send_event(this);'"

    def parse(self):
        self.html_id = 0

        def get_tag_end(start_tag, tag_type, cursor):
            tag_closing = self.etags[self.stags.index(tag_type)]
            end_position = self.template[cursor:].find(tag_closing)
            if end_position == 0: # if not found or no closing
                end_position = start_tag
                cursor = start_tag
            else:
                old_cursor = cursor
                cursor = cursor + end_position + len(tag_closing)
                end_position += old_cursor # Match end_tag to old cursor
            return end_position, cursor

        def get_next_tag(position):
            start_tag = None
            for tag in self.stags:
                tag_found = self.template[position:].find(tag)
                if tag_found >= 0:
                    if start_tag:
                        if position + tag_found + len(tag) < start_tag:
                            start_tag = position + tag_found + len(tag)
                            tag_type = tag
                    else:
                        start_tag = position + tag_found + len(tag)
                        tag_type = tag

            if start_tag is not None:
                end_tag, cursor = get_tag_end(start_tag, tag_type, position)
            else:
                tag_type = None
                start_tag = None
                end_tag = None
                cursor = position

            return tag_type, start_tag, end_tag, cursor

        def get_html_id(html_id):
            return html_id + 1, 'html_' + str(html_id)

        def parse_tag(tag_type, tag):
            """ Parse tag regarding his type
            """
            if tag_type == self.stags[0]: # {{
                parsed_tag = tag.split(';')
                self.id_table[parsed_tag[1]] = [parsed_tag[0]]
                if len(parsed_tag) >= 3:
                    self.id_table[parsed_tag[1]].extend(parsed_tag[2:])
                self.pre_render.append(parsed_tag[1])

            elif tag_type == self.stags[1]: # {%
                self.html_id, id_ = get_html_id(self.html_id)
                parsed_tag = ['html', tag]
                self.id_table[id_] = parsed_tag
                self.pre_render.append(id_)

            elif tag_type == self.stags[2]: # {#
                pass

            elif tag_type == self.stags[3]: # \n
                self.pre_render.append('\n')

        cursor = 0 # Parsing position

        while cursor < len(self.template):
            # tag_meta = type, start, end, cursor end
            tag_meta = get_next_tag(cursor)
            if tag_meta[0]:
                tag = self.template[tag_meta[1]:tag_meta[2]].strip()
                parse_tag(tag_meta[0], tag)
                cursor = tag_meta[3]
            else:
                cursor = len(self.template)

    def add_label(self, data, id_):
        """{{ label;id;text }}"""
        if len(data) >= 2:
            tag = data[0]
            text = data[1]
        return "<p id='{}'>{}</p>".format(id_, text)

    def add_button(self, data, id_):
        """{{ button;id;button_label }}"""
        if len(data) >= 2:
            tag = data[0]
            label = data[1]
        return "<button {} id='{}' value='{}'>{}</button>".format(self.get_onclick(), id_, id_, label)

    def add_input(self, data, id_):
        """{{ input;id;value;type }}"""
        if len(data) >= 2:
            tag = data[0]
            value = data[1]
        type_ = 'text'
        return "<input {} id='{}' value='{}' placeholder='{}' type='{}'>".format(self.get_onchange(), id_, value, value, type_)

    def add_html(self, html_data, id_):
        """{% <some></html> %}"""
        if len(html_data) >= 2:
            tag = html_data[0]
            html = html_data[1]
        return html

    def add_line(self, extra, id_):
        """\n"""
        return '<br>'


if __name__ == '__main__':
    template = """{{ label;label_0;My Input Label }}{{ input;form_0;input label }}{# Comment #}
    {% <h1>Raw html</h1> %}{# ID cannot start with html_ #}}
    {{button;button_0;My Button}}"""
    templater = Templater(template)
    templater.parse()
    print(templater.render())
