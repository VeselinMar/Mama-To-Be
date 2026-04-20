# Mama-To-Be

A comprehensive web platform designed to support expectant mothers and parents throughout their pregnancy journey. Built as a Django web application, Mama-To-Be provides valuable resources through community-driven content and pregnancy-safe nutrition guidance.

## About

Mama-To-Be started as a final project for a Python Web Development curriculum. With my wife expecting at the time, I saw an opportunity to create something meaningful that could bring real value to expectant mothers and parents-to-be. What began as an educational project has evolved into a platform designed to support families during one of life's most exciting journeys.

**Live**: *https://www.mom-to-be.at/de/*

## Core Features

### Articles
The heart of community knowledge sharing - a user-generated content platform where expectant mothers share their experiences:

- **Create & Edit Articles**: Logged-in users can write and share their pregnancy experiences, tips, and advice
- **Category Organization**: Articles organized by pregnancy-related categories for easy browsing
- **Multi-language Support**: Full internationalization - articles can be translated and viewed in multiple languages
- **Search Functionality**: Powerful full-text search across article titles and content to find relevant information
- **Recent Articles Feed**: Browse the latest community contributions
- **Category-Specific Views**: Filter articles by specific topics and categories
- **Author Profiles**: Each article is linked to its author's profile
- **Publication System**: Draft and publish workflow for article management
- **Slug-based URLs**: SEO-friendly article URLs
- **Pagination**: Clean browsing with 9 articles per page

### Food & Recipes
Essential guidance for healthy pregnancy eating with community-contributed recipes:

- **Recipe Creation & Editing**: Logged-in users can create and share pregnancy-safe recipes
- **Dynamic Ingredient Management**: 
  - Add multiple ingredients with quantities and units
  - Autocomplete ingredient search (top 10 matches)
  - Create new ingredients on-the-fly with nutritional data
  - Support for various measurement units (grams, cups, tablespoons, etc.)
- **Nutritional Tracking**: Store protein, carbs, and fat content for ingredients
- **Recipe Details**:
  - Multi-step cooking instructions
  - Ingredient notes and substitutions
  - Preparation and cooking time
  - Servings information
- **Recipe Discovery**:
  - Browse all community recipes
  - Paginated recipe list (9 per page)
  - Author attribution and profiles
  - Multi-language recipe support
- **JSON-based Ingredient System**: Efficient storage and retrieval of recipe components
- **Author Control**: Only recipe creators can edit their recipes

###  User System
- **User Authentication**: Secure login and registration system
- **Personal Profiles**: Custom user profiles with usernames and profile pictures
- **Author Attribution**: Track which community member wrote each article or recipe
- **Access Control**: Content editing restricted to original authors
- **WebP Image Processing**: Optimized image handling for profile pictures

###  Platform Features
- **Multi-language Support**: Complete internationalization using Django Parler
- **Responsive Design**: Seamless experience across desktop and mobile devices
- **PostgreSQL Full-Text Search**: Fast and accurate search functionality
- **Cloud Media Storage**: User-uploaded images stored in Azure Blob Storage
- **CDN Delivery**: Content delivered through Firebase CDN for optimal performance
- **Language Switching**: Automatic content translation based on user language preference

##  Technology Stack

### Backend
- **Python** - Django 4.x
- **Django Parler** - Multi-language content management
- **PostgreSQL** - Relational database with full-text search capabilities
- **Pillow** - Image processing for WebP conversion
- **Gunicorn** - WSGI HTTP Server

### Frontend
- **HTML**
- **CSS**
- **JavaScript**
- **AJAX** - Dynamic ingredient autocomplete and creation
- **JSON** - Client-server data exchange for recipes

### Cloud Infrastructure & DevOps
- **Render** - Application hosting platform
- **PostgreSQL on Render** - Managed database service
- **Azure Blob Storage** - User-uploaded media files (profile pictures, article images)
- **Firebase CDN** - Content delivery network for static assets
- **Docker** & **Docker Compose** - Containerization for local development
- **Nginx** - Web server and reverse proxy
- **GitHub Actions** - CI/CD pipeline

### Database
- **PostgreSQL 12+** with:
  - Full-text search (SearchVector)
  - JSON field support
  - Relational integrity
  - Optimized queries with `select_related` and `prefetch_related`


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this software, even for commercial purposes, as long as you include the original copyright notice.