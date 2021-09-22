# Blogka

Minimalist blogging platform powered by markdown and your server's file system. Blogka will render and serve any markdown files whose names end in `.md` in a specified directory as HTML.

## Usage

Blogka is a WSGI app and therefore can be run using any WSGI server such as gunicorn, e.g.

```
gunicorn blogka
```

It has three configuration options, set via environment variables.

- `BLOGKA_TITLE` The title of the blog. If unspecified, no title will be rendered and thr HTML page titles will be simply "Blog".
- `BLOGKA_ARTICLES_DIRECTORY` The directory, absolute or relative to the CWD, in which articles are stored as markdown files with names ending in `.md`. If unspecified, defaults to the CWD.
- `BLOGKA_STYLESHEET` Path to a custom CSS stylesheet.

## Installation

```
pip install git+https://github.com/geajack/blogka.git
```

## Security note

Treat any files in the articles directory as public. Any file whose name doesn't end in `.md` can be accessed directly at `/articles/<filename>`. This is necessary for local image embedding to work correctly and intuitively.