# SmartSort Website

A modern, responsive website showcasing the SmartSort adaptive sorting algorithm project.

## Features

- **Modern Design**: Clean, dark-themed UI with Geist font family
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Interactive Demo**: Live sorting demonstration with different data types
- **Complete Documentation**: All project documentation in one place
- **Performance Metrics**: Real-time statistics and benchmarks

## Structure

```
website/
├── index.html          # Main HTML file
├── css/
│   └── styles.css      # All styles with Geist fonts
├── js/
│   └── main.js         # Interactive functionality
└── README.md           # This file
```

## Sections

1. **Home/Hero**: Project introduction with key statistics
2. **Features**: 6 key features of SmartSort
3. **Documentation**: Tabbed documentation with 5 sections
   - Overview
   - Quick Start
   - API Reference
   - Algorithms
   - Examples
4. **Demo**: Interactive sorting demonstration
5. **Usage**: Installation and usage commands
6. **Performance**: Benchmark results and test statistics

## Interactive Demo

The demo allows you to:
- Select data type (Random, Sorted, Reverse, Nearly Sorted, Dense Range)
- Adjust array size (5-50 elements)
- See real-time analysis and strategy selection
- View sorting statistics

## Technologies

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **JavaScript**: Vanilla JS for interactivity
- **Fonts**: Geist and Geist Mono

## Usage

Simply open `index.html` in a modern web browser. No build process or server required.

```bash
# Open in default browser (Windows)
start index.html

# Or just double-click index.html
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Customization

### Colors

Edit CSS variables in `styles.css`:

```css
:root {
    --bg-primary: #000000;
    --accent-primary: #0070f3;
    /* ... more variables */
}
```

### Content

Edit content directly in `index.html` or modify the documentation sections.

## Font Note

The website uses Geist and Geist Mono fonts. The font files should be placed in a `media/` directory, or the CSS will fall back to system fonts (Arial).

To use the fonts properly, ensure the following font files are in `website/media/`:
- 8a480f0b521d4e75-s.8e0177b5.woff2
- 7178b3e590c64307-s.b97b3418.woff2
- caa3a2e1cccd8315-s.p.853070df.woff2
- 3e19a33f554fa0a0-s.fcfe2d47.woff2
- 4a404718ad388446-s.d8e620cc.woff2
- 64c5f24155ea0bd5-s.p.591f1055.woff2

## License

Educational use - part of the SmartSort project.
