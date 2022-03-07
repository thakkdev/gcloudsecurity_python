from flask import Flask, url_for, Response, request
from flask import render_template, session, redirect
from flask.helpers import make_response
from matplotlib.figure import Figure
from pricegraph import plotgraph
from util import access_secret_version
import os
from middleware import validatetoken
from authlib.integrations.flask_client import OAuth

app = Flask(__name__, static_folder="static", static_url_path="")

# get sessionkey from Secret Manager
sessionKey = access_secret_version('pricestats', 'sessionkey', '1')

# assign session key for managing Flask session
app.config['SECRET_KEY'] = sessionKey

app.config.from_object('config')

#register OAuth
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/')
def index():
    """ renders index.html page
    """
    return render_template('index.html')


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    idinfo = oauth.google.parse_id_token(token)
    
    if idinfo['iss'] != 'https://accounts.google.com':
        return f"wrong issuer" 

    userid = idinfo['sub']

    accesstoken = token.get('access_token')
    if accesstoken:
        session[userid] = accesstoken
        ipaddr = request.remote_addr
        session[ipaddr] = userid
        resp = make_response(redirect('/home')) # instead of return redirect('/home')
        resp.set_cookie('access_token', accesstoken)
        #resp.set_cookie('refresh_token', 'YOUR_REFRESH_TOKEN') TODO
        return resp

@app.route('/home')
@validatetoken
def homepage():
    sessiontoken = pullaccesstoken()
    if sessiontoken == 'Error':
     return f'Access Denied'
 
    return render_template('home.html', accesstoken= sessiontoken)        

  
@app.route('/data', methods = ['POST', 'GET'])
@validatetoken
def data():
    """ renders data.html page. /data action called on form submit within index.html
    """
    if request.method == 'GET':
        return f"Access Denied"  #deny access if get request directly to data.html
    
    if request.method == 'POST':
        formdata = request.form
        session['formvar'] = formdata #store formdata in session
        sessiontoken = pullaccesstoken() 
        if sessiontoken == 'Error':
            return f"Access Denied" 

        return render_template('data.html', form_data = formdata, accesstoken = sessiontoken )
 
@app.route("/imageshow.jpeg")
@validatetoken
def plot_jpeg():
    """ renders the image. /imageshow.jpeg action is invoked from img tag of data.html
    """       
    formvar = session.pop('formvar', None) #fetch formdata from session
    output = plotgraph(formvar) #call to generate price chart
    return Response(output.getvalue(), mimetype="image/jpeg")

def pullaccesstoken():
    ipaddr = request.remote_addr
    
    #In production deny access for ipaddr with localhost address or IP's in a 
    # given range TODO
    useridsession = session.get(ipaddr)
    if useridsession == None:
        return 'Error'
        
    accesstokensession = session.get(useridsession)
    if accesstokensession == None:
        return 'Error'
    
    return accesstokensession

@app.route('/logout')
def logout():
    ipaddr = request.remote_addr
    useridsession = session.get(ipaddr)
    # check for useridsession. 
    # useridsession key  maps to accesstoken. If exists then remove key from session
    if useridsession != None:
            session.pop(useridsession)
    
    #remove ipaddr key that maps to userid
    session.pop(ipaddr)
    return redirect('/')

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')