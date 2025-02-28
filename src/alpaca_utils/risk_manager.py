import pandas as pd
import numpy as np

class RiskManager:
    def __init__(
        self,
        risk_per_trade=0.01,         # e.g., 1% of equity at risk
        atr_period=14,
        atr_multiplier=1,
        risk_reward_ratio=2,
        max_position_fraction=0.01,  # e.g., 1% of buying power per trade
    ):
        """
        :param risk_per_trade: Fraction of equity to risk per trade (default = 0.01).
        :param atr_period: Number of periods for ATR calculation (Wilder's smoothing).
        :param atr_multiplier: Multiplier to apply to the ATR for stop loss distance.
        :param risk_reward_ratio: Take-profit ratio relative to risk.
        :param max_position_fraction: Fraction of buying power allocated to a single trade.
        """
        self.risk_per_trade = risk_per_trade
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier
        self.risk_reward_ratio = risk_reward_ratio
        self.max_position_fraction = max_position_fraction

    def compute_atr(self, df: pd.DataFrame) -> float:
        """
        Computes the Average True Range (ATR) using Wilder's smoothing (EMA with alpha=1/period).
        Expects columns: ['high', 'low', 'close'].
        Returns the latest ATR value as a float.
        """
        df = df.copy()
        df["previous_close"] = df["close"].shift(1)

        # True ranges
        df["high_low"] = df["high"] - df["low"]
        df["high_pc"] = (df["high"] - df["previous_close"]).abs()
        df["low_pc"] = (df["low"] - df["previous_close"]).abs()

        df["true_range"] = df[["high_low", "high_pc", "low_pc"]].max(axis=1)
        
        # Wilder’s smoothing for ATR
        df["atr"] = df["true_range"].ewm(alpha=1/self.atr_period, adjust=False).mean()

        atr = df["atr"].iloc[-1]
        return atr

    def calculate_trade_parameters(
        self,
        df: pd.DataFrame,
        entry_price: float,
        equity: float,
        buying_power: float,
        cash: float,
        side: str = "BUY"
    ):
        """
        1. Computes an ATR-based stop loss and take profit.
        2. Calculates a risk-based share count (risk_per_trade of equity).
        3. Caps by max_position_fraction * buying_power.
        4. Ensures affordability for BUY trades, using 'cash'.
        5. Skips the trade if final quantity <= 0 or if stop-loss is effectively zero.

        :param df: Historical DataFrame with columns 'high','low','close'.
        :param entry_price: The assumed trade entry price.
        :param equity: Current account equity (for risk).
        :param buying_power: Available buying power (for notional cap).
        :param cash: Actual free cash on hand (for BUY trades).
        :param side: 'BUY' or 'SELL'.
        :return: dict with keys: 'quantity', 'stop_loss', 'take_profit', 'atr'.
        """
        # 1) Compute ATR and basic validation
        atr = self.compute_atr(df)
        if np.isnan(atr) or atr < 1e-5:
            raise ValueError("Invalid or near-zero ATR. Market data may be insufficient or stale.")

        # 2) Determine Stop Loss & Take Profit
        if side.upper() == "BUY":
            stop_loss = entry_price - (atr * self.atr_multiplier)
            # Prevent negative or trivial stop-loss
            stop_loss = max(stop_loss, 0.01)
            risk_per_share = entry_price - stop_loss
            take_profit = entry_price + (self.risk_reward_ratio * risk_per_share)
        elif side.upper() == "SELL":
            stop_loss = entry_price + (atr * self.atr_multiplier)
            risk_per_share = stop_loss - entry_price
            take_profit = entry_price - (self.risk_reward_ratio * risk_per_share)
        else:
            raise ValueError("Invalid trade side. Must be 'BUY' or 'SELL'.")

        # If stop_loss is effectively at entry_price, risk_per_share could be near zero
        if risk_per_share <= 1e-5:
            # Too tight; skip this trade
            return {
                "quantity": 0,
                "stop_loss": None,
                "take_profit": None,
                "atr": round(atr, 4),
            }

        # 3) Risk-Based Quantity (equity * risk_per_trade / risk_per_share)
        risk_amount = equity * self.risk_per_trade
        quantity_risk_based = int(risk_amount // risk_per_share)

        # 4) Notional Cap (max_position_fraction × buying_power)
        max_notional = buying_power * self.max_position_fraction
        quantity_notional_cap = int(max_notional // entry_price)

        # 5) Affordability for BUY (use 'cash'), else large cap for SELL
        quantity_cash_cap = int(cash // entry_price) if side.upper() == "BUY" else 999999

        # 6) Final quantity is the minimum of all constraints
        final_quantity = min(quantity_risk_based, quantity_notional_cap, quantity_cash_cap)

        # If final_quantity is zero or negative, skip the trade
        if final_quantity <= 0:
            return {
                "quantity": 0,
                "stop_loss": None,
                "take_profit": None,
                "atr": round(atr, 4),
            }

        return {
            "quantity": final_quantity,
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "atr": round(atr, 4),
        }
