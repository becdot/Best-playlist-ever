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
    
def easykeys(list_of_keys):
    return ["{0}_{1}".format(*(key.lower()).split()) for key in list_of_keys if len(key.split()) > 1 else key.lower()]
for key in list_of_keys:
        return     
                
print get_unique_keys(filename, 'dict/dict/dict')


tree = etree.parse(test_filename)
inner_dicts = tree.xpath('/dict/dict')
for dict in inner_dicts:
    for node in dict.xpath('key'):
        #print 'Current:', node.text
        #print 'Next:', node.getnext().text
        pass
        
        
class Song:
    def __init__(self):
        for key in my_list:
            setattr(self, key, '')






                        

# 4. Store relevant song data (plays, skips, last played)

# 5. Apply sorting algorithm

# 6. Return top songs

# 7. Create a new itunes playlist