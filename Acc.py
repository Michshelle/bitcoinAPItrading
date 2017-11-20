class btfAccount():

    def __init__(self):
        
        self.dict = {}
        self.dict['APIK'] = 'xx'
        self.dict['APIS'] = '00'

        

        
    def __getitem__(self,item):
	
        return self.dict[item] 
  

	    
        