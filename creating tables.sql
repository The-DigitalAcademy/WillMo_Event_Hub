-- Customers Table
CREATE TABLE "Customers" (
  "contact" varchar,
  "name" varchar,
  "surname" varchar,
  "email" varchar PRIMARY KEY,
  "password" varchar
);

-- Location Table
CREATE TABLE "Location" (
  "location_id" serial PRIMARY KEY,
  "province" varchar,
  "city" varchar,
  "venue_title" varchar,
  "google_maps" varchar
);

-- Type Table
CREATE TABLE "Type" (
  "type_id" serial PRIMARY KEY,
  "type" varchar
);

-- Category Table
CREATE TABLE "Category" (
  "category_id" serial PRIMARY KEY,
  "category" varchar
);

-- Events Table
CREATE TABLE "Events" (
  "event_id" serial PRIMARY KEY,
  "capacity" integer,
  "quantity" integer,
  "start_date" date,
  "start_time" time,
  "description" varchar,
  "event_title" varchar,
  "location_id" integer,
  "category_id" integer,
  "price" float,
  "image" varchar,
  "event_url" varchar,
  "organizer_id" integer,  -- Foreign key linking to Organizer
  FOREIGN KEY ("location_id") REFERENCES "Location" ("location_id"),
  FOREIGN KEY ("category_id") REFERENCES "Category" ("category_id"),
  FOREIGN KEY ("organizer_id") REFERENCES "Organizer" ("organizer_id")  -- Linking Organizer to Event
);

-- Cart Table
CREATE TABLE "Cart" (
  "cart_id" serial PRIMARY KEY,
  "email" varchar,
  "event_id" integer,
  "quantity" integer,
  "user_quantity" integer,
  FOREIGN KEY ("email") REFERENCES "Customers" ("email"),
  FOREIGN KEY ("event_id") REFERENCES "Events" ("event_id")
);

-- Bookings Table
CREATE TABLE "Bookings" (
  "booking_id" serial PRIMARY KEY,
  "email" varchar,
  "event_id" integer,
  "booking_date" timestamp default current_timestamp,
  "status" varchar default 'pending',  --pending/confirmed
  FOREIGN KEY ("email") REFERENCES "Customers" ("email"),
  FOREIGN KEY ("event_id") REFERENCES "Events" ("event_id")
);

-- CustomerType Table
CREATE TABLE "CustomerType" (
  "type_id" integer,
  "email" varchar,
  FOREIGN KEY ("type_id") REFERENCES "Type" ("type_id"),
  FOREIGN KEY ("email") REFERENCES "Customers" ("email")
);

-- CustomerMap Table
CREATE TABLE "CustomerMap" (
  "email" varchar,
  "event_id" integer,
  FOREIGN KEY ("email") REFERENCES "Customers" ("email"),
  FOREIGN KEY ("event_id") REFERENCES "Events" ("event_id")
);

-- BookingEventMap Table
CREATE TABLE "BookingEventMap" (
  "booking_id" integer,
  "event_id" integer,
  FOREIGN KEY ("event_id") REFERENCES "Events" ("event_id"),
  FOREIGN KEY ("booking_id") REFERENCES "Bookings" ("booking_id")
);

-- Organizer Table
CREATE TABLE "Organizer" (
  "organizer_id" serial PRIMARY KEY,
  "contact" varchar,  -- Contact refers to the Customer's contact info
  "email" varchar,  -- Email of the organizer (should match Customer's email)
  "bank_name" varchar,
  "bank_account_number" varchar,
  "account_holder_name" varchar,
  "bank_code" varchar,
  FOREIGN KEY ("email") REFERENCES "Customers" ("email"),  -- Linking Organizer to Customer
  FOREIGN KEY ("contact") REFERENCES "Customers" ("contact")  -- Linking Organizer's contact to Customer's contact
);
