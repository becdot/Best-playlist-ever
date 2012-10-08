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
            
            
    ### Make this function more efficient?
    def keys_as_types(self, str_or_int):
        "Returns a list of keys that have either string or integer values, depending on input"
        
        "E.g. ['album', 'artist', 'file_location'] -> string values, ['play_count', 'skip_count'] -> int values"
    
        assert (str_or_int == int or str_or_int == str), 'The value must be either str or int'
        keys_and_types = set((key, type(getattr(instance, key)))
                          for key in self.keys
                            for k, v in getattr(self, key).iteritems()
                               for instance in v)
        return [pair[0] for pair in keys_and_types if pair[1] == str_or_int]

            
    def filter_by_key(self, key, search_term):
        key = key.lower()
        assert (key in self.keys), "Your key does not exist"
        
        assert (key in self.keys_as_types(type(search_term))), "Your search term must be of the appropriate type"
        
        if isinstance(search_term, str): 
            assert (search_term or search_term.lower() or search_term.capitalize() or search_term.upper() or search_term.title()
                    in getattr(self, key).keys()), "Your search term was not found. Please check the spelling and try again."
        if isinstance(search_term, int): assert search_term in getattr(self, key).keys(), "Your search term was not found. Please check the spelling and try again."
        
        # 1. Need to check whether search_term is type int or str, as appropriate
        return (getattr(self, key))[search_term]
        
               
                            
### Add this into the Song DB class, instead of having it be a standalone method?
def fill_key_dicts(key, song_list):
    "Takes a key and a list of Song instances and returns {song.key : [Song1, Song2, Song3]}"
    key_dict = {} # -> e.g. key = artist
    for song in song_list: # -> for song in ['song1', 'song2', 'song3']
        if getattr(song, key):
            if getattr(song, key) not in key_dict: # -> if song.artist(='Bach') not in key_dict
                key_dict[getattr(song, key)] = [] # -> key_dict['Bach'] = []
                key_dict[getattr(song, key)].append(song) # -> key_dict['Bach'] = [song1]
            else:
                key_dict[getattr(song, key)].append(song)
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
        if isinstance(node.text, str): # if the text is not already in unicode
            text_node = (node.text).decode('utf-8', 'replace') # make it into unicode
        if node.getnext().text: # if there is a next node
            if node.getnext().tag == 'integer': # and it is an integer
                next_text_node = int(node.getnext().text) # store it as an integer
                songdict[formatkey(text_node.encode('utf-8', 'replace'))] = next_text_node # and add it to the dictionary
            else: # if the next node is not an integer
                next_text_node = node.getnext().text # store it as a variable
                if isinstance(node.getnext().text, str): # unless the text of the following node is not already in unicode
                    next_text_node = (node.getnext().text).decode('utf-8', 'replace') # make it into unicode
                songdict[formatkey(text_node.encode('utf-8', 'replace'))] = next_text_node.encode('utf-8', 'replace') # and add it to the dictionary
    return dict(defaultdict.items() + songdict.items())
        
def buildsongs(filename, xpath_string):
    "A generator that yields populated Song instances (filled with both filled and default values)"
    defaultdict = defaultkeys(easykeys(get_unique_keys(filename, xpath_string)))        
    return (Song(buildsong(song_dict, defaultdict)) for song_dict in xml_dict_generator(filename, xpath_string))
         

container = SongDB(filename, 'dict/dict/dict')
#print container.keys_as_types(filename, 'dict/dict/dict', int)

for instance in container.filter_by_key('Artist', 'Bach'): print instance



#for key in container.keys:
#    for k, v in getattr(container, key).iteritems():
#        for instance in v:
#            print key, instance


                        


# 6. Apply sorting algorithm

# 7. Return top songs

# 8. Create a new itunes playlist