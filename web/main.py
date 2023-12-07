from flask import Flask, render_template, request
from config import COMPILE_DIR, TOOL_CHAIN_PATH, DIST_DIR, COMPILE_SCRIPT, PORT
from subprocess import run, TimeoutExpired, CalledProcessError
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            file = request.files['srcfile']
            file.save(f'{COMPILE_DIR}/src.c')
            run([COMPILE_SCRIPT, TOOL_CHAIN_PATH, 'src.c', DIST_DIR],
                cwd=COMPILE_DIR, timeout=10, check=True)
            data = open(f'{DIST_DIR}/test.data', 'r', encoding='utf-8').read()
            dump = open(f'{DIST_DIR}/test.dump', 'r', encoding='utf-8').read()
            return render_template('index.html', data=data, dump=dump)
        except TimeoutExpired as tle:
            return 'TLE'
        except CalledProcessError as ce:
            return 'CE'
        except BaseException as e:
            return str(e)


if __name__ == '__main__':
    app.run(port=PORT, debug=True)
