# AUBoutique 🛍️  
**Online Boutique Platform – Python · PyQt · SQLite**

## Project Overview  
AUBoutique is a full-stack desktop simulation of an e-commerce platform built as an undergraduate project. It enables product listing, searching, purchases, ratings, and multi-currency support, combined with secure peer-to-peer chat functionality between buyers and sellers.

## Key Features  
- **Custom application layer** for data routing: forwards incoming messages from the server to the correct client thread, ensuring asynchronous, thread-safe communication. 
- User accounts for buyers and sellers — authentication, role based access.  
- Product catalog: listing, search/filter, and star ratings 
- Shopping cart & checkout process (simulation of purchase flow).  
- Peer-to-peer real-time chat implemented via socket networking enabling direct buyer–seller communication.  
- SQLite backend for lightweight storage and data persistence.
- Designed a multi-currency mechanism allowing users to view and transact in different currencies seamlessly.
- Responsive GUI built in PyQt for desktop deployment and user interaction.

## Tech Stack  
| Layer        | Technologies |
|--------------|-------------|
| Front-end UI | PyQt |
| Business Logic| Python |
| Persistence  | SQLite |
| Networking   | Python sockets (TCP) |
| Security     | Secure authentication flows, basic password hashing |



