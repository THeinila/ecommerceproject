from configparser import ConfigParser
def config(filename="src\data\database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for p in params:
            db[p[0]] = p[1]
    else:
        raise Exception(f"Section {section} not found in file {filename}")
    
    return db

