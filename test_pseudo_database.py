import unittest

from pseudo_database import PseudoDatabase


class TestPseudoDatabase(unittest.TestCase):

    def test_empty_db(self):
        # empty db raises unknown category for operations that need a category
        # db remains unlocked for delete on unknown category
        # read all returns empty db
        pseudo_database = PseudoDatabase()
        self.assertRaises(PseudoDatabase.UnknownCategory, pseudo_database.read, "red", "2")
        self.assertRaises(PseudoDatabase.UnknownCategory, pseudo_database.read_category, "blue")
        self.assertRaises(PseudoDatabase.UnknownCategory, pseudo_database.delete, "green", "4")
        self.assertFalse(pseudo_database.locked)
        contents = pseudo_database.read_all()
        self.assertDictEqual(contents, {})

    def test_single_item_db(self):
        # still raises unknown category for operations on uncreated categories
        # db remains unlocked for delete on unknown category
        # item can be read, single item list returned on category read
        # read all returns single entry
        pseudo_database = PseudoDatabase()
        item = PseudoDatabase.Item(label="14")
        pseudo_database.create(category="yellow", item=item)
        self.assertRaises(PseudoDatabase.UnknownCategory, pseudo_database.read, "red", "2")
        self.assertRaises(PseudoDatabase.UnknownCategory, pseudo_database.read_category, "blue")
        self.assertRaises(PseudoDatabase.UnknownCategory, pseudo_database.delete, "green", "4")
        self.assertFalse(pseudo_database.locked)
        read_item = pseudo_database.read(category="yellow", label="14")
        self.assertEqual(item, read_item)
        category_list = pseudo_database.read_category(category="yellow")
        item_list = [item]
        self.assertListEqual(category_list, item_list)
        category_dict = {"yellow": item_list}
        contents = pseudo_database.read_all()
        self.assertDictEqual(contents, category_dict)
        pseudo_database.reset("admin")  # clear db for any future test

    def test_multi_category_and_item_db(self):
        # still raises unknown category for operations on uncreated categories
        # item can be added to created category
        # item can be added to a new category
        # items and categories can be read
        # items can be deleted
        # read all returns expected value after manipulations
        pseudo_database = PseudoDatabase()
        item14 = PseudoDatabase.Item(label="14")
        pseudo_database.create(category="yellow", item=item14)
        item21 = PseudoDatabase.Item(label="21")
        pseudo_database.add(category="yellow", item=item21)
        item7 = PseudoDatabase.Item(label="7")
        pseudo_database.add(category="red", item=item7)
        item4 = PseudoDatabase.Item(label="4")
        pseudo_database.add(category="red", item=item4)
        # category okay but item does not exist
        self.assertRaises(PseudoDatabase.ItemNotFound, pseudo_database.read, "red", "2")
        self.assertRaises(PseudoDatabase.UnknownCategory, pseudo_database.read_category, "blue")
        self.assertRaises(PseudoDatabase.UnknownCategory, pseudo_database.delete, "green", "4")
        self.assertFalse(pseudo_database.locked)
        read_item = pseudo_database.read(category="yellow", label="21")
        self.assertEqual(item21, read_item)
        pseudo_database.delete(category="yellow", label="21")
        category_list = pseudo_database.read_category(category="yellow")
        item_list = [item14]
        self.assertListEqual(category_list, item_list)
        red_category_list = pseudo_database.read_category(category="red")
        red_item_list = [item7, item4]  # order important, haven't used sorted lists
        self.assertListEqual(red_category_list, red_item_list)
        pseudo_database.delete(category="red", label="7")
        red_item_list.remove(item7)
        red_category_list = pseudo_database.read_category(category="red")
        self.assertListEqual(red_category_list, red_item_list)
        pseudo_database.delete(category="red", label="4")
        # after last element in category is deleted, category is deleted
        self.assertRaises(PseudoDatabase.UnknownCategory, pseudo_database.read_category, "red")
        # and all that's left is single item
        category_dict = {"yellow": item_list}
        contents = pseudo_database.read_all()
        self.assertDictEqual(contents, category_dict)
        pseudo_database.reset("admin")  # clear db for any future test


if __name__ == '__main__':
    unittest.main()
