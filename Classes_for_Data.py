

class Restaurant(object):
    
    def __init__(self, restau_dict, school_id, school_name):
        self.yelp_id = restau_dict['id']
        self.name = restau_dict['name']
        self.school_id = school_id
        self.school_name = school_name
        self.rating = restau_dict['rating']
        self.distance = restau_dict['distance'] / 1000
        if 'price' in restau_dict:
            self.price = restau_dict['price']
        else:
            self.price = None
        self.transactions = restau_dict['transactions']
        self.categories = restau_dict['categories']

    def __repr__(self):
        return "{} in {}km".format(self.yelp_id, self.distance)

    def __str__(self):
        return self.name

    def __contains__(self, transc):
        return transc in self.transactions

    def get_Restaur_dict(self):
        return {
            'yelp_id' : self.yelp_id,
            'name' : self.name,
            'school_id' : self.school_id,
            'rating' : self.rating,
            'distance' : self.distance,
            'price' : self.price
        }

    def get_Transc_dict(self):   # get dict with ls of transcs
        return {
            'yelp_id' : self.yelp_id,
            'transactions' : self.transactions
        }

    def get_Catego_dict(self):
        return {
            'yelp_id' : self.yelp_id,
            'categories' : self.categories
        }

class School(object):

    def __init__(self, school_name, data_dict):
        self.name = school_name
        self.state = data_dict['location']['state']
        self.city = data_dict['location']['city']

    def __repr__(self):
        return "{} in {}, {}".format(self.name, self.city, self.state)

    def __contains__(self, restaurant):
        return restaurant.school_name == self.name

    def get_School_dict(self):
        return {
            'name' : self.name,
            'city' : self.city,
            'state' : self.state
        }