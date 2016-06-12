import urwid
import random
import socket
import sys

if len(sys.argv) < 3:
    print("Invalid argument")
    sys.exit()

HOST = sys.argv[1]
PORT = sys.argv[2]


def get_server_details(host, port):
    # Data Place Holders
    urt_server_details = {}

    # Socket Request Message
    MESSAGE = "\377\377\377\377getstatus"

    # Get response from server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((host, int(port)))
        sock.send(MESSAGE.encode('latin-1'))
        response, addr = sock.recvfrom(1024)
        sock.close()
        response_lines = response.decode('latin-1').split("\n")
    except (Exception,) as exc:
        raise exc

    # Retrieve the server settings
    config_string_parts = response_lines[1].split("\\")
    urt_server_details['configs'] = {}
    for i in range(1, len(config_string_parts), 2):
        urt_server_details['configs'][config_string_parts[i].strip()] = config_string_parts[i + 1].strip()

    urt_server_details['players'] = []
    for x in range(2, (len(response_lines) - 1)):
        player_data = response_lines[x].split(" ")

        # print(player_data)

        player_dictionary = {"ping": player_data[1], "score": player_data[0], "name": player_data[2][1:-1]}
        urt_server_details['players'].append(player_dictionary)

    return urt_server_details


def handle_keypress(key):
    raise urwid.ExitMainLoop()


def update_ui(event_loop, user_data=None):
    player = urwid.Text(markup="Player", align='left')
    score = urwid.Text(markup="Score", align='left')
    ping = urwid.Text(markup="Ping", align='left')

    title_row = urwid.Columns([
        urwid.AttrMap(urwid.Text(markup="Urban Terror Server Monitor", align='center'), 'title')
    ])

    server_info_row = urwid.Columns([
        urwid.AttrMap(urwid.Text(markup="{} - {}".format(HOST, PORT), align='center'), 'server')
    ])

    header_row = urwid.Columns([
        urwid.AttrMap(player, 'header'),
        urwid.AttrMap(score, 'header'),
        urwid.AttrMap(ping, 'header'),
    ])

    server_details = get_server_details(HOST, int(PORT))
    players = server_details['players']

    rows = [urwid.Divider(" "), title_row, server_info_row, urwid.Divider(" "), header_row, ]
    for x in players:
        rows.append(urwid.Columns([
            urwid.Text(markup=x['name'], align='left'),
            urwid.Text(markup=x['score'], align='left'),
            urwid.Text(markup=x['ping'], align='left'),

        ]))

    piles = urwid.Pile(rows)
    main_window = urwid.Filler(body=piles, valign='top')

    event_loop.widget = main_window
    event_loop.set_alarm_in(3, update_ui)


palette = [
    ('title', 'light green, bold', 'black'),
    ('server', 'yellow, bold', 'black'),
    ('header', 'dark red, bold', 'white'),
]

main_loop = urwid.MainLoop(
    widget=urwid.Filler(urwid.Text(markup="Urban Terror Monitor", align='center')),
    palette=palette,
    unhandled_input=handle_keypress
)
main_loop.set_alarm_in(0, update_ui)
main_loop.run()
