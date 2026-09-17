import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface CursorPosition {
  x: number;
  y: number;
  click?: boolean;
}

interface CursorProps {
  x: number;
  y: number;
  isClicking?: boolean;
}

export const Cursor: React.FC<CursorProps> = ({ x, y, isClicking = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Subtle breathing idle motion
  const idleWiggle = Math.sin(frame / 12) * 1.5;

  return (
    <div
      style={{
        position: "absolute",
        left: x + idleWiggle,
        top: y + idleWiggle,
        pointerEvents: "none",
        zIndex: 9999,
        transform: "translate(-2px, -2px)",
        filter: "drop-shadow(0 4px 12px rgba(0,0,0,0.65))",
        transition: "all 0.05s ease-out",
      }}
    >
      {/* Click Ripple */}
      {isClicking && (
        <div
          style={{
            position: "absolute",
            left: -16,
            top: -16,
            width: 44,
            height: 44,
            borderRadius: "50%",
            border: "2px solid #8b5cf6",
            backgroundColor: "rgba(139, 92, 246, 0.25)",
            animation: "none",
            transform: `scale(${interpolate(frame % 15, [0, 15], [0.4, 1.6])})`,
            opacity: interpolate(frame % 15, [0, 15], [0.9, 0]),
          }}
        />
      )}

      {/* SVG Modern macOS/Figma Cursor */}
      <svg
        width="26"
        height="32"
        viewBox="0 0 26 32"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{
          transform: isClicking ? "scale(0.88)" : "scale(1)",
          transition: "transform 0.08s ease-out",
        }}
      >
        <path
          d="M2.5 1.5L23.5 15.5L12.5 17.5L8.5 28.5L2.5 1.5Z"
          fill="#1E1E2E"
          stroke="#FFFFFF"
          strokeWidth="2.2"
          strokeLinejoin="round"
        />
        <circle cx="5" cy="5" r="2.5" fill="#8B5CF6" />
      </svg>
    </div>
  );
};
