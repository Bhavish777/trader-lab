# Trader Lab Frontend

This is the frontend for Trader Lab.

The goal of this part of the project is to make the trading dashboard feel usable instead of just showing API data. Users can search for stocks, check a quote, place demo trades, and see how their portfolio changes.

## What it does right now

The frontend currently lets a user:

- See a portfolio summary
- Search for stocks
- Preview the latest stock quote
- Buy supported USD stocks
- Sell stocks they already hold
- View priced holdings
- View trade history
- Reset the demo portfolio
- See loading and error messages when something is not working

## Current limitations

This is still an MVP version.

Right now, the demo portfolio supports USD trades only. Stocks from other markets, such as Indian or Canadian listings, can still be searched and viewed, but buying them is blocked until multi-currency support is added.

The app also does not have user accounts yet, so it currently works as one demo portfolio instead of separate portfolios for different users.

The design is still early and will be improved in later phases.
