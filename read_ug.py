import requests
import json
from bs4 import BeautifulSoup
import re

url = "https://tabs.ultimate-guitar.com/tab/hillsong-worship/cornerstone-chords-1149440"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

js_store_div = soup.find('div', class_='js-store')

if js_store_div and 'data-content' in js_store_div.attrs:
    data_content = js_store_div['data-content']
    data_json = json.loads(data_content)

    song_data = data_json['store']['page']['data']['tab_view']['wiki_tab']['content']
    lines = song_data.splitlines()

[print(x) for x in lines]


def replace_chords_with_lyrics(chord_line, lyric_line):
    # Extract chords and their positions
    chord_positions = []
    split_chord_line = re.split(r'(\[ch\].*?\[/ch\])', chord_line)

    current_pos = 0
    for part in split_chord_line:
        if part.startswith('[ch]'):
            chord = part.replace('[ch]', '').replace('[/ch]', '')
            chord_positions.append((current_pos, chord))
        else:
            current_pos += len(part)
    
    # Insert chords into lyrics at respective positions
    result = ""
    lyric_index = 0
    for pos, chord in chord_positions:
        result += lyric_line[lyric_index:pos] + f"[{chord}]"
        lyric_index = pos

    result += lyric_line[lyric_index:]  # Add remaining part of lyrics
    return result

# Iterate through the list of lines
for i in range(len(lines)):
    if '[ch]' in lines[i]:
        # This line contains chords
        chord_line = lines[i]
        if i + 1 < len(lines) and '[tab]' in lines[i + 1]:
            # Next line is lyrics
            lyric_line = re.sub(r'\[/?tab\]', '', lines[i + 1])
            combined_line = replace_chords_with_lyrics(chord_line, lyric_line)
            output_lines.append(combined_line)
        else:
            # If there are no lyrics, just add the chord line as is
            output_lines.append(re.sub(r'\[/?ch\]', '', lines[i]))
    elif '[tab]' not in lines[i]:
        # Add non-tab and non-chord lines directly (like section headers)
        output_lines.append(lines[i])

# Write the result to a text file in ChordPro format
with open('song_chordpro.txt', 'w', encoding='utf-8') as file:
    for line in output_lines:
        if line.strip():
            file.write(line + '\n')

print("ChordPro formatted lyrics saved to 'song_chordpro.txt'")


