import yfinance as yf
import matplotlib.pyplot as plt

def moving_averages(tickers):
    # Loop through each stock
    buy_list = []
    sell_list = []
    for ticker in tickers:
        print(f'Processing {ticker}')

        # Run 5 year algorithm
        data = yf.download(ticker, period='5y', interval='1d')
        data['Open_avg_200'] = data['Open'].rolling(window=200).mean()
        data['Open_avg_50'] = data['Open'].rolling(window=50).mean()

        if data['Open_avg_50'][-1] > data['Open_avg_200'][-1]:
            buy_list.append(ticker)
        else:
            sell_list.append(ticker)

        data.plot(y=['Open', 'Open_avg_50', 'Open_avg_200'], title=ticker)
        plt.savefig(f'images/{ticker}_movingAvg.png')

    return buy_list, sell_list