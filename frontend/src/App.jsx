import { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:5000";

export default function App() {
  const [username, setUsername] = useState("sabrina");
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [limit, setLimit] = useState(50);
  const [error, setError] = useState("");

  const fetchArticles = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/api/articles/${username}?limit=${limit}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setArticles(data);
    } catch (e) {
      setError(e.message || "Failed to fetch");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArticles();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div style={{ maxWidth: 900, margin: "2rem auto", fontFamily: "system-ui, Arial" }}>
      <h1>Personalized News</h1>

      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="username"
          style={{ padding: 8, flex: 1 }}
        />
        <input
          type="number"
          min="1"
          max="200"
          value={limit}
          onChange={(e) => setLimit(e.target.value)}
          style={{ width: 100, padding: 8 }}
        />
        <button onClick={fetchArticles} style={{ padding: "8px 12px", cursor: "pointer" }}>
          Refresh
        </button>
      </div>

      {loading && <p>Loading…</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <div style={{ display: "grid", gap: 12 }}>
        {articles.map((a) => (
          <article key={a._id} style={{
            border: "1px solid #ddd",
            borderRadius: 8,
            padding: 12
          }}>
            <div style={{ fontSize: 12, opacity: 0.7, marginBottom: 4 }}>
              {a.source} • {a.published || ""}
            </div>
            <a href={a.link} target="_blank" rel="noreferrer" style={{ fontSize: 18, fontWeight: 600 }}>
              {a.title}
            </a>
            {a.summary && <p style={{ marginTop: 8 }}>{a.summary}</p>}
          </article>
        ))}
      </div>
    </div>
  );
}
