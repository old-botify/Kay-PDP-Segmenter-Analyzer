import pandas as pd
import re
from typing import Dict, List, Tuple
import numpy as np
from collections import Counter

class ProductCategorizer:
    def __init__(self):
        self.category_patterns = {
            'Rings': {
                'patterns': [
                    r'ring(?!\s+tone)',
                    r'band(?!\s+watch)',
                    r'engagement',
                    r'wedding band'
                ],
                'subcategories': {
                    'Engagement': {
                        'patterns': [
                            r'engagement',
                            r'bridal\s+set',
                            r'solitaire.*diamond',
                            r'halo.*engagement',
                            r'princess.*cut.*engagement'
                        ],
                        'weight': 5
                    },
                    'Fashion': {
                        'patterns': [
                            r'fashion',
                            r'statement',
                            r'birthstone',
                            r'quinceanera',
                            r'gemstone',
                            r'stackable'
                        ],
                        'weight': 3
                    },
                    'Promise': {
                        'patterns': [
                            r'promise',
                            r'commitment',
                            r'couples',
                            r'together'
                        ],
                        'weight': 4
                    },
                    'Anniversary': {
                        'patterns': [
                            r'anniversary',
                            r'eternity',
                            r'years together',
                            r'celebration'
                        ],
                        'weight': 4
                    },
                    'Wedding Bands': {
                        'patterns': [
                            r'wedding\s+band',
                            r'matrimony',
                            r'bridal\s+band',
                            r'mens\s+band',
                            r'wedding\s+ring'
                        ],
                        'weight': 5
                    }
                }
            },
            'Necklaces': {
                'patterns': [
                    r'necklace',
                    r'pendant',
                    r'chain',
                    r'choker',
                    r'collar'
                ],
                'subcategories': {
                    'Chains': {
                        'patterns': [
                            r'chain\s+necklace',
                            r'rope\s+chain',
                            r'cable\s+chain',
                            r'figaro\s+chain',
                            r'box\s+chain'
                        ],
                        'weight': 4
                    },
                    'Fashion': {
                        'patterns': [
                            r'fashion',
                            r'statement',
                            r'pendant',
                            r'gemstone',
                            r'birthstone'
                        ],
                        'weight': 3
                    }
                }
            },
            'Earrings': {
                'patterns': [
                    r'earring',
                    r'stud',
                    r'hoop',
                    r'ear'
                ],
                'subcategories': {
                    'Hoops': {
                        'patterns': [
                            r'hoop',
                            r'huggie',
                            r'endless'
                        ],
                        'weight': 4
                    },
                    'Drop': {
                        'patterns': [
                            r'drop',
                            r'dangle',
                            r'chandelier',
                            r'tassel'
                        ],
                        'weight': 4
                    },
                    'Stud': {
                        'patterns': [
                            r'stud',
                            r'solitaire\s+earring'
                        ],
                        'weight': 4
                    },
                    'Solitaire': {
                        'patterns': [
                            r'solitaire\s+earring',
                            r'single\s+stone'
                        ],
                        'weight': 4
                    }
                }
            },
            'Bracelets': {
                'patterns': [
                    r'bracelet',
                    r'bangle',
                    r'cuff'
                ],
                'subcategories': {
                    'Chains': {
                        'patterns': [
                            r'chain\s+bracelet',
                            r'link\s+bracelet',
                            r'tennis\s+bracelet',
                            r'rope\s+bracelet'
                        ],
                        'weight': 4
                    },
                    'Fashion': {
                        'patterns': [
                            r'fashion',
                            r'bangle',
                            r'cuff',
                            r'gemstone',
                            r'wrap'
                        ],
                        'weight': 3
                    }
                }
            },
            'Watches': {
                'patterns': [
                    r'watch(?!.+band)',
                    r'timepiece',
                    r'chronograph'
                ]
            },
            'Personalized': {
                'patterns': [
                    r'personalized',
                    r'custom',
                    r'engrav',
                    r'name.*necklace',
                    r'monogram',
                    r'initial'
                ]
            },
            'Coordinates': {
                'patterns': [
                    r'coordinate',
                    r'latitude',
                    r'longitude',
                    r'location\s+jewelry'
                ]
            },
            'Sets': {
                'patterns': [
                    r'set',
                    r'matching',
                    r'collection',
                    r'suite',
                    r'box\s+set'
                ]
            },
            'Previously Owned Jewelry': {
                'patterns': [
                    r'previously\s+owned',
                    r'pre[-\s]owned',
                    r'estate\s+jewelry'
                ]
            },
            'Previously Owned Watches': {
                'patterns': [
                    r'previously\s+owned.*watch',
                    r'pre[-\s]owned.*watch',
                    r'estate.*watch'
                ]
            },
            'Charms': {
                'patterns': [
                    r'charm(?!\s+bracelet)',
                    r'dangle',
                    r'add[-\s]on'
                ]
            }
        }

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for processing."""
        if pd.isna(text) or not isinstance(text, str):
            return ""
            
        # Handle invalid values
        if text.strip() in ['#NAME?', 'nan', 'None', 'null']:
            return ""
            
        # Handle URL encodings and special characters
        replacements = {
            '%25': '%',
            '%E2%80%9D': '"',
            '%C3%B1': 'n',
            '√±': 'n',
            '‚Äù': '"',
            '%20': ' ',
            '\u2019': "'",
            '\u201c': '"',
            '\u201d': '"'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        # Remove remaining URL encodings
        text = re.sub(r'%[0-9A-Fa-f]{2}', ' ', text)
        
        # Remove special characters but keep essential punctuation
        text = re.sub(r'[^\w\s\-&,.]', ' ', text)
        
        # Normalize spaces
        text = ' '.join(text.split())
        
        return text.lower()

    def _find_matching_keywords(self, text: str) -> List[Tuple[str, str, int]]:
        """Find all matching keywords in text with their categories and positions."""
        text = text.lower()
        matches = []
        
        # Define keywords for each category
        keywords = {
            'ring': 'Rings',
            'necklace': 'Necklaces',
            'pendant': 'Necklaces',
            'chain': 'Necklaces',
            'bracelet': 'Bracelets',
            'bangle': 'Bracelets',
            'earring': 'Earrings',
            'stud': 'Earrings',
            'watch': 'Watches'
        }
        
        for keyword, category in keywords.items():
            # Special handling for 'ring' to avoid matching within 'earring'
            if keyword == 'ring':
                if 'ring' in text and 'earring' not in text:
                    pos = text.find('ring')
                    if pos != -1:
                        matches.append((keyword, category, pos))
            else:
                pos = text.find(keyword)
                if pos != -1:
                    matches.append((keyword, category, pos))
                    
        return matches

    def categorize_product(self, url: str, title: str, breadcrumb2: any, breadcrumb3: any) -> Tuple[str, str]:
        """Categorize a product using multiple methods."""
        # Clean all inputs
        url = self._clean_text(url)
        title = self._clean_text(title)
        breadcrumb2 = self._clean_text(breadcrumb2)
        breadcrumb3 = self._clean_text(breadcrumb3)
        
        # First check title for direct matches
        matches = self._find_matching_keywords(title)
        if matches:
            # Sort by position (earlier matches get priority)
            matches.sort(key=lambda x: x[2])
            main_category = matches[0][1]
            
            # Determine subcategory
            if main_category == 'Necklaces':
                if any(x[0] == 'chain' for x in matches):
                    return main_category, 'Chains'
                return main_category, 'Fashion'
            elif main_category == 'Earrings':
                if 'hoop' in title:
                    return main_category, 'Hoops'
                elif 'stud' in title:
                    return main_category, 'Stud'
                elif 'drop' in title or 'dangle' in title:
                    return main_category, 'Drop'
                return main_category, 'Fashion'
            
            return main_category, 'Fashion'
        
        # Combine text for additional analysis
        combined_text = f"{title} {breadcrumb2} {breadcrumb3}"
        
        # Check for "Previously Owned"
        if 'previously owned' in combined_text:
            if 'watch' in combined_text:
                return "Previously Owned Watches", "General"
            return "Previously Owned Jewelry", "General"

        # Pattern matching for categories
        best_main_category = None
        best_main_score = 0
        best_subcategory = None
        best_sub_score = 0

        for main_cat, main_data in self.category_patterns.items():
            # Skip previously owned categories as they're handled above
            if main_cat in ['Previously Owned Jewelry', 'Previously Owned Watches']:
                continue
                
            patterns = main_data.get('patterns', [])
            score = sum(len(re.findall(pattern, combined_text)) for pattern in patterns)
            
            if score > best_main_score:
                best_main_score = score
                best_main_category = main_cat
                
                # Check subcategories if available
                if isinstance(main_data, dict) and 'subcategories' in main_data:
                    for sub_cat, sub_data in main_data['subcategories'].items():
                        sub_score = sum(len(re.findall(pattern, combined_text)) * sub_data['weight'] 
                                      for pattern in sub_data['patterns'])
                        if sub_score > best_sub_score:
                            best_sub_score = sub_score
                            best_subcategory = sub_cat

        if best_main_score == 0:
            return "Uncategorized", "Uncategorized"
            
        return best_main_category, best_subcategory or "Fashion"

    def process_csv(self, input_file: str, output_file: str):
        """Process the input CSV file and add categorization columns."""
        try:
            # First, check for 'sep=' line
            with open(input_file, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                
            if first_line.startswith('sep='):
                # If 'sep=' line exists, skip it when reading with pandas
                df = pd.read_csv(input_file, skiprows=1, dtype=str)
            else:
                # If no 'sep=' line, read normally
                df = pd.read_csv(input_file, dtype=str)
            
            df['Main_Category'] = ''
            df['Subcategory'] = ''
            
            for idx, row in df.iterrows():
                main_cat, sub_cat = self.categorize_product(
                    row.get('Full URL', ''),
                    row.get('Title', ''),
                    row.get('Breadcrumb Level 2', ''),
                    row.get('Breadcrumb Level 3', '')
                )
                df.at[idx, 'Main_Category'] = main_cat
                df.at[idx, 'Subcategory'] = sub_cat
            
            # When writing the output, preserve the 'sep=' line if it existed
            if first_line.startswith('sep='):
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(first_line + '\n')
                    df.to_csv(f, index=False)
            else:
                df.to_csv(output_file, index=False)
            
            print("\nCategory Distribution:")
            print(df['Main_Category'].value_counts())
            print("\nSubcategory Distribution:")
            print(df['Subcategory'].value_counts())
            
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            raise

def main():
    categorizer = ProductCategorizer()
    input_file = 'input.csv'  # Update with your input file name
    output_file = 'categorized_products.csv'
    
    try:
        categorizer.process_csv(input_file, output_file)
        print(f"\nProcessing complete. Results saved to {output_file}")
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()