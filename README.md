# Kay.com Product Categorizer

A Python-based tool for automatically categorizing Kay Jewelers product pages using regex pattern matching. The tool analyzes product URLs, titles, and breadcrumb navigation to accurately classify items into main categories and subcategories.

## Features

- Automated product categorization using regex patterns
- Support for major jewelry categories including:
  - Rings (Engagement, Fashion, Promise, Anniversary, Wedding Bands)
  - Necklaces (Chains, Fashion)
  - Earrings (Hoops, Drop, Stud, Solitaire)
  - Bracelets (Chains, Fashion)
  - Watches
  - Personalized Jewelry
  - Coordinates
  - Sets
  - Previously Owned Jewelry/Watches
  - Charms
- Text cleaning and normalization
- CSV processing with detailed category distribution reporting

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd kay-product-categorizer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your input CSV file in the project directory
2. Update the input/output filenames in main() if needed
3. Run the script:
```bash
python product_categorizer.py
```

The script will generate a new CSV file with added categorization columns and print category distribution statistics.

## Input CSV Requirements

The input CSV should contain the following columns:
- Full URL
- Title
- Breadcrumb Level 2
- Breadcrumb Level 3

## Roadmap

### Short-term
- [ ] Refine personalized jewelry pattern matching
  - Add more specific patterns for name necklaces
  - Improve detection of custom engraving options
  - Add patterns for birthstone jewelry
  - Include family jewelry patterns
- [ ] Add unit tests for edge cases
- [ ] Implement logging system

### Mid-term
- [ ] Add support for new product categories
- [ ] Improve subcategory classification accuracy
- [ ] Add configuration file for easy pattern updates
- [ ] Create command-line interface for better usability

### Long-term
- [ ] Implement machine learning classification as supplement to regex
- [ ] Add API endpoint for real-time categorization
- [ ] Create web interface for manual category corrections
- [ ] Add support for bulk processing multiple files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.