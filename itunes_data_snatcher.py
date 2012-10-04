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
    
### Might want to change so that this function does not use the mod operater
def get_unique_keys(filename, xpath_string):
    "Creates a set of unique keys (e.g. ['Name', 'Play Count']) from a nested xml dictionary"               
    keys = set(kvpairs.text for dict in xml_dict_generator(filename, xpath_string) 
                                for i, kvpairs in enumerate(dict) 
                                    if i % 4 == 0 or i % 4 == 2)
    return keys
    
# 3. Format data
    
def formatkey(key):
    """Returns a lowercase version of a key, separated by an underscore
       e.g. 'Track Name' -> 'track_name'"""
       
    if len(key.split()) > 1:
        return "{0}_{1}".format(*(key.lower()).split())
    else:
        return key.lower()
    
def easykeys(list_of_keys):
    "Returns a list of formatted keys ('Track Name' -> 'track_name')"
    return [formatkey(key) for key in list_of_keys]
                
def defaultkeys(list_of_keys):
    "Returns a dictionary with default values from a list of keys"
    #return {key:None for key in list_of_keys} Need Python 2.7!
    defaultdict = {}
    for key in list_of_keys:
        defaultdict[key] = None
    return defaultdict
    
# 4. Create a Song class
                
class Song:
    "A class for itunes songs, with track name, artist, album, play count, etc data"
    
    def __init__(self, song_dict):
        for key, value in song_dict.iteritems():
            setattr(self, key, value)
            
    def __str__(self):
        return "{name} by {artist} in album {album}".format(name=self.name, artist=self.artist, album=self.album)

# 5. Create and populate song instances

def buildsong(xml_song_dict, defaultdict):
    "Returns a python dictionary populated with data from a single xml dictionary, with default values for any missing keys"
    "Also encodes incoming data into unicode, and then decodes it into ascii when returning"
    songdict = {}
    for node in xml_song_dict.xpath('key'):
        text_node = (node.text).encode('ascii', 'ignore')
        if node.getnext().text:
            next_text_node = (node.getnext().text).encode('ascii', 'ignore')
        songdict[formatkey(text_node.decode())] = next_text_node.decode()
    return dict(defaultdict.items() + songdict.items())
        
def buildsongs(filename, xpath_string):
    "Yields populated Song instances (filled with both filled and default values)"
    defaultdict = defaultkeys(easykeys(get_unique_keys(filename, xpath_string)))        
    return (Song(buildsong(song_dict, defaultdict)) for song_dict in xml_dict_generator(filename, xpath_string))
     
for song in buildsongs(filename, 'dict/dict/dict'): print song
    
  
                        


# 6. Apply sorting algorithm

# 7. Return top songs

# 8. Create a new itunes playlist