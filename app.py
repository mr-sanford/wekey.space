from doctest import debug
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, desc, and_, or_
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wekey.db'
db = SQLAlchemy(app)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_sort = db.Column(db.String(50), nullable=True)
    part = db.Column(db.String(100), nullable=True)
    cat = db.Column(db.String(100), nullable=True)
    subcat = db.Column(db.String(100), nullable=True)
    header = db.Column(db.String(200), nullable=True)
    card = db.Column(db.Text, nullable=True)
    article = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Record %r>' % self.id

@app.context_processor
def base_data():
    sig_name = db.session.query(Record.cat).filter_by(part='sig').order_by(Record.cat).distinct()
    today_year = datetime.now().year
    return dict(sig_name = sig_name, today_year = today_year)
@app.route('/')
def index():
    new_article = db.session.query(Record).filter(or_(Record.part=='sig', Record.part=='notes')).order_by(desc(Record.id)).limit(6).distinct()
    return render_template('index.html', new_article=new_article)
@app.route('/sig')
def sig():
    sig_name = db.session.query(Record.cat).filter_by(part='sig').order_by(Record.cat).distinct() # Получаем список
    # уникальных брендов сигнализаций
    return render_template('sig.html', sig_name=sig_name)

@app.route('/sig/<string:name>')
def SigModel(name):  # put application's code here
    sig_models = db.session.query(Record).filter_by(cat=name, part='sig').order_by(Record.type_sort, Record.subcat)
    return render_template('sig_models.html', sig_models=sig_models)

@app.route('/sig/<string:name>/<string:model>')
def sig_model(name, model):  # put application's code here
    sig_article = db.session.query(Record).filter_by(cat=name, subcat=model, part='sig')
    return render_template('sig_article.html', sig_article=sig_article)

@app.route('/OldCarMulti')
@app.route('/oldcarmulti')
def OldCarMulti():  # put application's code here
    oldcarmulti_models = db.session.query(Record).filter_by(part="OldCarMulti").order_by(Record.type_sort)
    oldcarmulti_models_uniq = db.session.query(Record.cat).filter_by(part="OldCarMulti").order_by(Record.cat).distinct()
    return render_template('oldcarmulti.html', oldcarmulti_models=oldcarmulti_models, oldcarmulti_models_uniq=oldcarmulti_models_uniq)

@app.route('/OldCarMulti/<string:name>/<string:model>')
@app.route('/oldcarmulti/<string:name>/<string:model>')
def OldCarMulti_model(name, model):  # put application's code here
    oldcarmulti_article = db.session.query(Record).filter_by(cat=name, subcat=model, part='OldCarMulti')
    return render_template('oldcarmulti_article.html', oldcarmulti_article=oldcarmulti_article)

@app.route('/ucar')
def ucar():  # put application's code here
    ucar_article = db.session.query(Record).filter_by(cat='ucar', subcat='v2', part='ucar')
    return render_template('ucar.html', ucar_article=ucar_article)

@app.route('/notes')
def notes():  # put application's code here
    notes_article = db.session.query(Record).filter_by(part="notes").order_by(Record.type_sort)
    return render_template('notes.html', notes_article=notes_article)

@app.route('/notes/<string:cat>/<string:subcat>')
def notes_noteview(cat, subcat):  # put application's code here
    notes_articleview = db.session.query(Record).filter_by(cat=cat, subcat=subcat, part='notes')
    return render_template('notes_article.html', notes_articleview=notes_articleview)

@app.route('/carkey')
def carkey():
    return render_template('carkey.html')
@app.route('/gateway')
def gateway():
    return render_template('gateway.html')

# if __name__ == '__main__':
#     app.run(debug=True)
#f