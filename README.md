# Medical Imaging Equipment Order & Business Management System
A web-based **Medical Imaging Equipment Business Management System** developed as a DBMS project for managing the business relationship between a medical imaging equipment company and its hospital clients.

The system allows hospitals/clients to **register, manage their profiles, view available medical imaging equipment, place orders, and track their order status**. On the administrative side, the system provides functionality to **manage equipment, hospitals/clients, orders, invoices, shipments, and basic business reports**.

## Key Features

### Hospital / Client

* User registration and login
* Hospital/client profile management
* View available medical imaging equipment
* Place equipment orders
* View previous and current orders
* Track order status

### Administrator

* Admin login and access
* Manage medical imaging equipment
* Manage hospital/client records
* View and manage orders
* Update order status
* Manage invoice information
* Manage shipment information
* View basic dashboard and business reports

## Main Database Entities

* **User** — account and authentication information
* **Hospital** — hospital/client information
* **Equipment/Machine** — medical imaging equipment details
* **Order** — order-level information
* **OrderItem** — equipment and quantity within an order
* **Invoice** — invoice information associated with orders
* **Shipment** — shipment and delivery information

  **Hospital/Client** → **Register/Login** → **View Equipment** → **Place Order** → **Order Items** → **Admin Processes Order** → **Invoice → Shipment** → **Order Tracking** → **Delivery**

The database uses relationships between these entities to maintain consistency and represent the complete order lifecycle.

## Technology Stack

| * **Backend:**          | Python, Django                                |
| * **API:**              | Django REST Framework                         |
| * **Database:**         | PostgreSQL                                    |
| * **Application Type:** |Web-based business management system           |
| * **API Architecture:** | REST API                                      |
| * **FrontEnd:**         | Nextjs                                        |

## Project's normalization schema

Database model: Relational schema
Normalization level: 3NF (Third Normal Form)

| **Main tables can be represented as:**                                           |
|----------------------------------------------------------------------------------|                                           
| User      | (user_id, username, email, password, ...)                            |
| Hospital  | (hospital_id, user_id, hospital_name, address, ...)                  |
| Equipment | (equipment_id, name, description, price, quantity, ...)              |
| Order     | (order_id, hospital_id, order_date, status, total_amount, ...)       |
| OrderItem | (order_item_id, order_id, equipment_id, quantity, unit_price, ...)   |
| Invoice   | (invoice_id, order_id, invoice_date, amount, ...)                    |
| Shipment  | (shipment_id, order_id, shipment_date, status, ...)                  |

## API Reference

| Endpoint            | Description                      |
| ------------------- | -------------------------------- |
| `/api/accounts/`    | User authentication and accounts |
| `/api/hospitals/`   | Hospital/client management       |
| `/api/machines/`    | Medical equipment management     |
| `/api/orders/`      | Order management                 |
| `/api/order-items/` | Order item management            |
| `/api/invoices/`    | Invoice management               |
| `/api/shipments/`   | Shipment management              |
| `/api/dashboard/`   | Admin dashboard and reports      |

## Project Scope

The project focuses on implementing the **core business and database operations** required for a medical imaging equipment supplier. It is designed as a manageable academic DBMS project rather than a full-scale enterprise logistics platform.

**Hospital/Client Management** — Registration, login, profile management, and maintaining hospital/client records.
**Medical Equipment Management** — Adding, updating, viewing, and managing medical imaging equipment.
**Order Management** — Allowing hospitals/clients to place orders and maintaining order and order-item details.
**Order Tracking** — Allowing clients to view their orders and track their current status.
**Invoice & Shipment Management** — Maintaining invoice and shipment information associated with orders.
**Admin Dashboard & Reports** — Providing administrators with basic information and summaries about clients, equipment, orders, and shipments

## Out of Scope

Advanced features such as:

**Online Payment Processing** — No integrated online payment gateway or transaction processing.
**Real-Time Shipment Tracking** — No GPS-based or real-time delivery tracking.
**Advanced Role & Permission Management** — No complex multi-level roles or enterprise permission system.
**Advanced Analytics & Notifications** — No advanced predictive analytics, automated notifications, or AI-based features.

## Project Objective

The main objective is to develop a structured database-driven application that demonstrates how a medical imaging equipment business can manage its clients, equipment, orders, invoices, and shipments through a centralized system.

## Contributors:
* **Mahnoor Khan**
* **Ayesha Abid**


