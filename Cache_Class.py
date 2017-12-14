from datetime import datetime
import json

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG = False

class Cache(object):
        
    def __init__(self, filename):
        self.CACHE_DICTION = {}
        self.CACHE_FNAME = filename
        self.open_cache_file()

    def open_cache_file(self):
        try:
            with open(self.CACHE_FNAME) as cache_file:
                print("open existed cache file")
                cache_json = cache_file.read()
                self.CACHE_DICTION = json.loads(cache_json)
        except FileNotFoundError:
            print("cache file ", self.CACHE_FNAME, " not exists")

    def has_cache_expired(self, timestamp_str, expire_in_days = 7):
        now = datetime.now()
        
        # datetime.strptime converts a formatted string into datetime object
        cache_timestamp = datetime.strptime(timestamp_str, DATETIME_FORMAT)

        # subtracting two datetime objects gives you a timedelta object
        delta = now - cache_timestamp
        delta_in_days = delta.days

        # now that we have days as integers, we can just use comparison
        # and decide if cache has expired or not
        if delta_in_days >= expire_in_days:
            return True # It's been longer than expiry time
        else:
            return False

    def get_from_cache(self, identifier):
        """If unique identifier exists in specified cache dictionary and has not expired, return the data associated with it from the request, else return None"""
        identifier = identifier.upper() # Assuming none will differ with case sensitivity here
        dictionary = self.CACHE_DICTION
        if identifier in dictionary:
            data_assoc_dict = dictionary[identifier]
            if self.has_cache_expired(data_assoc_dict['timestamp'],data_assoc_dict["expire_in_days"]):
                if DEBUG:
                    print("Cache has expired for {}".format(identifier))
                # also remove old copy from cache
                del dictionary[identifier]
                data = None
            else:
                data = dictionary[identifier]['values']
        else:
            data = None
        return data

    def set_in_cache(self, identifier, data, expire_in_days = 7):
        """Add identifier and its associated values (literal data) to the data cache dictionary, and save the whole dictionary to a file as json"""
        identifier = identifier.upper()
        self.CACHE_DICTION[identifier] = {
            'values': data,
            'timestamp': datetime.now().strftime(DATETIME_FORMAT),
            'expire_in_days': expire_in_days
        }

        with open(self.CACHE_FNAME, 'w') as cache_file:
            cache_json = json.dumps(self.CACHE_DICTION, indent = 4)
            cache_file.write(cache_json)
