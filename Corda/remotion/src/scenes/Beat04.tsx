import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Beat04: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });
  const pulse = interpolate(Math.sin(frame / 10), [-1, 1], [0.6, 1.0]);

  const validators = [
    { id: "Validator 01", state: "CRAWL_COMPLETE", color: "#10b981" },
    { id: "Validator 02", state: "CRAWL_COMPLETE", color: "#10b981" },
    { id: "Validator 03", state: "EVALUATING_LLM", color: "#38bdf8" },
    { id: "Validator 04", state: "CRAWL_COMPLETE", color: "#10b981" },
    { id: "Validator 05", state: "EVALUATING_LLM", color: "#38bdf8" },
  ];

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "0 80px",
      }}
    >
      <div
        style={{
          opacity: entrance,
          transform: `translateY(${interpolate(entrance, [0, 1], [20, 0])}px)`,
          padding: "8px 24px",
          borderRadius: 9999,
          background: "rgba(99, 102, 241, 0.15)",
          border: "1px solid rgba(99, 102, 241, 0.4)",
          color: "#818cf8",
          fontSize: 13,
          fontWeight: 700,
          letterSpacing: "0.2em",
          textTransform: "uppercase",
          fontFamily: "monospace",
          marginBottom: 16,
        }}
      >
        GenLayer Consensus Engine
      </div>

      <h2
        style={{
          opacity: entrance,
          color: "#ffffff",
          fontSize: 50,
          fontWeight: 800,
          textAlign: "center",
          letterSpacing: "-0.02em",
          margin: "0 0 36px 0",
          fontFamily: "system-ui, sans-serif",
        }}
      >
        Comparative Principle Consensus
      </h2>

      {/* Architecture Layout */}
      <div style={{ display: "flex", gap: 32, width: "100%", maxWidth: 1300 }}>
        {/* Left: Code Methods */}
        <div
          style={{
            flex: 1,
            background: "rgba(15, 23, 42, 0.85)",
            border: "1px solid rgba(255, 255, 255, 0.12)",
            borderRadius: 18,
            padding: 28,
          }}
        >
          <div style={{ color: "#94a3b8", fontSize: 13, fontWeight: 700, fontFamily: "monospace", letterSpacing: "0.1em", marginBottom: 16 }}>
            INTELLIGENT CONTRACT APIS
          </div>

          {/* gl.nondet.web.get */}
          <div
            style={{
              background: "rgba(3, 7, 18, 0.8)",
              borderRadius: 12,
              padding: "16px 20px",
              border: "1px solid rgba(56, 189, 248, 0.3)",
              marginBottom: 16,
            }}
          >
            <div style={{ color: "#38bdf8", fontFamily: "monospace", fontSize: 16, fontWeight: 700 }}>
              gl.nondet.web.get(url)
            </div>
            <div style={{ color: "#94a3b8", fontSize: 13, marginTop: 6 }}>
              Independent internet crawling by isolated GenVM nodes
            </div>
          </div>

          {/* gl.eq_principle.prompt_comparative */}
          <div
            style={{
              background: "rgba(3, 7, 18, 0.8)",
              borderRadius: 12,
              padding: "16px 20px",
              border: "1px solid rgba(16, 185, 129, 0.3)",
            }}
          >
            <div style={{ color: "#34d399", fontFamily: "monospace", fontSize: 16, fontWeight: 700 }}>
              gl.eq_principle.prompt_comparative()
            </div>
            <div style={{ color: "#94a3b8", fontSize: 13, marginTop: 6 }}>
              Substantive multi-validator semantic judgment under strict principle
            </div>
          </div>
        </div>

        {/* Right: Validator Nodes Status */}
        <div
          style={{
            flex: 1.2,
            background: "rgba(15, 23, 42, 0.85)",
            border: "1px solid rgba(16, 185, 129, 0.3)",
            borderRadius: 18,
            padding: 28,
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
            <span style={{ color: "#94a3b8", fontSize: 13, fontWeight: 700, fontFamily: "monospace", letterSpacing: "0.1em" }}>
              DECENTRALIZED VALIDATORS (5/5)
            </span>
            <span style={{ color: "#10b981", fontSize: 13, fontWeight: 700, fontFamily: "monospace" }}>
              ACTIVE CONSENSUS
            </span>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {validators.map((v, i) => (
              <div
                key={v.id}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  background: "rgba(3, 7, 18, 0.7)",
                  border: "1px solid rgba(255, 255, 255, 0.08)",
                  borderRadius: 10,
                  padding: "12px 18px",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <div
                    style={{
                      width: 10,
                      height: 10,
                      borderRadius: "50%",
                      background: v.color,
                      boxShadow: `0 0 8px ${v.color}`,
                    }}
                  />
                  <span style={{ color: "#f3f4f6", fontFamily: "monospace", fontSize: 15, fontWeight: 600 }}>
                    {v.id}
                  </span>
                </div>
                <span
                  style={{
                    color: v.color,
                    fontSize: 12,
                    fontFamily: "monospace",
                    fontWeight: 700,
                    letterSpacing: "0.05em",
                  }}
                >
                  {frame > 30 ? "VOTED: MISMATCH" : v.state}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
