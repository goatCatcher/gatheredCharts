## Music PDF Generator Documentation

### 1. Database Layer: JSON File for Each Song

Each song should be stored as a **JSON file**, with the following structure:

- **Metadata**: Contains details about the song, including:
  - **Title**: The name of the song.
  - **Key**: Key song is transcribed in
  - **Lead**: Song leader
- **Sections**: Contains the individual sections of the song, each with:
  - **Section ID**: A unique identifier for each section (e.g., `chorus_1`, `verse_2`, `note_1`).
  - **Content**: Markdown-style string data for each section, with chords in line.
    - **Example**:
      ```
      "Swing [D]low, sweet [G]chari[D]ot,",
      "Comin’ for to carry me [A7]home."
      ```
- **Structure**: A list of **Section IDs** representing the **order** in which they should appear in the song.

Additionally, create a `night[N].json` file which lists the **order of songs** for a specific event or night. Each song should be referenced by its file name, providing an easy way to compile a setlist.

### 2. Function to Write HTML Input String for Each Song

Write a function to convert each **song JSON file** into an **HTML string** with the following requirements:

- **Parsing ChordPro Format**: Each section of the song should be parsed to correctly handle chords and lyrics alignment.
- **Special Handling for Specific IDs**:
  - **Note IDs**: Should be rendered differently (e.g., italicized or highlighted) to clearly indicate they are notes for the band (no chords).
  - **Instrumental IDs**: Should be visually distinct to indicate instrumental-only sections (no lyrics).

The function should produce a formatted HTML snippet that represents the song, including metadata, sections, and special handling for particular IDs.

### 3. Compile All Songs to an HTML Document (CSS Layer)

Requirements:

- Create a function that accepts a `night[N].json` script and compiles all the referenced song files into a **single HTML document**.
- **CSS Styling**: The HTML should include embedded CSS to ensure:
  - **Two-column layout**: Content should be presented in a format where each song fills the first column before moving to the second.
  - **Consistent Styles**: Use consistent styling for chords, lyrics, metadata, and special sections (notes, instrumental).
  - **Printing Considerations**: The layout should be optimized for A4-sized printing, respecting page breaks and ensuring readable chord-lyrics alignment.

### 4. Write to PDF

After compiling the HTML, the next step is to generate a **PDF**.

- **HTML to PDF Conversion**: Use a library like **WeasyPrint** or **pdfkit** to convert the generated HTML into a **PDF** document.
- **Requirements**:
  - The PDF should maintain the **two-column format** and respect A4 page dimensions.
  - Ensure **high readability** of chords, lyrics, and metadata, with appropriate handling of page breaks.

### Additional Considerations

- **Transposition Functionality**: Implement the ability to **transpose chords** before generating the HTML. This can be done via a transposition function that modifies chord notation within the JSON before HTML generation. Can either enter a step number or a key
- **Multiple chord input styles**: Users can input chords using letter of number notation.
- **Reusable Sections**: Common sections like choruses can be reused across songs. Store these separately and reference them in multiple song JSON files to avoid redundancy.
- **Special Formatting for Notes**: Consider using distinct colors or styles for **notes** to ensure they are visually separated from performance lyrics and chords. This helps band members quickly identify important information.
- **Error Handling**: Add error handling to ensure the JSON files are formatted correctly. If a song or section ID is missing, provide clear error messages to guide the user in correcting the issue.
- **Future Scalability**: The JSON structure and HTML generation functions should be designed to allow easy extension. For example, adding new metadata fields (e.g., tempo, genre) or new section types should not require major code changes.

- **Convert from UG**: Specify an UG url, scrape the song and convert into JSON format
