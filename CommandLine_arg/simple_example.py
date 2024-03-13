#gerekli kutuphaneleri yukluyoruz
import argparse

#argumanları olusturun ve ayristirin
ap=argparse.ArgumentParser()
ap.add_argument("-n","--name",required=True)
#kesik cizgilerin olmasi lazims
help="Name of the user"

args=vars(ap.parse_args())


#simdi kullaniciya mesaj verelim

print("Hi there {}, It s nice to meet you!".format(args["name"]))