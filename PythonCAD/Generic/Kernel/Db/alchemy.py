from tempfile import NamedTemporaryFile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Connection(object):
    """
    Connection objects are used to maintain sessions related to
    document instances or application settings instances.

    """
    def __init__(self, db_schema, db_path=None):
        self.db_path = db_path

        # If document path is not supplied, create a new file in user's temp directory
        if self.db_path is None:
            temporary_file = NamedTemporaryFile(prefix='pycad_', suffix='.alq')
            self.db_path = temporary_file.name
            temporary_file.close()

        # TODO: Move echo setting to debug settings of some sort
        # TODO: Capture echo in a log file
        engine = create_engine('sqlite:///{0}'.format(self.db_path), echo=False)
        Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        self.session = Session()
        # TODO: Check if it will add new tables when a file is opened, warn about changes if so
        db_schema.metadata.create_all(bind=engine, checkfirst=True)

    def __del__(self):
        self.session.close()
