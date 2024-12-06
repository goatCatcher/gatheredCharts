import re

from weasyprint import HTML

from gathered_charts.generate_music import (
    generate_full_html,
    parse_chordpro_to_lyrics_with_chords,
)
from gathered_charts.transpose import transpose_chord

# Example ChordPro lines
chordpro_lines = [
    "{title: Swing Low Sweet Chariot}",
    "{key: D}",
    "{start_of_chorus}",
    "Swing [D]low, sweet [G]chari[D]ot,",
    "Comin’ for to carry me [A7]home.",
    "Swing [D7]low, sweet [G]chari[D]ot,",
    "Comin’ for to [A7]carry me [D]home.",
    "{end_of_chorus}",
    "{start_of_chorus}",
    "I [D]looked over Jordan, and [G]what did I [D]see,",
    "Comin’ for to carry me [A7]home.",
    "A [D]band of angels [G]comin’ after [D]me,",
    "Comin’ for to [A7]carry me [D]home.",
    "{end_of_chorus}",
]

line = "Swing [D]low, sweet [G]chari[D]ot"
chrd = "      D          G    D"
line = "Swing low, sweet chariot"

lyrics = re.sub(
    r"\[([A-G][#b]?[^\]]*)\]", "", line
).strip()  # Remove the chords, leaving only lyrics
print(lyrics)
chords = []

transpose_steps = 0
current_pos = 0
match = re.finditer(r"\[([A-G][#b]?[^\]]*)\]", line)
for match_i in re.finditer(r"\[([A-G][#b]?[^\]]*)\]", line):
    chord = match_i.group(1)
    chord = transpose_chord(chord, transpose_steps)  # Transpose if needed
    chord_start = (
        match_i.start() - current_pos
    )  # Find the position to align with lyrics
    print(chord, chord_start)
    chords.append((chord, chord_start))
    print(chords)
    current_pos += len(chord) + 2  # Update current position (including the brackets)

# Generate chord line and lyrics line for HTML
chord_line = ""
last_pos = 0
for chord, position in chords:
    chord_line += (
        "&nbsp;" * (position - last_pos) + f"<span class='chord'>{chord}</span>"
    )
    last_pos = position + len(chord)

song_content_html = parse_chordpro_to_lyrics_with_chords(
    chordpro_lines, transpose_steps=0
)

# Generate full HTML
html_output = generate_full_html(chordpro_lines, transpose_steps=2)

# Save HTML output
with open("song.html", "w", encoding="utf8") as file:
    file.write(html_output)

HTML("song.html").write_pdf("song.pdf")
