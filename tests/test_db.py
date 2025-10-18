import unittest

from src.db.con_singleton import setup_db_con, DBConnSingleton
from src.db import Base
from src.models import Document, TagDocType, TagInfo

class TestDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        TEST_DB_PATH = ':memory:'
        setup_db_con(TEST_DB_PATH, Base)
        DBConnSingleton()

    def reset_db(self) -> None:
        conn = DBConnSingleton().get_connection()
        Base.metadata.drop_all(bind=conn)
        Base.metadata.create_all(bind=conn)
        conn.close()

    def setUp(self):
        self.DOCNAME = 'test_doc'
        self.DOCPATH = 'test/path'
        self.TYPENAME = 'Test Type'
        self.DOCNAME = 'test.pdf'
        self.INFONAME = 'test_info'

        self.reset_db()
        self.session = DBConnSingleton().get_session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_create_doc_and_tag(self) -> None:
        doctype = TagDocType(name = self.TYPENAME)
        doc = Document(filename = self.DOCNAME, rel_path = 'rel/path',
                       doc_type = doctype)
        self.session.add(doc)
        self.session.commit()

        db_doc = (self.session.query(Document)
                              .where(Document.filename == self.DOCNAME)
                              .one())
        self.assertEqual(db_doc.filename, self.DOCNAME, 'Doc name not matching.')
        self.assertEqual(db_doc.doc_type.name, self.TYPENAME, 'Type name not matching')

    def test_doc_info_interaction(self) -> None:
        self.session.add(TagInfo(name = self.INFONAME))
        self.session.add(Document(filename = self.DOCNAME,
                                  rel_path = self.DOCPATH,
                                  doc_type = TagDocType(name = self.TYPENAME)))
        self.session.commit()

        doc = (self.session.query(Document)
                   .where(Document.rel_path == self.DOCPATH)
                   .where(Document.filename == self.DOCNAME).one())
        tag_info = (self.session.query(TagInfo)
                    .where(TagInfo.name == self.INFONAME)
                    .one())
        doc.add_info_tag(tag_info)
        self.assertListEqual(doc.info_tags, [tag_info])
        doc.rmv_info_tag(tag_info)
        self.assertListEqual(doc.info_tags, [])

if __name__ == '__main__':
    unittest.main()