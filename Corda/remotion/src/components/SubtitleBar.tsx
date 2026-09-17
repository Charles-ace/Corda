import React from "react";
import { useCurrentFrame } from "remotion";
import { beats, FPS } from "../timing";

export const SubtitleBar: React.FC = () => {
  const frame = useCurrentFrame();
  const currentSeconds = frame / FPS;

  // Find active beat
  const activeBeat = beats.find(b => currentSeconds >= b.start && currentSeconds < b.end) || beats[beats.length - 1];

  return (
    <div
      style={{
        position: "absolute",
        bottom: 50,
        left: 140,
        right: 140,
        display: "flex",
        justifyContent: "center",
        zIndex: 50,
      }}
    >
      <div
        style={{
          background: "rgba(10, 15, 30, 0.88)",
          border: "1px solid rgba(255, 255, 255, 0.15)",
          borderRadius: 14,
          padding: "16px 36px",
          maxWidth: 1300,
          textAlign: "center",
          boxShadow: "0 10px 40px rgba(0, 0, 0, 0.7)",
          backdropFilter: "blur(20px)",
        }}
      >
        <span
          style={{
            color: "#f9fafb",
            fontSize: 22,
            fontWeight: 500,
            lineHeight: 1.45,
            fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
            letterSpacing: "0.01em",
          }}
        >
          {activeBeat ? activeBeat.text : ""}
        </span>
      </div>
    </div>
  );
};
