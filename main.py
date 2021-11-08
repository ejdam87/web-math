from flask import Flask, send_file, request, send_from_directory,render_template
from linear_back.determinant import Determinant
from io import BytesIO
import graph_back.my_plot_lib as my_plot_lib
import relations_back.out as o
from PIL import Image
from typing import Tuple, Callable
import helper


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.static_folder = r'public\static'




@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  """
  HTTP response for other actions
  """
  
  if (len(path) == 0):

    return send_from_directory('public', 'main_page.html')

  return send_from_directory('public', path)


@app.route('/info', methods=['post', "get"])
def info():

  return send_from_directory('public', 'info.html')


@app.route('/linear', methods=['post', "get"])
def linear():

  return send_from_directory('public', 'linear_system.html')


@app.route('/graph', methods=['post', "get"])
def graph():

  return send_from_directory('public', 'graph_visualization.html')


@app.route('/relations', methods=['post', "get"])
def relations():

  return send_from_directory('public', 'relations.html')


@app.route('/get_graph', methods=["post"])
def get_graph():

	"""
	Response for get_graph action
	Return picture with wanted plot
	"""

	canvas = Image.new('RGB', (400, 400), (0,0,0))
	my_plot_lib.create_cartesian(canvas)
	selected = request.form.get("selected")
	color = request.form.get("color")

	r, g, b = helper.hexColor(color)

	if selected == "linear":
		my_plot_lib.draw_plot(canvas, my_plot_lib.linear, (r, g, b))
	elif selected == "quadratic":
		my_plot_lib.draw_plot(canvas, my_plot_lib.quadratic, (r, g, b))
	elif selected == "cubic":
		my_plot_lib.draw_plot(canvas, my_plot_lib.cubic, (r, g, b))

	return helper.serve_pil_image(canvas)


@app.route('/solve_relation', methods=["get", 'post'])
def solve_relation():

	base = request.form.get('base')
	relation = request.form.get('relation')
	closures = request.form.get('closures')

	closures = closures.split(",")

	res = o.get_all(base, relation, closures)
	return res


@app.route('/solve', methods=['post'])
def solve() -> str:
	"""
	Returns HTTP response for solve action (result of system)
	"""

	# Getting coefs from formular
	x1 = float(request.form.get('x1'))
	y1 = float(request.form.get('y1'))
	z1 = float(request.form.get('z1'))
	r1 = float(request.form.get('r1'))

	x2 = float(request.form.get('x2'))
	y2 = float(request.form.get('y2'))
	z2 = float(request.form.get('z2'))
	r2 = float(request.form.get('r2'))

	x3 = float(request.form.get('x3'))
	y3 = float(request.form.get('y3'))
	z3 = float(request.form.get('z3'))
	r3 = float(request.form.get('r3'))

	# Creating determinants
	D = [
	[x1, y1, z1],
	[x2, y2, z2],
	[x3, y3, z3]
	  ]

	Dx = [
	[r1, y1, z1],
	[r2, y2, z2],
	[r3, y3, z3]
	  ]

	Dy = [
	[x1, r1, z1],
	[x2, r2, z2],
	[x3, r3, z3]
	  ]

	Dz = [
	[x1, y1, r1],
	[x2, y2, r2],
	[x3, y3, r3]
	  ]


	# Counting determinants with usage of Crammer's rule
	D_d = Determinant(D)
	D_x = Determinant(Dx)
	D_y = Determinant(Dy)
	D_z = Determinant(Dz)


	x = D_x.get_value() / D_d.get_value()
	y = D_y.get_value() / D_d.get_value()
	z = D_z.get_value() / D_d.get_value()


	if abs(x) == 0:   # Weird glitch (its possible to get -0)
		x = abs(x)
	if abs(y) == 0:
		y = abs(y)
	if abs(z) == 0:
		z = abs(z)

	return f"{x} {y} {z}"

app.run()
