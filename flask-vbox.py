#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# Librerias requeridas para correr aplicaciones basadas en Flask
# Applicacion con flask y VBoxManage , gestion de VMS}
# Estudiantes: Santiago Juri y Daniel Hernandez.
# Asignatura: Sistemas Operativos
# Pontificia Universidad Javeriana
from flask import Flask, jsonify,abort, make_response, request
import subprocess

app = Flask(__name__)

tasks = [
 {
  'id': 0,
  'nombreVM': None,
  'memoriaRAM': None,
  'numberCPU': None
 }
 ]

# Web service que se invoca al momento de ejecutar el comando
# curl http://localhost:5000

@app.route('/',methods = ['GET'])
def index():
	return "Hola Javeriana"

# Este metodo retorna la lista de sistemas operativos soportados 
# por VirtualBox Los tipos de sistemas operativos soportados deben 
# ser mostrados al ejecutar  el comando
# curl http://localhost:5000/vms/ostypes	
# Este es el codigo del itemsem 1
#VBoxManage ​ #list ostypes
@app.route('/vms/ostypes',methods = ['GET'])
def ostypes():
	output= subprocess.check_output(['VBoxManage','list','ostypes'])
	#output = "Work to be done\n"
	return output

# Este metodo retorna la lista de maquinas asociadas 
# con un usuario al ejecutar el comando
# curl http://localhost:5000/vms
# Este es el codigo del item 2a
@app.route('/vms',methods = ['GET'])
def listvms():
	output = subprocess.check_output(['VBoxManage','list','vms'])
	return output

# Este metodo retorna aquellas maquinas que se encuentran en ejecucion al 
# ejecutar el comando
# curl http://localhost:5000/vms/running
# Este es el codigo del item 2b
@app.route('/vms/running',methods = ['GET'])
def runninglistvms():
	output = subprocess.check_output(['VBoxManage','list','runningvms'])
	# Tu codigo aqui
	return output

# Este metodo retorna las caracteristica de una maquina virtual cuyo nombre es
# vmname 3.z
@app.route('/vms/info/<vmname>', methods = ['GET'])
def vminfo(vmname):
	output = subprocess.check_output(['VBoxManage','showvminfo','vmname 3'])
	return output

# Usted deberá realizar además los items 4 y 5 del enunciado del proyecto 
# considerando que:
# El item 4 deberá usar el método POST del protocolo HTTP
# Metodo de ejecucion
#curl -i -H "Content-Type: application/json" -X POST -d '{"nombreVM":"NombreAqui","memoriaRAM": 0, "numberCPU": 0}' http://localhost:5000/vms/info/newvm/
@app.route('/vms/info/newvm/', methods = ['POST'])
def newvm():
	if not request.json or not 'nombreVM' in request.json:
		abort(400)
 	task = {
 		'id': tasks[-1]['id'] + 1,
  		'nombreVM': request.json['nombreVM'],
  		'memoriaRAM': request.json['memoriaRAM'],
  		'numberCPU': request.json['numberCPU']
 }

 	VMName=str(task['nombreVM'])
 	VMRAM=str(task['memoriaRAM'])
 	numberCPU=str(task['numberCPU'])
 	accesPermission=subprocess.Popen(['chmod','a+x','creacionvm.sh'])
 	creacionvm=subprocess.Popen(['./creacionvm.sh',VMName, numberCPU,VMRAM])
 	tasks.append(task)
 	return jsonify({'task': task}),201

# - El item 5 deberá usar el método DELETE del protocolo HTTP
# Metodo de ejecucion:
# curl -i -X DELETE http://localhost:5000/vms/vmname
@app.route('/vms/<string:vm_name>', methods = ['DELETE'])
def delete_VM(vm_name):
	task = [task for task in tasks if task['nombreVM'] == str(vm_name) ]
	if len(task) == 0 or vm_name==None:
		abort(404)
	deleteVM=subprocess.Popen(['VBoxManage','unregistervm','--delete', str(vm_name)])
	tasks.remove(task[0])
	return jsonify({'result': True })

################################################################
#MainAplication
if __name__ == '__main__':
        app.run(debug = True, host='0.0.0.0')
