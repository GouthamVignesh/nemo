from googleplaces import GooglePlaces, types


def nearby_pharmacy() :
    YOUR_API_KEY = 'AIzaSyDkfWiMGRhbIWJwk578id9e2X2Nhd7n-90'

    google_places = GooglePlaces(YOUR_API_KEY)

    query_result = google_places.nearby_search(
        location='Coimbatore, Tamil Nadu', keyword='doctor',
        radius=2000, types=[types.TYPE_DOCTOR])

    strr = " "
    flag = 0
    for place in query_result.places:
        place.get_details()
        strr = strr + "\n Name :" + (str(place.name).upper()) + "\n Address:" + str(place.formatted_address) + "\n Phone Number :" + (str(place.international_phone_number).upper()) + "\n Map Url :" + str(place.url) + "\n Web Link :" + str(place.website) + "\n Ratings:" + str(place.rating) +"\n \n"
        flag = flag+1
        if flag == 5:
            break

    return strr
    #returns nearby Pharmacy
    # dependency : python-google-places 1.4.1
