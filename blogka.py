import flask
import markdown
import pathlib
import os
from os import listdir, walk
from pathlib import Path
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
    slug = filename.stem
    return slug


def filename_from_slug(slug):
    return slug + ".md"


def get_articles_directory():
    return Path(os.environ.get("BLOGKA_ARTICLES_DIRECTORY", "."))


application = flask.Flask("blogka")

@application.errorhandler(FileNotFoundError)
def error(exception):
    return flask.render_template(
        "error.jinja",
        error_code=404,
        error_message="Article not found"
    ), 404


@application.route("/")
@application.route("/<int:page_number>")
def index(page_number=1):
    directory = get_articles_directory()
    filenames = list(directory.glob("*.md"))
    filenames.sort(key=lambda filename: -os.path.getctime(directory / filename))

    articles_per_page = 10
    start_index = articles_per_page * (page_number - 1)
    
    n_pages = len(filenames) // 10
    if len(filenames) % 10 > 0:
        n_pages += 1

    filenames = filenames[start_index:start_index + articles_per_page]

    articles = []
    for filename in filenames:
        path = directory / filename
        slug = slug_from_filename(filename)
        with open(path, "r") as article_file:
            content = render(article_file.read())
        snippet = ArticleSnippet(content, slug)
        articles.append(snippet)
    return flask.render_template(
        "index.jinja",
        articles=articles,
        page_number=page_number,
        n_pages=n_pages
    )

@application.route("/articles/<slug>")
def article(slug=None):
    filename = filename_from_slug(slug)
    path = get_articles_directory() / filename
    with open(path, "r") as article_file:
        content = article_file.read()
    html = render(content)
    return flask.render_template(
        "article.jinja",
        content=html
    )


if __name__ == "__main__":
    application.run(port=8000)