import re
from typing import Any, Dict, List, Tuple

from gathered_charts.transpose import transpose_chord


def handle_metadata(lines: List[str]) -> None:
    output_sections = []
    for line in lines:
        if line.startswith("{title:"):
            title = line[len("{title:") : -1].strip()
            output_sections.append(f"<h1>{title}</h1>")
            print(output_sections)
            continue
        if line.startswith("{key:"):
            key = line[len("{key:") : -1].strip()
            output_sections.append(f"<div class='metadata'>Key: {key}</div>")
            print(output_sections)
            continue
        if line.startswith("{start_of_"):
            section_name = (
                line[len("{start_of_") : -1].strip().replace("_", " ").capitalize()
            )
            output_sections.append(f"<h2>{section_name}</h2>")
            print(output_sections)
            continue
        if line.startswith("{end_of_"):
            output_sections.append("<hr/>")  # Add an optional divider after sections
            print(output_sections)
            continue


def parse_chordpro_to_lyrics_with_chords(
    lines: List[str], transpose_steps: int = 0
) -> str:
    output_sections = []

    for line in lines:
        # Parse the line to extract chords
        # The regex is updated to match any content inside the brackets
        lyrics = re.sub(
            r"\[([^\]]+)\]", "", line
        ).strip()  # Remove the chords, leaving only lyrics
        chords: List[Tuple[str, int]] = []

        current_pos = 0
        for match in re.finditer(r"\[([^\]]+)\]", line):
            chord = match.group(1)
            chord = transpose_chord(chord, transpose_steps)  # Transpose if needed
            chord_start = (
                match.start() - current_pos
            )  # Find the position to align with lyrics

            # Add a space if chords are next to each other to prevent them from colliding
            if chords and chord_start == chords[-1][1] + len(chords[-1][0]):
                chord_start += 1  # Add a space between chords

            chords.append((chord, chord_start))
            current_pos += (
                len(chord) + 2
            )  # Update current position (including the brackets)

        # Skip lines that have no lyrics and no chords
        if not lyrics and not chords:
            continue

        # Calculate the number of spaces needed to align chords before the lyrics
        if chords and chords[0][1] == 0 and not lyrics:
            # Add leading spaces for multiple chords before lyrics start
            leading_chord_length = sum(len(chord[0]) + 1 for chord in chords[:-1])
            chords[-1] = (chords[-1][0], leading_chord_length)

        # Generate chord line and lyrics line for HTML
        chord_line = ""
        lyrics_line = (
            " " * chords[-1][1] + lyrics
            if chords and chords[-1][1] > 0 and lyrics
            else lyrics
        )
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

    return "\n".join(output_sections)


def generate_full_html(chordpro_lines: List[str], transpose_steps: int = 0) -> str:
    # Generate song content in HTML format
    song_content_html = parse_chordpro_to_lyrics_with_chords(
        chordpro_lines, transpose_steps
    )

    # Full HTML structure including headers, style, and song content
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1 {{
                text-align: center;
                font-size: 28px;
                margin-bottom: 10px;
            }}
            .metadata {{
                text-align: center;
                font-size: 16px;
                color: #666;
                margin-bottom: 20px;
            }}
            h2 {{
                font-size: 20px;
                margin-top: 30px;
            }}
            .chords-line {{
                white-space: pre;
                font-family: monospace;
                color: #444;
                font-size: 18px;
                font-weight: bold;
                line-height: 1.4;
            }}
            .lyrics-line {{
                white-space: pre;
                font-family: Arial, sans-serif;
                line-height: 1.4;
                margin-bottom: 10px;
            }}
            .chord {{
                color: #d9534f;
            }}
        </style>
    </head>
    <body>
        {song_content_html}
    </body>
    </html>
    """
    return html


def generate_song_html(
    title: str, key: str, lead: str, sections: List[Dict[str, Any]]
) -> str:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @media print {{
                @page {{
                    size: A4;
                    margin: 20mm;
                }}
            }}
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            .song-header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .song-header h1 {{
                font-size: 28px;
                margin: 0;
            }}
            .song-header .metadata {{
                font-size: 16px;
                color: #666;
            }}
            .song-container {{
                column-count: 2;
                column-gap: 40px;
                column-fill: balance; /* Balances content to ensure more equal column heights */
                height: 100%; /* Ensure the content respects A4 page height */
                break-after: avoid-page; /* Try to avoid breaking in the middle of the columns */
            }}
            .song-section {{
                margin-bottom: 20px;
                break-inside: avoid;
            }}
            .song-section h2 {{
                font-size: 16px;
                padding-bottom: 5px;
                margin-bottom: 5px;
            }}
            .chords-line {{
                white-space: pre;
                font-family: monospace;
                color: #444;
                font-size: 20px;
                font-weight: bold;
                line-height: 1.4;
            }}
            .lyrics-line {{
                white-space: pre;
                font-family: Arial, sans-serif;
                line-height: 1.4;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="song-header">
            <h1>{title}</h1>
            <div class="metadata">Key: {key} | Lead: {lead}</div>
        </div>
        <div class="song-container">
    """

    # Iterate over each section and add the content
    for section in sections:
        html += f"""
        <div class="song-section">
            <h2>{section['name'].capitalize()}</h2>
        """

        for chord_line, lyrics_line in section["lines"]:
            html += f"""
                <div class="chords-line">{chord_line}</div>
                <div class="lyrics-line">{lyrics_line}</div>
            """

        html += """
        </div>
        """

    html += """
        </div>
    </body>
    </html>
    """
    return html
