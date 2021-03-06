from flask import Flask, request, send_from_directory, render_template, jsonify
from linear_back.determinant import Determinant
import graph_back.func_vis as func_vis
import relations_back.out as o
import matrix_back.matrix_mul as matrix_mul
from PIL import Image
from typing import Tuple, Callable
import helper


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.static_folder = r'public\static'


#---------------------Page-getters-------------------------------------------#

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path: str) -> str:
    """
    HTTP response for other actions
    """

    if (len(path) == 0):

        return send_from_directory('public', 'main_page.html')

    return send_from_directory('public', path)


@app.route('/info', methods=['post', "get"])
def info() -> str:

    return send_from_directory('public', 'info.html')


@app.route('/eq_solving', methods=['post', "get"])
def eq_solving() -> str:

    return send_from_directory('public', 'equation_solving.html')


@app.route('/matrix', methods=['post', "get"])
def matrix() -> str:

    return send_from_directory('public', 'matrix.html')


@app.route('/equations', methods=['post', "get"])
def equations() -> str:

    return send_from_directory('public', 'equations.html')


@app.route('/linear', methods=['post', "get"])
def linear() -> str:

    return send_from_directory('public', 'linear_system.html')


@app.route('/graph', methods=['post', "get"])
def graph() -> str:

    return send_from_directory('public', 'graph_visualization.html')


@app.route('/relations', methods=['post', "get"])
def relations() -> str:

    return send_from_directory('public', 'relations.html')

#---------------------Page-getters-------------------------------------------#





#---------------------App-functions------------------------------------------#

@app.route('/get_graph', methods=["post"])
def get_graph():

    formula = request.form.get('formula')
    color = request.form.get('color')

    plot = func_vis.get_figure(formula, color)

    return helper.serve_img(plot)


@app.route('/get_matrices', methods=["get", "post"])
def get_matrices() -> str:

    m1, m2 = matrix_mul.create_random_multiply_duo(3, (-6, 6))

    m1s = matrix_mul.stringify_matrix(m1)
    m2s = matrix_mul.stringify_matrix(m2)

    for i in range(len(m1s)):
        m1s[i] = m1s[i].replace(" ", "&nbsp;")
    for i in range(len(m2s)):
        m2s[i] = m2s[i].replace(" ", "&nbsp;")
    # Convert spaces to space equivalent in HTML

    return jsonify(m1="<br>".join(m1s), m2="<br>".join(m2s))


@app.route('/solve_matrix_mul', methods=["post"])
def solve_matrix_mul():

    return "Server response"


@app.route('/solve_relation', methods=["get", 'post'])
def solve_relation() -> str:

    base = request.form.get('base')
    relation = request.form.get('relation')
    closures = request.form.get('closures')

    closures = closures.split(",")

    res = o.get_all(base, relation, closures)
    return res


@app.route('/solve', methods=['post'])
def solve() -> str:

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

#---------------------App-functions------------------------------------------#


app.run()
