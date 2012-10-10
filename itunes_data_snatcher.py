from lxml import etree

import operator
import datetime
# Contains environment-specific information, may comment out
import environment 

# 1. Find itunes data
username = environment.username  # Change this to reflect your username!
filename = "/Users/%s/Music/iTunes/iTunes Music Library.xml" % (username)
test_filename = "itunes_sample.xml"
xpath_string = 'dict/dict/dict'

# 2. Parse and format data
                  
def xml_dict_generator(filename, xpath_string):
    "Generates inner xml dictionaries (but not individual key/value pairs)"
    
    tree = etree.parse(filename)
    inner_dict = tree.xpath(xpath_string)
    for dict in inner_dict: yield dict

def formatkey(key):
    "Returns a lowercase version of a key, separated by an underscore, e.g. 'Track Name' -> 'track_name'"
       
    if len(key.split()) > 1:
        return '_'.join(key.split()).lower()
    else:
        return key.lower()
    
def unique_keys(filename, xpath_string):
    "Returns a set of formatted unique keys (e.g. ['name', 'play_count']) from a nested xml dictionary"               

    keys = set(formatkey(node.text)
            for dict in xml_dict_generator(filename, xpath_string)
                for node in dict.xpath('key'))
    return keys
    
        
KEYS = unique_keys(filename, xpath_string)    
  
      
def python_dict_generator(xml_dict):
    "Returns a python dictionary populated with data from a single xml dictionary, and None values where the xml key does not exist"

    songdict = {}
    for node in xml_dict.xpath('key'):
        if not isinstance(node.text, unicode): # if the text is not already in unicode
            text_node = (node.text).decode('utf-8', 'replace') # make it into unicode
            text_node = formatkey(text_node)
        if node.getnext().text: # if there is a next node
            if node.getnext().tag == 'integer': # and it is an integer
                next_text_node = int(node.getnext().text) # store it as an integer
                songdict[text_node.encode('utf-8', 'ignore')] = next_text_node # and add it to the dictionary
            else: # if the next node is not an integer
                next_text_node = node.getnext().text
                if not isinstance(next_text_node, unicode): # if the text of the following node is not already in unicode
                    next_text_node = (next_text_node).decode('utf-8', 'replace') # make it into unicode
                songdict[text_node.encode('utf-8', 'ignore')] = next_text_node.encode('utf-8', 'ignore') # and add it to the dictionary
                
    for key in KEYS:
        if key not in songdict:
            songdict[key] = None
    
    return songdict
       
# 3. Create a Song class
                
class Song():
    "A class for itunes songs, with track name, artist, album, play count, etc data"
    
    def __init__(self, song_dict):
        for key, value in song_dict.iteritems():
            setattr(self, key, value)
            
    def __str__(self):
        return "{name} by {artist} in album {album}".format(name=self.name, artist=self.artist, album=self.album)     
        
# 4. Create and populate song instances
        
def buildsongs(filename, xpath_string):
    "A generator that yields populated Song instances (filled with both filled and default values)"
    
    return (Song(python_dict_generator(song_dict)) for song_dict in xml_dict_generator(filename, xpath_string))   


# 5. Create a SongDB class, that essentially acts as a database for a list of songs

class SongDB:
    "Contains a list of Song instances, and provides methods for sorting and filtering by Song attributes"
    
    def __init__(self, filename, xpath_string):
        self.songs = [song for song in buildsongs(filename, xpath_string)]
        self.keys = KEYS
        for key in self.keys:
            setattr(self, key, self.fill_key_dicts(key, self.songs))             
                  
        
    ### way to make faster? possibly using dictionary comprehensions, or looping through keys instead of songs
    def fill_key_dicts(self, key, song_list):
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
        
    ### try to define recursively?
    def sort_functions(self, *function):
        "Takes a variable number of functions, and returns a list of songs for which all functions evaluate as true"
        
        for i in range(len(function)):
            if i == 0:
                song_matches = [song for song in self.songs if function[i](song)] 
            else:
                song_matches = [song for song in song_matches if function[i](song)]
        return song_matches    
    
    def match_criteria(self, key, value, input_operator):
        "Returns a function that checks a key and value against an operator and returns a Boolean (eg artist == 'Bach' or play_count >= 20)"
    
        operator_dict = {'==': operator.eq, '!=': operator.ne, '>=': operator.ge, '>': operator.gt, '<=': operator.le, '<': operator.lt}
        input_operator = operator_dict[input_operator]
        key = key.lower()
        assert (key in self.keys), "Your key does not exist"
                
        def compare(song_inst):
            if input_operator(getattr(song_inst, key), value):
                return True
            return False
            
        return compare
         
# 6. Define custom functions for filtering                        

def play_density(song):
    "Returns a float of play_count / total_time_elapsed_since_song_was_added_to_itunes_library"

    date_added = format_date_object(song)
    time_elapsed = datetime.datetime.now() - date_added
    plays = 0.0
    if song.play_count:
        plays = float(song.play_count)
    density = plays / time_elapsed.days
            
    return density
    

def format_date_object(song):
    "Takes a song and returns a datetime object (created from song.date_added)"
    
    input_date = song.date_added
    output_date = datetime.datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%SZ")
    
    return output_date
    


# 7. Apply sorting algorithm

# 8. Return top songs

# 9. Create a new itunes playlist


# ** Testing **
container = SongDB(filename, xpath_string)


criteria = container.match_criteria('play_date_utc', '2012-10-03', '>=')
recent_songs = [instance for instance in container.sort_functions(criteria)]
print len(recent_songs)
densities = [(play_density(instance), instance, instance.play_date_utc) for instance in recent_songs]
densities.sort()
densities.reverse()
for t in densities[:20]: print t[1], 'has a play density of', t[0]