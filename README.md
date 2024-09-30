# Grocery Shopping Microservices

This repository contains two Flask microservices for grocery shopping: `Product Service` and `Cart Service`.

## Service

### Cart Service

The Cart Service is responsible for managing users' shopping carts. It interacts with the Product Service to retrieve product details. The following endpoints are available:

- `/cart/{user_id}` - Retrieve the current contents of a user's shopping cart.
- `/cart/{user_id}/add/{product_id}` - Add a specified quantity of a product to the user's cart.
- `/cart/{user_id}/remove/{product_id}` - Remove a specified quantity of a product from the user's cart.

**Cart Service URL**:  
[Cart Service on Render](https://cart-service-te5m.onrender.com/cart/1)

### Communication Between Services

The Cart Service uses the following environment variable to communicate with the Product Service:

### Testing the APIs

You can test the endpoints using tools like `curl`, Postman, or your browser.
