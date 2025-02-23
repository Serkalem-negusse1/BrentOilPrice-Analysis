import React, { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

const Dashboard = () => {
  const [prices, setPrices] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [events, setEvents] = useState([]);
  const [forecast, setForecast] = useState([]);

  useEffect(() => {
    const fetchHistoricalPrices = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/historical_prices");
        setPrices(res.data);
      } catch (error) {
        console.error("Error fetching historical prices:", error);
      }
    };

    const fetchChangePoints = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/change_points");
        setChangePoints(res.data);
      } catch (error) {
        console.error("Error fetching change points:", error);
      }
    };

    const fetchEventImpact = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/event_impact");
        setEvents(res.data);
      } catch (error) {
        console.error("Error fetching event impact:", error);
      }
    };

    const fetchForecast = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/forecast");
        setForecast(res.data);
      } catch (error) {
        console.error("Error fetching forecast:", error);
      }
    };

    fetchHistoricalPrices();
    fetchChangePoints();
    fetchEventImpact();
    fetchForecast();
  }, []);

  return (
    <div>
      <h1>Brent Oil Price Dashboard</h1>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={prices}>
          <XAxis dataKey="Date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Price" stroke="blue" />
        </LineChart>
      </ResponsiveContainer>

      <h2>Predicted Oil Prices</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={forecast}>
          <XAxis dataKey="Date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="ARIMA_Forecast" stroke="red" />
          <Line type="monotone" dataKey="GARCH_Forecast" stroke="green" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Dashboard;
