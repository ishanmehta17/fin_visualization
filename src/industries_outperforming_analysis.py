import requests


def get_fmp_api_key():
    return <YOUR_API_KEY>


def get_symbols():
    # Define the API URL
    url = f"https://financialmodelingprep.com/api/v3/available-traded/list?apikey=" + get_fmp_api_key()

    # Make the request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Filter the data to get symbols with exchange as NYSE or NASDAQ
        filtered_data = [item for item in data if
                         item['exchangeShortName'] in ['NYSE', 'NASDAQ'] and item['type'] == "stock"]

        # Extract and return the symbols
        symbols = [item['symbol'] for item in filtered_data]
        return symbols
    else:
        print(f"Error: {response.status_code}")
        return []


def get_price_change(symbol):
    try:
        url = f"https://financialmodelingprep.com/api/v3/stock-price-change/{symbol}?apikey=" + get_fmp_api_key()
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"getPriceChange : API request failed with status: {response.status_code}")

        data = response.json()
        if data:
            return {
                '1Y': round(data[0]['1Y'], 2) if '1Y' in data[0] else '',
                '3Y': round(data[0]['3Y'], 2) if '3Y' in data[0] else '',
                '5Y': round(data[0]['5Y'], 2) if '5Y' in data[0] else '',
            }
        return {'1Y': '', '3Y': '', '5Y': ''}
    except Exception as error:
        raise Exception(f"Error in getPriceChange: {error}")


def get_industry(symbol):
    try:
        # Replace 'API_KEY' with your actual API key
        url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey=" + get_fmp_api_key()
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"API request failed with status: {response.status_code}")

        data = response.json()
        if data:
            return data[0]['industry']
        else:
            raise Exception("No data found for the given symbol.")
    except Exception as error:
        raise Exception(f"Error in getIndustry: {error}")


# Example usage
def get_data():
    spyPriceChange = get_price_change('SPY')
    industryToAllStocks = {}
    industyToAllBeatingStocks = {}
    symbols = get_symbols()
    for symbol in symbols:
        try:
            stockPriceChange = get_price_change(symbol)
            industry = get_industry(symbol)
            industryToAllStocks[industry] = industryToAllStocks.get(industry, 0) + 1
            if (stockPriceChange['1Y'] > spyPriceChange['1Y'] and
                    stockPriceChange['3Y'] > spyPriceChange['3Y'] and
                    stockPriceChange['5Y'] > spyPriceChange['5Y'] and stockPriceChange['1Y'] < 3000):
                industyToAllBeatingStocks[industry] = industyToAllBeatingStocks.get(industry, 0) + 1
        except:
            print("Skipped")

    print(industryToAllStocks)
    print(industyToAllBeatingStocks)


def get_industries_outperforming_sorted():
    industryToAllStocksCount = \
        {'Software - Application': 265, 'Computer - Hardware': 39, 'Biotechnology': 725,
         'Pollution & Treatment Controls': 17, 'Engineering & Construction': 37, 'Medical - Instruments & Supplies': 56,
         'Chemicals - Specialty': 55, 'Restaurants': 57, 'REIT - Mortgage': 93, 'Shell Companies': 432,
         'Metal Fabrication': 20, 'Semiconductors': 66, 'Auto - Manufacturers': 44,
         'Drug Manufacturers - Specialty & Generic': 100, 'Agricultural - Inputs': 20, 'Banks - Regional': 433,
         'Metals & Mining - Other Industrial': 29, 'Capital Markets': 85, 'Real Estate - Development': 13,
         'Conglomerates': 24, 'Oil & Gas - Equipment & Services': 51, 'Auto - Parts': 59, 'Department Stores': 6,
         'Utilities - Independent Power Producers': 5, 'Healthcare - Information Services': 70,
         'Oil & Gas - Exploration & Production': 69, 'Oil & Gas - Integrated': 16, None: 174, 'Gambling': 26,
         'Construction - Residential': 24, 'Machinery - Specialty': 74, 'Scientific & Technical Instruments': 38,
         'Banks - Diversified': 48, 'REIT - Healthcare Facilities': 19, 'Communications - Equipment': 65,
         'Building - Products & Equipment': 35, 'Rental & Leasing Services': 37, 'Chemicals': 17, 'Grocery Stores': 12,
         'Security & Protection Services': 28, 'Tools & Accessories': 12, 'Mortgage Finance': 14, 'Credit Services': 71,
         'Retail - Specialty': 99, 'Utilities - Regulated Electric': 47, 'REIT - Specialty': 20,
         'Information Technology Services': 68, 'Medical - Care Facilities': 50, 'Diagnostics & Research': 67,
         'Household & Personal Products': 26, 'Farm & Heavy Construction Machinery': 29, 'Real Estate - Services': 43,
         'Oil & Gas - Midstream': 64, 'Utilities - Regulated Gas': 16, 'Insurance - Life': 35,
         'Education & Training Services': 43, 'Advertising Agencies': 44, 'Farm Products': 27,
         'Food - Packaged Foods': 66, 'Tobacco': 11, 'REIT - Residential': 25, 'Marine Shipping': 46,
         'REIT - Industrial': 39, 'Aerospace & Defense': 75, 'Airlines': 19, 'Packaging & Containers': 24,
         'Insurance - Diversified': 29, 'Asset Management': 244, 'Gold': 29, 'Entertainment': 63,
         'Electrical - Equipment & Parts': 54, 'Software - Packaged': 1, 'Textiles': 4, 'REIT - Retail': 41,
         'Medical - Devices': 156, 'Electronics - Distributors': 10, 'Waste Management': 18,
         'Semiconductors - Equipment & Materials': 29, 'Trucking': 16, 'Home Improvement Retail': 9,
         'Infrastructure Operations': 2, 'Insurance - Specialty': 20, 'Staffing & Employment Services': 26,
         'Electronic - Gaming & Multimedia': 25, 'Furnishings, Fixtures & Appliances': 34,
         'Metals & Mining - Other Precious': 8, 'Apparel - Retail': 35, 'Solar': 26,
         'Electronic - Equipment & Parts': 48, 'Insurance - Property & Casualty': 56, 'Consulting Services': 17,
         'Insurance - Brokers': 18, 'Financial Data & Stock Exchanges': 10, 'Lumber & Wood Production': 5,
         'Utilities - Regulated Water': 15, 'Steel': 21, 'Copper': 4, 'Apparel - Footwear & Accessories': 14,
         'Drug Manufacturers - General': 19, 'Building - Materials': 16, 'Consumer - Electronics': 17,
         'Apparel - Manufacturing': 23, '': 17, 'Personal Products & Services': 16,
         'Business - Equipment & Supplies': 5, 'Software - Infrastructure': 150, 'Coal - Thermal': 7,
         'Business - Speciality Services': 35, 'Real Estate - Diversified': 4, 'Utilities - Renewable': 30,
         'REIT - Diversified': 36, 'Travel Services': 16, 'REIT - Hotel & Motel': 36,
         'Beverages - Wineries & Distilleries': 12, 'Utilities - Diversified': 17, 'Investment - Managers': 3,
         'Financial - Conglomerates': 14, 'Lodging': 15, 'Aluminum': 4, 'Beverages - Alcoholic': 7,
         'Food - Distribution': 11, 'Auto - Truck Dealerships': 30, 'Oil & Gas - Drilling': 11,
         'Internet Content & Information': 69, 'Insurance - Reinsurance': 15, 'Industrial - Distribution': 16,
         'Recreational Vehicles': 18, 'Oil & Gas - Refining & Marketing': 18, 'Beverages - Non-Alcoholic': 18,
         'Integrated Freight & Logistics': 20, 'Broadcasting': 20, 'Luxury Goods': 12, 'Publishing': 10, 'Silver': 3,
         'Resorts & Casinos': 20, 'Medical - Distribution': 9, 'Healthcare - Plans': 11,
         'Telecommunications - Services': 69, 'REIT - Office': 37, 'Leisure': 33, 'Discount Stores': 10, 'Uranium': 4,
         'Airports & Air Services': 10, 'Coal - Coking': 6, 'Pharmaceuticals - Retailers': 11, 'NULL': 4,
         'Confectioners': 4, 'Paper & Forest Products': 6, 'Pharmaceuticals - Major': 1, 'Railroads': 13,
         'Investment - Banking & Investment Services': 1, 'Investment - Banks/Brokers': 1,
         'Manufacturing - Miscellaneous': 1}
    industyToAllBeatingStocksCount = \
        {'Biotechnology': 25, 'Engineering & Construction': 14, 'Shell Companies': 7, 'Construction - Residential': 17,
         'Semiconductors': 9, 'Drug Manufacturers - Specialty & Generic': 4, 'Electrical - Equipment & Parts': 8,
         'Building - Products & Equipment': 16, 'Oil & Gas - Midstream': 5, 'Pollution & Treatment Controls': 1,
         'Aerospace & Defense': 10, 'Trucking': 5, 'Infrastructure Operations': 2, 'Marine Shipping': 8,
         'Waste Management': 3, 'Tools & Accessories': 2, 'Furnishings, Fixtures & Appliances': 3,
         'Farm & Heavy Construction Machinery': 2, 'Steel': 3, 'Building - Materials': 11,
         'Oil & Gas - Exploration & Production': 13, None: 12, 'Credit Services': 4, 'Coal - Thermal': 2,
         'Information Technology Services': 7, 'Consulting Services': 5, 'Retail - Specialty': 7,
         'Metal Fabrication': 4, 'Aluminum': 1, 'Auto - Parts': 1, 'Home Improvement Retail': 3, 'Conglomerates': 3,
         'Semiconductors - Equipment & Materials': 10, 'Industrial - Distribution': 7, 'Rental & Leasing Services': 7,
         'Capital Markets': 9, 'Software - Application': 15, 'Machinery - Specialty': 17,
         'Medical - Instruments & Supplies': 3, 'Insurance - Life': 5, 'Apparel - Retail': 2, 'Computer - Hardware': 6,
         'Oil & Gas - Refining & Marketing': 4, 'Insurance - Brokers': 4, 'Oil & Gas - Equipment & Services': 5,
         'Lodging': 3, 'Medical - Distribution': 3, 'Healthcare - Plans': 2, 'Diagnostics & Research': 3,
         'Scientific & Technical Instruments': 1, 'Electronic - Equipment & Parts': 9,
         'Drug Manufacturers - General': 1, 'Food - Packaged Foods': 3, 'Asset Management': 7,
         'Education & Training Services': 3, 'Insurance - Diversified': 4, 'Restaurants': 4,
         'Household & Personal Products': 1, 'Uranium': 3, 'Insurance - Specialty': 2, 'Packaging & Containers': 1,
         'Food - Distribution': 1, 'Chemicals - Specialty': 7, 'Software - Infrastructure': 9,
         'Medical - Care Facilities': 2, 'Solar': 2, 'Electronics - Distributors': 3, 'Auto - Manufacturers': 4,
         'Gambling': 1, 'Travel Services': 2, 'Business - Speciality Services': 4, 'Real Estate - Services': 1,
         'Apparel - Footwear & Accessories': 2, 'Internet Content & Information': 5, 'Beverages - Non-Alcoholic': 2,
         'Banks - Diversified': 3, 'Grocery Stores': 1, 'Personal Products & Services': 1, 'Coal - Coking': 3,
         'Security & Protection Services': 1, 'Mortgage Finance': 2, 'REIT - Specialty': 1, 'Discount Stores': 1,
         'Resorts & Casinos': 1, 'Auto - Truck Dealerships': 4, 'Leisure': 1, 'Medical - Devices': 3,
         'Department Stores': 1, 'Gold': 1, 'Utilities - Independent Power Producers': 1, 'Lumber & Wood Production': 1,
         'Airports & Air Services': 1, 'Publishing': 1, 'Copper': 1, '': 1, 'Insurance - Property & Casualty': 7,
         'Railroads': 1, 'Metals & Mining - Other Industrial': 1, 'Utilities - Regulated Water': 1,
         'Advertising Agencies': 1, 'Staffing & Employment Services': 1, 'Real Estate - Development': 2,
         'Banks - Regional': 5, 'Utilities - Renewable': 1, 'Consumer - Electronics': 1,
         'Communications - Equipment': 1}

    result = {}
    for key in industryToAllStocksCount:
        if key in industryToAllStocksCount and key in industyToAllBeatingStocksCount:
            result[key] = round(industyToAllBeatingStocksCount[key] / industryToAllStocksCount[key], 4)

    sorted_dict = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    for key in sorted_dict:
        if (key is not None and key != ''):
            print(key + ' : ' + str(sorted_dict[key]))


if __name__ == "__main__":
    # get_data() - Initially run this to gather data
    get_industries_outperforming_sorted()
