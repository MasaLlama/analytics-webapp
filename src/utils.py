from configparser import ConfigParser

def Configurator(file='./user_config.ini', section='DATA' ):
  
  
  #create a parser
  parser = ConfigParser()
  #read config file
  parser.read(file)
  
  #get section, defaults to postgresql
  db = {}
  
  # Checks to see if section (postgresql) parser exists
  if parser.has_section(section):
    params = parser.items(section)
    for param in params:
      db[param[0]] = param[1]
      
  # Returns an error if a parameter is called that is not listed in the initialization file
  else:
    raise Exception(f'Section {section} not found in the {file} file')
  
  return db