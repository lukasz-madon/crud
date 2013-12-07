import os
from server import app, db


if not os.path.exists("db.sqlite"):
    db.create_all()

app.run(debug=True)