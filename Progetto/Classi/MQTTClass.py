from umqtt.simple import MQTTClient
from MessageMaker import MM

class MQTT:
    
    def __init__(self, sub_callback_handler):
        """ Definizione variabili connessione MQTT """
        self.CLIENT_ID   = 'esp32'
        self.BROKER      = '192.168.131.51'
        self.USER        = ''
        self.PASSWORD    = ''
        self.TOPIC       = b'TheBox'
        self.TOPIC_SUB1  = b'TheBox/OpenCavueaux'
        self.TOPIC_SUB2  = b'TheBox/CloseCaveaux'
        self.TOPIC_SUB3  = b'TheBox/CaveauxStatus'
        self.TOPIC_SUB4  = b'TheBox/CaveauxStatus/Temp'
        self.TOPIC_SUB5  = b'TheBox/CaveauxStatus/Hum'
        self.TOPIC_SUB6  = b'TheBox/Pin'
        self.TOPIC_SUB7  = b'TheBox/Pin/Result'
        self.SUB_TOPICS  = [self.TOPIC_SUB1, self.TOPIC_SUB2,
                            self.TOPIC_SUB3, self.TOPIC_SUB4,
                            self.TOPIC_SUB5, self.TOPIC_SUB6,
                            self.TOPIC_SUB7]
        
        """ Inizializzazione dell'oggetto client """
        self.client = MQTTClient(self.CLIENT_ID, self.BROKER,
                                 user=self.USER, password=self.PASSWORD,
                                 keepalive=60)
        self.client.set_callback(sub_callback_handler)
    
        """ Inizializzazione oggetto MMaker """
        self.mMaker = MM()
    
    """Subscribe def"""
    def subscribes(self):
        for topic in self.SUB_TOPICS:
            self.client.subscribe(topic)


    def checkAndRead_msg(self, wifi, was_connected_MQTT, values):
        if wifi.isconnected() and self.client is not None and was_connected_MQTT:
            try:
                #print('primo')

                self.client.check_msg()
                message = self.mMaker.temperatureMsg(values["Temperature"])
                if message is not None:
                    self.publish(self.TOPIC_SUB4,message)
                message = self.mMaker.humidityMsg(values["Humidity"])
                if message is not None:
                    self.publish(self.TOPIC_SUB5,message)
                    
                    
            except OSError as e:
                print("Errore OSError in check_msg:", e)
                try:
                    self.disconnect()
                except:
                    pass
                try:
                    self.connect()
                    self.subscribes()
                    return 1
                    print("Riconnesso MQTT dopo errore")
                except Exception as e2:
                    print("Errore riconnessione MQTT:", e2)
                    return 0
        return was_connected_MQTT      
                    
    def getSUB_TOPICS(self):
        return self.SUB_TOPICS
    
    def connect(self):
        self.client.connect()
    
    def disconnect(self):
        self.client.disconnect()
        
    def publish(self, TOPIC, msg):
        self.client.publish(TOPIC, msg)
