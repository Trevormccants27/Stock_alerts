import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices


def plot_efficient_frontier(portfolio_qty):
        # Run 1 year algorithm
        df = yf.download(portfolio_qty.columns.tolist(), period='3mo', interval='1d')
        df = df['Adj Close']

        mu = expected_returns.mean_historical_return(df)
        S = risk_models.sample_cov(df)
        ef = EfficientFrontier(mu, S)

        # Calculate current Portfolio value
        portfolio_value = portfolio_qty * df.apply(lambda x: x[pd.Series.last_valid_index(x)])
        total_portfolio_value = portfolio_value.sum(axis = 1)[0]
        portfolio_weights = portfolio_value / total_portfolio_value

        fig, ax = plt.subplots()
        plotting.plot_efficient_frontier(ef, ax=ax, show_assets=True)

        # Generate random portfolios
        # n_samples = 10000
        # w = np.random.dirichlet(np.ones(len(mu)), n_samples)
        # rets = w.dot(mu)
        # stds = np.sqrt(np.diag(w @ S @ w.T))
        # sharpes = rets / stds
        # ax.scatter(stds, rets, marker=".", c=sharpes, cmap="viridis_r")

        # Find the tangency portfolio
        ef = EfficientFrontier(mu, S)
        weights = ef.max_sharpe()
        weights = ef.clean_weights()
        allocation, leftover = get_discrete_allocation(weights, df, total_portfolio_value)
        print('--------------- MAX SHARPE RATIO ---------------')
        weights = process_weights(weights)
        print(weights)
        print("Discrete allocation:", allocation)
        print("Funds remaining: ${:.2f}".format(leftover))
        ret_tangent, std_tangent, _ = ef.portfolio_performance(verbose=True)
        ax.scatter(std_tangent, ret_tangent, marker="*", s=100, c="r", label="Max Sharpe")

        # Plot current portfolio
        print('--------------- CURRENT PORTFOLIO ---------------')
        ef = EfficientFrontier(mu, S)
        ef.set_weights(portfolio_weights.iloc[0].to_dict())
        portfolio_weights = ef.clean_weights()
        portfolio_allocation, portfolio_leftover = get_discrete_allocation(portfolio_weights, df, total_portfolio_value)
        portfolio_weights = process_weights(portfolio_weights)
        print(portfolio_weights)
        print("Discrete allocation:", portfolio_allocation)
        print("Funds remaining: ${:.2f}".format(portfolio_leftover))
        ret_tangent, std_tangent, _ = ef.portfolio_performance(verbose=True)
        ax.scatter(std_tangent, ret_tangent, marker="*", s=100, c="b", label="Current Portfolio")

        # Output
        ax.set_title("3 Month Efficient Frontier")
        ax.legend()
        plt.tight_layout()
        
        plt.savefig(f'images/efficient_frontier.png', dpi=200)

def process_weights(weights):
    weights = pd.DataFrame.from_dict(weights, orient='index').transpose()
    weights = weights.loc[:, (weights != 0).any(axis=0)]
    return weights

def get_discrete_allocation(weights, df, total_portfolio_value):
    latest_prices = get_latest_prices(df)

    da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=total_portfolio_value)
    allocation, leftover = da.greedy_portfolio()

    return allocation, leftover