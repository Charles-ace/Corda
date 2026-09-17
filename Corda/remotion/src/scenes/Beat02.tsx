import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Beat02: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });
  const alertPulse = interpolate(Math.sin(frame / 8), [-1, 1], [0.8, 1.0]);

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
          transformOrigin: "center",
          scale: `${alertPulse}`,
        }}
      >
        ⚠️ Telemetry Conflict Detected
      </div>

      <h2
        style={{
          opacity: entrance,
          color: "#ffffff",
          fontSize: 54,
          fontWeight: 800,
          textAlign: "center",
          letterSpacing: "-0.02em",
          margin: "0 0 48px 0",
          fontFamily: "system-ui, sans-serif",
        }}
      >
        The Contradiction Exposed
      </h2>

      <div
        style={{
          display: "flex",
          gap: 36,
          width: "100%",
          maxWidth: 1300,
        }}
      >
        {/* Left: Claim */}
        <div
          style={{
            flex: 1,
            background: "rgba(15, 23, 42, 0.85)",
            border: "1px solid rgba(16, 185, 129, 0.35)",
            borderRadius: 18,
            padding: 32,
            boxShadow: "0 20px 50px rgba(0,0,0,0.6)",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
            <span style={{ color: "#34d399", fontWeight: 700, fontSize: 13, fontFamily: "monospace", letterSpacing: "0.1em" }}>
              PRIVACY_POLICY.MD
            </span>
            <span style={{ background: "rgba(16, 185, 129, 0.2)", color: "#34d399", padding: "4px 10px", borderRadius: 6, fontSize: 11, fontWeight: 700 }}>
              CLAIM
            </span>
          </div>

          <div
            style={{
              background: "rgba(3, 7, 18, 0.6)",
              borderRadius: 12,
              padding: 24,
              border: "1px dashed rgba(16, 185, 129, 0.3)",
              fontFamily: "system-ui, sans-serif",
              color: "#e2e8f0",
              fontSize: 20,
              lineHeight: 1.6,
            }}
          >
            "This project is strictly <strong style={{ color: "#34d399" }}>self-hosted</strong> and values developer privacy. <strong style={{ color: "#34d399" }}>We do not collect telemetry</strong>, crash analytics, or usage metrics of any kind."
          </div>
        </div>

        {/* Right: Code */}
        <div
          style={{
            flex: 1.1,
            background: "rgba(15, 23, 42, 0.85)",
            border: "1px solid rgba(239, 68, 68, 0.5)",
            borderRadius: 18,
            padding: 32,
            boxShadow: "0 0 35px rgba(239, 68, 68, 0.2)",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
            <span style={{ color: "#f87171", fontWeight: 700, fontSize: 13, fontFamily: "monospace", letterSpacing: "0.1em" }}>
              APP/TELEMETRY.PY
            </span>
            <span style={{ background: "rgba(239, 68, 68, 0.2)", color: "#f87171", padding: "4px 10px", borderRadius: 6, fontSize: 11, fontWeight: 700 }}>
              GROUND TRUTH
            </span>
          </div>

          <div
            style={{
              background: "rgba(3, 7, 18, 0.85)",
              borderRadius: 12,
              padding: 24,
              border: "1px solid rgba(239, 68, 68, 0.3)",
              fontFamily: "Consolas, Monaco, monospace",
              fontSize: 18,
              lineHeight: 1.7,
            }}
          >
            <div style={{ color: "#f87171", background: "rgba(239, 68, 68, 0.15)", padding: "2px 8px", borderRadius: 4, marginBottom: 6 }}>
              + import posthog
            </div>
            <div style={{ color: "#94a3b8" }}>
              &nbsp;&nbsp;posthog.api_key = "phc_live_992182..."
            </div>
            <div style={{ color: "#f87171", background: "rgba(239, 68, 68, 0.15)", padding: "2px 8px", borderRadius: 4, marginTop: 6 }}>
              + posthog.capture("task_dispatch", payload)
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
