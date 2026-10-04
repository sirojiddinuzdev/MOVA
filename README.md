# MOVA Backend Architecture

Clean, modular architecture ready for production.

## Stack recommendation

- **Runtime**: Node.js 20+ (TypeScript) or Python 3.11+ (FastAPI)
- **API**: REST + optional GraphQL
- **Auth**: JWT + refresh tokens
- **DB**: PostgreSQL 15+
- **Cache / queues**: Redis
- **Storage**: S3-compatible abstraction
- **Payments**: Provider-agnostic PaymentService

## Module structure

```
backend/
├── src/
│   ├── modules/
│   │   ├── auth/
│   │   ├── profiles/
│   │   ├── search/
│   │   ├── deals/
│   │   ├── reviews/
│   │   ├── reputation/
│   │   ├── messaging/
│   │   ├── payments/
│   │   ├── disputes/
│   │   ├── notifications/
│   │   └── admin/
│   ├── shared/
│   │   ├── database/
│   │   ├── storage/
│   │   ├── events/
│   │   └── middleware/
│   └── main.ts
├── tests/
└── package.json / requirements.txt
```

## Key rules

1. Reviews can only be created for `status = completed` deals.
2. One review per user per deal (enforced by unique constraint).
3. Mutual reviews: hide until both submitted or review window expires.
4. Agreement changes after confirmation are logged in history.
5. Dispute preserves full timeline + evidence.
6. Never store secrets in client code.
7. Rate limiting on auth, search, messaging.
8. Soft deletes on user-generated content.

## Payment abstraction

```ts
interface PaymentService {
  createIntent(amount, currency, metadata): Promise<PaymentIntent>
  capture(intentId): Promise<PaymentStatus>
  refund(intentId, amount?): Promise<PaymentStatus>
  payout(sellerId, amount): Promise<Payout>
}
```

Mock provider included for local development.

## Search & Match

- Full-text + filters
- Match score is a weighted recommendation (skills, location, budget, availability, history)
- Smart search NLP converts natural language → structured filters (optional ML service)

## Next steps

1. Implement auth module
2. Wire PostgreSQL schema
3. Add real payment provider
4. WebSocket for messaging
5. Admin panel API
