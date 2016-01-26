import subprocess

from flask.ext.script import Manager

from geophoto import app
from geophoto import models

manager = Manager(app)

@manager.command
def load():
    subp = subprocess.Popen('mogrify -path geocoded -auto-orient ./geocoded_in/*.jpg', shell=True)
    models.process_photos()
    subp.wait()

@manager.command
def run():
    app.secret_key = 'super secret key'
    app.run(
        host='0.0.0.0',
        port=8008,
        debug=True
    )


if __name__ == "__main__":
    manager.run()
