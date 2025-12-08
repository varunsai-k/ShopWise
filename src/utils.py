import sqlite3
from dotenv import load_dotenv
import os

DB_PATH=os.getenv("DB_PATH","ecommerce.db")
DB_PATH=f"{os.getcwd()}/{DB_PATH}"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check if tables already exist
    cur.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='orders';
    """)
    table_exists = cur.fetchone()

    if table_exists:
        print("Database already initialized. Skipping setup.")
        return

    print("Initializing database...")

    # Run your existing script as-is
    cur.executescript(


        """
        CREATE TABLE users (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT
        );

        CREATE TABLE products (
        product_id TEXT PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL,
        stock INTEGER,
        description TEXT
        );

        CREATE TABLE cart (
        cart_id TEXT PRIMARY KEY,
        user_id TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
        );

        CREATE TABLE cart_items (
        item_id TEXT PRIMARY KEY,
        cart_id TEXT,
        product_id TEXT,
        quantity INTEGER,
        FOREIGN KEY(cart_id) REFERENCES cart(cart_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
        );

        CREATE TABLE orders (
        order_id TEXT PRIMARY KEY,
        user_id TEXT,
        order_date TEXT,
        total_amount REAL,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
        );

        CREATE TABLE order_items (
        item_id TEXT PRIMARY KEY,
        order_id TEXT,
        product_id TEXT,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
        );

        CREATE TABLE shipping (
        shipment_id TEXT PRIMARY KEY,
        order_id TEXT,
        shipped_date TEXT,
        delivery_date TEXT,
        status TEXT,
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
        );

        CREATE TABLE returns (
        return_id TEXT PRIMARY KEY,
        order_id TEXT,
        product_id TEXT,
        return_date TEXT,
        reason TEXT,
        status TEXT,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
        );

        CREATE TABLE refunds (
        refund_id TEXT PRIMARY KEY,
        return_id TEXT,
        refund_amount REAL,
        refund_date TEXT,
        status TEXT,
        FOREIGN KEY(return_id) REFERENCES returns(return_id)
        );

        CREATE TABLE return_pickups (
        pickup_id TEXT PRIMARY KEY,
        return_id TEXT,
        pickup_date TEXT,
        status TEXT,
        FOREIGN KEY(return_id) REFERENCES returns(return_id)
        );

        CREATE TABLE product_details (
        product_id TEXT PRIMARY KEY,
        brand TEXT,
        model TEXT,
        specifications TEXT,
        FOREIGN KEY(product_id) REFERENCES products(product_id)
        );

        CREATE TABLE product_qa (
        qa_id TEXT PRIMARY KEY,
        product_id TEXT,
        question TEXT,
        answer TEXT,
        FOREIGN KEY(product_id) REFERENCES products(product_id)
        );

        INSERT INTO users VALUES
        ('USR-2025-001','Aakash Sharma','aakash@example.com','9876543210'),
        ('USR-2025-002','Priya Reddy','priya@example.com','9876543211'),
        ('USR-2025-003','Rahul Verma','rahul@example.com','9876543212'),
        ('USR-2025-004','Sneha Kapoor','sneha@example.com','9876543213'),
        ('USR-2025-005','Manoj Iyer','manoj@example.com','9876543214'),
        ('USR-2025-006','Ananya Singh','ananya@example.com','9876543215'),
        ('USR-2025-007','Vikram Rao','vikram@example.com','9876543216'),
        ('USR-2025-008','Rohit Gupta','rohit@example.com','9876543217'),
        ('USR-2025-009','Sanya Mehta','sanya@example.com','9876543218'),
        ('USR-2025-010','Tarun Nair','tarun@example.com','9876543219'),
        ('USR-2025-011','Deepika Jain','deepika@example.com','9876543220'),
        ('USR-2025-012','Harish Yadav','harish@example.com','9876543221'),
        ('USR-2025-013','Meera Joshi','meera@example.com','9876543222'),
        ('USR-2025-014','Arjun Patel','arjun@example.com','9876543223'),
        ('USR-2025-015','Lavanya Rao','lavanya@example.com','9876543224');

        INSERT INTO products VALUES
        ('PRD-2025-001','Apple iPhone 15 Pro Max','Electronics',129999,40,'Apple flagship phone with A17 chip'),
        ('PRD-2025-002','Samsung Galaxy S24 Ultra','Electronics',118999,32,'Premium Samsung smartphone'),
        ('PRD-2025-003','Sony WH-1000XM5 Headphones','Audio',29999,58,'Noise-cancelling wireless headset'),
        ('PRD-2025-004','Dell XPS 13 Plus Laptop','Computers',154999,20,'OLED display lightweight laptop'),
        ('PRD-2025-005','Nike Air Max 270','Footwear',12999,95,'Running shoes with air cushion'),
        ('PRD-2025-006','Adidas Men’s Hoodie','Apparel',3499,70,'Comfortable cotton hoodie'),
        ('PRD-2025-007','HP LaserJet Pro M404dn','Printers',24999,25,'Laser printer for office'),
        ('PRD-2025-008','Apple Watch Series 10','Wearables',45999,50,'Smartwatch with fitness sensor'),
        ('PRD-2025-009','Lenovo ThinkPad X1 Carbon','Computers',167999,18,'Premium ultrabook laptop'),
        ('PRD-2025-010','Logitech MX Master 4 Mouse','Accessories',9999,75,'Ergonomic wireless mouse'),
        ('PRD-2025-011','Boat Airdopes 200','Audio',1999,220,'TWS earbuds with long battery'),
        ('PRD-2025-012','Canon EOS R6 Mark II','Cameras',249999,12,'Full-frame mirrorless camera'),
        ('PRD-2025-013','Samsung 55-inch QLED TV','Home Appliances',79999,30,'4K HDR smart TV'),
        ('PRD-2025-014','LG 1.5 Ton Inverter AC','Home Appliances',42999,22,'Energy-saving air conditioner'),
        ('PRD-2025-015','Prestige Nonstick Cookware Set','Kitchen',3499,110,'5-piece premium cookware set');


        INSERT INTO cart VALUES
        ('CRT-2025-001','USR-2025-001','2025-11-01 10:15:00'),
        ('CRT-2025-002','USR-2025-001','2025-11-05 11:00:00'),
        ('CRT-2025-003','USR-2025-002','2025-11-02 12:20:00'),
        ('CRT-2025-004','USR-2025-003','2025-11-03 13:25:00'),
        ('CRT-2025-005','USR-2025-004','2025-11-04 09:05:00'),
        ('CRT-2025-006','USR-2025-005','2025-11-05 14:45:00'),
        ('CRT-2025-007','USR-2025-006','2025-11-06 15:10:00'),
        ('CRT-2025-008','USR-2025-007','2025-11-07 16:30:00'),
        ('CRT-2025-009','USR-2025-008','2025-11-08 13:50:00'),
        ('CRT-2025-010','USR-2025-009','2025-11-09 17:25:00'),
        ('CRT-2025-011','USR-2025-010','2025-11-10 08:40:00'),
        ('CRT-2025-012','USR-2025-011','2025-11-11 12:15:00'),
        ('CRT-2025-013','USR-2025-012','2025-11-12 14:50:00'),
        ('CRT-2025-014','USR-2025-013','2025-11-13 09:55:00'),
        ('CRT-2025-015','USR-2025-014','2025-11-14 10:10:00'),
        ('CRT-2025-016','USR-2025-015','2025-11-15 11:30:00');


        INSERT INTO cart_items VALUES
        ('CIT-2025-001','CRT-2025-001','PRD-2025-001',1),
        ('CIT-2025-002','CRT-2025-001','PRD-2025-005',2),
        ('CIT-2025-003','CRT-2025-002','PRD-2025-003',1),
        ('CIT-2025-004','CRT-2025-002','PRD-2025-008',1),
        ('CIT-2025-005','CRT-2025-003','PRD-2025-002',1),
        ('CIT-2025-006','CRT-2025-004','PRD-2025-004',1),
        ('CIT-2025-007','CRT-2025-005','PRD-2025-006',3),
        ('CIT-2025-008','CRT-2025-006','PRD-2025-007',1),
        ('CIT-2025-009','CRT-2025-007','PRD-2025-010',2),
        ('CIT-2025-010','CRT-2025-008','PRD-2025-011',2),
        ('CIT-2025-011','CRT-2025-009','PRD-2025-009',1),
        ('CIT-2025-012','CRT-2025-010','PRD-2025-012',1),
        ('CIT-2025-013','CRT-2025-011','PRD-2025-013',1),
        ('CIT-2025-014','CRT-2025-012','PRD-2025-014',1),
        ('CIT-2025-015','CRT-2025-013','PRD-2025-015',1),
        ('CIT-2025-016','CRT-2025-014','PRD-2025-001',1),
        ('CIT-2025-017','CRT-2025-015','PRD-2025-005',1),
        ('CIT-2025-018','CRT-2025-016','PRD-2025-008',1),
        ('CIT-2025-019','CRT-2025-016','PRD-2025-011',1),
        ('CIT-2025-020','CRT-2025-016','PRD-2025-015',2);

        INSERT INTO orders VALUES
        ('ORD-2025-001','USR-2025-001','2025-11-05 10:20:00',129999,'Processing'),
        ('ORD-2025-002','USR-2025-001','2025-11-10 12:15:00',45999,'Delivered'),
        ('ORD-2025-003','USR-2025-002','2025-11-07 15:45:00',29999,'Shipped'),
        ('ORD-2025-004','USR-2025-003','2025-11-08 09:30:00',154999,'Processing'),
        ('ORD-2025-005','USR-2025-004','2025-11-09 14:50:00',154998,'Delivered'),
        ('ORD-2025-006','USR-2025-005','2025-11-10 11:20:00',10497,'Delivered'),
        ('ORD-2025-007','USR-2025-006','2025-11-11 16:05:00',118999,'Shipped'),
        ('ORD-2025-008','USR-2025-006','2025-11-12 13:35:00',19998,'Processing'),
        ('ORD-2025-009','USR-2025-007','2025-11-13 17:10:00',24999,'Delivered'),
        ('ORD-2025-010','USR-2025-008','2025-11-14 08:40:00',249999,'Processing'),
        ('ORD-2025-011','USR-2025-008','2025-11-15 12:50:00',167999,'Shipped'),
        ('ORD-2025-012','USR-2025-009','2025-11-16 14:30:00',79999,'Delivered'),
        ('ORD-2025-013','USR-2025-010','2025-11-17 09:15:00',3998,'Delivered'),
        ('ORD-2025-014','USR-2025-011','2025-11-18 10:45:00',42999,'Processing'),
        ('ORD-2025-015','USR-2025-012','2025-11-19 11:30:00',3499,'Delivered'),
        ('ORD-2025-016','USR-2025-013','2025-11-20 09:00:00',12999,'Delivered'),
        ('ORD-2025-017','USR-2025-014','2025-11-21 10:25:00',45999,'Processing'),
        ('ORD-2025-018','USR-2025-015','2025-11-22 14:15:00',1999,'Delivered'),
        ('ORD-2025-019','USR-2025-002','2025-11-23 12:10:00',118999,'Shipped'),
        ('ORD-2025-020','USR-2025-003','2025-11-24 16:00:00',24999,'Processing');

        INSERT INTO order_items VALUES
        ('OIT-2025-001','ORD-2025-001','PRD-2025-001',1,129999),
        ('OIT-2025-002','ORD-2025-002','PRD-2025-008',1,45999),
        ('OIT-2025-003','ORD-2025-003','PRD-2025-003',1,29999),
        ('OIT-2025-004','ORD-2025-004','PRD-2025-004',1,154999),
        ('OIT-2025-005','ORD-2025-005','PRD-2025-004',1,154998),
        ('OIT-2025-006','ORD-2025-006','PRD-2025-006',3,3499),
        ('OIT-2025-007','ORD-2025-007','PRD-2025-002',1,118999),
        ('OIT-2025-008','ORD-2025-008','PRD-2025-010',2,9999),
        ('OIT-2025-009','ORD-2025-009','PRD-2025-007',1,24999),
        ('OIT-2025-010','ORD-2025-010','PRD-2025-012',1,249999),
        ('OIT-2025-011','ORD-2025-011','PRD-2025-009',1,167999),
        ('OIT-2025-012','ORD-2025-012','PRD-2025-013',1,79999),
        ('OIT-2025-013','ORD-2025-013','PRD-2025-011',2,1999),
        ('OIT-2025-014','ORD-2025-014','PRD-2025-014',1,42999),
        ('OIT-2025-015','ORD-2025-015','PRD-2025-015',1,3499),
        ('OIT-2025-016','ORD-2025-016','PRD-2025-005',1,12999),
        ('OIT-2025-017','ORD-2025-017','PRD-2025-008',1,45999),
        ('OIT-2025-018','ORD-2025-018','PRD-2025-011',1,1999),
        ('OIT-2025-019','ORD-2025-019','PRD-2025-002',1,118999),
        ('OIT-2025-020','ORD-2025-020','PRD-2025-007',1,24999);

        INSERT INTO shipping VALUES
        ('SHP-2025-001','ORD-2025-001','2025-11-06','2025-11-10','In Transit'),
        ('SHP-2025-002','ORD-2025-002','2025-11-11','2025-11-15','Delivered'),
        ('SHP-2025-003','ORD-2025-003','2025-11-08','2025-11-12','Delivered'),
        ('SHP-2025-004','ORD-2025-004','2025-11-09','2025-11-14','In Transit'),
        ('SHP-2025-005','ORD-2025-005','2025-11-10','2025-11-16','Delivered'),
        ('SHP-2025-006','ORD-2025-006','2025-11-11','2025-11-13','Delivered'),
        ('SHP-2025-007','ORD-2025-007','2025-11-12','2025-11-18','Shipped'),
        ('SHP-2025-008','ORD-2025-008','2025-11-13','2025-11-19','Processing'),
        ('SHP-2025-009','ORD-2025-009','2025-11-14','2025-11-20','Delivered'),
        ('SHP-2025-010','ORD-2025-010','2025-11-15','2025-11-21','In Transit'),
        ('SHP-2025-011','ORD-2025-011','2025-11-16','2025-11-22','Shipped'),
        ('SHP-2025-012','ORD-2025-012','2025-11-17','2025-11-23','Delivered'),
        ('SHP-2025-013','ORD-2025-013','2025-11-18','2025-11-24','Delivered'),
        ('SHP-2025-014','ORD-2025-014','2025-11-19','2025-11-25','In Transit'),
        ('SHP-2025-015','ORD-2025-015','2025-11-20','2025-11-26','Delivered'),
        ('SHP-2025-016','ORD-2025-016','2025-11-21','2025-11-26','Delivered'),
        ('SHP-2025-017','ORD-2025-017','2025-11-22','2025-11-27','Processing'),
        ('SHP-2025-018','ORD-2025-018','2025-11-23','2025-11-28','Delivered'),
        ('SHP-2025-019','ORD-2025-019','2025-11-24','2025-11-29','Shipped'),
        ('SHP-2025-020','ORD-2025-020','2025-11-25','2025-11-30','Processing');

        INSERT INTO returns VALUES
        ('RET-2025-001','ORD-2025-002','PRD-2025-008','2025-11-16','Not satisfied','Approved'),
        ('RET-2025-002','ORD-2025-006','PRD-2025-006','2025-11-14','Wrong size','Processed'),
        ('RET-2025-003','ORD-2025-007','PRD-2025-002','2025-11-18','Defective item','Approved'),
        ('RET-2025-004','ORD-2025-009','PRD-2025-007','2025-11-20','Damaged packaging','Processed'),
        ('RET-2025-005','ORD-2025-010','PRD-2025-012','2025-11-22','Not as described','Approved'),
        ('RET-2025-006','ORD-2025-011','PRD-2025-009','2025-11-23','Wrong color','Processed'),
        ('RET-2025-007','ORD-2025-012','PRD-2025-013','2025-11-24','Defective item','Approved'),
        ('RET-2025-008','ORD-2025-014','PRD-2025-014','2025-11-25','Not cooling properly','Processed'),
        ('RET-2025-009','ORD-2025-001','PRD-2025-001','2025-11-10','Scratched screen','Approved'),
        ('RET-2025-010','ORD-2025-003','PRD-2025-003','2025-11-12','Uncomfortable fit','Processed'),
        ('RET-2025-011','ORD-2025-005','PRD-2025-004','2025-11-16','Battery issue','Approved'),
        ('RET-2025-012','ORD-2025-008','PRD-2025-010','2025-11-19','Not as expected','Processed'),
        ('RET-2025-013','ORD-2025-015','PRD-2025-015','2025-11-26','Chipped surface','Approved'),
        ('RET-2025-014','ORD-2025-016','PRD-2025-005','2025-11-21','Wrong size','Processed'),
        ('RET-2025-015','ORD-2025-018','PRD-2025-011','2025-11-28','Not pairing with device','Approved');
            
        INSERT INTO refunds VALUES
        ('RFD-2025-001','RET-2025-001',45999,'2025-11-17','Completed'),
        ('RFD-2025-002','RET-2025-002',10497,'2025-11-15','Completed'),
        ('RFD-2025-003','RET-2025-003',118999,'2025-11-19','Pending'),
        ('RFD-2025-004','RET-2025-004',24999,'2025-11-21','Completed'),
        ('RFD-2025-005','RET-2025-005',249999,'2025-11-23','Pending'),
        ('RFD-2025-006','RET-2025-006',167999,'2025-11-24','Completed'),
        ('RFD-2025-007','RET-2025-007',79999,'2025-11-25','Completed'),
        ('RFD-2025-008','RET-2025-008',42999,'2025-11-26','Pending'),
        ('RFD-2025-009','RET-2025-009',129999,'2025-11-11','Completed'),
        ('RFD-2025-010','RET-2025-010',29999,'2025-11-13','Completed'),
        ('RFD-2025-011','RET-2025-011',154998,'2025-11-17','Pending'),
        ('RFD-2025-012','RET-2025-012',9999,'2025-11-20','Completed'),
        ('RFD-2025-013','RET-2025-013',3499,'2025-11-27','Completed'),
        ('RFD-2025-014','RET-2025-014',12999,'2025-11-22','Pending'),
        ('RFD-2025-015','RET-2025-015',1999,'2025-11-29','Completed');   

        INSERT INTO return_pickups VALUES
        ('PKP-2025-001','RET-2025-001','2025-11-17','Completed'),
        ('PKP-2025-002','RET-2025-002','2025-11-15','Completed'),
        ('PKP-2025-003','RET-2025-003','2025-11-19','Scheduled'),
        ('PKP-2025-004','RET-2025-004','2025-11-21','Completed'),
        ('PKP-2025-005','RET-2025-005','2025-11-23','Scheduled'),
        ('PKP-2025-006','RET-2025-006','2025-11-24','Completed'),
        ('PKP-2025-007','RET-2025-007','2025-11-25','Scheduled'),
        ('PKP-2025-008','RET-2025-008','2025-11-26','Completed'),
        ('PKP-2025-009','RET-2025-009','2025-11-11','Completed'),
        ('PKP-2025-010','RET-2025-010','2025-11-13','Completed'),
        ('PKP-2025-011','RET-2025-011','2025-11-17','Scheduled'),
        ('PKP-2025-012','RET-2025-012','2025-11-20','Completed'),
        ('PKP-2025-013','RET-2025-013','2025-11-27','Completed'),
        ('PKP-2025-014','RET-2025-014','2025-11-22','Scheduled'),
        ('PKP-2025-015','RET-2025-015','2025-11-29','Completed');

        INSERT INTO product_details VALUES
        ('PRD-2025-001','Apple','iPhone 15 Pro Max','A17 Bionic chip, 6.7-inch OLED, 48MP camera'),
        ('PRD-2025-002','Samsung','Galaxy S24 Ultra','Snapdragon 8 Gen3, 6.8-inch AMOLED, 200MP camera'),
        ('PRD-2025-003','Sony','WH-1000XM5','Wireless, Noise cancelling, 30h battery'),
        ('PRD-2025-004','Dell','XPS 13 Plus','Intel i9, 16GB RAM, 1TB SSD, OLED display'),
        ('PRD-2025-005','Nike','Air Max 270','Air cushioning, Lightweight, Running shoes'),
        ('PRD-2025-006','Adidas','Men’s Hoodie','Cotton, Breathable, Comfortable fit'),
        ('PRD-2025-007','HP','LaserJet Pro M404dn','Monochrome laser, 40ppm, Duplex printing'),
        ('PRD-2025-008','Apple','Watch Series 10','Fitness tracker, Heart rate, GPS'),
        ('PRD-2025-009','Lenovo','ThinkPad X1 Carbon','i7 CPU, 16GB RAM, 512GB SSD, Carbon chassis'),
        ('PRD-2025-010','Logitech','MX Master 4','Ergonomic, Wireless, High precision'),
        ('PRD-2025-011','Boat','Airdopes 200','True wireless earbuds, 25h battery'),
        ('PRD-2025-012','Canon','EOS R6 Mark II','Full-frame mirrorless, 24MP, 4K video'),
        ('PRD-2025-013','Samsung','QLED 55-inch TV','4K Smart TV, HDR10+, 120Hz refresh'),
        ('PRD-2025-014','LG','1.5 Ton Inverter AC','Energy saving, Fast cooling, Low noise'),
        ('PRD-2025-015','Prestige','Nonstick Cookware Set','5-piece set, Non-stick, Oven safe');

        INSERT INTO product_qa VALUES
        ('QA-2025-001','PRD-2025-001','Does it support 5G?','Yes, fully supports 5G networks.'),
        ('QA-2025-002','PRD-2025-001','Is the warranty included?','Yes, 1-year manufacturer warranty included.'),
        ('QA-2025-003','PRD-2025-002','Is the S Pen included?','No, S Pen is sold separately.'),
        ('QA-2025-004','PRD-2025-002','Does it support wireless charging?','Yes, 50W wireless charging supported.'),
        ('QA-2025-005','PRD-2025-003','Is it water resistant?','Yes, IPX4 splash resistant.'),
        ('QA-2025-006','PRD-2025-004','Does it have a touch screen?','Yes, OLED touch display.'),
        ('QA-2025-007','PRD-2025-005','Are these shoes true to size?','Yes, recommended to pick your normal size.'),
        ('QA-2025-008','PRD-2025-005','Is it suitable for outdoor running?','Yes, designed for all terrains.'),
        ('QA-2025-009','PRD-2025-006','Is it machine washable?','Yes, gentle cycle recommended.'),
        ('QA-2025-010','PRD-2025-007','Does it support duplex printing?','Yes, automatic duplex printing supported.'),
        ('QA-2025-011','PRD-2025-008','Can I track my workouts?','Yes, detailed activity tracking included.'),
        ('QA-2025-012','PRD-2025-009','Does it have a fingerprint sensor?','Yes, integrated on power button.'),
        ('QA-2025-013','PRD-2025-010','Is it compatible with Mac?','Yes, fully compatible with Mac and Windows.'),
        ('QA-2025-014','PRD-2025-011','How long is the battery life?','Up to 25 hours with case.'),
        ('QA-2025-015','PRD-2025-012','Does it have 4K video recording?','Yes, 4K 60fps supported.');
            
        """
    )
    
    conn.commit()
    cur.close()
    conn.close()
