from lxml import etree
# Contains environment-specific information, may comment out
import environment 

# 1. Find itunes data
username = environment.username  # Change this to reflect your username!
filename = "/Users/%s/Music/iTunes/iTunes Music Library.xml" % (username)
test_filename = "test_xml.xml"

# 2. Parse data using lxml

def xml_dict_generator(filename, xpath_string):
    "Generates inner xml dictionaries (but not individual key/value pairs)"
    tree = etree.parse(filename)
    inner_dict = tree.xpath(xpath_string)
    for dict in inner_dict: yield dict
    
def get_unique_keys(filename, xpath_string):
    "Creates a set of unique keys (e.g. ['Name', 'Play Count']) from a nested xml dictionary"               
    keys = set(kvpairs.text for dict in xml_dict_generator(filename, xpath_string) 
                                for i, kvpairs in enumerate(dict) 
                                    if i % 4 == 0 or i % 4 == 2)
    return keys
    
def formatkey(key):
    if len(key.split()) > 1:
        return "{0}_{1}".format(*(key.lower()).split())
    else:
        return key.lower()
    
def easykeys(list_of_keys):
    return [formatkey(key) for key in list_of_keys]
                
def defaultkeys(list_of_keys):
    #return {key:None for key in list_of_keys} Need Python 2.7!
    defaultdict = {}
    for key in list_of_keys:
        defaultdict[key] = None
    return defaultdict
                
class Song:
    def __init__(self, song_dict):
        for key, value in song_dict.iteritems():
            setattr(self, key, value)
            
    def __str__(self):
        return "{name} by {artist} in album {album}".format(name=self.name, artist=self.artist, album=self.album)

def buildsong(song_dict, defaultdict):
    songdict = {}
    for node in song_dict.xpath('key'):
        songdict[formatkey(node.text)] = node.getnext().text
    return dict(defaultdict.items() + songdict.items())
        
def buildsongs(filename, xpath_string):
    defaultdict = defaultkeys(easykeys(get_unique_keys(filename, xpath_string)))        
    return (Song(buildsong(song_dict, defaultdict)) for song_dict in xml_dict_generator(filename, xpath_string))
    
    
for song in buildsongs('itunes_sample.xml', 'dict/dict/dict'): print song
    
   

                        

# 4. Store relevant song data (plays, skips, last played)

# 5. Apply sorting algorithm

# 6. Return top songs

# 7. Create a new itunes playlist