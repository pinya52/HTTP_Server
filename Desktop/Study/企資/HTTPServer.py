#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import threading
import time

class Server():
    def _listen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pars = ('127.0.0.1', 8000)
        s.bind(pars)
        s.listen(5)

        while True:
            (clientsocket, address) = s.accept()
            print("Recieved connection from {addr}".format(addr=address))
            threading.Thread(target=self.serverClient, args=(clientsocket, address)).start()
            
    def _generate_headers(self, response_code):
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\r\n'
        elif response_code == 301:
            header += 'HTTP/1.1 301 Moved Permanently\r\n'
            header += 'Location : /good.html\r\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\r\n'
            
        header += 'content-type: text/html\r\n'
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now} \r\n'.format(now=time_now)
        header += 'Connnection: close \r\n\r\n'
        return header

    def serverClient(self, clientsocket, address):
        while True:
            data = clientsocket.recv(1024)
            data = data.decode()
            request_method = data.split(' ')[0]
            print('From client:', data)
            
            if request_method == 'GET':
                file_requested = data.split(' ')[1]
                
                if file_requested == "/redirect.html":
                    response = self._generate_headers(301)

                elif file_requested == "/good.html":
                    response = self._generate_headers(200)
                    response += "<!Doctype><html><body>good.html</body></html>"

                else:
                    response = self._generate_headers(404)
                    response += "<!Doctype><html><body>404 Not Found</body></html>"

                response_file = response.encode()
                clientsocket.send(response_file)
                
                clientsocket.close()
            break


s = Server()
s._listen()


# In[ ]:




