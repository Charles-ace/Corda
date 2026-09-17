import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const Header: React.FC = () => {
  const frame = useCurrentFrame();
  const pulse = interpolate(Math.sin(frame / 15), [-1, 1], [0.6, 1.0]);

  return (
    <div
      style={{
        position: "absolute",
        top: 48,
        left: 80,
        right: 80,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        zIndex: 50,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <div
          style={{
            width: 44,
            height: 44,
            borderRadius: "50%",
            background: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 0 24px rgba(16, 185, 129, 0.4)",
          }}
        >
          <span style={{ color: "#030712", fontWeight: 900, fontSize: 24, fontFamily: "sans-serif" }}>C</span>
        </div>
        <div>
          <div style={{ color: "#ffffff", fontWeight: 800, fontSize: 24, letterSpacing: "0.06em", fontFamily: "system-ui, sans-serif" }}>
            CORDA
          </div>
          <div style={{ color: "rgba(255, 255, 255, 0.5)", fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", fontFamily: "monospace" }}>
            Autonomous Privacy Oracle
          </div>
        </div>
      </div>

      {/* Network pill */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "10px 22px",
          borderRadius: 9999,
          background: "rgba(16, 185, 129, 0.08)",
          border: "1px solid rgba(16, 185, 129, 0.25)",
          backdropFilter: "blur(10px)",
        }}
      >
        <div
          style={{
            width: 9,
            height: 9,
            borderRadius: "50%",
            backgroundColor: "#10b981",
            opacity: pulse,
            boxShadow: "0 0 12px #10b981",
          }}
        />
        <span style={{ color: "#10b981", fontSize: 13, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", fontFamily: "monospace" }}>
          GENLAYER STUDIONET 61999 • VERIFIED
        </span>
      </div>
    </div>
  );
};
