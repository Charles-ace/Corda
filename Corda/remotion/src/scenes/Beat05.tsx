import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Beat05: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });
  const badgePulse = interpolate(Math.sin(frame / 8), [-1, 1], [0.95, 1.05]);

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "0 100px",
      }}
    >
      <div
        style={{
          opacity: entrance,
          transform: `translateY(${interpolate(entrance, [0, 1], [20, 0])}px)`,
          padding: "8px 24px",
          borderRadius: 9999,
          background: "rgba(239, 68, 68, 0.15)",
          border: "1px solid rgba(239, 68, 68, 0.4)",
          color: "#f87171",
          fontSize: 13,
          fontWeight: 700,
          letterSpacing: "0.2em",
          textTransform: "uppercase",
          fontFamily: "monospace",
          marginBottom: 20,
        }}
      >
        Consensus Finalized
      </div>

      <h2
        style={{
          opacity: entrance,
          color: "#ffffff",
          fontSize: 52,
          fontWeight: 800,
          textAlign: "center",
          letterSpacing: "-0.02em",
          margin: "0 0 32px 0",
          fontFamily: "system-ui, sans-serif",
        }}
      >
        The Finalized Verdict
      </h2>

      {/* Main Report Card */}
      <div
        style={{
          width: "100%",
          maxWidth: 1100,
          background: "rgba(15, 23, 42, 0.9)",
          border: "1px solid rgba(239, 68, 68, 0.4)",
          borderRadius: 20,
          padding: 36,
          boxShadow: "0 20px 60px rgba(0, 0, 0, 0.8)",
          backdropFilter: "blur(20px)",
        }}
      >
        {/* Verdict Banner */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            background: "rgba(239, 68, 68, 0.12)",
            border: "1px solid rgba(239, 68, 68, 0.4)",
            borderRadius: 14,
            padding: "18px 28px",
            marginBottom: 28,
            transform: `scale(${badgePulse})`,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <span style={{ fontSize: 28 }}>🚨</span>
            <div>
              <div style={{ color: "#f87171", fontSize: 12, fontWeight: 700, letterSpacing: "0.15em", textTransform: "uppercase", fontFamily: "monospace" }}>
                DECISION ORACLE
              </div>
              <div style={{ color: "#ffffff", fontSize: 28, fontWeight: 900, letterSpacing: "0.02em" }}>
                DISCLOSURE_MISMATCH
              </div>
            </div>
          </div>

          <div
            style={{
              padding: "8px 18px",
              borderRadius: 8,
              background: "rgba(16, 185, 129, 0.2)",
              color: "#34d399",
              fontSize: 13,
              fontWeight: 800,
              fontFamily: "monospace",
            }}
          >
            CONSENSUS REACHED (5/5)
          </div>
        </div>

        {/* Details Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
          <div
            style={{
              background: "rgba(3, 7, 18, 0.7)",
              borderRadius: 12,
              padding: 20,
              border: "1px solid rgba(255, 255, 255, 0.08)",
            }}
          >
            <div style={{ color: "#94a3b8", fontSize: 12, fontWeight: 700, fontFamily: "monospace", textTransform: "uppercase", marginBottom: 8 }}>
              DISCLOSED CLAIM
            </div>
            <div style={{ color: "#cbd5e1", fontSize: 15, lineHeight: 1.5 }}>
              The project asserts zero telemetry collection and 100% self-hosted operation.
            </div>
          </div>

          <div
            style={{
              background: "rgba(3, 7, 18, 0.7)",
              borderRadius: 12,
              padding: 20,
              border: "1px solid rgba(239, 68, 68, 0.3)",
            }}
          >
            <div style={{ color: "#f87171", fontSize: 12, fontWeight: 700, fontFamily: "monospace", textTransform: "uppercase", marginBottom: 8 }}>
              EVIDENCE EXTRACTED
            </div>
            <div style={{ color: "#cbd5e1", fontSize: 15, lineHeight: 1.5 }}>
              Active PostHog telemetry initialization detected in `app/telemetry.py` transmitting task dispatch events.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
