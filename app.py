from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import subprocess
import os
import os.path

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///problemset.db'
db = SQLAlchemy(app)

class Problem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(8), nullable=False)
  origin = db.Column(db.String(256))
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return f"Problem('{self.id}', '{self.name}', '{self.origin}', '{self.date_created}')"


@app.route('/', methods=['POST', 'GET'])
def index():
  problems = Problem.query.order_by(Problem.date_created).all()
  return render_template('index.html', tasks=problems)

@app.route('/<name>/delete')
def delete(name):
  current_id = int(name[1:])
  task_to_delete = Problem.query.get_or_404(current_id)
  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return 'There was an issue deleting your task.'

@app.route('/<name>')
def view(name):
  current_id = int(name[1:])
  task_to_preview = Problem.query.get_or_404(current_id)
  return render_template('preview.html', task=task_to_preview)

@app.route('/<name>/edit', methods=['POST', 'GET'])
def edit(name):
  current_id = int(name[1:])
  task_to_update = Problem.query.get_or_404(current_id)

  tex_path = 'static/problemset/' + name + '/' + name + '.tex'
  tex_sol_path = 'static/problemset/' + name + '/' + name + '-solution.tex'
  if request.method == 'POST':

    with open(tex_path, 'w') as f:
      f.write(request.form['ace-editor'])
    with open(tex_sol_path, 'w') as g:
      g.write(request.form['sol-ace-editor'])
    
    subprocess.run(['./compile.sh', name])
    
    current_origin = request.form['origin']
    task_to_update.origin = current_origin
    db.session.commit()
    return redirect('/')
  
  else:
    with open(tex_path, 'r') as f:
      tex_file = f.read()
    with open(tex_sol_path, 'r') as g:
      tex_sol_file = g.read()
    return render_template('edit.html', task=task_to_update, tex_file=tex_file, tex_sol_file=tex_sol_file)


@app.route('/add', methods=['POST', 'GET'])
def add():
  previous = Problem.query.order_by(Problem.id.desc()).first()
  
  current_id = previous.id + 1
  # current_id = 1 ## you nust use it when you dont have aby problems in db
  current_name = 'P' + str(current_id).zfill(3)
  
  if request.method == 'POST':
    os.mkdir('static/problemset/'+current_name)
    problem_path = 'static/problemset/'+current_name+'/'+current_name+'.tex'
    with open(problem_path, 'w') as f:
      f.write(request.form['ace-editor'])

    solution_path = 'static/problemset/'+current_name+'/'+current_name+'-solution.tex'
    with open(solution_path, 'w') as g:
      g.write(request.form['sol-ace-editor'])

    current_origin = request.form['origin']
    new_task = Problem(id=current_id,name=current_name,origin=current_origin)
    subprocess.run(['./compile.sh', current_name])

    db.session.add(new_task)
    db.session.commit()
    return redirect('/')
  else:
    with open('static/tex/template.tex', 'r') as f:
      tex_template = f.read()
    return render_template('add.html', tex_template=tex_template, current_name=current_name)


if __name__ == '__main__':
  app.run(debug=True)
