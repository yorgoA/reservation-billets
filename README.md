# reservation-billets
To check if all endpoints work :
1. curl http://localhost:8080/
2. curl http://localhost:8080/users
3. curl http://localhost:8080/etcd-test
4. curl http://localhost:8080/events
5. curl -X POST http://localhost:8080/reserve -H "Content-Type: application/json" -d '{"event_id": 1, "user_id": 1, "num_tickets": 2}'
6. curl http://localhost:8080/reservations
7. 
