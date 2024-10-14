from flask import Flask, render_template, request, jsonify
from subprocess import run, TimeoutExpired, CalledProcessError
from werkzeug.exceptions import RequestEntityTooLarge
from config import *
import const
from compile import compile as my_compile

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", const=const, rooturi = ROOT_URI)


@app.route("/submit", methods=["POST"])
def on_post():
    try:
        file = request.files["srcfile"]
        march = request.form["march"]
        target = request.form["target"]
        if file.filename.split(".")[-1] not in const.ACCEPTED_FILE_TYPES:
            return jsonify({"error": "文件类型错误"}), 400
        if march not in const.ACCEPTED_MARCH:
            return jsonify({"error": "march 参数错误"}), 400
        if target not in ["fpga", "sim"]:
            return jsonify({"error": "target 参数错误"}), 400
        files = my_compile(file, march, target)
        files = [f.replace(DIST_DIR, DIST_URI) for f in files]
        files = [{"filename": f.split("/")[-1], "uri": f} for f in files]
        return render_template("result.html", files=files, rooturi=ROOT_URI)
    except Exception as e:
        error = str(e)
        return render_template("result.html", error=error, rooturi=ROOT_URI)


app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 16 MB


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return (
        jsonify(
            {
                "error": "文件过大",
                "message": f"上传的文件大小不能超过 {app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024)} MB.",
            }
        ),
        413,
    )


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
