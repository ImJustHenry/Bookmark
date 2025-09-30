# Project Title

## Bookmark!: A Full Stack Web Application for Affordable Textbook Shopping

Investigators:
Mehul Antony — [mantony2@slu.edu](mailto:mantony2@slu.edu)
Alexander Myers — [amyersXX@slu.edu](mailto:amyersXX@slu.edu)
James Mueller — [jmuellerXX@slu.edu](mailto:jmuellerXX@slu.edu)
Henry Wang — [hwang59@slu.edu](mailto:hwang59@slu.edu)
Revateesa Dammalapati - [revateesa.dammalapati@slu.edu]
# Project Statement

One-sentence summary:
We will design and implement a full stack web application that streamlines the process of finding affordable college textbooks by aggregating prices across multiple online retailers.

Expanded description:
College students often face difficulties when purchasing textbooks due to high costs, numerous editions, and varying retailer offerings. Our application, **Bookmark!**, addresses these challenges by creating a centralized platform where students can search textbooks by title, author, ISBN, or edition number. The platform will fetch and compare prices from multiple major retailers, display availability and condition (new, used, etc.), and provide direct purchase links. By consolidating information, we aim to reduce the time, cost, and stress students face in acquiring their textbooks.

# Methods

Frontend: HTML, CSS, Bootstrap, Jinja templating via Flask
Backend: Flask (Python) with API fetching and data rendering
Database: PostgreSQL using SQLAlchemy ORM in Flask
APIs: Google Books API, eBay API (others if accessible)
Additional Tools: Figma for prototyping

# Use Cases

* Help students save money on textbooks
* Help students quickly locate correct editions
* Help sellers identify appropriate price ranges

# Users

Primary users: College students searching for textbooks
Secondary users: Sellers or researchers analyzing textbook pricing trends

# Architecture

* **Frontend**: HTML, CSS, Bootstrap UI, Flask Jinja templates
* **Backend**: Python Flask server fetching data from APIs
* **Database**: PostgreSQL for storing queries and caching book data
* **APIs**: Google Books + eBay for price and edition data

# Team Skillset

Alex: HTML, C++, Python, browser knowledge
Mehul: HTML, Python, Java, Figma, Project Management
Henry: HTML, CSS, MySQL, PHP, Python
James: HTML, Java, Python, C++, new to SQL

# Challenges and Risks

* Limited access to some APIs (Amazon, Chegg, AbeBooks, Walmart)
* Security concerns with fetching and displaying external data
* Learning curve for integrating multiple APIs and ORMs
* Potential issues with mimicking browser behavior for scraping or API calls

# Plan and Schedule

Goal 1: Extract relevant data from web pages and APIs
Goal 2: Front-end prototyping in Figma
Goal 3: Build basic HTML, CSS, Bootstrap components
Goal 4: Establish frontend-backend communication via Flask
Goal 5: Implement title → ISBN conversion and search handling
Goal 6: Add AI-generated textbook descriptions (optional enhancement)

# Resources Needed

## Software:

Flask (Python framework)
PostgreSQL (database)
Bootstrap (UI)
Figma (prototyping)
Google Books + eBay APIs

## Hardware:

Standard laptops for development and testing

## Other:

GitHub (version control)
Discord (team coordination)

# Architectural Diagram

(Placeholder: User → Web App (Flask frontend/backend) → Database + APIs)
