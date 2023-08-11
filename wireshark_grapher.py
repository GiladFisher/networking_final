import pyshark
import pandas as pd
from datetime import timedelta


def group_and_sum_within_interval(group):
    time_threshold = timedelta(seconds=2)
    within_interval = (group['timestamp'] - group['timestamp'].shift(1)) <= time_threshold
    grouped = group[within_interval]
    return pd.Series({
        'start_datetime': grouped['timestamp'].iloc[0],
        'total_size': grouped['length'].sum()
    })


pcap_file = 'filtered_recording_1.pcapng'
capture = pyshark.FileCapture(pcap_file)

packet_data = []
cnt = 0
for packet in capture:
    # print(packet.sniff_time)
    packet_info = {
        'timestamp': packet.sniff_time,
        'length': packet.length,
        'source_ip': packet.IPV6.src if hasattr(packet, 'IPV6') else None,
        'destination_ip': packet.IPV6.dst if hasattr(packet, 'IPV6') else None,
    }
    packet_data.append(packet_info)
    cnt += 1
    if cnt > 27000:
        break
    # print(packet_info)

df = pd.DataFrame(packet_data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.sort_values(by=['timestamp'], inplace=True)

result = df.groupby(df['timestamp'].diff().gt(timedelta(seconds=1)).cumsum()) \
           .apply(group_and_sum_within_interval).reset_index(drop=True)
print(result)

# print(df)
