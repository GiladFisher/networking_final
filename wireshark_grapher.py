import pyshark
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt

# def group_and_sum_within_interval(group):
#     time_threshold = timedelta(seconds=2)
#     within_interval = (group['timestamp'] - group['timestamp'].shift(1)) <= time_threshold
#     grouped = group[within_interval]
#     return pd.Series({
#         'start_datetime': grouped['timestamp'].iloc[0],
#         'total_size': grouped['length'].sum()
#     })


#  Convert pcap to csv
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
# recording_to_csv('filtered_recording_2.csv', 'filtered_recording_2.pcapng')
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


start_time = None
accumulated_length = 0

# Create lists to store the results
start_times = []
total_lengths = []

# Iterate through the DataFrame
for index, row in df.iterrows():
    if row['time_diff'] < 1:
        accumulated_length += row['length']
        if start_time is None:
            start_time = row['timestamp']
    else:
        if start_time is not None:
            start_times.append(start_time)
            total_lengths.append(accumulated_length)
        else:
            print('start_time is None *****')
        accumulated_length = 0
        start_time = None

result_df = pd.DataFrame({'start_time': start_times, 'total_length': total_lengths})
# convert to MB
result_df['total_length'] = result_df['total_length'] / 1048576  # convert to MB
# result_df['total_length'] = result_df['total_length'] ** 0.5  # to make small values more visible
print(result_df.head())
print(result_df.info())
print(result_df.describe())
print(result_df.shape)

plt.figure(figsize=(20, 10))
plt.bar(result_df['start_time'], result_df['total_length'], width=0.0001)

# Add labels and title
plt.xlabel('Start Time')
plt.ylabel('MB')
plt.title('Total Length vs. Start Time')

# Display the plot
# plt.xticks(result_df['start_time'])
# plt.tight_layout()
plt.show()
