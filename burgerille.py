#!/usr/bin/python

import sys
from bs4 import BeautifulSoup as bs
import requests
import simplekml

import googlemaps


def main(argv):
    if (len(argv) != 3):
        print "Usage: {} <google maps API key> <number of pages to fetch>".format(argv[0])
        print "Get the API key from https://developers.google.com/maps/documentation/javascript/get-api-key"
        sys.exit(1)
    gmaps_key = argv[1]
    number_pages = argv[2]

    gmaps = googlemaps.Client(key=gmaps_key)

    places = []
    urls = ["https://burgerille.fi/tag/suomi/page/{}/".format(i) for i in range(1,12)]
    for url in urls:
        page = requests.get(url)
        soup = bs(page.content, features="html.parser")
        soup.find_all(class_="entry-title")
        for i in soup.find_all(class_="entry-title"):
            link = i.find_all("a")[0].get("href")
            # discard name of burger
            place = i.text.split(", ",1)[1]
            places.extend([[place, link]])

    kml = simplekml.Kml()
    for [place, link] in places:
        geocode_result = gmaps.geocode(place)[0]
        address = geocode_result["formatted_address"]
        lat = geocode_result["geometry"]["location"]["lat"]
        lng = geocode_result["geometry"]["location"]["lng"]
        kml.newpoint(name=place, description=u"<![CDATA[<a href=\"{}\">{}</a><br/>{}]]>".format(link, place, address), coords=[(lng, lat)])

    print kml.kml().encode("utf-8")


if __name__ == "__main__":
    main(sys.argv)
