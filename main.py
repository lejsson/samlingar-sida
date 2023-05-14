from app import app, db
from app.models import User, Post, PostContent
app.run(debug=False)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'PostContent': PostContent}

#app.run(host="0.0.0.0", port=2322)
