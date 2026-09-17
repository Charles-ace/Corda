export type Beat = {
  id: string;
  start: number; // in seconds
  end: number;   // in seconds
  title: string;
  text: string;
};

export const FPS = 30;

// Default semantic beat timing structure (automatically updated by generate_narration script once audio is generated)
export const beats: Beat[] = [
  {
    id: "BEAT_01",
    title: "BEAT_01: The Privacy Question",
    start: 0.0,
    end: 7.0,
    text: "Every developer asks the same question: when open-source AI frameworks claim to be private, do their public codebases actually keep that promise?"
  },
  {
    id: "BEAT_02",
    title: "BEAT_02: The Contradiction Exposed",
    start: 7.0,
    end: 16.5,
    text: "Take this framework: documentation boldly claims 'Self-hosted, 100% private, no telemetry.' But inspect the actual code. Active PostHog imports, API keys initialized, and telemetry capture events firing on task dispatch."
  },
  {
    id: "BEAT_03",
    title: "BEAT_03: Corda Console Ingestion",
    start: 16.5,
    end: 22.5,
    text: "That is where Corda steps in. By supplying the target repository code and public privacy policy directly into the Corda console..."
  },
  {
    id: "BEAT_04",
    title: "BEAT_04: GenLayer Comparative Consensus Pipeline",
    start: 22.5,
    end: 33.5,
    text: "...Corda triggers an Intelligent Contract on GenLayer. Non-deterministic web nodes independently crawl the documentation and code manifests, running comparative semantic evaluation across decentralized validators."
  },
  {
    id: "BEAT_05",
    title: "BEAT_05: The Finalized Verdict",
    start: 33.5,
    end: 42.0,
    text: "The multi-validator consensus is finalized: Disclosure Mismatch. Corda extracts the exact contradiction, detailing the active analytics SDKs against the unfulfilled marketing promise."
  },
  {
    id: "BEAT_06",
    title: "BEAT_06: Tamper-Evident On-Chain Proof",
    start: 42.0,
    end: 51.5,
    text: "Every report is immutably committed to GenLayer Studionet with GenVM Result: Success. Contract zero x seven zero c two, finalized across independent validators with public transaction proofs."
  },
  {
    id: "BEAT_07",
    title: "BEAT_07: Closing Anthem",
    start: 51.5,
    end: 56.0,
    text: "Claims are easy. Evidence is harder. Corda."
  }
];

export const TOTAL_DURATION_SECONDS = beats[beats.length - 1].end;
export const TOTAL_DURATION_FRAMES = Math.ceil(TOTAL_DURATION_SECONDS * FPS);
