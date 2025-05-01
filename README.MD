# Dummy API Website

This project is a Flask-based web application that uses JWT authentication and Flask-Login to manage user sessions. It provides functionality to display and interact with a JSON representation of products stored in a database.

## Features

- **JWT Authentication**: Secure token-based authentication for API access.
- **Flask-Login Integration**: Manages user sessions and ensures only authenticated users can access protected routes.
- **Product Display**: Fetches and displays product data from the database in JSON format.
- **Search and Sorting**: Allows users to search for products and sort them based on criteria like price.
- **Pagination**: Supports paginated views of product data for better user experience.

## Routes and Functionality

### Public Routes:
- `/home`: Displays the homepage. Redirects unauthenticated users to the login page.

### Protected Routes:
- `/product/price`: Fetches and sorts product data by price (ascending or descending).
- `/product/all`: Displays all products or paginated results based on the `page` parameter.
- `/product/search_<attribute>=<value>`: Searches for products based on attributes like `title`, `sku`, or `category`.
- `/product/s=<search_query>`: Performs a generic search using the provided query.

## Setup and Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/Toby1219/dummyyApi-website.git
   cd dummyyApi-website
   ```

2. **Create a virtual environment**:
   ```
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   - Ensure the database is configured and populated with product data.

5. **Add you .env file**:
   - view config.py in order to create.env file 

6. **Run the application**:
   ```
   flask run
   ```

7. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

## Requirements

- Python 3.8+
- Flask
- Flask-Login
- Flask-JWT
- or just install 
```
pip install -r requirements.txt
```

## License

This project is private and not licensed for public use.

---