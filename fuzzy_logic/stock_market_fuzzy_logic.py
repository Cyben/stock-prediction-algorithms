class StockMarketFuzzyLogic:
    """
    Credit to :
        https://medium.com/@abdulazizalghannami/modeling-trading-decisions-using-fuzzy-logic-ff21c431b961

    Each stock will be described by the following set of input variables:
    - beta as X₁
    - normalized bid-ask spread n(t) as X₂
    - double crossover method value Indicator_t(50,200) as X₃
    - relative strength index RSI(t) as X₄

    Then we will construct three rule blocks:
    Rule block 1: Validity of strategy
    Rule block 2: Strength of signals
    Rule block 3: Confidence and trading decision

         Input Variables                  Rule block 1
    -------------------------       ------------------------
    | * beta (x1)           |  x1   | Validity of strategy |
    |                       | ----> |                      | ↘            Rule block 3
    | * normalized bid-ask  |  x2   |   very/slight/not    |   ↘     --------------------
    |   spread (x2)         |       -----------------------      ↘   | Confidence and   |
    |                       |             Rule block 2             → | trading decision | ----> OUTPUT
    | * double crossover    |       ------------------------     ↗   |                  |
    |   method value (x3)   |  x3   | Strength of signals  |   ↗     --------------------
    |                       | ----> |                      | ↗
    | * relative strength   |  x4   | strong buy/sell      |
    |   index (x4)          |       | average but/sell     |
    -------------------------       | neutral              |
                                    ------------------------

    Threshold Values for Membership Function of Input Variables:

    ---------------------------------------------------------------------------------------------------
    |                    VARIABLE                    |                    CRITERIA                    |
    ---------------------------------------------------------------------------------------------------
    | Beta (value range: 0-2)                        | Highly volatile: greater than 1.0              |
    |                                                | Lowly volatile: less than 1.0                  |
    ---------------------------------------------------------------------------------------------------
    | Normalized bid-ask spreat (value range: 0 - 1) | Illiquid: greater than 0.015                   |
    |                                                | Liquid: less or equal to 0.015                 |
    ---------------------------------------------------------------------------------------------------
    | Double crossover method value                  | Buy signal: greater than 1.0                   |
    | ( value range: -1000, 1000)                    | Sell signal: less than 1.0                     |
    ---------------------------------------------------------------------------------------------------
    | Relative strength index (value range: 0 - 100) | Overbought: greater than 70                    |
    |                                                | Upward trend: more than 50                     |
    |                                                | Downward trend: less than 50                   |
    |                                                | Oversold: less than 30                         |
    ---------------------------------------------------------------------------------------------------
    """

    def __init__(self, ma_s, ma_l, rsi, beta_stock, bid_price, ask_price):
        """
        (Technical Indicators)
        Args:
            ma_s - Short-term moving average (MAt(s))
            ma_l - Long-term moving average (MAt(t))
            rsi - Relative Strength Index (RSI): which is a type of momentum oscillator
            beta_stock - The beta of the stock
            bid_price - The bid price is the highest price a buyer will pay for a stock
            ask_price - The ask price is the lowest price a seller will accept to sell the stock
        """
        self.ma_s = ma_s
        self.ma_l = ma_l
        self.rsi = rsi
        self.beta_stock = beta_stock
        self.bid_price = bid_price
        self.ask_price = ask_price
        self.bid_ask_spread = (self.ask_price - self.bid_price) / self.ask_price
        self.dcm = self.ma_s - self.ma_l

    def block1(self):
        """
        Validity of strategy

        * beta_stock - x1
        * bid_ask_spread - x2

        Rules:

        If X₁ is Highly volatile and X₂ is Illiquid then Validity of strategy is Slight
        If X₁ is Highly volatile and X₂ is Liquid then Validity of strategy is Very
        If X₁ is Lowly volatile and X₂ is Illiquid then Validity of strategy is Not
        If X₁ is Lowly volatile and X₂ is Liquid then Validity of strategy is Slight
        """

        if self.beta_stock > 1:
            return "slight" if self.bid_ask_spread > 0.015 else "very"
        elif self.beta_stock < 1:
            return "not" if self.bid_ask_spread > 0.015 else "slight"
        else:
            return "slight"

        # if x1 > 1 and x2 > 0.015:
        #     return "slight"
        # elif x1 > 1 and x2 <= 0.015:
        #     return "very"
        # elif x1 < 1 and x2 > 0.015:
        #     return "not"
        # elif x1 < 1 and x2 <= 0.015:
        #     return "slight"

    def block2(self):
        """
        Strength of signals

        * dcm - x3
        * rsi - x4

        Rules:

        If X₃ is Buy signal and X₄ is Overbought then Strength of signals is Average buy
        If X₃ is Sell signal and X₄ is Overbought then Strength of signals is Neutral
        If X₃ is Buy signal and X₄ is Upward trend then Strength of signals is Strong buy
        If X₃ is Sell signal and X₄ is Upward trend then Strength of signals is Neutral
        If X₃ is Buy signal and X₄ is Downward trend then Strength of signals is Neutral
        If X₃ is Sell signal and X₄ is Downward trend then Strength of signals is Strong sell
        If X₃ is Buy signal and X₄ is Oversold then Strength of signals is Neutral
        If X₃ is Sell signal and X₄ is Oversold then Strength of signals is Average sell
        """

        if self.rsi > 70:
            return "neutral" if self.dcm < 1 else "average buy"
        elif self.rsi > 50:
            return "neutral" if self.dcm < 1 else "strong buy"
        elif self.rsi >= 30:
            return "strong sell" if self.dcm < 1 else "neutral"
        else:
            return "average sell" if self.dcm < 1 else "neutral"

        # if x3 > 1 and x4 > 70:
        #     return "average buy"
        # elif x3 < 1 and x4 > 70:
        #     return "neutral"
        # elif x3 > 1 and x4 > 50:
        #     return "strong buy"
        # elif x3 < 1 and x4 > 50:
        #     return "neutral"
        # elif x3 > 1 and x4 > 30:
        #     return "neutral"
        # elif x3 < 1 and x4 > 30:
        #     return "strong sell"
        # elif x3 > 1 and x4 < 30:
        #     return "neutral"
        # elif x3 < 1 and x4 < 30:
        #     return "average sell"

    def block3(self):
        """
        Confidence and trading decision

        * Validity of strategy - block1
        * Strength of signals - block2

        Rules:

        If Validity of Strategy is Slight and Strength of signals is Average buy then Low confidence buy decision
        If Validity of Strategy is Slight and Strength of signals is Strong buy then Moderate confidence buy decision
        If Validity of Strategy is Slight and Strength of signals is Neutral then No confidence trade decision
        If Validity of Strategy is Slight and Strength of signals is Strong sell then Moderate confidence sell decision
        If Validity of Strategy is Slight and Strength of signals is Average Sell then Low confidence sell decision
        If Validity of Strategy is Very and Strength of signals is Average buy then Moderate confidence buy decision
        If Validity of Strategy is Very and Strength of signals is Strong buy then High confidence buy decision
        If Validity of Strategy is Very and Strength of signals is Neutral then No confidence trade decision
        If Validity of Strategy is Very and Strength of signals is Strong sell then High confidence sell decision
        If Validity of Strategy is Very and Strength of signals is Average Sell then Moderate confidence sell decision
        If Validity of Strategy is Not and Strength of signals is Average buy then No confidence trade decision
        If Validity of Strategy is Not and Strength of signals is Strong buy then No confidence trade decision
        If Validity of Strategy is Not and Strength of signals is Neutral then No confidence trade decision
        If Validity of Strategy is Not and Strength of signals is Strong sell then No confidence trade decision
        If Validity of Strategy is Not and Strength of signals is Average Sell then No confidence trade decision
        """

        validity_of_strategy = self.block1()
        strength_of_signals = self.block2()

        if validity_of_strategy == "slight":
            if strength_of_signals == "average buy":
                return "low confidence buy"
            elif strength_of_signals == "strong buy":
                return "moderate confidence buy"
            elif strength_of_signals == "neutral":
                return "no confidence trade"
            elif strength_of_signals == "strong sell":
                return "moderate confidence sell"
            elif strength_of_signals == "average sell":
                return "low confidence sell"
        elif validity_of_strategy == "very":
            if strength_of_signals == "average buy":
                return "moderate confidence buy"
            elif strength_of_signals == "strong buy":
                return "high confidence buy"
            elif strength_of_signals == "neutral":
                return "no confidence trade"
            elif strength_of_signals == "strong sell":
                return "high confidence sell"
            elif strength_of_signals == "average sell":
                return "moderate confidence sell"
        elif validity_of_strategy == "not":
            return "no confidence trade"

        # v_o_s = block1(beta, nbas)
        # s_o_s = block2(indicator, rsi)
        # if v_o_s == "slight" and s_o_s == "average buy":
        #     return "low confidence buy"
        # elif v_o_s == "slight" and s_o_s == "strong buy":
        #     return "moderate confidence buy"
        # elif v_o_s == "slight" and s_o_s == "neutral":
        #     return "no confidence trade"
        # elif v_o_s == "slight" and s_o_s == "strong sell":
        #     return "moderate confidence sell"
        # elif v_o_s == "slight" and s_o_s == "average sell":
        #     return "low confidence sell"
        # elif v_o_s == "very" and s_o_s == "average buy":
        #     return "moderate confidence buy"
        # elif v_o_s == "very" and s_o_s == "strong buy":
        #     return "high confidence buy"
        # elif v_o_s == "very" and s_o_s == "neutral":
        #     return "no confidence trade"
        # elif v_o_s == "very" and s_o_s == "strong sell":
        #     return "high confidence sell"
        # elif v_o_s == "very" and s_o_s == "average sell":
        #     return "moderate confidence sell"
        # elif v_o_s == "not" and s_o_s == "average buy":
        #     return "no confidence trade"
        # elif v_o_s == "not" and s_o_s == "strong buy":
        #     return "no confidence trade"
        # elif v_o_s == "not" and s_o_s == "neutral":
        #     return "no confidence trade"
        # elif v_o_s == "not" and s_o_s == "strong sell":
        #     return "no confidence trade"
        # elif v_o_s == "not" and s_o_s == "average sell":
        #     return "no confidence trade"
