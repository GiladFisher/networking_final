import pyshark
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt

def group_and_sum_within_interval(group):
    time_threshold = timedelta(seconds=2)
    within_interval = (group['timestamp'] - group['timestamp'].shift(1)) <= time_threshold
    grouped = group[within_interval]
    return pd.Series({
        'start_datetime': grouped['timestamp'].iloc[0],
        'total_size': grouped['length'].sum()
    })

def recording_to_csv(filename, recording):
    pcap_file = recording #'filtered_recording_1.pcapng'
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
        # cnt += 1
        # if cnt > 2700:
        #     break
        # print(packet_info)

    df = pd.DataFrame(packet_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by=['timestamp'], inplace=True)
    df['length'] = df['length'].astype(float)
    df.to_csv(filename, index=False)

# recording_to_csv('filtered_recording_1.csv', 'filtered_recording_1.pcapng')

df = pd.read_csv('filtered_recording_1.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
print(df.info())
print(df.head())

df['time_diff'] = df['timestamp'] - df['timestamp'].shift(1)
df['time_diff'] = df['time_diff'].dt.seconds + df['time_diff'].dt.microseconds / 1000000
df['time_diff'] = df['time_diff'].fillna(0)
df.sort_values(by=['timestamp'], inplace=True)
print(df.head())
print(df['time_diff'].describe())
# result = df.groupby(df['timestamp'].diff().gt(timedelta(seconds=1)).cumsum()) \
#            .apply(group_and_sum_within_interval).reset_index(drop=True)
# result['total_size'] = result['total_size'].astype(float)
# print(result)
# plt.figure(figsize=(10, 6))  # Adjust the figure size if needed

# Plot the data
# plt.plot(result['start_datetime'], result['total_size'], marker='o', linestyle='-', color='b')
#
# # Add labels and title
# plt.xlabel('Datetime')
# plt.ylabel('Total Size')
# plt.title('Total Size vs. Datetime')
#
# # Display the plot
# plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
# plt.tight_layout()  # Adjust layout for better spacing
# plt.show()

# print(df)
