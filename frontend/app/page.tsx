"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Status = "idle" | "loading" | "error" | "done";

export default function Home() {
  const [topic, setTopic] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState("");
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!topic.trim() || status === "loading") return;

    if (pdfUrl) URL.revokeObjectURL(pdfUrl);
    setPdfUrl(null);
    setError("");
    setStatus("loading");

    try {
      const res = await fetch(`${API_URL}/api/generate/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: topic.trim() }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.error || `Request failed (${res.status})`);
      }

      const blob = await res.blob();
      setPdfUrl(URL.createObjectURL(blob));
      setStatus("done");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
      setStatus("error");
    }
  }

  return (
    <main>
      <div className="card">
        <div>
          <h1>Research &amp; Blog Generator</h1>
          <p className="subtitle">
            Enter a topic and get a short, fun blog post as a PDF.
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="e.g. Quantum Computing"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            disabled={status === "loading"}
          />
          <button type="submit" disabled={status === "loading" || !topic.trim()}>
            {status === "loading" ? "Generating…" : "Generate PDF"}
          </button>
        </form>

        {status === "loading" && (
          <p className="status">
            Researching and writing your blog post — this can take a minute or two.
          </p>
        )}

        {status === "error" && <p className="error">{error}</p>}

        {status === "done" && pdfUrl && (
          <a className="download" href={pdfUrl} download="blog.pdf">
            Download PDF
          </a>
        )}
      </div>
    </main>
  );
}
