from sqlalchemy.orm import sessionmaker

from webapp.forms import LoginForm, TaskForm
from webapp.model import db, User, Tasks
import os
import logging


#result = db.engine.execute("SELECT id FROM User")
#names = [row[0] for row in result]
#print(names)


