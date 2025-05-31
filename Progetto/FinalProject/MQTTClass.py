from umqtt.simple import MQTTClient
from MessageMaker import MM

class MQTT:
    
    """ Costruttore """
    def __init__(self, sub_callback_handler):
        """ Definizione variabili connessione MQTT """
        self.CLIENT_ID   = 'esp32'
        self.BROKER      = '192.168.131.51'
        self.USER        = ''
        self.PASSWORD    = ''
        self.TOPIC       = b'TheBox'
        self.TOPIC_SUB1  = b'TheBox/OpenCaveaux'
        self.TOPIC_SUB2  = b'TheBox/CloseCaveaux'
        self.TOPIC_SUB3  = b'TheBox/CaveauxStatus'
        self.TOPIC_SUB4  = b''
        self.TOPIC_SUB5  = b'TheBox/CaveauxStatus/Hum'
        self.TOPIC_SUB6  = b'TheBox/Pin'
        self.TOPIC_SUB7  = b'TheBox/Pin/WrongPassword'
        self.TOPIC_SUB8  = b'TheBox/Allarme/Furto'
        self.TOPIC_SUB9  = b'TheBox/Allarme/Risolto'
        self.TOPIC_SUB10 = b'TheBox/Allarme/PinErrato'
        self.TOPIC_SUB11 = b'TheBox/Status/Ping'
        self.TOPIC_SUB12 = b'TheBox/Status/Pong'
        self.TOPIC_SUB13 = b'TheBox/Allarme/StopBuzzer'
        self.TOPIC_SUB14 = b'TheBox/CaveauxStatus/Temp/NuovaSoglia'
        self.TOPIC_SUB15 = b'TheBox/CaveauxStatus/Hum/NuovaSoglia'
        self.TOPIC_SUB16 = b'TheBox/CaveauxStatus/Dis/NuovaSoglia'
        self.SUB_TOPICS  = [self.TOPIC_SUB1, self.TOPIC_SUB2,
                            self.TOPIC_SUB3, self.TOPIC_SUB4,
                            self.TOPIC_SUB5, self.TOPIC_SUB6,
                            self.TOPIC_SUB7, self.TOPIC_SUB8,
                            self.TOPIC_SUB9, self.TOPIC_SUB10,
                            self.TOPIC_SUB11, self.TOPIC_SUB12,
                            self.TOPIC_SUB13, self.TOPIC_SUB14,
                            self.TOPIC_SUB15, self.TOPIC_SUB16]
        
        self.SUB_TOPICS_SUB=[self.TOPIC_SUB2, self.TOPIC_SUB6,
                             self.TOPIC_SUB11, self.TOPIC_SUB13,
                             self.TOPIC_SUB14, self.TOPIC_SUB15,
                             self.TOPIC_SUB16]
        
        """ Inizializzazione dell'oggetto client """
        self.client = MQTTClient(self.CLIENT_ID, self.BROKER,
                                 user=self.USER, password=self.PASSWORD,
                                 keepalive=60)
        self.sub_callback_handler = sub_callback_handler
        self.client.set_callback(self.sub_callback_handler)
    
        """ Inizializzazione oggetto MMaker """
        self.mMaker = MM()
    
    
    """ Il client si sottoscrive ai topics """
    def subscribes(self):
        for topic in self.SUB_TOPICS_SUB:
            self.client.subscribe(topic)


    def checkAndRead_msg(self, wifi, was_connected_MQTT, values):
        if wifi.isconnected() and self.client is not None and was_connected_MQTT:
            try:
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
                    self.client.set_callback(self.sub_callback_handler)
                    self.connect()
                    self.subscribes()
                    
                    print("Riconnesso MQTT dopo errore")
                    return 1

                except Exception as e2:
                    print("Errore riconnessione MQTT:", e2)
                    return 0     
        return was_connected_MQTT      
        
        
    """ Restituisce l'insieme di topics """
    def getSUB_TOPICS(self):
        return self.SUB_TOPICS
    
    
    def connect(self):
        self.client.connect()
    
    
    def disconnect(self):
        self.client.disconnect()
        
        
    """ Pubblica su TOPIC il messaggio msg """
    def publish(self, TOPIC, msg):
        self.client.publish(TOPIC, msg)
