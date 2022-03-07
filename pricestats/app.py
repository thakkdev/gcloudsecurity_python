from flask import Flask, Response, request, render_template, session
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from pricegraph import plotgraph
from util import access_secret_version
import os

app = Flask(__name__)

sessionKey = access_secret_version('pricestats', 'sessionkey', '1')

app.config['SECRET_KEY'] = sessionKey

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly"
    if request.method == 'POST':
        formdata = request.form
        session['formvar'] = formdata
        return render_template('data.html', form_data = formdata)

@app.route("/imageshow.jpeg")
def plot_jpeg():
    """ renders the plot on the fly.
    """
    formvar = session.pop('formvar', None)
    output = plotgraph(formvar)
    return Response(output.getvalue(), mimetype="image/jpeg")

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')