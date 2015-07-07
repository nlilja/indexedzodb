from unittest.case import TestCase
import unittest

import ZODB

from indexedzodb.models import ZODBModel


zodb = ZODB.DB(None)
connection = zodb.open()


class Company(ZODBModel):
    name = None
    established = 0

    class Meta:
        table = "company"
        connection = connection
        index_fields = ('name', 'established',)


class LocalDataTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def tearDown(self):
        TestCase.tearDown(self)

    def test_basic_models(self):
        self.assertTrue(Company.count() == 0)

        Company(name="Brickmakers Inc", established=1989).save()
        Company(name="Timmy's Tea Mugs", established=1980).save()
        Company(name="Seaside Cafe", established=2005).save()
        Company(name="Bob's Dive Bar", established=2005).save()

        self.assertTrue(Company.select(sort_index='name')[0].name == "Bob's Dive Bar")

        self.assertTrue(Company.count() == 4)
        self.assertTrue(len(Company.select(established=2005)) == 2)
 
        # Check remove from index
        c = Company.get(name='Seaside Cafe')
        c.delete()
 
        self.assertTrue(Company.count(name='Seaside Cafe') == 0)
 
        Company(name="Seaside Cafe", established=2005).save()
 
        # Quotes
        c = Company.get(name="Timmy's Tea Mugs")
        self.assertTrue(c is not None)
 
        Company(name="Slash \\'n\\' Quotes").save()
        c = Company.get(name="Slash \\'n\\' Quotes")
        self.assertTrue(c is not None)



if __name__ == '__main__':
    unittest.main()
