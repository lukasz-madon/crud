from invoke import run, task

@task
def clean(client=True, server=True, extra=''):
    patterns = ["heroku"]
    if client:
        run("cd client && grunt clean")
    if server:
        patterns.append("server/static")
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        run("rm -rf %s" % pattern)

@task
def build(docs=False):
    run("python setup.py build")
    if docs:
        run("sphinx-build docs docs/_build")