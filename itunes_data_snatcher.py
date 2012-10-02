from lxml import etree

# 1. Find itunes data
username = ""  # Change this to reflect your username!
filename = "/Users/%s/Music/iTunes/iTunes Music Library.xml" % (username)
test_filename = "test_xml.xml"

# 2. Parse data using lxml

def get_unique_keys(xml_file, outer_xml_string):
    "Parses an xml file and returns a dictionary of dictionaries, with unique ids as the keys"
    
    tree = etree.parse(xml_file)
    outer_dict = tree.xpath(outer_xml_string)
    new_dict = {}
    
    for unique_id in outer_dict:
        new_dict[int(unique_id.text)] = {}
    return new_dict
        
def singlexml_to_dict(single_xml_dict):
    "Takes a single nested xml dictionary and returns the keys and values as a new python dictionary"
    "E.g. <dict><key>Track</key><string>Song</string>...</dict> --> {Track: 'Song', Length: '2.3'}"
    
    keys = []
    values = []
    i = 0

    for keyvalues in single_xml_dict:
        i += 1
        if i % 2 != 0:
            keys.append(keyvalues.text)
        else:
            value = keyvalues.text
            if keyvalues.tag == 'integer':
                value = int(value)
            values.append(value)
                  
    return dict(zip(keys, values))
    
def xml_to_dict (xml_file, unique_dict, inner_xml_string):
    "Takes the dictionary with unique ids/empty dictionaries, and fills it with key/value information extracted from the inner nest of the xml document"
    "E.g. {123: {Track: 'Song', Length: '2.0'}, 456: {Track: 'Song2', Length: '2.5'}}"
    
    tree = etree.parse(xml_file)
    inner_dict = tree.xpath(inner_xml_string)
    kvdict_list = []
    
    # Creates a list of dictionaries with key/value information
    for dict in inner_dict:
        kvdict = singlexml_to_dict(dict)
        kvdict_list.append(kvdict)
    
    # Assigns the filled dictionaries as values to the dictionaries with unique ids
    for i, key in enumerate(unique_dict):
        unique_dict[key] = kvdict_list[i]
    return unique_dict    
             
print xml_to_dict(filename, get_unique_keys(filename, 'dict/dict/key'), 'dict/dict/dict')
    
    

# 3. Throw out uninteresting songs

# 4. Store relevant song data (plays, skips, last played)

# 5. Apply sorting algorithm

# 6. Return top songs

# 7. Create a new itunes playlist