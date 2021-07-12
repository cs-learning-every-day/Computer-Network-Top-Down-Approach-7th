import time
from socket import *
from rich.table import Table
from rich.console import Console
from rich.progress import track

console = Console()

serverName = "localhost"
serverPort = 12000

console.print("Pinging %s:%d:" % (serverName, serverPort), style="bold red")

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Sequence Number", justify="right", no_wrap=True, style="red")
table.add_column("From", justify="right", style="bold cyan")
table.add_column("Message", justify="right", style="magenta")
table.add_column("Times(s)", justify="right", style="green")

send_message = "My name is XmchxCoder, I do some ping test."

average_rtt = None
minimum_rtt = float("inf")
maximum_rtt = float("-inf")
lost_packet_count = 0
PING_TEST_COUNT = 10

for i in track(range(1, PING_TEST_COUNT + 1), description="Pinging..."):
    start_time = time.time()
    serverAddr = None
    try:
        clientSocket.sendto(send_message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddr = clientSocket.recvfrom(1024)
        rtt = time.time() - start_time
        if maximum_rtt < rtt:
            maximum_rtt = rtt
        if minimum_rtt > rtt:
            minimum_rtt = rtt
        table.add_row(str(i), str(serverAddr), "successful", str("%.3f" % rtt))
    except OSError as e:
        lost_packet_count += 1
        table.add_row(str(i), str(serverAddr), "time out", "None")

average_rtt = (minimum_rtt + maximum_rtt) / 2

console.print(table)

console.print("Ping statistics for %s:%d:\n"
              "\tPackets: [bold]Sent = %d, Received = %d, Lost = %d[/bold]"
              % (serverName, serverPort,
                 PING_TEST_COUNT, PING_TEST_COUNT - lost_packet_count, lost_packet_count),
              style="magenta")

console.print("Approximate round trip times in milli-seconds:\n"
              "\t[bold]Minimum = [red]%.3fms[/red], Maximum = [red]%.3fms[/red], Average = [red]%.3fms[/red][/bold]"
              % (minimum_rtt*1000, maximum_rtt*1000, average_rtt*1000),
              style="green")

clientSocket.close()
