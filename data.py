import codecs
def Articles():
    f=codecs.open('/home/manishankar/Desktop/Py/tamil.txt','r','utf-8')
    r=f.read()
    articles = [
        {
            'id': 1,
            'title':'Article One',
            'body':r,
            'author':'mani',
            'create_date':'04-25-2017'
        },
        {
            'id': 2,
            'title':'Article Two',
            'body':'kasdjfkjads fjsdokf oisdn ihsdb uisdfn snksldnviosdoi sdninsd nsdiuhdi hsdif',
            'author':'shankar',
            'create_date':'04-25-2017'
        },
        {
            'id': 3,
            'title':'Article Three',
            'body':'klhdoif haisodhfiwaegrweoifj idn ifhwehf hnksdn jsh fweh bfgwuf fhi nkwfhw fifhwuegfuwnkshvis vjsadhiwne fhwef wfj9wq uwehf wehfwhe8fw ',
            'author':'hello',
            'create_date':'04-25-2017'
        }
    ]
    return articles

