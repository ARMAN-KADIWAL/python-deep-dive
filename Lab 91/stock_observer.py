from observer_pattern import Observer, Subject
import random
import time

class Stock(Subject):
    def __init__(self, symbol, initial_price):
        self.symbol = symbol
        self.price = initial_price
        self._observers = []
        self.price_history = [initial_price]
    
    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Investor {observer.name} is now watching {self.symbol}")
    
    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Investor {observer.name} stopped watching {self.symbol}")
    
    def notify(self):
        for observer in self._observers:
            observer.update(self, {
                'symbol': self.symbol,
                'price': self.price,
                'previous_price': self.price_history[-2] if len(self.price_history) > 1 else self.price,
                'change': self.price - (self.price_history[-2] if len(self.price_history) > 1 else self.price)
            })
    
    def set_price(self, new_price):
        self.price_history.append(new_price)
        self.price = new_price
        print(f"\n{self.symbol} price updated to ${new_price:.2f}")
        self.notify()

class Investor(Observer):
    def __init__(self, name, buy_threshold=None, sell_threshold=None):
        self.name = name
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.portfolio = {}
    
    def update(self, subject, data):
        symbol = data['symbol']
        price = data['price']
        change = data['change']
        
        change_percent = (change / data['previous_price'] * 100) if data['previous_price'] != 0 else 0
        direction = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        
        print(f"\n[Investor: {self.name}] {symbol} Alert:")
        print(f"  Current Price: ${price:.2f} {direction}")
        print(f"  Change: ${change:+.2f} ({change_percent:+.1f}%)")
        
        # Investment decisions
        if self.buy_threshold and price <= self.buy_threshold:
            print(f"  🟢 BUY SIGNAL: Price ${price:.2f} <= threshold ${self.buy_threshold:.2f}")
            self.portfolio[symbol] = self.portfolio.get(symbol, 0) + 100  # Buy 100 shares
            print(f"  Portfolio: {self.portfolio.get(symbol, 0)} shares of {symbol}")
        
        elif self.sell_threshold and price >= self.sell_threshold:
            if symbol in self.portfolio and self.portfolio[symbol] > 0:
                print(f"  🔴 SELL SIGNAL: Price ${price:.2f} >= threshold ${self.sell_threshold:.2f}")
                self.portfolio[symbol] = max(0, self.portfolio[symbol] - 50)  # Sell 50 shares
                print(f"  Portfolio: {self.portfolio.get(symbol, 0)} shares of {symbol}")

class TradingBot(Observer):
    def __init__(self, name):
        self.name = name
        self.trades_executed = 0
    
    def update(self, subject, data):
        symbol = data['symbol']
        price = data['price']
        change = data['change']
        
        print(f"\n[Trading Bot: {self.name}] Analyzing {symbol}...")
        
        # Simple trading algorithm
        if abs(change) > 2:  # Significant price movement
            action = "BUY" if change < -2 else "SELL"
            self.trades_executed += 1
            print(f"  🤖 AUTO-{action}: Significant movement detected (${change:+.2f})")
            print(f"  Trades executed today: {self.trades_executed}")

def simulate_stock_market():
    print("=== Stock Market Observer Pattern Demo ===")
    
    # Create stocks
    apple = Stock("AAPL", 150.00)
    tesla = Stock("TSLA", 800.00)
    
    # Create investors with different strategies
    conservative_investor = Investor("Alice (Conservative)", buy_threshold=145, sell_threshold=160)
    aggressive_investor = Investor("Bob (Aggressive)", buy_threshold=155, sell_threshold=145)
    day_trader = Investor("Charlie (Day Trader)")
    
    # Create trading bot
    trading_bot = TradingBot("AlgoTrader-1")
    
    # Attach observers to stocks
    apple.attach(conservative_investor)
    apple.attach(aggressive_investor)
    apple.attach(trading_bot)
    
    tesla.attach(day_trader)
    tesla.attach(trading_bot)
    
    # Simulate market movements
    print("\n" + "="*60)
    print("Market Opening...")
    
    # Apple stock movements
    apple.set_price(148.50)  # Slight drop
    time.sleep(1)
    
    apple.set_price(144.00)  # Significant drop - should trigger buy
    time.sleep(1)
    
    apple.set_price(162.00)  # Big jump - should trigger sell
    time.sleep(1)
    
    # Tesla stock movements
    tesla.set_price(795.00)  # Slight drop
    time.sleep(1)
    
    tesla.set_price(820.00)  # Jump up
    time.sleep(1)
    
    print(f"\n{'-'*60}")
    print("Market Closing...")

if __name__ == "__main__":
    simulate_stock_market()

