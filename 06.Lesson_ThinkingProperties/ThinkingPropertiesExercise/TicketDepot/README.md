# Rules

## Valid States

def noTicketsRemaining()
    - remaining tickets == 0

def sellerCreated()
    - owner != address(0)
    - transactionFee != 0

1. if `createEvent` has never been called, then numEvents is 0

## State Transitions

2. if not in state sellerCreated(), then all non-view functions should revert 

## Variable Transitions

3. once transactionFee is set to nonzero, it cannot be set back to zero

## High-Level Properties

4. A call to offerTicket will always succeed if the ticket is not already offered
5. The number of tickets increases once it's set to a nonzero value

## Unit Tests

6. `buyNewTicket` always succeeds if msg.value >= ticket_price + fee
7. `buyOfferedTicket` always succeeds if msg.value >= offered_ticket_price
8. TicketDepot's balance always increases by exactly msg.value in `buyNewTicket` and `buyOfferedTicket`

## Risk Analysis

9. calls to `buyNewTicket` do not affect earlier ticket IDs
10. calls to `createEvent` do not affect earlier event IDs

# Rule Priority

TODO (though I do not find this that useful).

## High Priority

- 
## Medium Priority

- 
## Low Priority

