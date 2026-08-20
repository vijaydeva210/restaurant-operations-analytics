import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

const API = "http://127.0.0.1:8000/api";

function App() {
  const [summary, setSummary] = useState({});
  const [ordersByHour, setOrdersByHour] = useState([]);
  const [partners, setPartners] = useState([]);
  const [feedback, setFeedback] = useState([]);
  const [orderStatus, setOrderStatus] = useState([]);
  const [returns, setReturns] = useState([]);
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");

        const responses = await Promise.all([
          fetch(`${API}/summary/`),
          fetch(`${API}/orders-by-hour/`),
          fetch(`${API}/delivery-partners/`),
          fetch(`${API}/feedback-categories/`),
          fetch(`${API}/order-status/`),
          fetch(`${API}/returns/`),
        ]);

        for (const response of responses) {
          if (!response.ok) {
            throw new Error("Failed to load dashboard data");
          }
        }

        const [
          summaryData,
          hourlyData,
          partnerData,
          feedbackData,
          statusData,
          returnData,
        ] = await Promise.all(responses.map((response) => response.json()));

        setSummary(summaryData);
        setOrdersByHour(hourlyData);
        setPartners(partnerData);
        setFeedback(feedbackData);
        setOrderStatus(statusData);
        setReturns(returnData);
      } catch (err) {
        console.error(err);
        setError("Unable to load dashboard data.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  const activePartners = partners.filter(
    (partner) =>
      String(partner.status).toLowerCase() === "active"
  ).length;

  const inactivePartners = partners.length - activePartners;

  const partnerChartData = [
    {
      status: "Active",
      count: activePartners,
    },
    {
      status: "Inactive",
      count: inactivePartners,
    },
  ];

  /*
    The backend may return the hourly value as:
    { hour: 10, orders: 5 }
    or
    { hour: 10, count: 5 }

    We normalize it here so the chart always receives:
    { hour: 10, orders: 5 }
  */
  const normalizedHourlyData = ordersByHour.map((item) => ({
    hour: item.hour ?? item.time ?? item.hour_label,
    orders: Number(item.orders ?? item.count ?? item.total ?? 0),
  }));

  if (loading) {
    return (
      <div className="loading-screen">
        <h2>Loading dashboard...</h2>
        <p>Connecting to restaurant analytics data.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-screen">
        <h2>Dashboard unavailable</h2>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="header">
        <div>
          <h1>Restaurant Operations Analytics</h1>
          <p>Real-time operational overview</p>
        </div>

        <div className="status">
          <span></span>
          System Connected
        </div>
      </header>

      <main>
        {/* SUMMARY CARDS */}
        <section className="cards">
          <div className="card">
            <h3>Total Orders</h3>
            <strong>{summary.total_orders ?? 0}</strong>
          </div>

          <div className="card">
            <h3>Delivered</h3>
            <strong>{summary.delivered_orders ?? 0}</strong>
          </div>

          <div className="card">
            <h3>Cancelled</h3>
            <strong>{summary.cancelled_orders ?? 0}</strong>
          </div>

          <div className="card">
            <h3>Total Revenue</h3>
            <strong>
              ₹{Number(summary.total_revenue ?? 0).toLocaleString("en-IN")}
            </strong>
          </div>
        </section>

        {/* ORDERS + STATUS */}
        <section className="grid two">
          <div className="panel">
            <h2>Orders by Hour</h2>

            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={normalizedHourlyData}
                margin={{
                  top: 10,
                  right: 20,
                  left: 0,
                  bottom: 10,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                  dataKey="hour"
                  tickFormatter={(value) => `${value}:00`}
                />

                <YAxis allowDecimals={false} />

                <Tooltip
                  formatter={(value) => [`${value} orders`, "Orders"]}
                  labelFormatter={(label) => `${label}:00`}
                />

                <Line
                  type="monotone"
                  dataKey="orders"
                  stroke="#2563eb"
                  strokeWidth={3}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="panel">
            <h2>Order Status</h2>

            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={orderStatus}
                  dataKey="count"
                  nameKey="status"
                  cx="50%"
                  cy="45%"
                  outerRadius={95}
                  label
                >
                  {orderStatus.map((entry, index) => (
                    <Cell
                      key={index}
                      fill={[
                        "#16a34a",
                        "#dc2626",
                        "#f59e0b",
                        "#2563eb",
                        "#9333ea",
                      ][index % 5]}
                    />
                  ))}
                </Pie>

                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* DELIVERY + FEEDBACK */}
        <section className="grid two">
          <div className="panel">
            <h2>Delivery Partners</h2>

            <div className="partner-summary">
              <div>
                <span className="dot active"></span>
                <strong>{activePartners}</strong>
                <small>Active</small>
              </div>

              <div>
                <span className="dot inactive"></span>
                <strong>{inactivePartners}</strong>
                <small>Inactive</small>
              </div>
            </div>

            <ResponsiveContainer width="100%" height={230}>
              <BarChart data={partnerChartData}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="status" />

                <YAxis allowDecimals={false} />

                <Tooltip />

                <Bar
                  dataKey="count"
                  fill="#2563eb"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="panel">
            <h2>Customer Feedback</h2>

            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={feedback}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="category" />

                <YAxis allowDecimals={false} />

                <Tooltip />

                <Bar
                  dataKey="count"
                  fill="#7c3aed"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* RETURNS */}
        <section className="panel">
          <h2>Returns & Replacements</h2>

          <div className="return-grid">
            {returns.map((item) => (
              <div className="return-item" key={item.type}>
                <strong>{item.count}</strong>
                <span>{item.type}</span>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;