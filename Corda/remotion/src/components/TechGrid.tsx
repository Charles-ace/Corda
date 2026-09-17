import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const TechGrid: React.FC = () => {
  const frame = useCurrentFrame();
  const scanY = (frame * 4) % 1080;
  const pulse = interpolate(Math.sin(frame / 25), [-1, 1], [0.12, 0.28]);

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        backgroundColor: "#030712",
        overflow: "hidden",
        pointerEvents: "none",
      }}
    >
      {/* Perspective grid */}
      <div
        style={{
          position: "absolute",
          inset: -200,
          backgroundImage:
            "linear-gradient(to right, rgba(16, 185, 129, 0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(16, 185, 129, 0.05) 1px, transparent 1px)",
          backgroundSize: "64px 64px",
          transform: "perspective(600px) rotateX(25deg)",
          transformOrigin: "50% 100%",
        }}
      />
      {/* Ambient gradient glow */}
      <div
        style={{
          position: "absolute",
          top: "-15%",
          left: "25%",
          width: "50vw",
          height: "50vh",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, rgba(99, 102, 241, 0.05) 50%, transparent 80%)",
          filter: "blur(80px)",
        }}
      />
      {/* Scanline */}
      <div
        style={{
          position: "absolute",
          top: scanY,
          left: 0,
          right: 0,
          height: "2px",
          background: "linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.45), transparent)",
          boxShadow: "0 0 15px rgba(16, 185, 129, 0.6)",
        }}
      />
      {/* Corner HUD markers */}
      <div style={{ position: "absolute", top: 32, left: 32, width: 28, height: 28, borderTop: "2px solid rgba(16, 185, 129, 0.5)", borderLeft: "2px solid rgba(16, 185, 129, 0.5)" }} />
      <div style={{ position: "absolute", top: 32, right: 32, width: 28, height: 28, borderTop: "2px solid rgba(16, 185, 129, 0.5)", borderRight: "2px solid rgba(16, 185, 129, 0.5)" }} />
      <div style={{ position: "absolute", bottom: 32, left: 32, width: 28, height: 28, borderBottom: "2px solid rgba(16, 185, 129, 0.5)", borderLeft: "2px solid rgba(16, 185, 129, 0.5)" }} />
      <div style={{ position: "absolute", bottom: 32, right: 32, width: 28, height: 28, borderBottom: "2px solid rgba(16, 185, 129, 0.5)", borderRight: "2px solid rgba(16, 185, 129, 0.5)" }} />
    </div>
  );
};
