import flask
import markdown
import pathlib
from os import listdir

def render(raw):
    html = markdown.markdown(raw)
    return html


def slug_from_filename(filename):
    slug, extension = filename.split(".", 1)
    return slug

application = flask.Flask("blogka")

@application.route("/")
def index():
    filenames = listdir("articles")
    articles = []
    for filename in filenames:
        path = "articles/" + filename
        slug = slug_from_filename(filename)
        articles.append(slug)
    return flask.render_template(
        "index.jinja",
        articles=articles
    )

@application.route("/<slug>")
def article(slug=None):
    path = "articles/" + slug + ".md"
    with open(path, "r") as article_file:
        content = article_file.read()
    html = render(content)
    return flask.render_template(
        "article.jinja",
        content=html
    )


if __name__ == "__main__":
    application.run(port=8000)