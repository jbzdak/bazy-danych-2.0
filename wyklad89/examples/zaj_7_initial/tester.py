import os
import subprocess
from tempfile import gettempdir
import uuid

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

import unittest

def load_script(script_file_name, database_name, change_owner_to=None):
    del_script_file = False
    try:
        if isinstance(script_file_name, StringIO):
            file = os.path.join(gettempdir(), str(uuid.uuid4()))
            del_script_file = True
            with open(file, 'w') as f:
                script_file_name.seek(0)
                f.write(script_file_name.read())
            script_file_name = file
        call = ['psql', '-f', script_file_name,
                 database_name]
        subprocess.check_call(call)
    except Exception:
        try:
            if del_script_file:
                os.remove(script_file_name)
        except Exception:
            pass
        raise

class SchemaUnittest(object):

    SCHEMA_FILE = "model_schema.sql"

    DATABASE = "bd"

    def setUp(self):
        load_script(StringIO("DROP SCHEMA public CASCADE;"), self.DATABASE)
        load_script(StringIO("CREATE SCHEMA public;"), self.DATABASE)
        load_script(self.SCHEMA_FILE, self.DATABASE)



    def tearDown(self):
        load_script(StringIO("DROP SCHEMA public CASCADE;"), self.DATABASE)
        load_script(StringIO("CREATE SCHEMA public;"), self.DATABASE)





