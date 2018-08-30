from flask import Flask, request
import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template

app = Flask(__name__)





@app.route('/')
def index():
    return render_template('index.hmtl')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False)
