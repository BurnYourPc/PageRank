from bottle import route, run, template, post, request
from src.createWorld import createWorld

@route('/')
def base():
    return "Hello!!"


@post('/createworld')
def pageRank():
    data = request.json
    urls = data["urls"]
    sites = []
    for url in urls:
        sites.append(url['site'])
    urldict = createWorld.countOutlinks(sites)
    print(urldict)
    return urldict


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8000)
