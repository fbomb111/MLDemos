from application import app

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():

    res = {"result": 0,
       "data": [], 
       "error": ''}

    res["result"] = 1
    res["data"] = [0.1, 0.2, 0.1, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0]

    return res

if __name__ == '__main__':
	# run!
	app.run()