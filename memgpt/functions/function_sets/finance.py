from pysnowball import utls
import pysnowball as ball

import re

host = "xueqiu.com"
# suggest
suggest_stock_url = "https://xueqiu.com/query/v1/suggest_stock.json?q="

def get_stock_symbol(keyword: str):
    url = suggest_stock_url + keyword
    response = utls.fetch(url, host)
    data = response.get("data", None)
    print(f"[get_stock_symbol], data:{data}")
    if isinstance(data, list) and len(data) > 0:
        return data[0].get("code", None)
    return None

get_stock_symbol.__module__= None

def search_stock_symbol(self, keyword: str):
    """
    Retrieve stock symbol. Performs a search based on a keyword to return interrelated symbols that match or are related to the input keyword. 
  
    This function generates a list of items, each containing a stock's symbol(code) and stock name(query).
    Args:
        keyword (str): String to search for.
    Returns:
        List(dict): list of stock symbol and name 
    """ 
    
    url = suggest_stock_url + keyword
    response = utls.fetch(url, host)
    if "data" in response:
        return [{"code": item["code"], "query": item["query"]} for item in response['Data']]
    return []

# SYMBOL_KEYS = ["symbol", "symbols"]
# def convert_symbol(args):
#     for key in SYMBOL_KEYS:
#         if key in args and isinstance(args[key], str):
#             match = re.match(r'^(\d{6})\.([A-Za-z]{2})$', args[key])
#             if match:
#                 args[key] = f"{match.group(2)}{match.group(1)}"
#     return args


def stock_kline(self, symbol: str, days: int = 100):
    """
    Generates K-line (candlestick) data for a specified financial instrument over a given number of days. K-line data is commonly used in financial analysis to visualize price movements over time.
  
    This function generates a list of items, which relevated to symbol user inputs.
    Args:
        symbol (str): The ticker symbol of the financial instrument for which to generate the K-line data.
        days (integer): The number of days over which the K-line data should be generated. The default is set to 100 days.
    Returns:
        List[dict]: the list of k-line infomation
    """

    response = ball.kline(symbol, days)
    infos = response.get("data", [])
    if not isinstance(infos, list) or len(infos) == 0:
        new_symbol = get_stock_symbol(symbol) 
        if new_symbol is not None:
            response = ball.kline(new_symbol, days)
            infos = response.get("data", [])
        else:
            return [] 
    return infos

def stock_quotec(self, symbol: str):
    """
    Retrieves real-time quote data for a specified stock symbol.
  
    This function generates a dict, containing symbol real time quote data.
    Args:
        symbol (str): The stock symbol for which the quote data is requested. This should be the ticker symbol of the stock as listed on its respective stock exchange. e.g. SZ000651, not 000651.SZ
    Returns:
        dict: the real-time info for stock symbol
    """ 

    response = ball.quotec(symbol)
    print(f"[stock_quotec]response: {response}")
    infos = response.get("data", [])
    if not isinstance(infos, list) or len(infos) == 0 or infos[0] is None:
        new_symbol = get_stock_symbol(symbol)
        print(f"[stock_quotec], new_symbol:{new_symbol}")
        if new_symbol is not None:
            response = ball.quotec(new_symbol)
            print(f"[stock_quotec], new_response:{response}")
            infos = response.get("data", [])
        else:
            print(f"[stock_quotec] return none")
            return {}     
    ret = infos[0] if len(infos)> 0 else {}
    print(f"[stock_quotec] ret: {ret}")
    return ret



