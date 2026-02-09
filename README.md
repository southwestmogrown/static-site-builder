# Static Site Builder

A lightweight Python-based static site generator that converts markdown and template files into a complete HTML website.

## Overview

This project provides a simple yet effective tool for building static websites. It uses Python to process content files and generate HTML pages using customizable templates, making it perfect for blogs, documentation sites, or personal websites.

## Features

- **Template-based HTML Generation**: Uses HTML templates to maintain consistent site styling
- **Modular Python Architecture**: Clean separation of concerns with dedicated modules for:
  - HTML node manipulation (`htmlnode.py`)
  - Text node processing (`textnode.py`)
  - Utility functions for content processing (`utilities.py`)
- **Comprehensive Testing**: Includes unit tests for core functionality
- **Shell Script Automation**: Build and test scripts for easy project management
- **MIT Licensed**: Open source and free to use

## Project Structure

```
static-site-builder/
├── src/                    # Python source code
│   ├── main.py            # Main entry point
│   ├── htmlnode.py        # HTML node class
│   ├── textnode.py        # Text node class
│   ├── utilities.py       # Utility functions
│   ├── test_htmlnode.py   # Tests for HTMLNode
│   ├── test_textnode.py   # Tests for TextNode
│   └── test_utilities.py  # Tests for utilities
├── content/               # Content files (markdown/raw content)
├── static/                # Static assets (CSS, images, etc.)
├── docs/                  # Generated output directory
├── template.html          # HTML template file
├── main.sh               # Main shell script
├── build.sh              # Build script
├── test.sh               # Test script
└── index.html            # Generated index page
```

## Technologies Used

- **Python** (86.5%) - Core logic for site generation
- **HTML** (6.9%) - Templates and output
- **CSS** (6%) - Styling
- **Shell** (0.6%) - Build automation

## Getting Started

### Prerequisites

- Python 3.10.x (see `.python-version` for specific version)
- Bash shell for running build scripts

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/southwestmogrown/static-site-builder.git
   cd static-site-builder
   ```

2. Run the build script:
   ```bash
   ./build.sh
   ```

### Running Tests

Execute the test suite to verify functionality:

```bash
./test.sh
```

### Building Your Site

To generate your static site:

```bash
./main.sh
```

This will process content files and generate HTML output in the `docs/` directory.

## Usage

1. Add your content files to the `content/` directory
2. Customize `template.html` to match your desired site design
3. Add static assets (CSS, images) to the `static/` directory
4. Run `./main.sh` to build your site
5. The generated HTML will be available in the `docs/` directory

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created by [southwestmogrown](https://github.com/southwestmogrown)

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.
