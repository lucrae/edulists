from flask.cli import FlaskGroup
from edulists import create_app, cli, db
from edulists.models import User, Subject, Subscription

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {
        'app': app,
        'db': db,
        'User': User,
        'Subject': Subject,
        'Subscription': Subscription,
    }

if __name__=='__main__':
    app.run()