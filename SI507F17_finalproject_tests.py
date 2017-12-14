from Cache_Class import *
from Session_Class import *
from Classes_for_Data import *
from Database_Class import *
import unittest
import json

class Test_Cache(unittest.TestCase):

    def setUp(self):
        self.cached_data = Cache('test_data.json')
        self.cached_token = Cache('test_token.json')

    def test_constructor(self):
        self.assertEqual(self.cached_data.CACHE_FNAME, 'test_data.json')
        self.assertEqual(self.cached_token.CACHE_FNAME, 'test_token.json')
        self.assertTrue(isinstance(self.cached_data.CACHE_DICTION, dict))
        self.assertTrue(isinstance(self.cached_token.CACHE_DICTION, dict))

    def test_has_cache_expired(self):
        timestr = '2017-12-01 21:06:03.557269'
        self.assertEqual(self.cached_data.has_cache_expired(timestr), True)
        self.assertEqual(self.cached_data.has_cache_expired(timestr, 365), False)

    def test_set_in_cache(self):
        self.cached_data.set_in_cache('id1', 'test1', 100)
        self.cached_data.open_cache_file()
        self.assertTrue('ID1' in self.cached_data.CACHE_DICTION)
        self.assertTrue(self.cached_data.CACHE_DICTION['ID1']['values'] == 'test1')
        self.assertTrue(self.cached_data.CACHE_DICTION['ID1']['expire_in_days'] == 100)

    def test_get_from_cache(self):
        self.assertTrue(self.cached_data.get_from_cache('iddd') == None)        
        self.cached_data.set_in_cache('id_expire', 'test_expire', 0)
        self.cached_data.set_in_cache('id2', 'test2')
        self.cached_data.open_cache_file()
        self.assertTrue(self.cached_data.get_from_cache('id2') == 'test2')
        self.assertTrue(self.cached_data.get_from_cache('id_expire') == None)

    def tearDown(self):
        pass

class Test_Session(unittest.TestCase):

    global yelp_session
    yelp_session = Session()

    def setUp(self):
        self.test_session = yelp_session
        self.endpoint_url = 'https://api.yelp.com/v3/businesses/search'
        self.test_params1 = {
            'term' : 'starbucks',
            'location' : 'umich'
        }
        self.test_params2 = {
            'term' : 'cafe',
            'location' : 'ucla'
        }

    def test_create_request_identifier(self):
        test_ident = create_request_identifier(self.endpoint_url, self.test_params1)
        self.assertIsInstance(test_ident, str)
        self.assertTrue(test_ident.isupper())
        self.assertEqual(test_ident, 'HTTPS://API.YELP.COM/V3/BUSINESSES/SEARCH?LOCATION_UMICH_TERM_STARBUCKS')

    def test_make_requests(self):
        self.assertTrue(isinstance(make_requests(self.endpoint_url, self.test_params1), dict))
        yelp_session = False
        self.assertTrue(isinstance(make_requests(self.endpoint_url, self.test_params2), dict), 
            "if yelp_session is False, make_requests() can create a new session to get data")

    def tearDown(self):
        pass

class Test_Restaurant(unittest.TestCase):

    def setUp(self):
        self.restaurant_dict1 = {
            "id": "oleana-restaurant-cambridge",
            "name": "Oleana Restaurant",
            
            "categories": [
                {
                    "alias": "mediterranean",
                    "title": "Mediterranean"
                }
            ],
            "rating": 4.5,
            "transactions": ["restaurant_reservation"],
            "price": "$$$",
            "location": {
                "city": "Cambridge",
                "country": "US",
                "state": "MA",
                
            },
            "distance": 1190
        }

        self.restaurant_dict2 = {
            "id": "island-creek-oyster-bar-boston",
            "name": "Island Creek Oyster Bar",
            "categories": [
                {
                    "alias": "seafood",
                    "title": "Seafood"
                },
                {
                    "alias": "bars",
                    "title": "Bars"
                }
            ],
            "rating": 4.5,
            "transactions": ["pickup", "delivery"],
            "location": {
                "city": "Boston",
                "state": "MA",
            },
            "distance": 1266
        }
        

        self.test_re1 = Restaurant(self.restaurant_dict1, 3, 'mit')
        self.test_re2 = Restaurant(self.restaurant_dict2, 5, 'mit')

    def test_constructor(self):
        self.assertEqual(self.test_re1.yelp_id, "oleana-restaurant-cambridge")
        self.assertEqual(self.test_re1.name, "Oleana Restaurant")
        self.assertEqual(self.test_re1.school_id, 3)
        self.assertEqual(self.test_re1.price, "$$$")
        self.assertEqual(self.test_re2.price, None)
        self.assertEqual(self.test_re1.transactions, ["restaurant_reservation"])
        self.assertEqual(self.test_re1.distance, 1.19)

    def test_repr_str(self):
        test_repr_re = repr(self.test_re1)
        test_str_re = str(self.test_re1)
        self.assertEqual(test_repr_re, "oleana-restaurant-cambridge in 1.19km")
        self.assertEqual(test_str_re, "Oleana Restaurant")

    def test_contains(self):
        self.assertTrue("restaurant_reservation" in self.test_re1.transactions)
        self.assertTrue("delivery" in self.test_re2.transactions)
        self.assertTrue("pickup" in self.test_re2.transactions)
        self.assertTrue("delivery" not in self.test_re1.transactions)

    def test_get_Restaur_dict(self):
        test_dict = {
            "yelp_id": "oleana-restaurant-cambridge",
            "name": "Oleana Restaurant",
            "school_id": 3,
            "rating": 4.5,
            "price": "$$$",
            "distance": 1.19
        }
        self.assertEqual(self.test_re1.get_Restaur_dict(), test_dict)

    def test_get_Tr_dict_Cat_dict(self):
        test_Tr_dict = {
            "yelp_id" : "oleana-restaurant-cambridge",
            "transactions" : ["restaurant_reservation"]
        }
        test_Cat_dict = {
            "yelp_id" : "island-creek-oyster-bar-boston",
            "categories" : [
                {
                    "alias": "seafood",
                    "title": "Seafood"
                },
                {
                    "alias": "bars",
                    "title": "Bars"
                }
            ]
        }
        self.assertEqual(self.test_re1.get_Transc_dict(), test_Tr_dict)
        self.assertEqual(self.test_re2.get_Catego_dict(), test_Cat_dict)

    def tearDown(self):
        pass

class Test_School(unittest.TestCase):

    def setUp(self):
        test_sc_dict = {
            "id": "oleana-restaurant-cambridge",
            "name": "Oleana Restaurant",
            
            "categories": [
                {
                    "alias": "mediterranean",
                    "title": "Mediterranean"
                }
            ],
            "rating": 4.5,
            "transactions": ["restaurant_reservation"],
            "price": "$$$",
            "location": {
                "city": "Cambridge",
                "country": "US",
                "state": "MA",
                
            },
            "distance": 1190
        }
        self.test_sc1 = School('mit', test_sc_dict)
        self.test_sc2 = School('umich', test_sc_dict)
        self.test_re = Restaurant(test_sc_dict, 3, 'mit')

    def test_repr_contains(self):
        test_repr = repr(self.test_sc1)
        self.assertEqual(test_repr, "mit in Cambridge, MA")
        self.assertTrue(self.test_re in self.test_sc1)
        self.assertTrue(self.test_re not in self.test_sc2)

    def test_get_School_dict(self):
        test_dict = {
            'name' : 'mit',
            'city' : 'Cambridge',
            'state' : 'MA'
        }
        self.assertEqual(self.test_sc1.get_School_dict(), test_dict)
        self.assertNotEqual(self.test_sc2.get_School_dict(), test_dict)

    def tearDown(self):
        pass

class Test_Database(unittest.TestCase):

    def setUp(self):
        with open('test_db.json') as testfile:
            test_read = testfile.read()
            self.test_dict_ls1 = json.loads(test_read)['columbia']
            self.test_dict_ls2 = json.loads(test_read)['umich']
        self.test_db_obj = Database()
        self.test_db_obj.setup_db()
        self.test_db_obj.insert_One_Request(self.test_dict_ls1, 'columbia university')
        self.test_db_obj.insert_One_Request(self.test_dict_ls2, 'umich')

    def test_get_sch_ls_pop_num(self):
        ret_sch_ls = self.test_db_obj.get_school_ls()
        self.assertTrue({'name' : 'columbia university'} in ret_sch_ls)
        self.assertTrue({'name' : 'umich'} in ret_sch_ls)
        self.assertEqual(self.test_db_obj.get_pop_num(), 7)

    def test_avg_Rating(self):
        ret_sch_ls, ret_avg_ls = self.test_db_obj.avg_Rating()
        self.assertTrue( 'umich' in ret_sch_ls)
        self.assertTrue( 'columbia university' in ret_sch_ls)
        self.assertTrue( 4.0 in ret_avg_ls)
        self.assertEqual(len(ret_sch_ls), 2)
        self.assertEqual(len(ret_avg_ls), 2)

    def test_percent_above_4(self):
        ret_sch_ls, ret_percent_4_ls = self.test_db_obj.percent_above_4()
        self.assertTrue('umich' in ret_sch_ls and 'columbia university' in ret_sch_ls)
        self.assertTrue(3 / 50 in ret_percent_4_ls and 4 / 50 in ret_percent_4_ls)

    def test_popular_category(self):
        ret_cat_name_ls, ret_cat_ratio_ls = self.test_db_obj.popular_category()
        self.assertEqual(ret_cat_name_ls, ['Others'], "popular is defined by more than 20")
        self.assertEqual(ret_cat_ratio_ls, [1], "popular is defined by more than 20")

    def test_transc_service(self):
        service_ls, ratio_ls = self.test_db_obj.transc_service()
        self.assertEqual(service_ls, ['w/ Service', 'w/o Service'])
        self.assertEqual(ratio_ls, [4 / 7, 1 - (4 / 7)])

    def test_price_level(self):
        ret_price_ls, ret_percent_ls = self.test_db_obj.price_level()
        self.assertEqual(ret_price_ls, ['$', '$$', '$$$', '$$$$'])
        self.assertEqual(ret_percent_ls, [0, 7 / 250, 0, 0])
    
    def tearDown(self):
        self.test_db_obj.close_connection()




if __name__ == '__main__':
    unittest.main(verbosity=2)