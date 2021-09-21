import flask
import markdown
import pathlib
import os
from os import listdir, walk
from pathlib import Path
from dataclasses import dataclass
from urllib.parse import urljoin

from markdown.inlinepatterns import InlineProcessor, LinkInlineProcessor, ImageInlineProcessor, LINK_RE, IMAGE_LINK_RE
from markdown.extensions import Extension

class AnchorProcessor(InlineProcessor):
    def __init__(self, pattern, md):
        super().__init__(pattern, md)
        self.link_processor = LinkInlineProcessor(pattern, md)

    def handleMatch(self, m, data):
        tag, start, end = self.link_processor.handleMatch(m, data)
        return tag.text, start, end

class ImageProcessor(InlineProcessor):
    def __init__(self, pattern, md):
        super().__init__(pattern, md)
        self.image_processor = ImageInlineProcessor(pattern, md)

    def handleMatch(self, m, data):
        tag, start, end = self.image_processor.handleMatch(m, data)
        base_articles_url = urljoin(flask.request.base_url, "/articles/")
        url = urljoin(base_articles_url, tag.attrib["src"])
        tag.attrib["src"] = url
        return tag, start, end

class IndexMarkdownExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.deregister("link")
        md.inlinePatterns.deregister("image_link")
        md.inlinePatterns.register(AnchorProcessor(LINK_RE, md), "no-link", 160)
        md.inlinePatterns.register(ImageProcessor(IMAGE_LINK_RE, md), "image-link", 150)


@dataclass
class ArticleSnippet:
    content: str
    slug: str

def render(raw):
    html = markdown.markdown(raw, extensions=[IndexMarkdownExtension(), "mdx_math"])
    return html


def get_blog_title():
    return os.environ.get("BLOGKA_TITLE", None)


def get_articles_directory():
    return Path(os.environ.get("BLOGKA_ARTICLES_DIRECTORY", "."))


application = flask.Flask("blogka")

@application.errorhandler(Exception)
def error(exception):
    return flask.render_template(
        "error.jinja",
        error_code=500,
        error_message="Internal error",
        blog_title=get_blog_title()
    ), 500


@application.errorhandler(FileNotFoundError)
def error(exception):
    return flask.render_template(
        "error.jinja",
        error_code=404,
        error_message="Article not found",
        blog_title=get_blog_title()
    ), 404

@application.route("/style.css")
def stylesheet():
    path = os.environ.get("BLOGKA_STYLESHEET", "static/style.css")
    return flask.send_file(path)

@application.route("/")
@application.route("/<int:page_number>")
def index(page_number=1):
    directory = get_articles_directory()
    filepaths = list(directory.glob("*.md"))
    filepaths.sort(key=os.path.getctime)
    filepaths.reverse()

    articles_per_page = 10
    start_index = articles_per_page * (page_number - 1)
    
    n_pages = len(filepaths) // 10
    if len(filepaths) % 10 > 0:
        n_pages += 1

    filepaths = filepaths[start_index:start_index + articles_per_page]

    articles = []
    for filepath in filepaths:
        slug = filepath.name
        with open(filepath, "r") as article_file:
            content = markdown.markdown(article_file.read(), extensions=[IndexMarkdownExtension(), "mdx_math"])
        snippet = ArticleSnippet(content, slug)
        articles.append(snippet)

    return flask.render_template(
        "index.jinja",
        articles=articles,
        page_number=page_number,
        n_pages=n_pages,
        blog_title=get_blog_title()
    )

@application.route("/articles/<filename>")
def article(filename=None):
    directory = get_articles_directory()
    path = directory / filename
    
    assert path.parent.resolve() == directory.resolve()

    if path.suffix == ".md":
        with open(path, "r") as article_file:
            content = article_file.read()
        html = markdown.markdown(content, extensions=["mdx_math"])
        return flask.render_template(
            "article.jinja",
            content=html,
            blog_title=get_blog_title()
        )
    else:
        return flask.send_file(str(path), attachment_filename=str(filename))


if __name__ == "__main__":
    application.run(port=8000)