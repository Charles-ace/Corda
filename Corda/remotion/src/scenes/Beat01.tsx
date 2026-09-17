import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Beat01: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleProgress = spring({ frame, fps, config: { damping: 14 } });
  const card1Progress = spring({ frame: frame - 15, fps, config: { damping: 14 } });
  const card2Progress = spring({ frame: frame - 30, fps, config: { damping: 14 } });

  const glowPulse = interpolate(Math.sin(frame / 12), [-1, 1], [0.3, 0.7]);

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "0 120px",
      }}
    >
      {/* Category Pill */}
      <div
        style={{
          opacity: titleProgress,
          transform: `translateY(${interpolate(titleProgress, [0, 1], [20, 0])}px)`,
          padding: "8px 20px",
          borderRadius: 9999,
          background: "rgba(16, 185, 129, 0.12)",
          border: "1px solid rgba(16, 185, 129, 0.3)",
          color: "#34d399",
          fontSize: 13,
          fontWeight: 700,
          letterSpacing: "0.2em",
          textTransform: "uppercase",
          fontFamily: "monospace",
          marginBottom: 24,
        }}
      >
        AI Privacy Verification Protocol
      </div>

      {/* Main Title */}
      <h1
        style={{
          opacity: titleProgress,
          transform: `translateY(${interpolate(titleProgress, [0, 1], [30, 0])}px)`,
          color: "#ffffff",
          fontSize: 68,
          fontWeight: 800,
          textAlign: "center",
          lineHeight: 1.15,
          letterSpacing: "-0.02em",
          fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
          maxWidth: 1300,
          margin: 0,
        }}
      >
        Do Open-Source AI Frameworks <br />
        <span
          style={{
            background: "linear-gradient(135deg, #10b981 0%, #38bdf8 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}
        >
          Keep Their Privacy Promises?
        </span>
      </h1>

      {/* Two Comparison Pillars */}
      <div
        style={{
          display: "flex",
          gap: 40,
          marginTop: 64,
          width: "100%",
          maxWidth: 1200,
        }}
      >
        {/* Left Card: The Promise */}
        <div
          style={{
            flex: 1,
            opacity: card1Progress,
            transform: `translateY(${interpolate(card1Progress, [0, 1], [40, 0])}px)`,
            background: "rgba(15, 23, 42, 0.75)",
            border: "1px solid rgba(56, 189, 248, 0.3)",
            borderRadius: 20,
            padding: 36,
            backdropFilter: "blur(12px)",
            boxShadow: "0 20px 50px rgba(0,0,0,0.5)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 18 }}>
            <div
              style={{
                width: 36,
                height: 36,
                borderRadius: 10,
                background: "rgba(56, 189, 248, 0.15)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#38bdf8",
                fontWeight: 700,
              }}
            >
              ✓
            </div>
            <div style={{ color: "#38bdf8", fontWeight: 700, letterSpacing: "0.1em", fontSize: 13, textTransform: "uppercase", fontFamily: "monospace" }}>
              Public Privacy Policy
            </div>
          </div>
          <div style={{ color: "#e2e8f0", fontSize: 24, fontWeight: 600, lineHeight: 1.4 }}>
            "100% self-hosted, private by design, zero telemetry collected."
          </div>
        </div>

        {/* Right Card: The Codebase */}
        <div
          style={{
            flex: 1,
            opacity: card2Progress,
            transform: `translateY(${interpolate(card2Progress, [0, 1], [40, 0])}px)`,
            background: "rgba(15, 23, 42, 0.75)",
            border: "1px solid rgba(239, 68, 68, 0.3)",
            borderRadius: 20,
            padding: 36,
            backdropFilter: "blur(12px)",
            boxShadow: "0 20px 50px rgba(0,0,0,0.5)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 18 }}>
            <div
              style={{
                width: 36,
                height: 36,
                borderRadius: 10,
                background: "rgba(239, 68, 68, 0.15)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#ef4444",
                fontWeight: 700,
              }}
            >
              ?
            </div>
            <div style={{ color: "#ef4444", fontWeight: 700, letterSpacing: "0.1em", fontSize: 13, textTransform: "uppercase", fontFamily: "monospace" }}>
              Ground Truth Codebase
            </div>
          </div>
          <div style={{ color: "#e2e8f0", fontSize: 24, fontWeight: 600, lineHeight: 1.4 }}>
            "Does the actual executable code respect the disclosure?"
          </div>
        </div>
      </div>
    </div>
  );
};
