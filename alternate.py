import wolframalpha
import wikipedia
def alternate():
	try:
	    app_id = "R2LUUJ-QTHXHRHLHK"
	    client = wolframalpha.Client(app_id)
	    r = client.query(my_input)
	    answer = next(r.results).text
	    talk=""+answer+""
	except:
	    my_input = my_input.split(' ')
	    my_input = " ".join(my_input[2:])
	    answer=wikipedia.summary(my_input,sentences=2)
	    talk=""+answer+""
	return talk