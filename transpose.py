import re
# Preferred scale
chromatic_scale = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
# Notes to convert
enharmonic_map = {'Db': 'C#', 'D#': 'Eb', 'Gb': 'F#', 'Ab': 'G#', 'A#': 'Bb'}

# Function to convert chord number to chord name based on the key
def number_to_chord(key, number):
    # Define major scale chords for each number in a major key
    major_scale_chords = {
        1: '', 2: 'm', 3: 'm', 4: '', 5: '', 6: 'm', 7: 'dim'
    }
    
    # Define the chromatic scale starting from C
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Find the index of the key
    key_index = chromatic_scale.index(key)
    
    # Get the target chord by adjusting the chromatic scale
    chord_index = (key_index + number - 1) % len(chromatic_scale)
    chord_name = chromatic_scale[chord_index] + major_scale_chords[number]
    
    return chord_name

def get_normalised_chord(chord):
    match = re.match(r"([A-G][#b]?)(.*)", chord)
    if match:
        root, suffix = match.groups()
        if root in enharmonic_map:
            root = enharmonic_map[root]
        return root, suffix

# Function to transpose chord by a given number of steps
def transpose_chord(chord, steps=0):
    
    root, suffix = get_normalised_chord(chord)
    
    # Find the transposed index
    index = (chromatic_scale.index(root) + steps) % 12
    
    # Return the transposed chord with the suffix
    return chromatic_scale[index] + suffix

def key_to_steps(original_key, target_key):
    
    # Get root note and suffix (e.g., minor) for original and target keys
    original_root, original_suffix = get_normalised_chord(original_key)
    target_root, target_suffix = get_normalised_chord(target_key)

    # Get the normalized index in the chromatic scale for both keys
    original_index = chromatic_scale.index(original_root)
    target_index = chromatic_scale.index(target_root)

    # Calculate steps required to transpose
    steps = (target_index - original_index) % 12

    # adjust the suffix accordingly to reflect relative major/minor movement
    if original_suffix == 'm' and target_suffix == '':
        steps = (steps - 3) % 12
    elif original_suffix == '' and target_suffix == 'm':
        steps = (steps + 3) % 12
    return steps

# Test cases
print(key_to_steps('Am', 'Bb'))  # Expected: correct relative step count
print(key_to_steps('C', 'Am'))   # Expected: 9 steps down (relative major to minor)
print(key_to_steps('G#', 'F#m')) # Expected: 1 step (enharmonic equivalent)
print(key_to_steps('Db', 'F#'))  # Expected: 5 steps


# Updated parse function to use both steps and key
def parse_chordpro_to_lyrics_with_chords(lines, transpose_steps=0, target_key=None, original_key=None):
    # Determine the number of steps if keys are specified
    if target_key and original_key:
        transpose_steps = key_to_steps(original_key, target_key)
    
    output_sections = []

    for line in lines:
        # Parse the line to extract chords
        # The regex is updated to match any content inside the brackets
        lyrics = re.sub(r'\[([^\]]+)\]', '', line).strip()  # Remove the chords, leaving only lyrics
        chords = []

        current_pos = 0
        for match in re.finditer(r'\[([^\]]+)\]', line):
            chord = match.group(1)
            
            # If chord is specified as a number, convert to chord name
            if chord.isdigit():
                chord = number_to_chord(target_key or original_key, int(chord))

            # Transpose the chord if needed
            chord = transpose_chord(chord, transpose_steps)  # Transpose if needed
            chord_start = match.start() - current_pos  # Find the position to align with lyrics
            
            # Add a space if chords are next to each other to prevent them from colliding
            if chords and chord_start == chords[-1][1] + len(chords[-1][0]):
                chord_start += 1  # Add a space between chords
            
            chords.append((chord, chord_start))
            current_pos += len(match.group())  # Update current position (including the brackets)

        # Skip lines that have no lyrics and no chords
        if not lyrics and not chords:
            continue

        # Generate chord line and lyrics line for HTML
        chord_line = ""
        lyrics_line = lyrics
        last_pos = 0
        for chord, position in chords:
            chord_line += " " * (position - last_pos) + chord
            last_pos = position + len(chord)

        # Append to output sections with HTML pre tags
        if chord_line.strip():  # Only add chord line if there are chords
            print(chord_line)
            output_sections.append(f"<pre class='chords-line'>{chord_line}</pre>")
        if lyrics_line.strip():  # Only add lyrics line if there are lyrics
            print(lyrics_line)
            output_sections.append(f"<pre class='lyrics-line'>{lyrics_line}</pre>")

    # return "\n".join(output_sections)

# Example usage
parse_chordpro_to_lyrics_with_chords(
    lines=["[1][2]This is a [3]chord"],
    target_key="A",  # Specify the target key
    original_key="G"  # Specify the original key of the song
)


