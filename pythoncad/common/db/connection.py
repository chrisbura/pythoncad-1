from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Connection(object):
    """
    Connection objects are used to maintain sessions related to
    document instances or application settings instances.

    """
    def __init__(self, db_path):
        self.db_path = db_path

        # TODO: Verify path
        # TODO: Move echo setting to debug settings of some sort
        # TODO: Capture echo in a log file
        self.engine = create_engine('sqlite:///{0}'.format(self.db_path), echo=False)
        Session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        self.session = Session()
        # TODO: Check if it will add new tables when a file is opened, warn about changes if so

    def cursor(self):
        return self.session

    def __del__(self):
        self.session.close()
