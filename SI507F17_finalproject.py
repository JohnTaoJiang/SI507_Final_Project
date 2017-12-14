from Session_Class import *
from Database_Class import *
from Drawing_Class import *
import sys

def generate_Reqs(school_ls):
    request_ls = []
    for school in school_ls:
        params_dict = {
            'term' : 'restaurants',
            'location' : school,
            'radius' : 2000,
            'limit' : 50,
            'sort_by' : 'rating'
        }
        request_ls.append(params_dict.copy())
    return request_ls



if __name__ == "__main__":

    command = None
    if len(sys.argv) != 2: 
        print("Usage : only and exactly one input argument!")
    else:
        command = sys.argv[1]
        if command == 'setup':
            school_ls = ['umich', 'ucla', 'mit', 'columbia university', 'UT Austin']
            db1 = Database()
            db1.setup_db()
            request_ls = generate_Reqs(school_ls)
            endpoint_url = 'https://api.yelp.com/v3/businesses/search'
            for req in request_ls:
                data_dict_ls = make_requests(endpoint_url, req)['businesses']
                db1.insert_One_Request(data_dict_ls, req['location'])
            print('*********Database built successfully*********')
            db1.close_connection()

        elif command == 'view':
            db1 = Database()
            Drawing = Visual()
            
            x_ls1, y_ls1 = db1.avg_Rating()
            x_ls2, y_ls2 = db1.percent_above_4()
            Drawing.BarChart(x_ls1, y_ls1, x_ls2, y_ls2)

            lab_ls1, rat_ls1 = db1.popular_category()
            lab_ls2, rat_ls2 = db1.transc_service()
            lab_ls3, rat_ls3 = db1.price_level()
            Drawing.Pie_Chart([lab_ls1, lab_ls2, lab_ls3], [rat_ls1, rat_ls2, rat_ls3])
            db1.close_connection()

        else:
            print("Usage: input argument can only be either 'setup' or 'view'")