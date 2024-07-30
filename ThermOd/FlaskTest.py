from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)


class People:

    def name(self, a):
       return a + "perros"


@app.route('/pet/<pompis>')
def hello_pompis(pompis):
   return render_template('index.html', name = pompis)

@app.route('/user/<user>')
def hello_name(user):
   pep = People()
   if user == "daniel":
      return redirect(url_for('hello_pompis', pompis = 'Michoacano_Gonito'))
   else:
      return render_template('index.html', name = pep.name(user + " "))


if __name__ == '__main__':
   app.run(debug = True)





