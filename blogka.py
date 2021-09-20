import flask

application = flask.Flask("blogka")

@application.route("/<slug>")
def article(slug=None):
    path = "articles/" + slug + ".md"
    with open(path, "r") as article_file:
        content = article_file.read()
    return flask.render_template(
        "article.jinja",
        content=content
    )


if __name__ == "__main__":
    application.run(port=8000)