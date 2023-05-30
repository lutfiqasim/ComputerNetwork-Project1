from socket import *
import os
serverPort = 9977
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("localhost",serverPort))
serverSocket.listen(1)
clientSocket =""
clientAddress =""
clientIP =""
clientPort =""
# Path to the directory containing the files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


#Error page template 
#Note to Dr: put here so that we can bind the current client ip and port Number to it 
ERROR_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Error 404</title>
    <style>
        body {{
            height: 100vh;
        }}
        .title {{
            color: red;
        }}
        .students p {{
            font-weight: bold;
        }}
        .container {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
        }}
        .s2 {{
            font-size: 18pt;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="title"><h1>HTTP/1.1 404 Not Found</h1></div>
        <div class="title"><h2>The Requested file was not found</h2></div>
        <div class="students">
            <strong class="s2">Nasrall Hassan-1200134</strong><br>
            <strong class="s2">Lotfi Haji-1202064</strong><br>
            <strong class="s2">Anas Naji - 1200231</strong><br>
            <p><b>Client IP:</b> {client_ip}</p>
            <p><b>Client Port:</b> {client_port}</p>
        </div>
        <div></div>
    </div>
</body>
"""


#Method to generate NOT allowed response
def generateResponse(status_code,content_type,content):

    response = f"HTTP/1.1 {status_code}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    #if status code is redirect then added it to response with location
    if status_code == "307 Temporary Redirect":
        response +=content.decode("utf-8")
    response += "\r\n" #self-Note: \r\n at begining of line in response indicates end of it
    response = response.encode("utf-8")+content
    return response



def handle_request(request):
    # Handles the incoming HTTP request and decides which appropriate response to send

    # request has two parts method name, and path
    parts = request.split()
    print("______")
    print (parts)
    print("______")
    method = parts[0]
    path = parts[1]
    data =""
    content_Type=""
    if method != "GET":
        try:
            with open ("part3\error.html","rb") as f:
                data = f.read()
                content_Type ="text/html"
        except OSError as e:
            print(f"IO Error {e}")
        return generateResponse("405 Method Not Allowed","text/html",data)

    if path in ["/","/index.html","/main_en.html","/en"]:
        #Send the index.html file in english format
        try:
            with open("part 3\index.html", "rb") as f:
                data = f.read()
                content_Type = "text/html"
        except OSError as e:
            print(e)
    elif path == "/ar":
        try:
            with open("part 3\index-ar.html","rb") as f:
                data = f.read()
                content_Type ="text/html"
        except OSError as e:
            print (e)
    elif path.endswith(".html"): # requested a different html file by path locally
        
        filepath = os.path.join(BASE_DIR,path.strip("/"))
        
        #check if the given path is a file then open it and read it
        if os.path.isfile(filepath):
            try:
                with open(filepath,"rb") as localf:
                    data = localf.read()
                    content_Type = "text/html"
            except OSError as e:
                print(e)
        else:
            print("NOT FOUND IMAGE")
            # errorpage = ERROR_PAGE_TEMPLATE.format(client_ip = clientIP,client_port = clientPort)
            # return generateResponse("404 Not Found","text/html",errorpage)
    elif path.endswith(".css"):
        filepath = os.path.join(BASE_DIR,path.strip("/"))
        if os.path.isfile(filepath):
            try:
                with open(filepath,"rb") as localcss:
                    data = localcss.read()
                    content_Type= "text/css"
            except OSError as e:
                print(f"While reading css \n{e}")
        else:
            print("NOT FOUND IMAGE")
            # errorpage = ERROR_PAGE_TEMPLATE.format(client_ip = clientIP,client_port = clientPort)
            # return generateResponse("404 Not Found","text/html",errorpage.encode("utf-8"))
    elif path.endswith(".png"):
        file_path = os.path.join(BASE_DIR, path.strip("/"))
        if os.path.isfile(file_path):
            try:
                with open(file_path, "rb") as file:
                    data = file.read()
                    content_Type = "image/png"
            except OSError as e:
                print(e)
        else:
            print("NOT FOUND")
            # error_page = ERROR_PAGE_TEMPLATE.format(client_ip=clientIP, client_port=clientPort)
            # return generateResponse("404 Not Found", "text/html", error_page)
    elif path.endswith(".jpg"):
        file_path = os.path.join(BASE_DIR, path.strip("/"))
        if os.path.isfile(file_path):
            try:
                with open(file_path, "rb") as file:
                    data = file.read()
                    content_Type = "image/jpg"
            except OSError as e:
                print(e)
        else:
            print("NOT FOUND")
            # error_page = ERROR_PAGE_TEMPLATE.format(client_ip=clientIP, client_port=clientPort)
            # return generateResponse("404 Not Found", "text/html", error_page)
    elif path == "/yt":
        return generateResponse("307 Temporary Redirect", "text/html","Location: https://www.youtube.com".encode("utf-8"))
    elif path == "/so":
        return generateResponse("307 Temporary Redirect", "text/html", "Location: https://stackoverflow.com".encode("utf-8"))
    elif path == "/rt":
        return generateResponse("307 Temporary Redirect", "text/html", "Location: https://www.ritaj.ps".encode("utf-8"))
    else:
        error_page = ERROR_PAGE_TEMPLATE.format(client_ip=clientIP, client_port=clientPort)
        return generateResponse("404 Not Found", "text/html", error_page.encode("utf-8"))
    if data and content_Type:
        return generateResponse("200 OK",content_Type,data)
    else:
        return "".encode("utf-8")
def main():
    
    print ("Server listening on port 9977.. and ready to recive")

    while True:
        global clientSocket
        global clientAddress
        clientSocket,clientAddress = serverSocket.accept()
        global clientIP
        global clientPort 
        clientIP,clientPort = clientAddress
        request = clientSocket.recv(2048).decode("utf-8")
        print("Recived Request from client:")
        print (request)

        response = handle_request(request)
        clientSocket.sendall(response)
        clientSocket.close()


if __name__ == "__main__":
    main()