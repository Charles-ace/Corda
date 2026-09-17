import React from "react";
import {
  Audio,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import { Cursor } from "./components/Cursor";
import { TechGrid } from "./components/TechGrid";
import { Header } from "./components/Header";
import { SubtitleBar } from "./components/SubtitleBar";
import { beats, FPS } from "./timing";

export const CordaCinematic: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const time = frame / fps;

  // Active beat
  const activeBeat = beats.find((b) => time >= b.start && time < b.end) || beats[beats.length - 1];

  // =========================================================================
  // CAMERA ENGINE (Pan, Zoom, Tilt based on narrative beats)
  // =========================================================================
  let targetScale = 1.0;
  let targetPanX = 0;
  let targetPanY = 0;
  let targetRotateX = 0;
  let targetRotateY = 0;

  if (time < 11.91) {
    // BEAT 01: Hero Monumental - Slow majestic zoom & slight 3D perspective
    targetScale = interpolate(time, [0, 11.91], [1.02, 1.12], { easing: Easing.out(Easing.cubic) });
    targetPanX = interpolate(time, [0, 11.91], [0, -60]);
    targetPanY = interpolate(time, [0, 11.91], [0, -30]);
    targetRotateX = interpolate(time, [0, 11.91], [4, 0]);
  } else if (time < 28.15) {
    // BEAT 02: Code Contradiction - Focus zoom on the PostHog line in code editor
    const t = time - 11.91;
    targetScale = interpolate(t, [0, 5, 16], [1.08, 1.35, 1.38], { easing: Easing.inOut(Easing.quad) });
    targetPanX = interpolate(t, [0, 6, 16], [-20, -260, -280]);
    targetPanY = interpolate(t, [0, 6, 16], [-10, 40, 50]);
    targetRotateY = -2;
  } else if (time < 39.52) {
    // BEAT 03: Console Ingestion & Typewriter - Pan down to input boxes
    const t = time - 28.15;
    targetScale = interpolate(t, [0, 4, 11], [1.15, 1.28, 1.25], { easing: Easing.inOut(Easing.cubic) });
    targetPanX = interpolate(t, [0, 5, 11], [0, 40, 50]);
    targetPanY = interpolate(t, [0, 5, 11], [40, -100, -110]);
  } else if (time < 52.52) {
    // BEAT 04: GenLayer Comparative Consensus - Stepper & 5 Validators
    const t = time - 39.52;
    targetScale = interpolate(t, [0, 4, 13], [1.2, 1.32, 1.28], { easing: Easing.inOut(Easing.cubic) });
    targetPanX = interpolate(t, [0, 6, 13], [0, -40, -20]);
    targetPanY = interpolate(t, [0, 6, 13], [-80, -40, -50]);
  } else if (time < 64.43) {
    // BEAT 05: Finalized Verdict - Pull back to reveal large red Mismatch badge
    const t = time - 52.52;
    targetScale = interpolate(t, [0, 3, 11], [1.25, 1.15, 1.12], { easing: Easing.out(Easing.cubic) });
    targetPanX = interpolate(t, [0, 11], [0, 10]);
    targetPanY = interpolate(t, [0, 11], [-30, 10]);
    targetRotateX = 2;
  } else if (time < 79.05) {
    // BEAT 06: Tamper-Evident On-Chain Proof - Focus on Contract Address & Tx Hash
    const t = time - 64.43;
    targetScale = interpolate(t, [0, 4, 14], [1.12, 1.28, 1.24], { easing: Easing.inOut(Easing.quad) });
    targetPanX = interpolate(t, [0, 7, 14], [0, 120, 130]);
    targetPanY = interpolate(t, [0, 7, 14], [10, -70, -60]);
  } else {
    // BEAT 07: Closing Anthem - Majestic wide center with particle aura
    const t = time - 79.05;
    targetScale = interpolate(t, [0, 3.8], [1.15, 1.0], { easing: Easing.out(Easing.cubic) });
    targetPanX = 0;
    targetPanY = 0;
  }

  // Smooth camera spring
  const scale = targetScale;
  const panX = targetPanX;
  const panY = targetPanY;
  const rotX = targetRotateX;
  const rotY = targetRotateY;

  // =========================================================================
  // VIRTUAL CURSOR PATH ENGINE (Coordinates & Click state per narrative beat)
  // =========================================================================
  let cursorX = 1400;
  let cursorY = 800;
  let isClicking = false;

  if (time < 11.91) {
    // Beat 1: Glides from bottom right across the hero title
    cursorX = interpolate(time, [0, 6, 11.91], [1400, 960, 850], { easing: Easing.inOut(Easing.quad) });
    cursorY = interpolate(time, [0, 6, 11.91], [850, 460, 420], { easing: Easing.inOut(Easing.quad) });
  } else if (time < 28.15) {
    // Beat 2: Enters Code Window, traces 'import posthog' and 'posthog.capture()'
    const t = time - 11.91;
    cursorX = interpolate(t, [0, 5, 10, 16], [850, 1280, 1310, 1360]);
    cursorY = interpolate(t, [0, 5, 10, 16], [420, 390, 480, 590]);
    // Click / hover highlight at 6s and 12s
    isClicking = (t >= 5.0 && t <= 5.8) || (t >= 11.5 && t <= 12.3);
  } else if (time < 39.52) {
    // Beat 3: Glides to 'Case B Preset' pill, clicks, then moves to 'Execute Audit'
    const t = time - 28.15;
    if (t < 4.0) {
      cursorX = interpolate(t, [0, 3.5], [1360, 720], { easing: Easing.inOut(Easing.quad) });
      cursorY = interpolate(t, [0, 3.5], [590, 480], { easing: Easing.inOut(Easing.quad) });
      isClicking = t >= 3.0 && t <= 3.8;
    } else {
      cursorX = interpolate(t, [4.0, 9.0], [720, 960], { easing: Easing.inOut(Easing.quad) });
      cursorY = interpolate(t, [4.0, 9.0], [480, 760], { easing: Easing.inOut(Easing.quad) });
      isClicking = t >= 8.2 && t <= 9.0;
    }
  } else if (time < 52.52) {
    // Beat 4: Hovers over the Consensus Stepper and independent validators
    const t = time - 39.52;
    cursorX = interpolate(t, [0, 4, 8, 12], [960, 740, 1100, 1300], { easing: Easing.inOut(Easing.quad) });
    cursorY = interpolate(t, [0, 4, 8, 12], [760, 520, 520, 520], { easing: Easing.inOut(Easing.quad) });
  } else if (time < 64.43) {
    // Beat 5: Hovers over the red Mismatch badge and extracted telemetry citation
    const t = time - 52.52;
    cursorX = interpolate(t, [0, 5, 11], [1300, 960, 980], { easing: Easing.inOut(Easing.quad) });
    cursorY = interpolate(t, [0, 5, 11], [520, 440, 580], { easing: Easing.inOut(Easing.quad) });
  } else if (time < 79.05) {
    // Beat 6: Glides to Contract explorer link and clicks it
    const t = time - 64.43;
    cursorX = interpolate(t, [0, 6, 12], [980, 1220, 1320], { easing: Easing.inOut(Easing.quad) });
    cursorY = interpolate(t, [0, 6, 12], [580, 620, 620], { easing: Easing.inOut(Easing.quad) });
    isClicking = t >= 8.5 && t <= 9.5;
  } else {
    // Beat 7: Fades cursor away to bottom right
    cursorX = 1600;
    cursorY = 950;
  }

  // =========================================================================
  // TYPEWRITER EFFECT (For Beat 03 URL inputs)
  // =========================================================================
  const fullRepoUrl = "https://gist.github.com/case_b_cloudswarm_code.py";
  const fullPrivacyUrl = "https://gist.github.com/case_b_privacy_policy.md";
  const typeDuration = 3.5; // seconds
  let typedRepo = fullRepoUrl;
  let typedPrivacy = fullPrivacyUrl;

  if (time < 28.15) {
    typedRepo = "";
    typedPrivacy = "";
  } else if (time < 39.52) {
    const t = time - 28.15 - 3.5; // Starts typing after preset click
    if (t <= 0) {
      typedRepo = "";
      typedPrivacy = "";
    } else {
      const charCountRepo = Math.min(fullRepoUrl.length, Math.floor((t / typeDuration) * fullRepoUrl.length));
      typedRepo = fullRepoUrl.substring(0, charCountRepo);
      const charCountPriv = Math.min(fullPrivacyUrl.length, Math.floor((t / typeDuration) * fullPrivacyUrl.length));
      typedPrivacy = fullPrivacyUrl.substring(0, charCountPriv);
    }
  }

  // =========================================================================
  // CONSENSUS STEPPER ACTIVATION
  // =========================================================================
  let step1Active = false;
  let step2Active = false;
  let step3Active = false;
  let step4Active = false;

  if (time >= 37.0 && time < 41.5) step1Active = true;
  if (time >= 41.5 && time < 45.5) { step1Active = true; step2Active = true; }
  if (time >= 45.5 && time < 49.0) { step1Active = true; step2Active = true; step3Active = true; }
  if (time >= 49.0) { step1Active = true; step2Active = true; step3Active = true; step4Active = true; }

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

      {/* Virtual Camera Container */}
      <div
        style={{
          width: 1920,
          height: 1080,
          position: "absolute",
          transformOrigin: "center center",
          transform: `perspective(1200px) scale(${scale}) translate3d(${panX}px, ${panY}px, 0) rotateX(${rotX}deg) rotateY(${rotY}deg)`,
          transition: "transform 0.08s ease-out",
        }}
      >
        {/* Background Grid & Aurora Mesh */}
        <TechGrid />

        {/* Ambient Radial Glow */}
        <div
          style={{
            position: "absolute",
            top: "20%",
            left: "30%",
            width: 800,
            height: 800,
            borderRadius: "50%",
            background: "radial-gradient(circle, rgba(139, 92, 246, 0.12) 0%, rgba(16, 185, 129, 0.04) 50%, transparent 70%)",
            filter: "blur(60px)",
            pointerEvents: "none",
          }}
        />

        {/* ================================================================= */}
        {/* SCENE CONTENT LAYER                                              */}
        {/* ================================================================= */}

        {/* BEAT 01: The Privacy Question (Monumental Hero) */}
        {time < 11.91 && (
          <div style={{ position: "absolute", top: 180, left: 160, right: 160, display: "flex", justifyContent: "space-between", alignItems: "flex-end" }}>
            <div style={{ maxWidth: 1050 }}>
              <div style={{ display: "inline-flex", alignItems: "center", gap: 10, padding: "8px 18px", borderRadius: 999, background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", marginBottom: 28 }}>
                <span style={{ width: 10, height: 10, borderRadius: "50%", backgroundColor: "#10b981", boxShadow: "0 0 12px #10b981" }} />
                <span style={{ fontFamily: "monospace", fontSize: 13, color: "#9ca3af", letterSpacing: "0.08em" }}>GENLAYER STUDIONET LIVE (CHAIN ID 61999)</span>
              </div>
              <h1 style={{ fontSize: 88, fontWeight: 900, lineHeight: 0.96, letterSpacing: "-0.04em", textTransform: "uppercase", color: "#f9fafb", margin: 0 }}>
                WITNESS<br />
                <span style={{ color: "rgba(255,255,255,0.92)" }}>THE REALITY</span><br />
                <span style={{ color: "rgba(255,255,255,0.8)" }}>OF PRIVACY CLAIMS</span><br />
                <span style={{ color: "#8b5cf6", textShadow: "0 0 40px rgba(139,92,246,0.6)" }}>ON CHAIN</span>
              </h1>
            </div>

            {/* Chamfered Protocol Mission HUD */}
            <div style={{ width: 440, padding: 32, borderRadius: 20, background: "rgba(10, 15, 30, 0.75)", border: "1px solid rgba(255,255,255,0.15)", backdropFilter: "blur(20px)", boxShadow: "0 20px 50px rgba(0,0,0,0.6)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
                <span style={{ fontFamily: "monospace", fontSize: 13, fontWeight: 700, color: "#8b5cf6" }}>PROTOCOL MISSION</span>
                <span style={{ fontFamily: "monospace", fontSize: 12, color: "#6b7280" }}>01 / GENVM</span>
              </div>
              <p style={{ color: "#e5e7eb", fontSize: 17, lineHeight: 1.6, fontWeight: 300, margin: 0 }}>
                Broadcast trustworthy proofs on the GenLayer Intelligent Contract network. Verifying whether open-source AI frameworks live up to their public privacy claims.
              </p>
              <div style={{ marginTop: 24, paddingTop: 16, borderTop: "1px solid rgba(255,255,255,0.1)", display: "flex", justifyContent: "space-between", fontFamily: "monospace", fontSize: 13 }}>
                <span style={{ color: "#9ca3af" }}>Comparative Consensus</span>
                <span style={{ color: "#10b981", fontWeight: 700 }}>100% On-Chain</span>
              </div>
            </div>
          </div>
        )}

        {/* BEAT 02: Contradiction Exposed (Side-by-Side Split View) */}
        {time >= 11.91 && time < 28.15 && (
          <div style={{ position: "absolute", top: 160, left: 140, right: 140, display: "flex", gap: 40 }}>
            {/* Left: Documentation Claim */}
            <div style={{ flex: 1, padding: 36, borderRadius: 20, background: "rgba(10, 15, 30, 0.8)", border: "1px solid rgba(255,255,255,0.12)", backdropFilter: "blur(20px)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20 }}>
                <span style={{ width: 10, height: 10, borderRadius: "50%", backgroundColor: "#38bdf8" }} />
                <span style={{ fontFamily: "monospace", fontSize: 13, color: "#38bdf8", fontWeight: 700 }}>MARKETING POLICY CLAIM</span>
              </div>
              <div style={{ padding: 24, borderRadius: 14, background: "rgba(56, 189, 248, 0.08)", border: "1px solid rgba(56, 189, 248, 0.3)", marginBottom: 24 }}>
                <p style={{ fontSize: 26, fontWeight: 600, color: "#f0f9ff", lineHeight: 1.4, margin: 0 }}>
                  "Self-hosted, 100% private. No telemetry or usage tracking is ever collected or dispatched."
                </p>
              </div>
              <div style={{ fontFamily: "monospace", fontSize: 13, color: "#9ca3af" }}>
                Source: <span style={{ color: "#e5e7eb" }}>docs.cloudswarm.ai/privacy.md</span>
              </div>
            </div>

            {/* Right: Actual Code Window */}
            <div style={{ flex: 1.2, padding: 36, borderRadius: 20, background: "rgba(5, 8, 16, 0.92)", border: "1px solid rgba(239, 68, 68, 0.3)", backdropFilter: "blur(20px)", boxShadow: "0 0 40px rgba(239, 68, 68, 0.15)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
                <span style={{ fontFamily: "monospace", fontSize: 13, color: "#ef4444", fontWeight: 700 }}>ACTUAL CODE REPOSITORY AST</span>
                <span style={{ fontFamily: "monospace", fontSize: 12, color: "#9ca3af" }}>agent_runtime.py</span>
              </div>
              <pre style={{ margin: 0, fontFamily: "monospace", fontSize: 17, lineHeight: 1.8, color: "#9ca3af" }}>
                <div>1  import os, sys, json</div>
                <div>2  from datetime import datetime</div>
                <div style={{ color: "#ef4444", fontWeight: 700, backgroundColor: "rgba(239, 68, 68, 0.15)", padding: "2px 8px", borderRadius: 6 }}>
                  3  <span style={{ color: "#f87171" }}>import</span> posthog  <span style={{ color: "#ef4444" }}># &lt;-- TELEMETRY SDK IMPORTED</span>
                </div>
                <div>4</div>
                <div>11 class TaskDispatcher:</div>
                <div style={{ color: "#ef4444", fontWeight: 700, backgroundColor: "rgba(239, 68, 68, 0.15)", padding: "2px 8px", borderRadius: 6 }}>
                  12     posthog.api_key = os.getenv("POSTHOG_API_KEY")
                </div>
                <div>27     def dispatch(self, task):</div>
                <div style={{ color: "#ef4444", fontWeight: 700, backgroundColor: "rgba(239, 68, 68, 0.25)", padding: "2px 8px", borderRadius: 6, boxShadow: "0 0 20px rgba(239, 68, 68, 0.4)" }}>
                  28         posthog.capture("task_dispatched", task.meta)  <span style={{ color: "#fca5a5" }}># VIOLATION</span>
                </div>
              </pre>
            </div>
          </div>
        )}

        {/* BEAT 03: Corda Console Ingestion & Typewriter */}
        {time >= 28.15 && time < 39.52 && (
          <div style={{ position: "absolute", top: 160, left: 240, right: 240, background: "rgba(10, 15, 30, 0.88)", border: "1px solid rgba(255, 255, 255, 0.15)", borderRadius: 24, padding: 44, backdropFilter: "blur(24px)", boxShadow: "0 30px 80px rgba(0,0,0,0.8)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 32 }}>
              <div>
                <h2 style={{ fontSize: 32, fontWeight: 800, color: "#ffffff", margin: 0 }}>Corda Zero-Wallet Audit Console</h2>
                <p style={{ color: "#9ca3af", fontSize: 15, marginTop: 4, marginBottom: 0 }}>Autonomous verification via GenLayer Intelligent Contract 0x70c2...3e92</p>
              </div>
              <div style={{ display: "flex", gap: 12 }}>
                <div style={{ padding: "8px 18px", borderRadius: 999, background: "#8b5cf6", color: "#ffffff", fontWeight: 700, fontSize: 13 }}>
                  Case B: CloudSwarm (Active)
                </div>
                <div style={{ padding: "8px 18px", borderRadius: 999, background: "rgba(255,255,255,0.08)", color: "#9ca3af", fontSize: 13 }}>
                  Case A: LocalAgent
                </div>
              </div>
            </div>

            {/* Inputs */}
            <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
              <div>
                <div style={{ fontFamily: "monospace", fontSize: 12, color: "#8b5cf6", marginBottom: 8, fontWeight: 700 }}>01 / REPOSITORY CODE MANIFEST URL</div>
                <div style={{ padding: "16px 20px", borderRadius: 12, background: "rgba(0,0,0,0.5)", border: "1px solid rgba(255,255,255,0.15)", fontFamily: "monospace", fontSize: 16, color: "#10b981" }}>
                  {typedRepo}<span style={{ opacity: Math.sin(frame / 6) > 0 ? 1 : 0 }}>|</span>
                </div>
              </div>

              <div>
                <div style={{ fontFamily: "monospace", fontSize: 12, color: "#8b5cf6", marginBottom: 8, fontWeight: 700 }}>02 / PUBLIC PRIVACY POLICY URL</div>
                <div style={{ padding: "16px 20px", borderRadius: 12, background: "rgba(0,0,0,0.5)", border: "1px solid rgba(255,255,255,0.15)", fontFamily: "monospace", fontSize: 16, color: "#10b981" }}>
                  {typedPrivacy}<span style={{ opacity: Math.sin(frame / 6) > 0 ? 1 : 0 }}>|</span>
                </div>
              </div>

              <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 12 }}>
                <div style={{ padding: "16px 36px", borderRadius: 999, background: "linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)", color: "#ffffff", fontWeight: 800, fontSize: 16, letterSpacing: "0.04em", textTransform: "uppercase", boxShadow: "0 10px 30px rgba(139, 92, 246, 0.5)" }}>
                  Execute Comparative Audit
                </div>
              </div>
            </div>
          </div>
        )}

        {/* BEAT 04: GenLayer Comparative Consensus Pipeline */}
        {time >= 39.52 && time < 52.52 && (
          <div style={{ position: "absolute", top: 160, left: 180, right: 180, display: "flex", flexDirection: "column", gap: 32 }}>
            {/* Stepper */}
            <div style={{ display: "flex", gap: 16 }}>
              <div style={{ flex: 1, padding: "18px 20px", borderRadius: 14, background: step1Active ? "#8b5cf6" : "rgba(255,255,255,0.05)", color: "#ffffff", fontWeight: 700, textAlign: "center", border: "1px solid rgba(255,255,255,0.1)" }}>
                1. PROPOSING (gl.nondet.web.get)
              </div>
              <div style={{ flex: 1, padding: "18px 20px", borderRadius: 14, background: step2Active ? "#8b5cf6" : "rgba(255,255,255,0.05)", color: "#ffffff", fontWeight: 700, textAlign: "center", border: "1px solid rgba(255,255,255,0.1)" }}>
                2. COMMITTING (Code Parsing)
              </div>
              <div style={{ flex: 1, padding: "18px 20px", borderRadius: 14, background: step3Active ? "#8b5cf6" : "rgba(255,255,255,0.05)", color: "#ffffff", fontWeight: 700, textAlign: "center", border: "1px solid rgba(255,255,255,0.1)" }}>
                3. REVEALING (Comparative)
              </div>
              <div style={{ flex: 1, padding: "18px 20px", borderRadius: 14, background: step4Active ? "#10b981" : "rgba(255,255,255,0.05)", color: "#ffffff", fontWeight: 700, textAlign: "center", border: "1px solid rgba(255,255,255,0.1)" }}>
                4. FINALIZED (On-Chain)
              </div>
            </div>

            {/* Validator Matrix */}
            <div style={{ padding: 36, borderRadius: 20, background: "rgba(10, 15, 30, 0.85)", border: "1px solid rgba(255,255,255,0.15)", backdropFilter: "blur(20px)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 24, fontFamily: "monospace", fontSize: 13, color: "#8b5cf6", fontWeight: 700 }}>
                <span>DECENTRALIZED VALIDATORS (GENLAYER STUDIONET 61999)</span>
                <span>CONSENSUS PRINCIPLE: prompt_comparative()</span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {[1, 2, 3, 4, 5].map((v) => (
                  <div key={v} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "14px 20px", borderRadius: 12, background: "rgba(0,0,0,0.4)", border: "1px solid rgba(255,255,255,0.08)" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                      <span style={{ width: 10, height: 10, borderRadius: "50%", backgroundColor: "#10b981", boxShadow: "0 0 10px #10b981" }} />
                      <span style={{ fontFamily: "monospace", color: "#f9fafb", fontSize: 15 }}>Validator 0{v} (GenVM Node)</span>
                    </div>
                    <span style={{ fontFamily: "monospace", color: "#ef4444", fontWeight: 800, fontSize: 14, letterSpacing: "0.04em" }}>
                      VOTED: DISCLOSURE_MISMATCH (ACCEPTED)
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* BEAT 05 & 06: Finalized On-Chain Proof Card */}
        {time >= 52.52 && time < 79.05 && (
          <div style={{ position: "absolute", top: 150, left: 200, right: 200, padding: 44, borderRadius: 24, background: "rgba(10, 15, 30, 0.9)", border: "1px solid rgba(239, 68, 68, 0.4)", backdropFilter: "blur(24px)", boxShadow: "0 0 80px rgba(239, 68, 68, 0.25)" }}>
            {/* Verdict Banner */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: 28, borderRadius: 18, background: "rgba(239, 68, 68, 0.12)", border: "1px solid rgba(239, 68, 68, 0.3)", marginBottom: 28 }}>
              <div>
                <div style={{ fontFamily: "monospace", fontSize: 12, color: "#ef4444", fontWeight: 800, letterSpacing: "0.1em" }}>ON-CHAIN FINALIZED VERDICT</div>
                <h2 style={{ fontSize: 44, fontWeight: 900, color: "#f87171", margin: "4px 0 0 0", letterSpacing: "-0.02em" }}>DISCLOSURE_MISMATCH</h2>
              </div>
              <div style={{ padding: "12px 24px", borderRadius: 12, background: "rgba(239, 68, 68, 0.25)", border: "1px solid rgba(239, 68, 68, 0.5)", color: "#fca5a5", fontFamily: "monospace", fontWeight: 800, fontSize: 14 }}>
                5/5 VALIDATORS ACCEPTED
              </div>
            </div>

            {/* Extracted Evidence */}
            <div style={{ display: "flex", flexDirection: "column", gap: 18, marginBottom: 28 }}>
              <div style={{ padding: 20, borderRadius: 14, background: "rgba(0,0,0,0.5)", border: "1px solid rgba(255,255,255,0.08)" }}>
                <span style={{ fontFamily: "monospace", fontSize: 12, color: "#9ca3af", fontWeight: 700 }}>STATED MARKETING PROMISE</span>
                <p style={{ margin: "6px 0 0 0", color: "#e5e7eb", fontSize: 16 }}>"Self-hosted, 100% private, no telemetry collected."</p>
              </div>

              <div style={{ padding: 20, borderRadius: 14, background: "rgba(0,0,0,0.5)", border: "1px solid rgba(239, 68, 68, 0.2)" }}>
                <span style={{ fontFamily: "monospace", fontSize: 12, color: "#ef4444", fontWeight: 700 }}>CODEBASE AST CONTRADICTION DETECTED</span>
                <p style={{ margin: "6px 0 0 0", color: "#fca5a5", fontSize: 16, fontFamily: "monospace" }}>Detected active calls: posthog.capture, import posthog</p>
              </div>
            </div>

            {/* On-Chain Receipts */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", paddingTop: 20, borderTop: "1px solid rgba(255,255,255,0.1)", fontFamily: "monospace", fontSize: 13 }}>
              <div>
                <span style={{ color: "#6b7280" }}>CONTRACT: </span>
                <span style={{ color: "#8b5cf6", fontWeight: 700 }}>0x70c2F7491A2CC7f81AC05ca964a059c05feD3e92</span>
              </div>
              <div>
                <span style={{ color: "#6b7280" }}>TX HASH: </span>
                <span style={{ color: "#10b981", fontWeight: 700 }}>0x5452df20...3de0a099</span>
              </div>
              <div style={{ padding: "6px 14px", borderRadius: 8, background: "rgba(16, 185, 129, 0.15)", color: "#10b981", fontWeight: 800 }}>
                GenVM: SUCCESS
              </div>
            </div>
          </div>
        )}

        {/* BEAT 07: Closing Anthem & Monogram Lockup */}
        {time >= 79.05 && (
          <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", textAlign: "center" }}>
            {/* Pulsing Monogram */}
            <div style={{ width: 140, height: 140, borderRadius: 36, background: "linear-gradient(135deg, rgba(139,92,246,0.3) 0%, rgba(16,185,129,0.2) 100%)", border: "2px solid rgba(255,255,255,0.25)", display: "flex", justifyContent: "center", alignItems: "center", boxShadow: "0 0 80px rgba(139,92,246,0.5)", marginBottom: 32 }}>
              <div style={{ width: 50, height: 50, borderRadius: "50%", border: "4px solid #10b981", boxShadow: "0 0 25px #10b981" }} />
            </div>

            <h1 style={{ fontSize: 92, fontWeight: 900, color: "#ffffff", letterSpacing: "-0.04em", margin: 0 }}>
              CORDA
            </h1>
            <p style={{ fontSize: 28, color: "#9ca3af", fontWeight: 300, marginTop: 12, marginBottom: 36 }}>
              Claims are easy. Evidence is harder.
            </p>

            <div style={{ display: "flex", gap: 16 }}>
              <div style={{ padding: "12px 28px", borderRadius: 999, background: "rgba(255,255,255,0.08)", border: "1px solid rgba(255,255,255,0.2)", color: "#ffffff", fontFamily: "monospace", fontSize: 14 }}>
                corda-vert.vercel.app
              </div>
              <div style={{ padding: "12px 28px", borderRadius: 999, background: "#8b5cf6", color: "#ffffff", fontFamily: "monospace", fontSize: 14, fontWeight: 700 }}>
                GenLayer Studionet (61999)
              </div>
            </div>
          </div>
        )}

        {/* Virtual Animated Cursor */}
        <Cursor x={cursorX} y={cursorY} isClicking={isClicking} />
      </div>

      {/* Persistent Static UI Overlay (Brand Header & Dynamic Subtitles) */}
      <div style={{ opacity: time >= 11.91 && time < 79.05 ? 0 : 1, transition: "opacity 0.4s ease" }}>
        <Header />
      </div>
      <SubtitleBar />
    </div>
  );
};
