from models.person import Person


from app import Base

class ControllerTest():
    
    def index():
        return {
            'msg': 'OK',
            'status_code' : 200,
        }
'''   
    def create_test():
        person = Person()
        
        person.dni = '1105156739'
        person.name = 'Miguel'
        person.last_name = 'Apolo'
        person.email = 'miguel.apolo@unl.edu.ec'
        person.password = '2001'
        person.status = True
        
        Base.session.add(person)
        Base.session.commit()
        
        return person.uid
       ''' 
