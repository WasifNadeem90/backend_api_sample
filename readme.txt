Project README

1. Project Installation Guide:

   To set up and run this FastAPI project, follow the steps below:

   a. Clone the repository:
      ```
      git clone https://github.com/your-username/your-project.git
      cd your-project
      ```
   b. Create and activate a virtual environment (recommended but optional):
      ```
      python -m venv venv
      source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
      ```
   c. Install project dependencies:
      ```
      pip install -r requirements.txt
      ```

2. Start the FastAPI Server:

   To start the FastAPI server, you can use Uvicorn. Replace `main` with the name of your main Python script:

   The server will be running at http://127.0.0.1:8000.

3. Populate the Database with Fake Data:

    To populate the database with fake data, run the `populate_fake_data` script. Replace `populate_fake_data.py` with
    the actual name of your script if it's different:

    This script will insert sample data into your database tables.

4. API Endpoints:

Here are the API endpoints available in the FastAPI application:

- **Root Endpoint**:
  - URL: http://127.0.0.1:8000/
  - Description: Redirects to the documentation (Swagger UI or ReDoc).

- **Create a Product**:
  - HTTP Method: POST
  - URL: http://127.0.0.1:8000/products/
  - Request Body: JSON data to create a product.
  - Response: Details of the created product.

- **Retrieve all Products**:
  - HTTP Method: GET
  - URL: http://127.0.0.1:8000/products/
  - Response: List of all products.

- **Retrieve Product by ID**:
  - HTTP Method: GET
  - URL: http://127.0.0.1:8000/products/{product_id}
  - Path Parameter: product_id (integer)
  - Response: Details of the specified product.

- **Create a Sale**:
  - HTTP Method: POST
  - URL: http://127.0.0.1:8000/sales/
  - Request Body: JSON data to create a sale record.
  - Response: Details of the created sale.

- **Retrieve Sales Data by Date Range**:
  - HTTP Method: GET
  - URL: http://127.0.0.1:8000/sales/
  - Query Parameters: start_date (date), end_date (date)
  - Response: List of sales records within the specified date range.

- **Analyze Revenue for a Specific Interval (daily, weekly, monthly, annual)**:
  - HTTP Method: GET
  - URL: http://127.0.0.1:8000/sales/revenue/
  - Query Parameters: interval (string), start_date (date), end_date (date)
  - Response: Revenue analysis based on the specified interval.

- **Create Inventory**:
  - HTTP Method: POST
  - URL: http://127.0.0.1:8000/inventory/
  - Request Body: JSON data to create an inventory record.
  - Response: Details of the created inventory.

- **Retrieve Current Inventory Status for a Specific Product**:
  - HTTP Method: GET
  - URL: http://127.0.0.1:8000/inventory/{product_id}
  - Path Parameter: product_id (integer)
  - Response: Details of the inventory for the specified product.

- **Update Inventory Levels for a Specific Product**:
  - HTTP Method: PUT
  - URL: http://127.0.0.1:8000/inventory/{product_id}
  - Path Parameter: product_id (integer)
  - Request Body: JSON data to update inventory quantity.
  - Response: Updated details of the inventory.

- **Get Low Stock Alerts**:
  - HTTP Method: GET
  - URL: http://127.0.0.1:8000/inventory/low-stock/
  - Query Parameter: threshold (integer, default is 10)
  - Response: List of products with low stock (quantity below the threshold).

Feel free to explore and test these endpoints using your browser or API client (e.g., Postman). The FastAPI
documentation (Swagger UI or ReDoc) can also be accessed at http://127.0.0.1:8000/docs for interactive API exploration.
