using System;
using System.Collections;
using System.Collections.Generic; 

namespace QuantConnect 
{
    using QuantConnect.Securities;
    using QuantConnect.Models; 

    public partial class BasicTemplateAlgorithm : QCAlgorithm, IAlgorithm 
    { 

        string symbol = "MSFT";        

        //Initialize the data and resolution you require for your strategy:
        public override void Initialize() 
        {            
            //Initialize the start, end dates for simulation; cash and data required.
            SetStartDate(2012, 06, 01);
            SetEndDate(DateTime.Now.Date.AddDays(-1)); 
            SetCash(30000); //Starting Cash in USD.
            AddSecurity(SecurityType.Equity, symbol, Resolution.Minute); //Minute, Second or Tick
            SetRunMode(RunMode.Series); //Series or Parallel for intraday strategies.
        }

        //Handle TradeBar Events: a TradeBar occurs on a time-interval (second or minute bars)
        public override void OnTradeBar(Dictionary<string, TradeBar> data) 
        {
            if (Portfolio.HoldStock == false)
            {
                //Orders are processed on leaving the event handler -- currently we have a maximum 20 orders per day.
                Order(symbol, 50); //symbol, quantity
                Debug("Sent order for " + symbol);
            } 
        }
        
        //Handle Tick Events - Only when you're requesting tick data
        public override void OnTick(Dictionary<string, List<Tick>> ticks) 
        {   
            if (Portfolio[symbol].HoldStock == false) 
            {
                Order(symbol, 50);
                Debug("Sent order for " + symbol);
            }
        }
    }
}