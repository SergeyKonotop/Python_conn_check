#!/usr/bin/python3

import socket, argparse, csv, datetime, re

parser = argparse.ArgumentParser(conflict_handler='resolve', add_help=True)
parser.add_argument('-h', help='host name')
parser.add_argument('-P', help='protocol')
parser.add_argument('-p', type=int, help='port' )
parser.add_argument('-f', help='input csv file')
args = parser.parse_args()

HOST = vars(args)['h']              
PORT = vars(args)['p']              
PROTOCOL = vars(args)['P']
FILE = vars(args)['f']

protocol_list = {'TCP': socket.SOCK_STREAM, 'tcp': socket.SOCK_STREAM, \
                 'UDP': socket.SOCK_DGRAM, 'udp': socket.SOCK_DGRAM}

def connect_to_host(HOST, PORT, PROTOCOL):
    try:
        with socket.socket(socket.AF_INET, protocol_list[PROTOCOL]) as s:
            cdatetime = datetime.datetime.now()
            date_time = '{:%d.%m.%Y %H:%M:%S}'.format(cdatetime)
            s.connect((HOST, PORT))
            result = PROTOCOL + ' ' + HOST + ':' + str(PORT) + ' OPEN \n' + 'exited with 0' + '\n' + date_time
            return result
    except TimeoutError:
        result = PROTOCOL + ' ' + HOST + ':' + str(PORT) + ' CLOSED \n' + 'exited with 1' + '\n' + date_time
        return result

if not FILE:
    result_list = connect_to_host(HOST, PORT, PROTOCOL).split('\n') 
    for item in range(2):
        print(result_list[item])
else:
#    file_path = r'/home/vagrant/'
#    full_file_path = file_path + FILE
    CLOSE = False
    with open('output.csv', 'w', newline='') as output_file:
        spamwriter = csv.writer(output_file, delimiter=',')
#                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        with open(FILE, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                output_str = connect_to_host(row[1], int(row[2]), row[0]).split('\n')
                res_list = re.split(' |:', output_str[0].strip()) + [output_str[2]]
                spamwriter.writerow(res_list)
                if 'CLOSED' in connect_to_host(row[1], int(row[2]), row[0]):
                    CLOSE = True
    if CLOSE:
        print('Exited with 1')
    else: 
        print('Exited with 0')
