import unittest

outerTitle = 'Bar'


class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.title = 'foo'
        self.title2 = 'Foo'

        global outerTitle
        outerTitle = 'bar'
        print("[setUp] - {}".format(outerTitle))

    def tearDown(self) -> None:
        global outerTitle
        outerTitle = 'Bar'
        print("[tearDown] - {}".format(outerTitle))

    def test_upper(self) -> None:
        print("[test_upper]")
        self.assertEqual(self.title.upper(), 'FOO')
        self.assertFalse(self.title2 == self.title)
        self.assertTrue(outerTitle == 'bar')

    def test_split(self) -> None:
        print("[test_split]")
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

        # check that s.split fails when the sep is not a string
        with self.assertRaises(TypeError):
            s.split(2)


def suiteCase():
    suite = unittest.TestSuite()
    suite.addTest(TestStringMethods('test_split'))
    return suite


if __name__ == '__main__':
    # runner = unittest.TextTestRunner()
    # runner.run(suiteCase())
    unittest.main()
    