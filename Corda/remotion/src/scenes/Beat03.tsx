import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Beat03: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });
  const typing1 = Math.min(38, Math.floor(frame * 1.5));
  const typing2 = Math.min(32, Math.max(0, Math.floor((frame - 25) * 1.5)));

  const repoText = "https://github.com/framework/core-agent".slice(0, typing1);
  const privacyText = "https://framework.dev/privacy.md".slice(0, typing2);

  const buttonActive = frame > 45;
  const buttonGlow = buttonActive ? interpolate(Math.sin(frame / 6), [-1, 1], [0.5, 0.9]) : 0;

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
          background: "rgba(16, 185, 129, 0.12)",
          border: "1px solid rgba(16, 185, 129, 0.3)",
          color: "#10b981",
          fontSize: 13,
          fontWeight: 700,
          letterSpacing: "0.2em",
          textTransform: "uppercase",
          fontFamily: "monospace",
          marginBottom: 20,
        }}
      >
        Oracle Ingestion
      </div>

      <h2
        style={{
          opacity: entrance,
          color: "#ffffff",
          fontSize: 54,
          fontWeight: 800,
          textAlign: "center",
          letterSpacing: "-0.02em",
          margin: "0 0 44px 0",
          fontFamily: "system-ui, sans-serif",
        }}
      >
        Corda Console Ingestion
      </h2>

      {/* Console Frame */}
      <div
        style={{
          width: "100%",
          maxWidth: 960,
          background: "rgba(15, 23, 42, 0.9)",
          border: "1px solid rgba(255, 255, 255, 0.15)",
          borderRadius: 20,
          padding: 36,
          boxShadow: "0 25px 60px rgba(0, 0, 0, 0.7)",
          backdropFilter: "blur(20px)",
        }}
      >
        {/* Input 1 */}
        <div style={{ marginBottom: 24 }}>
          <label style={{ display: "block", color: "#94a3b8", fontSize: 13, fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 10, fontFamily: "monospace" }}>
            Target Repository URL
          </label>
          <div
            style={{
              background: "rgba(3, 7, 18, 0.8)",
              border: "1px solid rgba(16, 185, 129, 0.4)",
              borderRadius: 12,
              padding: "16px 20px",
              fontFamily: "monospace",
              fontSize: 18,
              color: "#34d399",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <span>{repoText}{typing1 < 38 && "▎"}</span>
            <span style={{ fontSize: 12, color: "#64748b" }}>PUBLIC REPO</span>
          </div>
        </div>

        {/* Input 2 */}
        <div style={{ marginBottom: 32 }}>
          <label style={{ display: "block", color: "#94a3b8", fontSize: 13, fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 10, fontFamily: "monospace" }}>
            Privacy Policy URL
          </label>
          <div
            style={{
              background: "rgba(3, 7, 18, 0.8)",
              border: "1px solid rgba(56, 189, 248, 0.4)",
              borderRadius: 12,
              padding: "16px 20px",
              fontFamily: "monospace",
              fontSize: 18,
              color: "#38bdf8",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <span>{privacyText}{frame > 25 && typing2 < 32 && "▎"}</span>
            <span style={{ fontSize: 12, color: "#64748b" }}>MARKDOWN / DOC</span>
          </div>
        </div>

        {/* Action Button */}
        <div
          style={{
            background: buttonActive ? "linear-gradient(135deg, #10b981 0%, #059669 100%)" : "rgba(16, 185, 129, 0.2)",
            border: "1px solid #10b981",
            borderRadius: 14,
            padding: "18px 32px",
            textAlign: "center",
            color: buttonActive ? "#030712" : "#10b981",
            fontWeight: 800,
            fontSize: 18,
            letterSpacing: "0.05em",
            fontFamily: "system-ui, sans-serif",
            boxShadow: buttonActive ? `0 0 30px rgba(16, 185, 129, ${buttonGlow})` : "none",
            transform: buttonActive ? "scale(1.02)" : "scale(1)",
            transition: "all 0.2s ease",
          }}
        >
          {buttonActive ? "⚡ EXECUTING ON-CHAIN ORACLE..." : "INITIALIZE ANALYSIS"}
        </div>
      </div>
    </div>
  );
};
