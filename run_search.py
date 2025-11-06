#!/usr/bin/env python3
"""
Simple script to run book searches directly
"""

import sys
import os
sys.path.append('src')

from book_search_service import search_book_by_name, search_book_by_isbn
import json

def main():
    print("🚀 Book Search Application")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Search by book name")
        print("2. Search by ISBN")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            book_name = input("Enter book name: ").strip()
            if book_name:
                print(f"\n🔍 Searching for: {book_name}")
                print("⏳ Please wait...")
                
                result = search_book_by_name(book_name)
                
                if result['success']:
                    print(f"\n✅ Found {result['books_found']} books:")
                    print("-" * 40)
                    
                    for i, book_data in enumerate(result['books'][:3], 1):
                        book = book_data['book_info']
                        print(f"\n{i}. {book['title']}")
                        print(f"   Author: {book['author']}")
                        print(f"   ISBN: {book['isbn']}")
                        
                        if book_data['best_price']:
                            best = book_data['best_price']
                            print(f"   💰 Best Price: {best['price']} at {best['retailer']}")
                        else:
                            print(f"   💰 No prices found")
                else:
                    print(f"❌ Search failed: {result['error']}")
            else:
                print("❌ Please enter a book name")
                
        elif choice == "2":
            isbn = input("Enter ISBN: ").strip()
            if isbn:
                print(f"\n🔍 Searching for ISBN: {isbn}")
                print("⏳ Please wait...")
                
                result = search_book_by_isbn(isbn)
                
                if result['success']:
                    book = result['book_info']
                    print(f"\n✅ Found: {book['title']}")
                    print(f"   Author: {book['author']}")
                    print(f"   ISBN: {book['isbn']}")
                    
                    if result['best_price']:
                        best = result['best_price']
                        print(f"   💰 Best Price: {best['price']} at {best['retailer']}")
                    else:
                        print(f"   💰 No prices found")
                else:
                    print(f"❌ Search failed: {result['error']}")
            else:
                print("❌ Please enter an ISBN")
                
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
