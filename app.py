import cherrypy

import os.path,json,simplejson
from lib import get_top_ten_stocks, get_stock_by_name
from jinja2 import Environment, FileSystemLoader

cur_dir = os.path.dirname(os.path.abspath(__file__))
env =Environment(loader=FileSystemLoader(cur_dir),trim_blocks=True)

class StockListing(object):
    @cherrypy.expose
    def index(self):
        top_stocks = get_top_ten_stocks()
        template = env.get_template("index.html")
        return template.render(top_stocks = top_stocks)
    
    @cherrypy.expose
    def search_by_name(self, stock_name):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps(dict(get_stock_by_name(stock_name.upper()))).encode('utf8')

if __name__ == '__main__':
    

    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 80
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'public'
        },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        }
    }
    webapp = StockListing()
    cherrypy.quickstart(StockListing(), config = conf)
