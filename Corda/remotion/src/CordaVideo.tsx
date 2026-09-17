import React from "react";
import { Audio, Sequence, staticFile } from "remotion";
import { TechGrid } from "./components/TechGrid";
import { Header } from "./components/Header";
import { SubtitleBar } from "./components/SubtitleBar";
import { Beat01 } from "./scenes/Beat01";
import { Beat02 } from "./scenes/Beat02";
import { Beat03 } from "./scenes/Beat03";
import { Beat04 } from "./scenes/Beat04";
import { Beat05 } from "./scenes/Beat05";
import { Beat06 } from "./scenes/Beat06";
import { Beat07 } from "./scenes/Beat07";
import { beats, FPS } from "./timing";

export const CordaVideo: React.FC = () => {
  // Mapping of beat ID to Scene component
  const sceneComponents: Record<string, React.FC> = {
    BEAT_01: Beat01,
    BEAT_02: Beat02,
    BEAT_03: Beat03,
    BEAT_04: Beat04,
    BEAT_05: Beat05,
    BEAT_06: Beat06,
    BEAT_07: Beat07,
  };

  return (
    <div
      style={{
        width: 1920,
        height: 1080,
        position: "relative",
        overflow: "hidden",
        backgroundColor: "#030712",
        fontFamily: "system-ui, -apple-system, sans-serif",
      }}
    >
      {/* Audio Track */}
      <Audio src={staticFile("audio/narration.mp3")} />

      {/* Constant Background HUD Grid */}
      <TechGrid />

      {/* Persistent Brand Header */}
      <Header />

      {/* Beat Scenes */}
      {beats.map((beat) => {
        const SceneComponent = sceneComponents[beat.id] || Beat01;
        const fromFrame = Math.round(beat.start * FPS);
        const durationFrames = Math.max(1, Math.round((beat.end - beat.start) * FPS));

        return (
          <Sequence
            key={beat.id}
            from={fromFrame}
            durationInFrames={durationFrames}
            name={beat.title}
          >
            <SceneComponent />
          </Sequence>
        );
      })}

      {/* Dynamic Subtitle Bar */}
      <SubtitleBar />
    </div>
  );
};
