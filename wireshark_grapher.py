import pyshark
import pandas as pd

#   Load the PCAP file
pcap_file = 'filtered_recording_1.pcapng'
capture = pyshark.FileCapture(pcap_file)

packet_data = []

for packet in capture:
    print(packet.sniff_time)
    packet_info = {
        'timestamp': packet.sniff_time,
        'length': packet.length,
        'source_ip': packet.IPV6.src if hasattr(packet, 'IPV6') else None,
        'destination_ip': packet.IPV6.dst if hasattr(packet, 'IPV6') else None,
    }
    packet_data.append(packet_info)
    print(packet_info)

df = pd.DataFrame(packet_data)

print(df)
