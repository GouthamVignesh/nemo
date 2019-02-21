
def database():
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://nemo-bot-9ae9c.firebaseio.com/A/')
    result = firebase.get('ABDOMINAL PAIN', None)
    x=""+str(result)+""
    return x
