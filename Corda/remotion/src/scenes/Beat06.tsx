import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Beat06: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });
  const pulse = interpolate(Math.sin(frame / 12), [-1, 1], [0.85, 1.0]);

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
          background: "rgba(16, 185, 129, 0.15)",
          border: "1px solid rgba(16, 185, 129, 0.4)",
          color: "#34d399",
          fontSize: 13,
          fontWeight: 700,
          letterSpacing: "0.2em",
          textTransform: "uppercase",
          fontFamily: "monospace",
          marginBottom: 16,
        }}
      >
        On-Chain Immutability
      </div>

      <h2
        style={{
          opacity: entrance,
          color: "#ffffff",
          fontSize: 50,
          fontWeight: 800,
          textAlign: "center",
          letterSpacing: "-0.02em",
          margin: "0 0 32px 0",
          fontFamily: "system-ui, sans-serif",
        }}
      >
        Tamper-Evident On-Chain Proof
      </h2>

      {/* Explorer Modal Frame */}
      <div
        style={{
          width: "100%",
          maxWidth: 1200,
          background: "rgba(15, 23, 42, 0.95)",
          border: "1px solid rgba(16, 185, 129, 0.35)",
          borderRadius: 20,
          padding: 32,
          boxShadow: "0 25px 70px rgba(0, 0, 0, 0.85)",
          backdropFilter: "blur(24px)",
        }}
      >
        {/* Top bar */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid rgba(255, 255, 255, 0.1)", paddingBottom: 16, marginBottom: 20 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{ width: 10, height: 10, borderRadius: "50%", background: "#10b981", boxShadow: "0 0 10px #10b981" }} />
            <span style={{ color: "#ffffff", fontWeight: 700, fontSize: 14, fontFamily: "monospace" }}>
              GENLAYER STUDIONET EXPLORER (CHAIN ID 61999)
            </span>
          </div>

          <div style={{ display: "flex", gap: 10 }}>
            <span style={{ background: "rgba(16, 185, 129, 0.2)", color: "#34d399", padding: "4px 12px", borderRadius: 6, fontSize: 12, fontWeight: 700, fontFamily: "monospace" }}>
              STATUS: FINALIZED
            </span>
            <span style={{ background: "rgba(16, 185, 129, 0.2)", color: "#34d399", padding: "4px 12px", borderRadius: 6, fontSize: 12, fontWeight: 700, fontFamily: "monospace" }}>
              GENVM RESULT: SUCCESS
            </span>
          </div>
        </div>

        {/* Contract Row */}
        <div style={{ background: "rgba(3, 7, 18, 0.7)", borderRadius: 10, padding: "14px 20px", marginBottom: 14, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ color: "#94a3b8", fontSize: 13, fontFamily: "monospace", textTransform: "uppercase" }}>
            INTELLIGENT CONTRACT
          </span>
          <span style={{ color: "#10b981", fontSize: 15, fontFamily: "monospace", fontWeight: 700 }}>
            0x70c2F7491A2CC7f81AC05ca964a059c05feD3e92
          </span>
        </div>

        {/* Case B Tx */}
        <div style={{ background: "rgba(3, 7, 18, 0.7)", borderRadius: 10, padding: "14px 20px", marginBottom: 14, display: "flex", justifyContent: "space-between", alignItems: "center", borderLeft: "4px solid #ef4444" }}>
          <div>
            <div style={{ color: "#ef4444", fontSize: 11, fontFamily: "monospace", fontWeight: 700, letterSpacing: "0.1em" }}>
              CASE B TRANSACTION (MISMATCH)
            </div>
            <div style={{ color: "#e2e8f0", fontSize: 14, fontFamily: "monospace", fontWeight: 600, marginTop: 4 }}>
              0x5452df20d06d17850778e6a254fe9606944f0d8bb0da050faefe2fd33de0a099
            </div>
          </div>
          <span style={{ color: "#f87171", fontSize: 13, fontWeight: 800, fontFamily: "monospace" }}>
            DISCLOSURE_MISMATCH
          </span>
        </div>

        {/* Case A Tx */}
        <div style={{ background: "rgba(3, 7, 18, 0.7)", borderRadius: 10, padding: "14px 20px", display: "flex", justifyContent: "space-between", alignItems: "center", borderLeft: "4px solid #10b981" }}>
          <div>
            <div style={{ color: "#10b981", fontSize: 11, fontFamily: "monospace", fontWeight: 700, letterSpacing: "0.1em" }}>
              CASE A TRANSACTION (MATCH)
            </div>
            <div style={{ color: "#e2e8f0", fontSize: 14, fontFamily: "monospace", fontWeight: 600, marginTop: 4 }}>
              0xeb63270182d1999633cf71922261ff9e28d8411216019fa0f5e33fd7656c018c
            </div>
          </div>
          <span style={{ color: "#34d399", fontSize: 13, fontWeight: 800, fontFamily: "monospace" }}>
            DISCLOSURE_MATCH
          </span>
        </div>
      </div>
    </div>
  );
};
