import unittest

from src.db.con_singleton import setup_db_con, DBConnSingleton
from src.db import Base
from src.models.tags import TagDocType, TagInfo
from src.models.document import Document

class TestDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        TEST_DB_PATH = ':memory:'
        setup_db_con(TEST_DB_PATH, Base)
        DBConnSingleton()

    def setUp(self):
        self.session = DBConnSingleton().get_session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_create_doc_and_tag(self) -> None:
        DOCNAME = 'test.pdf'
        TYPENAME = 'Test Type'
        doctype = TagDocType(name = TYPENAME)
        doc = Document(filename = DOCNAME, rel_path = 'rel/path',
                       doc_type = doctype)
        self.session.add(doc)
        self.session.commit()

        db_doc = (self.session.query(Document)
                              .where(Document.filename == DOCNAME)
                              .one())
        self.assertEqual(db_doc.filename, DOCNAME, 'Doc name not matching.')
        self.assertEqual(db_doc.doc_type.name, TYPENAME, 'Type name not matching')

if __name__ == '__main__':
    unittest.main()