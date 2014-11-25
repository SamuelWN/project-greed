using System;
using System.Collections.Generic;
using System.Net;
using jarloo;

namespace Jarloo
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            string csvData;

            using (WebClient web = new WebClient())
            {
                csvData = web.DownloadString("http://finance.yahoo.com/d/quotes.csv?s=AAPL+GOOG+MSFT&f=snbaopl1");
            }

            List<Price> prices = YahooFinance.Parse(csvData);

            foreach (Price price in prices)
            {
                Console.WriteLine(string.Format("{0} ({1})  Bid:{2} Offer:{3} Last:{4} Open: {5} PreviousClose:{6}",price.Name,price.Symbol,price.Bid,price.Ask,price.Last,price.Open,price.PreviousClose));
            }

            Console.Read();

        }
    }
}