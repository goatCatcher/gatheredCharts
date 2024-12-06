from gathered_charts.generate_music import parse_chordpro_to_lyrics_with_chords

# Example usage
transposed_output = parse_chordpro_to_lyrics_with_chords(
    lines=["[1][2]This is a [3]chord"], transpose_steps=2
)
print(transposed_output)
