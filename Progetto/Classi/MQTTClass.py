from umqtt.simple import MQTTClient

def sub_callback_handler(topic,msg):
    
        if topic == MQTT_TOPIC_SUB1:
            data = ujson.loads(msg)
            
        if topic == MQTT_TOPIC_SUB2:
            if sta_if.isconnected() ==False and msg.decode() == "0":
                print('connetto')
                connectionWifi()   
                connectionClient()


class MQTT:    
    def __init__(self,broker,client_id,topic,topic_sub,user = "", password=""):
        self.broker = broker
        self.user = user
        self.password = password
        self.topic = topic
        self.topic_sub = topic_sub
        self.clients = MQTTClient(client_id, broker, user, password,keepalive=60)
        
    
    def connectClient(self):
         print("Connecting to MQTT server... ", end="")
         self.clients.connect()
         self.clients.set_callback(sub_callback_handler)
         self.clients.subscribe(self.topic_sub)
         print("Connected!")
         
    def publishClient(self,client.publish(topic, message)):
        self.clients.publish(topic, message)
 
