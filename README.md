### Book a Room Project

The "Book a Room" project is a web application designed to streamline hotel reservations. Users have the option to register accounts, including the ability to sign up as corporate users, utilizing a custom user model that extends Django's AbstractUser.

#### Core Entities

The core entities of the system are:

- **Hotels**: These are managed by hoteliers, who are authenticated users.
- **Reservations**: These represent bookings made by users for specific hotel stays.

#### Features

- **Corporate Registration**: Hotels can register as corporate entities.
- **Dynamic Pricing**: Update hotel prices according to the number of nights using AJAX.
- **Price Calculation**: Utilize AJAX to update the total price of the hotel, calculated by multiplying the base hotel price by the duration of the stay.
- **Payment Integration**: Integrate Stripe payment functionality for seamless transactions.
- **Dashboard Display**: Display previous paid reservations in the user dashboard and pending payments in the hotel cart page.

This project aims to provide a user-friendly and efficient platform for managing hotel reservations, catering to both individual and corporate users.