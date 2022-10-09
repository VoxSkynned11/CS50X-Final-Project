import os
from cs50 import SQL
from flask import Flask, render_template, redirect, request, session, url_for, flash, send_from_directory
from helpers import login_required
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

"""Gets a list of all images file names"""


db = SQL("sqlite:///images.db")

all_images = os.listdir('static/img')

select = 1
img = db.execute("SELECT * FROM images WHERE selected = ?", select)

app = Flask(__name__)

"""https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/"""
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


"""-------------------------------------------------------------"""


app.config["SECRET_KEY"]  = 'BAD_SECRET_KEY' #cookie stuff ._.

# Secret String
"""
if not os.environ.get("SS"):
    raise RuntimeError("SS not set")
"""

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
    img = db.execute("SELECT * FROM images WHERE selected = ?", select)
    return render_template("index.html", img=img)

@app.route("/projects")
def projects():
    all_images = db.execute("SELECT * FROM images")
    return render_template("projects.html", img=all_images)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/layout")
def layout():
    return render_template("index.html", img=img)


""" i don't really care about user friendness in a secret page """
@app.route("/secret", methods=["GET", "POST"])
def secret():
    session.clear()

    if request.method == "POST":
        if not request.form.get("adname") or not request.form.get("passwd") or not os.environ.get("SS"):
            return render_template("index.html", img=img)
        name = request.form.get("adname")
        passwd = request.form.get("passwd")
        ss = request.form.get("ss")

        # borrowed from cs50 pset9 ._.
        adm = db.execute("SELECT * FROM admin WHERE name = ?", name)

        if len(adm) != 1 or not check_password_hash(adm[0]["password"], request.form.get("passwd")):
            return render_template("index.html", img=img)

        if ss != os.environ.get("SS"):
            return render_template("index.html", img=img)

        session["user_id"] = adm[0]["id"]
        return redirect("/")

    else:
        return render_template("secret.html")
    """
        # temporary code to make an admin

    if request.method == "POST":
        name = request.form.get("adname")
        passwd = request.form.get("passwd")


            # generates hash for password to store in database
        passwd = generate_password_hash(passwd, method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO admin (name, password) VALUES (?, ?)", name, passwd)
        return render_template("index.html", img=img)
    """

@app.route("/admin", methods=["GET","POST"])
@login_required
def admin():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template("admin.html", img=img)

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template("admin.html", img=img)

        if not request.form.get("title") or not request.form.get("desc"):
            return render_template("admin.html", img=img)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            db.execute("INSERT INTO images (name) VALUES (?)", filename)
            img_id =  db.execute("SELECT id FROm images WHERE name = ? ORDER BY id DESC", filename)
            filename = f"{img_id[0]['id']}{filename}"

            db.execute("UPDATE images SET name = ? WHERE id = ?", filename, img_id[0]["id"])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            # OBS: since it`s possible to upload files with same filename, it searchs for the latest record

            title = request.form.get("title")
            desc = request.form.get("desc")

            if title:
                db.execute("UPDATE images SET title = ? WHERE id = ?", title, img_id[0]["id"])
            if desc:
                db.execute("UPDATE images SET desc = ? WHERE id = ?", desc, img_id[0]["id"])

            img = db.execute("SELECT * FROM images")
            return render_template("admin.html", img=img)

    else:
        img = db.execute("SELECT * FROM images")
        return render_template("admin.html", img=img)

@app.route("/delete", methods=["GET","POST"])
@login_required
def delete():
    if request.method == "POST":
        img_id = request.form.get("id")
        name = request.form.get("name")
        db.execute("DELETE FROM images WHERE id = ?", img_id)
        file_path = f"static/img/{name}"
        if os.path.isfile(file_path):
            os.remove(file_path)

        img = db.execute("SELECT * FROM images WHERE selected = ?", select)
        return redirect("/admin")
    else:
        return redirect("/")

@app.route("/update", methods=["GET","POST"])
@login_required
def update():
    if request.method == "POST":
        img_id = request.form.get("id")
        name = request.form.get("name")
        if request.form.get("title"):
            title = request.form.get("title")
        if request.form.get("desc"):
            desc = request.form.get("desc")
        if request.form.get("show").upper() in ["YES","Y"]:
            show = 1
        else:
            show = 0

        db.execute("UPDATE images SET title = ?, desc = ?, selected = ? WHERE id = ?", title, desc, show, img_id)


        return redirect("/")
    else:
        return redirect("/")









"""https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)