import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Beat07: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoScale = spring({ frame, fps, config: { damping: 12 } });
  const textEntrance = spring({ frame: frame - 15, fps, config: { damping: 14 } });
  const pulse = interpolate(Math.sin(frame / 15), [-1, 1], [0.85, 1.05]);

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
      {/* Emblem */}
      <div
        style={{
          transform: `scale(${logoScale})`,
          width: 96,
          height: 96,
          borderRadius: "50%",
          background: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          boxShadow: "0 0 50px rgba(16, 185, 129, 0.5)",
          marginBottom: 32,
        }}
      >
        <span style={{ color: "#030712", fontWeight: 900, fontSize: 52, fontFamily: "system-ui, sans-serif" }}>
          C
        </span>
      </div>

      {/* Main Anthem */}
      <h1
        style={{
          opacity: textEntrance,
          transform: `translateY(${interpolate(textEntrance, [0, 1], [30, 0])}px)`,
          color: "#ffffff",
          fontSize: 64,
          fontWeight: 900,
          textAlign: "center",
          lineHeight: 1.15,
          letterSpacing: "-0.03em",
          fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
          maxWidth: 1200,
          margin: 0,
        }}
      >
        Claims are easy. <br />
        <span
          style={{
            background: "linear-gradient(135deg, #10b981 0%, #38bdf8 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}
        >
          Evidence is harder.
        </span>
      </h1>

      <div
        style={{
          opacity: textEntrance,
          marginTop: 24,
          color: "#94a3b8",
          fontSize: 22,
          fontWeight: 600,
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          fontFamily: "monospace",
        }}
      >
        CORDA — POWERED BY GENLAYER
      </div>

      {/* CTA Button */}
      <div
        style={{
          opacity: textEntrance,
          marginTop: 44,
          padding: "16px 36px",
          borderRadius: 9999,
          background: "rgba(16, 185, 129, 0.15)",
          border: "1px solid #10b981",
          color: "#10b981",
          fontSize: 16,
          fontWeight: 800,
          letterSpacing: "0.1em",
          textTransform: "uppercase",
          fontFamily: "monospace",
          boxShadow: `0 0 30px rgba(16, 185, 129, ${pulse * 0.4})`,
        }}
      >
        studio.genlayer.com • contract 0x70c2...3e92
      </div>
    </div>
  );
};
