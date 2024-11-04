from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'  

@app.before_request
def inicializar_sesion():
    if 'inscritos' not in session:
        session['inscritos'] = []

@app.route('/')
def base():
    return redirect(url_for('registro'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')  
        seminarios_str = ', '.join(seminarios) 

    
        inscritos = session['inscritos']
        nuevo_inscrito = {
            'fecha': fecha,
            'nombre': nombre,
            'apellido': apellido,
            'turno': turno,
            'seminarios': seminarios_str
        }
        inscritos.append(nuevo_inscrito)
        session['inscritos'] = inscritos 
        return redirect(url_for('listado'))

    return render_template('registro.html')

@app.route('/listado')
def listado():
    inscritos = session.get('inscritos', [])
    return render_template('listado.html', inscritos=inscritos)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    inscritos = session.get('inscritos', [])
    if 0 <= id < len(inscritos):
        inscritos.pop(id)
        session['inscritos'] = inscritos
    return redirect(url_for('listado'))

if __name__ == '__main__':
    app.run(debug=True)