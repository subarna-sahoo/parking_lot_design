# Parking Lot

A low-level design (LLD) of a **parking lot system**, exposed as a small Flask/Connexion REST API. Vehicles get the nearest free slot, receive a ticket, and pay by the hour when they check out.

## Features

- **Nearest-slot allocation** from a fixed pool (10 slots by default)
- **Two-wheelers and four-wheelers**, each with its own hourly rate (2 and 4 per hour)
- **Tickets**: `reserved` on entry, `paid` on checkout. Hours are **rounded up** when billing.
- **Vehicle history** for one licence number or for all vehicles
- Guards against parking the same vehicle twice, a full lot, and invalid tickets
- Payment sits behind a `Payment` interface (`BasicPayment` is the default), so other payment methods can be added

## API

| Method | Path | Body / Query | Description |
|---|---|---|---|
| `GET` | `/` | | Health check |
| `POST` | `/vehicle/park` | `{ "licence_no", "contact_no", "vehicle_type": "two" \| "four" }` | Park a vehicle and get a ticket |
| `PUT` | `/vehicle/checkout/<ticket_id>` | | Check out and calculate the bill |
| `POST` | `/vehicle/history` | `?licence_no=<no>` (optional) | Parking history |

Postman collection: <https://www.getpostman.com/collections/9a85e60749ee4190e06f>

## Running

**Locally**

```bash
pip install -r requirements.txt
python app.py              # http://localhost:8000
```

**Docker**

```bash
docker build -t parking_lot_design .
docker run -d -p 8000:8000 parking_lot_design
```

Or use the published image:

```bash
docker pull subarnasahoo/parking_lot
docker run -d -p 8000:8000 subarnasahoo/parking_lot
```

**Tests**

```bash
PYTHONPATH=. python -m unittest discover -s test -p "*_test.py"
```

## Design

```
app.py                       Routes (Connexion/Flask)
services/parking_service.py  Slot allocation, tickets, checkout, history
models/
  vehicle/                   Vehicle, TwoWheeler, FourWheeler
  parking/                   ParkingSlot, ReservationTicket
  payment/                   Payment interface, BasicPayment, hourly prices
  constants.py               VehicleType, TicketStatus enums
repository/memory.py         In-memory store
exception/api_response.py    ParkingServiceException
```

## License

MIT. See [LICENSE](LICENSE).
