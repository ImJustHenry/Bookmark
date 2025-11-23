#!/usr/bin/env python3
"""
Quick test script to verify everything is working
"""

import sys
import os
sys.path.append('src')

from book_search_service import search_book_by_name, search_book_by_isbn
import json

def test_book_search():
    print("🧪 Quick Test - Book Search")
    print("=" * 40)
    
    # Test 1: Search by book name
    print("\n📚 Test 1: Search by Book Name")
    print("-" * 30)
    result = search_book_by_name("Clean Code")
    
    if result['success']:
        print(f"✅ Found {result['books_found']} books")
        for i, book in enumerate(result['books'][:2], 1):
            print(f"  {i}. {book['book_info']['title']} by {book['book_info']['author']}")
            if book['best_price']:
                print(f"     💰 Best Price: {book['best_price']['price']} at {book['best_price']['retailer']}")
    else:
        print(f"❌ Failed: {result['error']}")
    
    # Test 2: Search by ISBN
    print("\n🔍 Test 2: Search by ISBN")
    print("-" * 30)
    result = search_book_by_isbn("9780134685991")
    
    if result['success']:
        book = result['book_info']
        print(f"✅ Found: {book['title']} by {book['author']}")
        if result['best_price']:
            print(f"   💰 Best Price: {result['best_price']['price']} at {result['best_price']['retailer']}")
    else:
        print(f"❌ Failed: {result['error']}")
    
    print("\n🎉 Test Complete!")

if __name__ == "__main__":
    test_book_search()

