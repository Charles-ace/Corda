import React from "react";
import { Composition } from "remotion";
import { CordaVideo } from "./CordaVideo";
import { CordaCinematic } from "./CordaCinematic";
import { TOTAL_DURATION_FRAMES, FPS } from "./timing";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="CordaDemo"
        component={CordaVideo}
        durationInFrames={TOTAL_DURATION_FRAMES}
        fps={FPS}
        width={1920}
        height={1080}
      />
      <Composition
        id="CordaCinematic"
        component={CordaCinematic}
        durationInFrames={TOTAL_DURATION_FRAMES}
        fps={FPS}
        width={1920}
        height={1080}
      />
    </>
  );
};
