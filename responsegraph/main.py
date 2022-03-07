import io
from flask import Flask, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg
from graph import plotgraph


app = Flask(__name__)

@app.route("/")
def index():
    return f"""
    <form method=get action="/">
    <input type=submit value="update graph">
    </form>
    
    <h3>Plot as a png</h3>
    <img src="/matplot-as-image.png"
         alt="random points as png"
         height="800" width="1500"
    >
    """
@app.route("/matplot-as-image.png")
def plot_png():
    """ renders the plot on the fly.
    """
    #fig = Figure()
    fig = plotgraph()

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")

if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="localhost", port=8080, debug=True)
    