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
             
itunesdata = xml_to_dict(filename, get_unique_keys(filename, 'dict/dict/key'), 'dict/dict/dict')    

# 3. Throw out uninteresting songs

sample = {1851: {'Album': 'Velvet Goldmine', 'Skip Date': '2007-06-22T22:13:08Z', 'Persistent ID': '92D3C8B8E9F4818C', 'Location': 'file://localhost/Users/rebeccaliss/Music/iTunes/iTunes%20Music/Grant%20Lee%20Buffalo/Velvet%20Goldmine/The%20Whole%20Shebang.mp3', 'File Folder Count': 4, 'Total Time': 251820, 'Play Date UTC': '2012-07-10T23:23:22Z', 'Sample Rate': 44100, 'Genre': 'Soundtrack', 'Bit Rate': 128, 'Sort Name': 'Whole Shebang ', 'Play Count': 20, 'Kind': 'MPEG audio file', 'Name': 'The Whole Shebang ', 'Artist': 'Grant Lee Buffalo', 'Date Added': '2007-01-25T01:07:17Z', 'Artwork Count': 1, 'Play Date': 3424793002L, 'Date Modified': '2005-03-30T23:55:45Z', 'Library Folder Count': 1, 'Skip Count': 1, 'Track ID': 3167, 'Size': 4190919, 'Track Type': 'File'}, 1853: {'Album': 'Garden State', 'Persistent ID': '92D3C8B8E9F4818F', 'Track Number': 12, 'Track Type': 'File', 'File Folder Count': 4, 'Disc Number': 1, 'Total Time': 252794, 'Play Date UTC': '2010-10-06T21:08:11Z', 'Compilation': None, 'Sample Rate': 44100, 'Track Count': 13, 'Genre': 'Soundtrack', 'Bit Rate': 128, 'Play Count': 8, 'Kind': 'AAC audio file', 'Name': 'Let Go', 'Artist': 'Frou Frou', 'Disc Count': 1, 'Date Added': '2007-01-25T01:07:18Z', 'Play Date': 3369229691L, 'Location': 'file://localhost/Users/rebeccaliss/Music/iTunes/iTunes%20Music/Compilations/Garden%20State/12%20Let%20Go.m4a', 'Date Modified': '2005-11-05T02:59:41Z', 'Library Folder Count': 1, 'Composer': 'Garden State', 'Year': 2004, 'Track ID': 3169, 'Size': 4075991}}

def match_criteria(dictionary, key, value, operator):
    assert operator == '==' or '>' or '>=' or '<' or '<='
    for unique_id, dict in dictionary.iteritems():
        if key in dict:
            if isinstance(value, int):
                eval_string = '{0} {1} {2}'.format(dict[key], operator, value)
                if eval(eval_string):
                    yield dict['Name']
            else:
                eval_string = '"{0}" {1} "{2}"'.format(dict[key], operator, value)
                if eval(eval_string):
                    yield dict['Name']

for dict in match_criteria(itunesdata, 'Skip Count', 20, '>='):
    print dict

                        

# 4. Store relevant song data (plays, skips, last played)

# 5. Apply sorting algorithm

# 6. Return top songs

# 7. Create a new itunes playlist