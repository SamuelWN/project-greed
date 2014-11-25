
using System;
using System.Collections.Generic;
 
namespace Jarloo.YahooHistoricalLoader
{
    class Program
    {
        static void Main(string[] args)
        {
            List<HistoricalStock> data = HistoricalStockDownloader.DownloadData("AAPL", 1962);
 
            foreach (HistoricalStock stock in data)
            {
                Console.WriteLine(string.Format("Date={0} High={1} Low={2} Open={3} Close{4}",
				                                stock.Date,stock.High,stock.Low,stock.Open,stock.Close));
            }
 
            Console.Read();
        }
    }
}