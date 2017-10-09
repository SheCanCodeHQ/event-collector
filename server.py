import http.server
from urllib.parse import urlparse, parse_qs
import get_meetup_data
import eventbrite_collector
import subprocess

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    Page = '''\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Event Collector</title>
  </head>
  <body>
    <h1>Search for events</h1>
    <form class="" action="#" method="get">
      <label for="start">Start date: </label><input name="start" type="date" required="true"/>
      <label for="start">End date: </label><input name="end" type="date" required="true"/>
      <button type="submit">GO</button>
    </form>
    {csv_links}
  </body>
</html>
'''

    def do_GET(self):
        csv_paths = set('/{}'.format(filename) for filename in self.get_csv_files())
        if self.path in csv_paths:
            self.send_csv(self.path.lstrip('/'))
            return
        query_components = parse_qs(urlparse(self.path).query)
        if ('start' in query_components and 'end' in query_components):
            start, end = query_components['start'][0], query_components['end'][0]
            get_meetup_data.main(start, end)
            eventbrite_collector.main(start, end)
        page = self.create_page()
        self.send_page(page)

    def send_csv(self, filename):
        try:
            f = open(filename)
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/csv')
            self.end_headers()
            # Write content as utf-8 data
            self.wfile.write(bytes(f.read(), "utf8"))
            f.close()
        except IOError:
            self.send_error(404,'File Not Found: {}'.format(filename))

    def send_page(self, page):
        # Send response status code
        self.send_response(200)

         # Send headers
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()

        # Write content as utf-8 data
        self.wfile.write(bytes(page, "utf8"))

    def create_page(self):
        values = {
            'csv_links' : self.create_csv_links(),
        }
        page = self.Page.format(**values)
        return page

    def get_csv_files(self):
        try:
            result = subprocess.check_output('ls *.csv', shell=True)
            return str(result, 'utf-8').strip('\n').split('\n')
        except subprocess.CalledProcessError:
            return []

    def create_csv_links(self):
       files = self.get_csv_files()
       return '<br>'.join(['<a href="{0}"> {0} </a>'.format(filename) for filename in files])

if __name__ == '__main__':
    server_address = ('0.0.0.0', 8081)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    print('running server on {}:{}'.format(server_address[0],str(server_address[1])))
    httpd.serve_forever()
