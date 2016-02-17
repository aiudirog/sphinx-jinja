from docutils.parsers.rst import Directive
from docutils import nodes
from jinja2 import Template
from docutils.statemachine import StringList


class JinjaDirective(Directive):

    has_content = True
    required_arguments = 1
    app = None

    def run(self):
        node = nodes.Element()
        node.document = self.state.document
        cxt = self.app.config.jinja_contexts[self.arguments[0]]

        tpl = Template("\n".join(self.content))
        self.content[:] = StringList(tpl.render(**cxt).split("\n"))
        self.state.nested_parse(self.content, self.content_offset,
                                node, match_titles=1)
        return node.children


def setup(app):
    JinjaDirective.app = app
    app.add_directive('jinja', JinjaDirective)
    app.add_config_value('jinja_contexts', {}, 'html')