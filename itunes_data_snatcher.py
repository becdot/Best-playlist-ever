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
    
# 4. Create a parent class of Song, SongDB

class SongDB:
    "Contains a list of Song instances, and provides methods for sorting and filtering by Song attributes"
    
    def __init__(self, filename, xpath_string):
        self.songs = [song for song in buildsongs(filename, xpath_string)]
        self.keys = easykeys(get_unique_keys(filename, xpath_string))
        for key in self.keys:
            setattr(self, key, fill_key_dicts(key, self.songs))  
            
    def filter_by_key(self, key, search_term):
        assert (key.lower() in self.keys), "Your key does not exist"
        if isinstance(search_term, str): assert ((search_term.lower() or search_term.capitalize() or search_term.upper() or search_term.title()) \
               in getattr(self, key).keys()), "Your search term was not found. Please check the spelling and try again."
        # 1. Need to check whether search_term is type int or str, as appropriate
        # 2. Remove unicode support from SongDB
        return (getattr(self, key))[search_term]
        
               
                            
### Add this into the Song DB class, instead of having it be a standalone method?
def fill_key_dicts(key, song_list):
    "Takes a key and a list of Song instances and returns {song.key : [Song1, Song2, Song3]}"
    key_dict = {} # -> key = artist
    for song in song_list: # -> for song in ['song1', 'song2', 'song3']
        if getattr(song, key):
            u_songdotkey = getattr(song, key).encode('ascii', 'ignore')
            songdotkey = u_songdotkey.decode('ascii', 'ignore')
            if u_songdotkey not in key_dict: # -> if song.artist(='Bach') not in key_dict
                key_dict[u_songdotkey] = [] # -> key_dict['Bach'] = []
                key_dict[songdotkey].append(song) # -> key_dict['Bach'] = [song1]
            else:
                key_dict[songdotkey].append(song)
    return key_dict
                    
    
# 5. Create a Song class
                
class Song(SongDB):
    """A class for itunes songs, with track name, artist, album, play count, etc data
       Child class of SongDB"""
    
    def __init__(self, song_dict):
        for key, value in song_dict.iteritems():
            setattr(self, key, value)
            
    def __str__(self):
        return "{name} by {artist} in album {album}".format(name=self.name, artist=self.artist, album=self.album)        
        
# 6. Create and populate song instances

def buildsong(xml_song_dict, defaultdict):
    "Returns a python dictionary populated with data from a single xml dictionary, with default values for any missing keys"
    
    "Also encodes incoming data into unicode, and then decodes it into ascii when returning"
    songdict = {}
    for node in xml_song_dict.xpath('key'):
        text_node = (node.text).encode('ascii', 'ignore')
        if node.getnext().text:
            if node.getnext().tag == 'integer':
                next_text_node = int(node.getnext().text)
                songdict[formatkey(text_node.encode('ascii', 'ignore'))] = next_text_node
            else:
                next_text_node = (node.getnext().text).decode('utf-8')
                songdict[formatkey(text_node.encode('ascii', 'ignore'))] = next_text_node.encode('ascii', 'ignore')
    return dict(defaultdict.items() + songdict.items())
        
def buildsongs(filename, xpath_string):
    "A generator that yields populated Song instances (filled with both filled and default values)"
    defaultdict = defaultkeys(easykeys(get_unique_keys(filename, xpath_string)))        
    return (Song(buildsong(song_dict, defaultdict)) for song_dict in xml_dict_generator(filename, xpath_string))
         

#defaultdict = defaultkeys(easykeys(get_unique_keys('itunes_sample.xml', 'dict/dict/dict')))        
#list_of_songs = [buildsong(song_dict, defaultdict) for song_dict in xml_dict_generator('itunes_sample.xml', 'dict/dict/dict')]
#for i in list_of_songs: print i

#container = SongDB("itunes_sample.xml", 'dict/dict/dict')


#container.filter_by_key('play_count', '5')

#for key in container.keys:
#    for k, v in getattr(container, key).iteritems():
#        for instance in v:
#            print key, 'for', getattr(instance, 'name'), 'is', getattr(instance, key)

#for value in fill_key_dicts('album', container.songs).values():
#    for instance in value:
#        print instance
#print fill_key_dicts('album', container.songs)

                        


# 6. Apply sorting algorithm

# 7. Return top songs

# 8. Create a new itunes playlist