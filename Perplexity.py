from time import sleep
from uuid import uuid4
from requests import Session
from threading import Thread
from time import time, sleep
from json import loads, dumps
from random import getrandbits
from websocket import WebSocketApp
import websocket
import ssl
import requests


def __check_connection():
    '''check is server up and we can connect to it'''
    try:
        response = requests.get("https://www.perplexity.ai/")
        if response.status_code in [200,403]: #200 is ok and 403 is forbidden, if we get it than server is ok.
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return False
    
def create_perplexity(model="llama-2-70b-chat",print_additional_info=False):
    '''it is impossible to create object directly, so you should use this function and it
       will create object only if server is up'''
    if __check_connection():
        return __Perplexity(model,print_additional_info)
    else:
        return None

class __Perplexity:
    """A class to interact with the Perplexity website.
    To get started you need to create an instance of this class.
    For now this class only support one Answer at a time.
    """
    def __init__(self,model="llama-2-70b-chat", print_additional_info=False) -> None:
        self.session: Session = self.__init_session()

        #False by default because this information is printer for debug purposes
        self.print_additional_info = print_additional_info
        
        self.searching = False #run searching function while this variable is true
        
        self.t: str = self.__get_t()     # timestampParam
        self.sid: str = self.__get_sid() # Security IDentifier


        if not self.__ask_anonymous_user():
            self.__print_if_required("Failed to ask anonymous user")
            exit(-1)
        
        self.ws: WebSocketApp = self.__init_websocket()
        self.ws_message = "" #contains request strng
        self.ws_connected = False #socket isn't connected to the server at the start
        
        self.__auth_session()
        
        self.query_str = "" #contains user's prompt
        self.answer = "" #result of searching
        
        if self.__check_is_model_available(model):
            self.__print_if_required("{} isn't supported!".format(model))
            self.model = model
        else:
            exit(-1)

            

    def __check_is_model_available(self,model):
        models = ["llama-2-13b-sft","llama-2-70b-chat","llama-2-13b-chat","llama-2-7b-chat"]
        if model in models:
            return True
        else:
            return False
    def __print_if_required(self,text):
        if self.print_additional_info:
            print(text)

    
    def __endinstance(self):
        '''stop the connection'''
        __print_if_required("Terminating Perplexity instance...")
        self.ws_connected = False
        if self.ws and self.ws.sock:
            self.ws.sock.shutdown()
        
    def __init_session(self) -> Session:
        session: Session = Session()

        uuid = str(uuid4())
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
            'Origin': 'https://labs.perplexity.ai',
            'Host': 'labs-api.perplexity.ai'
        }
        
        session.headers.update(headers)
        session.get(url=f"https://www.perplexity.ai/search/{uuid}", allow_redirects=False)
                                 
        return session

    def __get_t(self) -> str:
        return format(getrandbits(32), "08x")

    def __get_sid(self) -> str:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
            'origin': 'https://labs.perplexity.ai',
            "referrer": "https://labs.perplexity.ai/",
            #'Host': 'labs-api.perplexity.ai',
            "accept": "*/*",
            "accept-language": "en-AU,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }
        
        self.session.headers.update(headers)
        
        response = self.session.get(
            url=f"https://labs-api.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}",
        )

        response_text = response.text[1:]

        if response_text:
            try:
                response_json = loads(response_text)
                if 'sid' in response_json:
                    return response_json["sid"]
                else:
                    self.__print_if_required('The "sid" key was not found in the response.')
                    return None
            except Exception as e:
                self.print_if_required('Error parsing JSON:', e)
                return None
        else:
            self.__print_if_required('Empty response')
            return None


    def __ask_anonymous_user(self) -> bool:
        response = self.session.post(
            url=f"https://labs-api.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}&sid={self.sid}",
            data="40{\"jwt\":\"anonymous-ask-user\"}"
        ).text

        return response == "OK"
                
    def __get_cookies_str(self) -> str:
        cookies = ""
        for key, value in self.session.cookies.get_dict().items():
            cookies += f"{key}={value}; "
        return cookies[:-2]
   
    def __on_open(self, ws):
        self.__print_if_required("Websocket connection opened.")
        self.ws_connected = True
        self.ws.send("2probe")
        
    def __on_message(self, _, message):
        if message is not None and isinstance(message, str):
            #print(message)
            if message == "2":
                self.ws.send("3")
            elif message == "3probe":
                self.ws.send("5")
            elif message == "6":
                if self.ws:
                    if self.ws_message != "":
                        self.ws.send(self.ws_message)

            if (self.searching) and message.startswith(f"42[\"{self.model}_query_progress"):
                # Check if the string contains '"status":"completed"' and '"final":true'
                if '"status":"completed"' in message and '"final":true' in message:
                    # Extract the output from the message
                    start = message.find('"output":"') + len('"output":"')
                    end = message.find('","final"')
                    output = message[start+1:end]
                    self.answer = output
                    self.searching = False
        else:
            self.__print_if_required('The message is None or not a string.')
                
    def __on_close(self, ws, close_status_code, close_msg):
        self.__print_if_required("Websocket connection closed.", close_status_code, close_msg)
        self.ws_connected = False
        self.__endinstance()


    def __on_error(self, ws, error):
        self.__print_if_required(f"Websocket error: {error}")
        self.__endinstance()
    
    def __init_websocket(self) -> websocket.WebSocketApp:       
        headers = {
            "Host": "labs-api.perplexity.ai",
            "Connection": "Upgrade",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183",
            "Upgrade": "websocket",
            "Origin": "https://labs.perplexity.ai",
            "Cookie": self.__get_cookies_str()
        }

        self.ws = WebSocketApp(
            url=f"wss://labs-api.perplexity.ai/socket.io/?EIO=4&transport=websocket&sid={self.sid}",
            header=headers,
            on_open=self.__on_open,
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close,
        )

        ws_thread = Thread(target=self.ws.run_forever, kwargs={'sslopt': {"cert_reqs": ssl.CERT_NONE}})
        ws_thread.daemon = True
        ws_thread.start()
        return self.ws

    def __auth_session(self) -> None:
        self.session.get(url="https://www.perplexity.ai/api/auth/session")


    def search(self, query: str, retry_count=0):
        if retry_count > 3:  # Maximum of 3 retries
            self.searching = False  # Reset the searching flag
            return 'Failed to get response after 3 retries.'

        formatted_query = query.replace('\n', '\\n').replace('\t', '\\t')
        self.query_str = formatted_query

        # If already searching, return an error, reset the searching flag, and retry
        if self.searching:
            self.searching = False
            return self.search(query, retry_count + 1)

        self.searching = True
        self.ws_message: str = f'42["perplexity_playground",{{"model":"{self.model}","messages":[{{"role":"user","content":"{formatted_query}","priority":0}}]}}]'
        start_time = time()
        timeout = 20  # Timeout in seconds
        
        # Waiting for connection to open
        while not self.ws.sock or not self.ws.sock.connected:
            self.__print_if_required("Waiting for connection to open...")
            if time() - start_time > timeout:
                return ""
            sleep(1)

        self.ws.send(self.ws_message)

        # Waiting for search to complete
        start_time = time()
        timeout = 40  # Timeout in seconds
        while self.searching:
            #print("Searching...")
            if time() - start_time > timeout:
                return self.search(query, retry_count + 1)
            sleep(1)

        # Process the response
        if self.answer != "":
            formatted_output = self.answer.replace('\\n', '\n').replace('\\t', '\t')
            return formatted_output
        else:
            self.searching = False  # Reset the searching flag before retrying
            return self.search(query, retry_count + 1)  # Recursive call if there is an error

        
