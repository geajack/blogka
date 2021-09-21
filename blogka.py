import flask
import markdown
import pathlib
from os import listdir
from dataclasses import dataclass

from markdown.inlinepatterns import InlineProcessor, LinkInlineProcessor, LINK_RE
from markdown.extensions import Extension

class AnchorProcessor(InlineProcessor):
    def __init__(self, pattern, md):
        super().__init__(pattern, md)
        self.link_processor = LinkInlineProcessor(pattern, md)

    def handleMatch(self, m, data):
        tag, start, end = self.link_processor.handleMatch(m, data)
        return tag.text, start, end

class IndexMarkdownExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.deregister("link")
        md.inlinePatterns.register(AnchorProcessor(LINK_RE, md), "no-link", 160)


@dataclass
class ArticleSnippet:
    content: str
    slug: str

def render(raw):
    html = markdown.markdown(raw, extensions=[IndexMarkdownExtension(), "mdx_math"])
    return html


def slug_from_filename(filename):
    slug, extension = filename.split(".", 1)
    return slug


def filename_from_slug(slug):
    return slug + ".md"


application = flask.Flask("blogka")

@application.route("/")
def index():
    filenames = listdir("articles")
    articles = []
    for filename in filenames:
        path = "articles/" + filename
        slug = slug_from_filename(filename)
        with open(path, "r") as article_file:
            content = render(article_file.read())
        snippet = ArticleSnippet(content, slug)
        articles.append(snippet)
    return flask.render_template(
        "index.jinja",
        articles=articles
    )

@application.route("/<slug>")
def article(slug=None):
    filename = filename_from_slug(slug)
    path = "articles/" + filename
    with open(path, "r") as article_file:
        content = article_file.read()
    html = render(content)
    return flask.render_template(
        "article.jinja",
        content=html
    )


if __name__ == "__main__":
    application.run(port=8000)